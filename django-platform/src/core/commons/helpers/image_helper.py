import base64
import binascii

from PIL import Image, ImageOps

# Preload PIL with the minimal subset of image formats we need
Image.preinit()
Image._initialized = 2

# Maps only the 6 first bits of the base64 data, accurate enough
# for our purpose and faster than decoding the full blob first
FILETYPE_BASE64_MAGICWORD = {
    b'/': 'jpg',
    b'R': 'gif',
    b'i': 'png',
    b'P': 'svg+xml',
}

EXIF_TAG_ORIENTATION = 0x112
# The target is to have 1st row/col to be top/left
# Note: rotate is counterclockwise
EXIF_TAG_ORIENTATION_TO_TRANSPOSE_METHODS = {  # Initial side on 1st row/col:
    0: [],                                          # reserved
    1: [],                                          # top/left
    2: [Image.FLIP_LEFT_RIGHT],                     # top/right
    3: [Image.ROTATE_180],                          # bottom/right
    4: [Image.FLIP_TOP_BOTTOM],                     # bottom/left
    5: [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],    # left/top
    6: [Image.ROTATE_270],                          # right/top
    7: [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],    # right/bottom
    8: [Image.ROTATE_90],                           # left/bottom
}

# Arbitraty limit to fit most resolutions, including Nokia Lumia 1020 photo,
# 8K with a ratio up to 16:10, and almost all variants of 4320p
IMAGE_MAX_RESOLUTION = 45e6

