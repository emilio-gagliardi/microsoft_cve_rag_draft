from fastapi import APIRouter, HTTPException
from sql_db.database import SQLDatabase
from schemas.sql_schemas import (
    SQLRecordCreate,
    SQLRecordUpdate,
    SQLRecordDelete,
    SQLRecordQuery,
    SQLRecordResponse,
    SQLRecordQueryResponse,
)
from typing import List

router = APIRouter()

# Initialize the SQLDatabase instance
db = SQLDatabase()


@router.post("/add", response_model=SQLRecordResponse)
def add_sql_record(record: SQLRecordCreate):
    try:
        new_record = db.add_record(record.model_dump())
        return SQLRecordResponse(
            id=new_record["id"],
            message="Record added successfully",
            created_at=new_record["created_at"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update/{id}", response_model=SQLRecordResponse)
def update_sql_record(id: str, record: SQLRecordUpdate):
    try:
        updated_record = db.update_record(id, record.model_dump(exclude_unset=True))
        return SQLRecordResponse(
            id=updated_record["id"],
            message="Record updated successfully",
            updated_at=updated_record["updated_at"],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{id}", response_model=SQLRecordResponse)
def delete_sql_record(id: str):
    try:
        db.delete_record(id)
        return SQLRecordResponse(id=id, message="Record deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/query", response_model=SQLRecordQueryResponse)
def query_sql_records(query: SQLRecordQuery):
    try:
        results, total_count = db.query_records(
            query.query, query.page, query.page_size
        )
        return SQLRecordQueryResponse(
            results=results,
            total_count=total_count,
            page=query.page,
            page_size=query.page_size,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk_add", response_model=SQLRecordResponse)
def bulk_add_sql_records(records: List[SQLRecordCreate]):
    try:
        new_records = [db.add_record(record.model_dump()) for record in records]
        return SQLRecordResponse(
            message=f"{len(new_records)} records added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/bulk_delete", response_model=SQLRecordResponse)
def bulk_delete_sql_records(ids: List[str]):
    try:
        for id in ids:
            db.delete_record(id)
        return SQLRecordResponse(message=f"{len(ids)} records deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
