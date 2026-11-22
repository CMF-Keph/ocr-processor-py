from threading import Lock

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextEntry(BaseModel):
  id: int
  text: str

class NewEntry(BaseModel):
  text: str

latest_text: TextEntry = TextEntry(id=0, text="");
state_lock = Lock()

@app.post("/api/texts")
def add_entry(new_entry: NewEntry) -> TextEntry:
  with state_lock:
    latest_text.id += 1
    latest_text.text = new_entry.text
    return latest_text.model_copy()


@app.get("/api/texts/latest")
def get_latest_entry() -> TextEntry:
  with state_lock:
    return latest_text.model_copy()