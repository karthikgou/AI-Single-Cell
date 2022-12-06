import fastapi
import uvicorn
from api import home
# from NormalTest import test

# rpy2

# import rpy2.robjects as robjects

# from rpy2.robjects.packages import importr

# Installing Packages

# scater = importr('scater')
# print("Scater package is installed without any issues")
# AnnotationDbi = importr('AnnotationDbi')
# print("AnnotationDbi package is installed without any issues")
# optparse = importr('optparse')
# print("optparse package is installed without any issues")
# anndata = importr('anndata')
# print("anndata package is installed without any issues")
# Seurat = importr('Seurat')
# print("Seurat package is installed without any issues")
# SingleCellExperiment = importr('SingleCellExperiment')
# print("SingleCellExperiment package is installed without any issues")
# SeuratDisk = importr('SeuratDisk')
# print("SeuratDisk package is installed without any issues")
# SeuratData = importr('SeuratData')
# print("SeuratData package is installed without any issues")
# patchwork = importr('patchwork')
# print("patchwork package is installed without any issues")
# loomR = importr('loomR')
# print("loomR package is installed without any issues")


app = fastapi.FastAPI()


def configure():
    app.include_router(home.router)
    # app.include_router(test.router)


configure()

if __name__ == '__main__':
    uvicorn.run(app)
