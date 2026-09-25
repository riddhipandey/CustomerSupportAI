from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.routes.support import router as support_router
from repositories.document_repository import DocumentRepository
from services.chunking_service import ChunkingService
from services.embedding_service import EmbeddingService
from services.document_service import DocumentService
from dependencies.dependencies import vector_repository, embedding_service, get_document_service
from services.pdf_service import PDFService

import logging_config
# document_repository = DocumentRepository()
# embedding_service = EmbeddingService()
# vector_repository = VectorRepository()

document_service = get_document_service()
pdf_service = PDFService()
chunking_Service = ChunkingService()

@asynccontextmanager
async def lifespan(app : FastAPI):
    # document_records = await document_service.get_document_embeddings()
    # print(document_records)

    # pages = pdf_service.extract_pdf_text(
    #     "data/sample_shipping_policy.pdf"
    # )

    # # chunking_text = "\n".join(page["text"] for page in pages)
    # chunks = chunking_Service.create_chunks(pages,"sample_shipping_policy.pdf", "Standard Corporate Shipping Policy", "POL-SHP-2026-V1")
    # document_records = await document_service.get_document_embeddings(chunks=chunks)
    # for record in document_records:
    #     print(record)

    # for i, chunk in enumerate(chunks):
    #     print(f"\n---Chunk {i+1} ---")
    #     print(chunk)
    
    
    
    print("application startup complete")

    await initialize_documents()
    
    yield
    #print only after application stops just before stoping.
    print("application shutting down")


app = FastAPI(lifespan = lifespan)
app.include_router(support_router)


async def initialize_documents():

    pages = pdf_service.extract_pdf_text(
        "data/sample_shipping_policy.pdf"
    )

    chunks = chunking_Service.create_chunks(
        pages,
        "sample_shipping_policy.pdf",
        "Standard Corporate Shipping Policy",
        "POL-SHP-2026-V1"
    )

    await document_service.get_document_embeddings(
        chunks=chunks
    )
