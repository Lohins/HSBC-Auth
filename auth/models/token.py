import secrets
from datetime import datetime, timedelta
from auth.models.utils import DataStorage
from auth.config import Config

class TokenNotFoundError(Exception):
    pass

class TokenExipredError(Exception):
    pass

class Token:
    def __init__(self, user_name, expires = 2 * 60 * 60) -> None:
        self.user_name = user_name
        self.token = secrets.token_hex(30)

        # token will be expired in 2 hours.
        self.expired_at = datetime.now() + timedelta(hours=Config.TOKEN_EXPIRY_IN_HOURS)

        DataStorage.user_token_table.append(self)
    
    def is_expired(self):
        return datetime.now() > self.expired_at

    # expire a token by asigning a timestamp in the past.
    def mark_expired(self):
        self.expired_at = datetime.now() - timedelta(hours=Config.TOKEN_EXPIRY_IN_HOURS)

    
    @classmethod
    def invalidate_token(cls, token):
        target_token = next((t for t in DataStorage.user_token_table if t.token == token), None)

        if not target_token:
            raise TokenNotFoundError('Token not found.')
        
        if target_token.is_expired():
            raise TokenExipredError('Token has been expired.')
        
        target_token.mark_expired()

    @classmethod
    def get_token(cls, token_str):
        target_token = next((t for t in DataStorage.user_token_table if t.token == token_str), None)

        if not target_token:
            raise TokenNotFoundError('Token not found.')
        
        if target_token.is_expired():
            raise TokenExipredError('Token has been expired.')
        
        return target_token