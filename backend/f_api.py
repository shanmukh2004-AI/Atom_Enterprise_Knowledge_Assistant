from fastapi import FastAPI
from pydantic import BaseModel
from rag import (chat, build_index_from_text, delete_document)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Atom AI Backend Running"}


class UserQuery(BaseModel):
    query: str
    history: list = []
@app.post("/chat")
def chatbot(data: UserQuery):
    answer = chat(data.query, data.history)
    return {"query": data.query,"answer": answer}
class UploadFile(BaseModel):
    file_name: str
    file_content: str
@app.post("/upload")
def upload(data: UploadFile):
    file_text = data.file_content
    build_index_from_text(data.file_name,file_text)
    return {"message": "File uploaded successfully"}
class DeleteFile(BaseModel):
    file_name: str
@app.post("/delete")
def delete(data: DeleteFile):
    delete_document(data.file_name)
    return {"message": "File deleted successfully"}