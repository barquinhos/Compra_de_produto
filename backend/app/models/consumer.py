from pydantic import BaseModel, Field, EmailStr
from pydantic.config import ConfigDict

class ConsumerBase(BaseModel):
    
    con_name: str = Field(..., min_length=3,max_length=100)
    con_email: str

class ConsumerCreate(ConsumerBase):

    con_password: str = Field(..., min_length=6, max_length=72)

class ConsumerLogin(BaseModel):

    con_email: EmailStr
    con_password: str = Field(..., min_length=6, max_length=72)

class ConsumerOut(ConsumerBase):

    con_id: int
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    
    access_token: str
    token_type: str = "bearer"