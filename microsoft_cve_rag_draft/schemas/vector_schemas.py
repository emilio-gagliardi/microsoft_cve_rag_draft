from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional, List, Dict
from datetime import datetime, timezone


class VectorRecordBase(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier of the record")
    created_at: Optional[datetime] = Field(
        None, description="Timestamp when the record was created"
    )
    updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the record was last updated"
    )
    field1: str = Field(
        ..., min_length=1, max_length=255, description="Description of field1"
    )
    field2: int = Field(..., gt=0, description="Description of field2")
    # Add other common fields here

    @field_validator("created_at", "updated_at", pre=True, always=True)
    def set_timestamps(cls, value, field):
        return value or datetime.now(timezone.utc)


class VectorRecordCreate(VectorRecordBase):
    pass


class VectorRecordUpdate(VectorRecordBase):
    id: str


class VectorRecordDelete(BaseModel):
    id: str


class VectorRecordQuery(BaseModel):
    query: Dict[str, str] = Field(..., description="Query parameters")
    page: Optional[int] = Field(1, description="Page number for pagination")
    page_size: Optional[int] = Field(10, description="Number of records per page")


class VectorRecordResponse(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier of the record")
    message: str = Field(..., description="Response message")
    created_at: Optional[datetime] = Field(
        None, description="Timestamp when the record was created"
    )
    updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the record was last updated"
    )


class VectorRecordQueryResponse(BaseModel):
    results: List[VectorRecordBase] = Field(
        ..., description="List of records matching the query"
    )
    total_count: int = Field(
        ..., description="Total count of records matching the query"
    )
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of records per page")


class BulkVectorRecordCreate(BaseModel):
    records: List[VectorRecordCreate]


class BulkVectorRecordDelete(BaseModel):
    ids: List[str]


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    code: int = Field(..., description="Error code")
