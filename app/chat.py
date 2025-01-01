import os
from dotenv import load_dotenv
from fastapi import FastAPI
from sse_starlette import EventSourceResponse
from starlette.middleware.cors import CORSMiddleware

from core.service import answer_question
from src.core.schemas import StreamRequest
from app.config import cors_settings, settings

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_settings.allow_origins.split(","),
    allow_credentials=cors_settings.allow_credentials,
    allow_methods=cors_settings.allow_methods.split(","),
    allow_headers=cors_settings.allow_headers.split(","),
)


@app.on_event("startup")
async def startup_event():
    
    # print(f"LANGCHAIN_TRACING_V2: {os.getenv('LANGCHAIN_TRACING_V2')}")
    # print(f"LANGCHAIN_PROJECT: {os.getenv('LANGCHAIN_PROJECT')}")
    # print(f"LANGCHAIN_API_KEY: {os.getenv('LANGCHAIN_API_KEY')}")
    # print(f"LANGCHAIN_API_KEY exists: {'LANGCHAIN_API_KEY' in os.environ}")

    print("Startup event finished - Application is ready to receive requests.")


@app.get("/")
async def get():
    return {"message": "Hello World"}


@app.post("/answer")
async def stream_answer(request: StreamRequest):
    return EventSourceResponse(answer_question(request.question))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "chat:app",
        host="0.0.0.0",
        port=9090,
        reload=True
    )
