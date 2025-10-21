from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic.config import ConfigDict
from .consumer import Token

class SellerBase(BaseModel):

    sel_name: str = Field(..., min_length=3, max_length=100)
    sel_email: EmailStr

class SellerCreate(SellerBase):

    sel_password: str = Field(..., min_length=6, max_length=72)
    
    @field_validator('sel_password')
    def validate_password_prefix(cls, v):
        if not v.startswith('sel'):
            raise ValueError('A senha do seller deve começar com "sel"')
        return v

class SellerLogin(BaseModel):

    sel_email: EmailStr
    sel_password: str = Field(..., min_length=6, max_length=72)

class SellerOut(SellerBase):

    sel_id: int
    model_config = ConfigDict(from_attributes=True)