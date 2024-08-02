from fastapi import APIRouter, HTTPException
from vector_db.database import (
    add_record,
    update_record,
    delete_record,
    query_records,
)
from schemas.vector_schemas import (
    VectorRecordCreate,
    VectorRecordUpdate,
    VectorRecordDelete,
    VectorRecordQuery,
    VectorRecordResponse,
    VectorRecordQueryResponse,
)
from typing import List

router = APIRouter()


@router.post("/add", response_model=VectorRecordResponse)
def add_vector_record(record: VectorRecordCreate):
    try:
        new_record = add_record(record.model_dump())
        return VectorRecordResponse(
            id=new_record.id,
            message="Record added successfully",
            created_at=new_record.created_at,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update/{id}", response_model=VectorRecordResponse)
def update_vector_record(id: str, record: VectorRecordUpdate):
    try:
        updated_record = update_record(id, record.model_dump(exclude_unset=True))
        return VectorRecordResponse(
            id=updated_record["id"],
            message="Record updated successfully",
            updated_at=updated_record["updated_at"],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{id}", response_model=VectorRecordResponse)
def delete_vector_record(id: str):
    try:
        delete_record(id)
        return VectorRecordResponse(id=id, message="Record deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/query", response_model=VectorRecordQueryResponse)
def query_vector_records(query: VectorRecordQuery):
    try:
        results, total_count = query_records(query.query, query.page, query.page_size)
        return VectorRecordQueryResponse(
            results=results,
            total_count=total_count,
            page=query.page,
            page_size=query.page_size,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk_add", response_model=VectorRecordResponse)
def bulk_add_vector_records(records: List[VectorRecordCreate]):
    try:
        new_records = [add_record(record.model_dump()) for record in records]
        return VectorRecordResponse(
            message=f"{len(new_records)} records added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/bulk_delete", response_model=VectorRecordResponse)
def bulk_delete_vector_records(ids: List[str]):
    try:
        for id in ids:
            delete_record(id)
        return VectorRecordResponse(message=f"{len(ids)} records deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
