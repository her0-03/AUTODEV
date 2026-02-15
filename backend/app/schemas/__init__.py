from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: str
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class GenerationJobResponse(BaseModel):
    id: str
    project_id: str
    status: str
    input_files: Optional[List[str]]
    output_path: Optional[str]
    error_log: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
