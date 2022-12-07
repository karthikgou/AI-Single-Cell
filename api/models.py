from pydantic import BaseModel


class Request(BaseModel):
    inputPath: str
    outputPath: str
    speciesType: str


class Test(BaseModel):
    a: int
    b: int
    c: int


class Result(BaseModel):
    task_id: str
    status: str
    result: str


class Task(BaseModel):
    task_id: str
    status: str
