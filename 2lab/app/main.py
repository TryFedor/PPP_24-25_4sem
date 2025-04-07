from fastapi import FastAPI
from app.api.user import router as user_router
from app.core.config import settings
from app.db import Base, engine
from app.api.tsp import router as tsp_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Hello World!"}


app.include_router(tsp_router)


