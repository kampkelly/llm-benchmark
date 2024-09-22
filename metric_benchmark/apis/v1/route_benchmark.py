from fastapi import APIRouter, Depends, status
from metric_benchmark.apis.benchmark_service import BenchmarkService

router = APIRouter()


@router.get("/rankings", status_code=status.HTTP_200_OK)
def get_database_info(benchmark_service: BenchmarkService = Depends(BenchmarkService)):
    response = benchmark_service.get_simulation_and_rankings()
    return response
