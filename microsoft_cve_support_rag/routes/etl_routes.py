from fastapi import APIRouter
from etl.main_etl import run_etl

from schemas.etl_schemas import (
    ETLRunResponse,
)

router = APIRouter()


@router.post("/run", response_model=ETLRunResponse)
def run_etl_pipeline():
    run_etl()
    return ETLRunResponse(message="ETL pipeline executed successfully")
