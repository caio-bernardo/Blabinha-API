from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     email: str = Field(index=True)
#     name: str = Field()
#     password: str = Field()
#     # chat = Relationship(back_populates="user")
