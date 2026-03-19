from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import HOST, PORT
from title_generator import get_title_generator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateTitleRequest(BaseModel):
    query: str


class GenerateTitleResponse(BaseModel):
    title: str
    keyphrase: str
    intents: List[str]
    duration_ms: int


@app.on_event("startup")
def startup_event() -> None:
    # Load both ML models once during startup.
    app.state.generator = get_title_generator()


@app.post("/generate-title", response_model=GenerateTitleResponse)
def generate_title(req: GenerateTitleRequest) -> GenerateTitleResponse:
    generator = getattr(app.state, "generator", None)
    if generator is None:
        raise HTTPException(status_code=503, detail="Title generator not ready")

    return generator.generate(req.query)


if __name__ == "__main__":
    # Convenience for local testing without uvicorn.
    import uvicorn

    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
