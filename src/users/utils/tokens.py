import datetime
from src.config import settings
import jwt


def create_access_or_refresh_token(sub: str, token_type: str) -> str:
    data_to_encode = {
        'sub': sub, 'token_type': token_type
    }
    expires_time = datetime.now(datetime.timezone.utc)
    if token_type == 'access_token':
        expires_time += datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    elif token_type == 'refresh_token':
        expires_time += datetime.timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    data_to_encode['exp'] = expires_time
    return jwt.encode(
        data_to_encode, settings.JWT_SECRET_KEY, algorithm=['HS256']
    )
