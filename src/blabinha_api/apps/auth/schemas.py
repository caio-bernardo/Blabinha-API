from sqlmodel import SQLModel, Field

class Token(SQLModel):
    refresh_token: str = Field(..., title="Refresh Token", description="Use the refresh token to get a new access token after expiration")
    access_token: str = Field(..., title="Access Token", description="Allows access to protected routes")
    token_type: str = Field(default="bearer", title="Token Type", description="The type of the token send. (Default: bearer)")

class TokenRefreshPayload(SQLModel):
    refresh_token: str = Field(...,
        title="Refresh Token",
        description="Use the refresh token to get a new access token after expiration")

class TokenData(SQLModel):
    username: str
