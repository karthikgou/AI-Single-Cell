import fastapi

from api.service import load_sce
from api.models import Request
from api.models import Task

router = fastapi.APIRouter()


@router.get('/')
async def index():
    return "Hello!!"


@router.post('/api/singleCellExperiment', response_model=Task, status_code=202)
async def singleCellExperiment(request: Request):
    load_sce(request.inputPath, request.speciesType, request.outputPath)

    return {"task_id": "1234567", "status": "Processing"}


# @router.get('/result/{task_id}', response_model=Result, status_code=200,
#             responses={202: {'model': Task, 'description': 'Accepted: Not Ready'}})
# async def fetch_result(task_id):
#     task = AsyncResult(task_id)
#     if not task.ready():
#         return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
#     result = task.get()
#     return {'task_id': task_id, 'status': str(result)}
