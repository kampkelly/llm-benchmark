from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import settings_config
from database.session import get_db
from metric_benchmark.apis.benchmark_service import BenchmarkService
from database import LLMRepository, MetricRepository, SimulatorRepository


def start_application(lifespan):
    app = FastAPI(title=settings_config.PROJECT_NAME, version=settings_config.PROJECT_VERSION, lifespan=lifespan)
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    llm_repository = LLMRepository(db)
    metric_repository = MetricRepository(db)
    simulator_repository = SimulatorRepository(db)
    benchmark_service = BenchmarkService(llm_repository, metric_repository, simulator_repository)
    benchmark_service.get_simulation_and_rankings()

    yield

app = start_application(lifespan)


@app.get("/healthz")
def read_root():
    # This endpoint is used to check the health of the application
    return {"message": "success"}
