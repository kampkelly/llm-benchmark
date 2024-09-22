from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.session import engine
from database import Base, settings_config
from database.session import get_db
from metric_simulator.metric_service import MetricService
from database import LLMRepository, MetricRepository, SimulatorRepository


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application(lifespan):
    app = FastAPI(title=settings_config.PROJECT_NAME, version=settings_config.PROJECT_VERSION, lifespan=lifespan)
    create_tables()
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    llm_repository = LLMRepository(db)
    metric_repository = MetricRepository(db)
    simulator_repository = SimulatorRepository(db)
    metric_service = MetricService(llm_repository, metric_repository, simulator_repository)
    # remove data points
    metric_service.remove_metrics()
    # Generate initial data points on startup
    metric_service.simulate_data_points()

    yield

app = start_application(lifespan)
