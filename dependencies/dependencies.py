from repositories.document_repository import DocumentRepository
from repositories.vector_repository import VectorRepository
from services.document_service import DocumentService
from services.embedding_service import EmbeddingService
from services.llm_service import LLMService
from services.support_service import SupportService

vector_repository = VectorRepository()
embedding_service = EmbeddingService()
llm_service = LLMService()
document_repository = DocumentRepository()

def get_vector_repository():
    return vector_repository

def get_embedding_service():
    return embedding_service

def get_llm_service():
    return llm_service

def get_document_service():
    return DocumentService(
        document_repository,
        embedding_service,
        vector_repository
    )
def get_support_service():
    return SupportService(
        llm_service,
        embedding_service,
        vector_repository
    )