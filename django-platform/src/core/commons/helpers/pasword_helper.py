from hashlib import sha256
import passlib.context

import logging

_logger = logging.getLogger(__name__)

DEFAULT_CRYPT_CONTEXT = passlib.context.CryptContext(
    # kdf which can be verified by the context. The default encryption kdf is
    # the first of the list
    ['pbkdf2_sha512', 'plaintext'],
    # deprecated algorithms are still verified as usual, but ``needs_update``
    # will indicate that the stored hash should be replaced by a more recent
    # algorithm. Passlib 1.6 supports an `auto` value which deprecates any
    # algorithm but the default, but Ubuntu LTS only provides 1.5 so far.
    deprecated=['plaintext'],
)

class PasswordHelper:
    @classmethod
    def _crypt_context(self):
        """ Passlib CryptContext instance used to encrypt and verify
        passwords. Can be overridden if technical, legal or political matters
        require different kdfs than the provided default.

        Requires a CryptContext as deprecation and upgrade notices are used
        internally
        """
        return DEFAULT_CRYPT_CONTEXT

    @classmethod
    def encrypt(self, pwd):
        ctx = self._crypt_context()
        hash_password = ctx.hash if hasattr(ctx, 'hash') else ctx.encrypt

        # encrypt
        encrypt_pwd = hash_password(pwd)
        return encrypt_pwd

    @classmethod
    def verify_password(self, pwd, hashed):
        valid, replacement = self._crypt_context()\
            .verify_and_update(pwd, hashed)

        return valid, replacement
