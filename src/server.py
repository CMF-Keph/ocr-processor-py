from threading import Lock

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from contextlib import asynccontextmanager
import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.initialize_database()
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_methods=["GET"],
)

class TextEntry(BaseModel):
  id: int
  text: str

class NewEntry(BaseModel):
  text: str

class SerieEntry(BaseModel):
  id: int
  name: str

class NewSerieEntry(BaseModel):
   name: str

@app.post("/api/series/{series_id}/texts")
async def add_entry_by_serie(series_id: int, new_entry: NewEntry) -> TextEntry:
    return TextEntry.model_validate(
        database.add_text_by_serie(new_entry.text, series_id)
    )

@app.post("/api/series")
async def add_entry_by_serie(new_entry: NewSerieEntry) -> SerieEntry:    
    return SerieEntry.model_validate(
        database.add_serie(new_entry.name)
    )

@app.get("/api/series/{series_id}/texts")
async def get_entries_by_serie(series_id) -> list[TextEntry]:
    return [
       TextEntry.model_validate(row)
       for row in database.get_texts_by_serie(series_id)
    ]

@app.get("/api/series")
async def get_series() -> list[SerieEntry]:
    return [
       SerieEntry.model_validate(row)
       for row in database.get_series()
    ]