class ImageHelper:
    # init
    def __init__(self, base64_source, verify_resolution=True):
        """Initialize the `base64_source` image for processing.

        :param base64_source: the original image base64 encoded
            No processing will be done if the `base64_source` is falsy or if
            the image is SVG.
        :type base64_source: string or bytes

        :param verify_resolution: if True, make sure the original image size is not
            excessive before starting to process it. The max allowed resolution is
            defined by `IMAGE_MAX_RESOLUTION`.
        :type verify_resolution: bool

        :return: self
        :rtype: ImageProcess

        :raise: ValueError if `verify_resolution` is True and the image is too large
        :raise: UserError if the base64 is incorrect or the image can't be identified by PIL
        """
        self.base64_source = base64_source or False
        self.operationsCount = 0

        if not base64_source or base64_source[:1] in (b'P', 'P'):
            # don't process empty source or SVG
            self.image = False
        else:
            self.image = base64_to_image(self.base64_source)

            # Original format has to be saved before fixing the orientation or
            # doing any other operations because the information will be lost on
            # the resulting image.
            self.original_format = (self.image.format or '').upper()

            self.image = image_fix_orientation(self.image)

            w, h = self.image.size
            if verify_resolution and w * h > IMAGE_MAX_RESOLUTION:
                raise ValueError(_("Image size excessive, uploaded images must be smaller than %s million pixels.", str(IMAGE_MAX_RESOLUTION / 10e6)))
    # end

    # image base 64
    def image_base64(self, quality=0, output_format=''):
        """Return the base64 encoded image resulting of all the image processing
        operations that have been applied previously.

        Return False if the initialized `base64_source` was falsy, and return
        the initialized `base64_source` without change if it was SVG.

        Also return the initialized `base64_source` if no operations have been
        applied and the `output_format` is the same as the original format and
        the quality is not specified.

        :param quality: quality setting to apply. Default to 0.
            - for JPEG: 1 is worse, 95 is best. Values above 95 should be
                avoided. Falsy values will fallback to 95, but only if the image
                was changed, otherwise the original image is returned.
            - for PNG: set falsy to prevent conversion to a WEB palette.
            - for other formats: no effect.
        :type quality: int

        :param output_format: the output format. Can be PNG, JPEG, GIF, or ICO.
            Default to the format of the original image. BMP is converted to
            PNG, other formats than those mentioned above are converted to JPEG.
        :type output_format: string

        :return: image base64 encoded or False
        :rtype: bytes or False
        """
        output_image = self.image

        if not output_image:
            return self.base64_source

        output_format = output_format.upper() or self.original_format
        if output_format == 'BMP':
            output_format = 'PNG'
        elif output_format not in ['PNG', 'JPEG', 'GIF', 'ICO']:
            output_format = 'JPEG'

        if not self.operationsCount and output_format == self.original_format and not quality:
            return self.base64_source

        opt = {'format': output_format}

        if output_format == 'PNG':
            opt['optimize'] = True
            if quality:
                if output_image.mode != 'P':
                    # Floyd Steinberg dithering by default
                    output_image = output_image.convert('RGBA').convert('P', palette=Image.WEB, colors=256)
        if output_format == 'JPEG':
            opt['optimize'] = True
            opt['quality'] = quality or 95
        if output_format == 'GIF':
            opt['optimize'] = True
            opt['save_all'] = True

        if output_image.mode not in ["1", "L", "P", "RGB", "RGBA"] or (output_format == 'JPEG' and output_image.mode == 'RGBA'):
            output_image = output_image.convert("RGB")

        return image_to_base64(output_image, **opt)
    # end

    # resize
    def resize(self, max_width=0, max_height=0):
        """Resize the image.

        The image is never resized above the current image size. This method is
        only to create a smaller version of the image.

        The current ratio is preserved. To change the ratio, see `crop_resize`.

        If `max_width` or `max_height` is falsy, it will be computed from the
        other to keep the current ratio. If both are falsy, no resize is done.

        It is currently not supported for GIF because we do not handle all the
        frames properly.

        :param max_width: max width
        :type max_width: int

        :param max_height: max height
        :type max_height: int

        :return: self to allow chaining
        :rtype: ImageProcess
        """
        if self.image and self.original_format != 'GIF' and (max_width or max_height):
            w, h = self.image.size
            asked_width = max_width or (w * max_height) // h
            asked_height = max_height or (h * max_width) // w
            if asked_width != w or asked_height != h:
                self.image.thumbnail((asked_width, asked_height), Image.LANCZOS)
                if self.image.width != w or self.image.height != h:
                    self.operationsCount += 1
        return self
    # end

    # crop
    def crop_resize(self, max_width, max_height, center_x=0.5, center_y=0.5):
        """Crop and resize the image.

        The image is never resized above the current image size. This method is
        only to create smaller versions of the image.

        Instead of preserving the ratio of the original image like `resize`,
        this method will force the output to take the ratio of the given
        `max_width` and `max_height`, so both have to be defined.

        The crop is done before the resize in order to preserve as much of the
        original image as possible. The goal of this method is primarily to
        resize to a given ratio, and it is not to crop unwanted parts of the
        original image. If the latter is what you want to do, you should create
        another method, or directly use the `crop` method from PIL.

        It is currently not supported for GIF because we do not handle all the
        frames properly.

        :param max_width: max width
        :type max_width: int

        :param max_height: max height
        :type max_height: int

        :param center_x: the center of the crop between 0 (left) and 1 (right)
            Default to 0.5 (center).
        :type center_x: float

        :param center_y: the center of the crop between 0 (top) and 1 (bottom)
            Default to 0.5 (center).
        :type center_y: float

        :return: self to allow chaining
        :rtype: ImageProcess
        """
        if self.image and self.original_format != 'GIF' and max_width and max_height:
            w, h = self.image.size
            # We want to keep as much of the image as possible -> at least one
            # of the 2 crop dimensions always has to be the same value as the
            # original image.
            # The target size will be reached with the final resize.
            if w / max_width > h / max_height:
                new_w, new_h = w, (max_height * w) // max_width
            else:
                new_w, new_h = (max_width * h) // max_height, h

            # No cropping above image size.
            if new_w > w:
                new_w, new_h = w, (new_h * w) // new_w
            if new_h > h:
                new_w, new_h = (new_w * h) // new_h, h

            # Correctly place the center of the crop.
            x_offset = int((w - new_w) * center_x)
            h_offset = int((h - new_h) * center_y)

            if new_w != w or new_h != h:
                self.image = self.image.crop((x_offset, h_offset, x_offset + new_w, h_offset + new_h))
                if self.image.width != w or self.image.height != h:
                    self.operationsCount += 1

        return self.resize(max_width, max_height)

    def colorize(self):
        """Replace the transparent background by a random color.

        :return: self to allow chaining
        :rtype: ImageProcess
        """
        if self.image:
            original = self.image
            color = (randrange(32, 224, 24), randrange(32, 224, 24), randrange(32, 224, 24))
            self.image = Image.new('RGB', original.size)
            self.image.paste(color, box=(0, 0) + original.size)
            self.image.paste(original, mask=original)
            self.operationsCount += 1
        return self
    