"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data"""
    user_id: Optional[int] = None
    username: Optional[str] = None


class AuthResponse(BaseModel):
    """Schema for authentication response"""
    message: str
    token: str
    user: UserResponse


# MIDI Schemas
class MidiFileBase(BaseModel):
    """Base MIDI file schema"""
    filename: str
    original_filename: str


class MidiFileCreate(MidiFileBase):
    """Schema for creating MIDI file"""
    midi_data: bytes
    duration: Optional[float] = None
    note_count: Optional[int] = None


class MidiFileResponse(BaseModel):
    """Schema for MIDI file response"""
    id: int
    filename: str
    original_filename: str
    duration: Optional[float]
    note_count: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class MidiFileDetail(MidiFileResponse):
    """Schema for detailed MIDI file response"""
    midi_data: str  # Base64 encoded
    
    class Config:
        from_attributes = True


class MidiLibraryResponse(BaseModel):
    """Schema for MIDI library response"""
    midis: list[MidiFileResponse]
    count: int
