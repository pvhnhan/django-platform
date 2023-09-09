import logging
import re
import datetime
import os

_logger = logging.getLogger(__name__)

try:
    import jwt
except ImportError:
    _logger.debug('Cannot `import jwt`.')

REGEX = r"^[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
SECRET_KEY = "!kLbMLtW4@lFnBlt"

class JwtProvider:
    def is_valid_email(self, email):
        return re.search(REGEX, email)

    def key(self):
        return os.environ.get('ODOO_JWT_KEY')

    def create_token(self, user):
        global SECRET_KEY
        try:
            headers = {
                "alg": "HS256",
                "typ": "JWT"
            }
            exp = datetime.datetime.utcnow() + datetime.timedelta(days=30)
            payload = {
                'exp': exp,
                'iat': datetime.datetime.utcnow(),
                'sub': user['id'],
                'lgn': user['login'],
            }

            token = jwt.encode(
                payload = payload,
                key=SECRET_KEY,
                algorithm='HS256',
                headers=headers
            )

            self.save_token(token, user['id'], exp)
            return token.decode('utf-8')
        except Exception as ex:
            _logger.error(ex)
            raise