from fastapi import FastAPI
from pydantic import BaseModel

from ml_framework_project.main import (
    diamonds_classification_pipeline,
    diamonds_regression_pipeline,
)

app = FastAPI(title="ml-framework-project")


class DiamondsPipelineRequest(BaseModel):
    file_path: str


@app.get("/")
def root() -> dict:
    return {"message": "ml-framework-project API"}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/pipelines/diamonds/regression")
def run_diamonds_regression(request: DiamondsPipelineRequest) -> dict:
    return diamonds_regression_pipeline(request.file_path)


@app.post("/pipelines/diamonds/classification")
def run_diamonds_classification(request: DiamondsPipelineRequest) -> dict:
    return diamonds_classification_pipeline(request.file_path)
