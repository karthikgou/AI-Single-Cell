from pydantic import BaseModel


class Request(BaseModel):
    inputPath: str
    outputPath: str
    speciesType: str


class Result(BaseModel):
    task_id: str
    status: str


class Task(BaseModel):
    task_id: str
    status: str