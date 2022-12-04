import os
from rpy2 import robjects


def load_sce(inputPath, species, outputPath):
    if os.path.exists(inputPath):
        if os.path.exists(os.path.join(inputPath, "annotation.txt")) and os.path.exists(
                os.path.join(inputPath, "annotation.txt")):
            robjects.r('''
                        f <- function(path, species, outputPath) { 
                            library(SingleCellExperiment) 
                            molecules <- read.delim(file.path(path,"molecules.txt"), sep = "\t", row.names = 1) 
                            annotation <- read.delim(file.path(path,"annotation.txt"), sep = "\t", stringsAsFactors = T)
                            sce <- SingleCellExperiment(assays=list(counts= as.matrix(molecules)), colData=annotation) 
                            altExp(sce,"ERCC") <- sce[grep("^ERCC-",rownames(sce)), ]
                            sce <- sce[grep("^ERCC-",rownames(sce),invert = T), ]
                            # Map ENSEMBL IDs to gene symbols
                            if (species == "mouse") {
                              library(EnsDb.Mmusculus.v79) 
                              ENSDB <- "EnsDb.Mmusculus.v79"
                              library(org.Mm.eg.db)  #library(org.Hs.eg.db) if human
                              EGDB <- "org.Mm.eg.db"
                            } else if (species == "human") {
                              library(EnsDb.Hsapiens.v86)
                              ENSDB <- "EnsDb.Hsapiens.v86"
                              library(org.Hs.eg.db)
                              EGDB <- "org.Hs.eg.db"
                            } else {
                              stop('You must set SPECIES to either "mouse" or "human" at the start of this code block!')
                            }
                            gene_names <- mapIds(get(EGDB), keys=rownames(sce), keytype="ENSEMBL", columns="SYMBOL",column="SYMBOL")
                            ensdb_genes <- genes(get(ENSDB))

                            rowData(sce)$SYMBOL <- gene_names
                            MT_names <- ensdb_genes[seqnames(ensdb_genes) == "MT"]$gene_id
                            is_mito <- rownames(sce) %in% MT_names
                            table(is.na(gene_names))
                            table(is_mito)
                            print("Remove all genes for which no symbols were found.")
                            sce <- sce[! is.na(rowData(sce)$SYMBOL),] # Remove all genes for which no symbols were found

                            print("Check if we can find mitochondrial proteins in the newly annotated symbols.")
                            grep("^MT-",rowData(sce)$SYMBOL,value = T) # Check if we can find mitochondrial proteins in the newly annotated symbols
                            grep("^RP[LS]",rowData(sce)$SYMBOL,value = T)
                            grep("ATP8",rowData(sce)$SYMBOL,value = T) # Quick search for mitochondrial protein ATP8, which is also called MT-ATP8
                            saveRDS(sce, file = file.path(outputPath))
                        } 
                        ''')
            r_f = robjects.globalenv['f']
            sce = (r_f(inputPath, species, outputPath))
            print(sce)
        else:
            print("File doesn't exists")
            raise NameError("File doesn't exists")  # Raise Error
    else:
        print("Directory doesn't exists")
        raise NameError("Directory doesn't exists")  # Raise Error

