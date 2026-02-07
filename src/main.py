from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import check_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
  yield


app = FastAPI(
  title="ITA API",
  description="API do projeto ITA",
  version="0.1.0",
  lifespan=lifespan,
)


@app.get("/")
def root():
  return {"message": "ITA API", "docs": "/docs"}


@app.get("/health")
async def health():
  db_ok = await check_db_connection()
  status = "ok" if db_ok else "degraded"
  return {"status": status, "database": "ok" if db_ok else "error"}
