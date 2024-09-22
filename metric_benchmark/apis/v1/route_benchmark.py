from fastapi import APIRouter, Depends, status
from metric_benchmark.apis.benchmark_service import BenchmarkService
from metric_benchmark.apis.auth import verify_api_key

router = APIRouter()


@router.get("/rankings", status_code=status.HTTP_200_OK)
def get_database_info(
    benchmark_service: BenchmarkService = Depends(BenchmarkService),
    api_key: str = Depends(verify_api_key)
):
    response = benchmark_service.get_simulation_and_rankings()
    return response
