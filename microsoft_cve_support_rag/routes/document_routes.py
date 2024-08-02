from fastapi import APIRouter, HTTPException
from documents_db.database import (
    add_record,
    update_record,
    delete_record,
    query_records,
    bulk_add_records,
    bulk_update_records,
    bulk_delete_records,
)
from schemas.document_schemas import (
    DocumentRecordCreate,
    DocumentRecordUpdate,
    DocumentRecordDelete,
    DocumentRecordQuery,
    DocumentRecordResponse,
    DocumentRecordQueryResponse,
    BulkDocumentRecordCreate,
    BulkDocumentRecordUpdate,
    BulkDocumentRecordDelete,
)

router = APIRouter()


@router.post("/add", response_model=DocumentRecordResponse)
def add_document_record(record: DocumentRecordCreate):
    try:
        new_record = add_record(record.model_dump())
        return DocumentRecordResponse(
            id=new_record["id"],
            message="Record added successfully",
            created_at=new_record["created_at"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update/{id}", response_model=DocumentRecordResponse)
def update_document_record(id: str, record: DocumentRecordUpdate):
    try:
        updated_record = update_record(id, record.model_dump())
        return DocumentRecordResponse(
            id=updated_record["id"],
            message="Record updated successfully",
            updated_at=updated_record["updated_at"],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{id}", response_model=DocumentRecordResponse)
def delete_document_record(id: str):
    try:
        delete_record(id)
        return DocumentRecordResponse(id=id, message="Record deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/query", response_model=DocumentRecordQueryResponse)
def query_document_records(query: DocumentRecordQuery):
    try:
        results, total_count = query_records(query.query, query.page, query.page_size)
        return DocumentRecordQueryResponse(
            results=results,
            total_count=total_count,
            page=query.page,
            page_size=query.page_size,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk_add", response_model=DocumentRecordResponse)
def bulk_add_document_records(records: BulkDocumentRecordCreate):
    try:
        new_records = bulk_add_records(records.model_dump()["records"])
        return DocumentRecordResponse(
            message=f"{len(new_records)} records added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/bulk_update", response_model=DocumentRecordResponse)
def bulk_update_document_records(records: BulkDocumentRecordUpdate):
    try:
        updated_records = bulk_update_records(records.model_dump()["records"])
        return DocumentRecordResponse(
            message=f"{len(updated_records)} records updated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/bulk_delete", response_model=DocumentRecordResponse)
def bulk_delete_document_records(ids: BulkDocumentRecordDelete):
    try:
        bulk_delete_records(ids.model_dump()["ids"])
        return DocumentRecordResponse(
            message=f"{len(ids.ids)} records deleted successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
