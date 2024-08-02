from fastapi import APIRouter, HTTPException
from graph_db.database import add_record, update_record, delete_record, query_records
from schemas.graph_schemas import (
    GraphRecordCreate,
    GraphRecordUpdate,
    GraphRecordDelete,
    GraphRecordQuery,
    GraphRecordResponse,
    GraphRecordQueryResponse,
)

router = APIRouter()


@router.post("/add", response_model=GraphRecordResponse)
def add_graph_record(record: GraphRecordCreate):
    try:
        new_record = add_record(record.model_dump())
        return GraphRecordResponse(
            id=new_record["id"],
            message="Record added successfully",
            created_at=new_record["created_at"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update/{id}", response_model=GraphRecordResponse)
def update_graph_record(id: str, record: GraphRecordUpdate):
    try:
        updated_record = update_record(id, record.model_dump())
        return GraphRecordResponse(
            id=updated_record["id"],
            message="Record updated successfully",
            updated_at=updated_record["updated_at"],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{id}", response_model=GraphRecordResponse)
def delete_graph_record(id: str):
    try:
        delete_record(id)
        return GraphRecordResponse(id=id, message="Record deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/query", response_model=GraphRecordQueryResponse)
def query_graph_records(query: GraphRecordQuery):
    try:
        results, total_count = query_records(query.query, query.page, query.page_size)
        return GraphRecordQueryResponse(
            results=results,
            total_count=total_count,
            page=query.page,
            page_size=query.page_size,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
