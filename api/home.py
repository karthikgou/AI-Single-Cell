import fastapi
from celery.result import AsyncResult
from starlette.responses import JSONResponse

# from api.service import load_sce
from celery_worker import load_sce, create_task
from api.models import Request, Test, Result
from api.models import Task

router = fastapi.APIRouter()


@router.get('/')
async def index():
    return "Hello!!"


@router.post('/ex1')
def example(request: Test):
    task = create_task.delay(request.a, request.b, request.c)
    return {"task_id": task.task_id, "status": "Processing"}


@router.post('/api/singleCellExperiment')
def singleCellExperiment(request: Request):
    task = load_sce.delay(request.inputPath, request.speciesType, request.outputPath)

    return {"task_id": task.task_id, "status": "Processing"}


@router.get('/result/{task_id}', response_model=Result, status_code=200,
            responses={202: {'model': Task, 'description': 'Accepted: Not Ready'}})
async def fetch_result(task_id):
    print("in the fetch_result function")
    task = AsyncResult(task_id)
    print(task.get())
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    return {'task_id': task_id, 'status': "Completed", "result": task.get()}
