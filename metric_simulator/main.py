import os
import asyncio
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from database.session import engine
from database import Base, settings_config
from database.session import get_db
from database.seed import seed_data
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from metric_simulator.metric_service import MetricService
from database import LLMRepository, MetricRepository, SimulatorRepository

load_dotenv()

scheduler = AsyncIOScheduler()

SCHEDULE_INTERVAL = os.getenv("SCHEDULE_INTERVAL", "3")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application(lifespan):
    app = FastAPI(title=settings_config.PROJECT_NAME, version=settings_config.PROJECT_VERSION, lifespan=lifespan)
    create_tables()
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    # seed initial app data
    seed_data(db)
    llm_repository = LLMRepository(db)
    metric_repository = MetricRepository(db)
    simulator_repository = SimulatorRepository(db)
    metric_service = MetricService(llm_repository, metric_repository, simulator_repository)

    async def run_simulate_data_points():
        await metric_service.simulate_data_points_with_retry()

    asyncio.create_task(run_simulate_data_points())

    scheduler.add_job(lambda: asyncio.create_task(run_simulate_data_points), 'interval',
                      minutes=int(SCHEDULE_INTERVAL))

    scheduler.start()

    yield

    scheduler.shutdown()

app = start_application(lifespan)
