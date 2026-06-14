from sqlmodel import SQLModel, Field, Relationship

# User table
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    hashed_password: str

    items: list["Item"] = Relationship(back_populates="owner")


# Database table model
class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    in_stock: bool = True
    owner_id: int | None = Field(default=None, foreign_key="user.id")  # <-- foreign key

    owner: User | None = Relationship(back_populates="items")


# Input model (client never sends owner_id — set automatically from logged-in user)
class ItemCreate(SQLModel):
    name: str
    price: float
    in_stock: bool = True


# Output model
class ItemRead(SQLModel):
    id: int
    name: str
    price: float
    in_stock: bool
    owner_id: int | None = None


# Input model for registration
class UserCreate(SQLModel):
    username: str
    password: str

# Output model
class UserRead(SQLModel):
    id: int
    username: str

# Token response model
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"