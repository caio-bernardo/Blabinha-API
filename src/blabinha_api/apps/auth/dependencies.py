from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_token_service():
    from .services import TokenService
    return TokenService()
