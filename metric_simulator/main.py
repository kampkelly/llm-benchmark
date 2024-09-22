from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.session import engine
from database import Base, settings_config


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings_config.PROJECT_NAME, version=settings_config.PROJECT_VERSION)
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    create_tables()
    return app


app = start_application()


@app.get("/healthz")
def read_root():
    # This endpoint is used to check the health of the application
    return {"message": "success"}
