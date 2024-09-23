import os
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from database.session import engine
from database import Base, settings_config
from database.session import get_db
from apscheduler.schedulers.background import BackgroundScheduler
from metric_simulator.metric_service import MetricService
from database import LLMRepository, MetricRepository, SimulatorRepository

load_dotenv()

scheduler = BackgroundScheduler()

SCHEDULE_INTERVAL = os.getenv("SCHEDULE_INTERVAL", "1")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application(lifespan):
    app = FastAPI(title=settings_config.PROJECT_NAME, version=settings_config.PROJECT_VERSION, lifespan=lifespan)
    create_tables()
    return app


scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    llm_repository = LLMRepository(db)
    metric_repository = MetricRepository(db)
    simulator_repository = SimulatorRepository(db)
    metric_service = MetricService(llm_repository, metric_repository, simulator_repository)
    # Generate initial data points on startup
    metric_service.simulate_data_points()

    # schedule simulation generation of data points every 1 minute
    scheduler.add_job(metric_service.simulate_data_points, 'interval', minutes=int(SCHEDULE_INTERVAL))
    scheduler.start()

    yield

    scheduler.shutdown()

app = start_application(lifespan)
