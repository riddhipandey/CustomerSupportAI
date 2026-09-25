from repositories.document_repository import DocumentRepository
from repositories.vector_repository import VectorRepository
from services.reranker_service import RerankerService
from services.document_service import DocumentService
from services.embedding_service import EmbeddingService
from services.llm_service import LLMService
from services.support_service import SupportService
from services.query_rewriter_service import QueryRewriterService

vector_repository = VectorRepository()
embedding_service = EmbeddingService()
llm_service = LLMService()
document_repository = DocumentRepository()
reranker_service = RerankerService()
query_rewriter_service = QueryRewriterService(llm_service)

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

def get_query_rewriter_service():
    return query_rewriter_service

def get_reranker_service():
    return reranker_service

def get_support_service():
    return SupportService(
        llm_service,
        embedding_service,
        vector_repository,
        reranker_service,
        query_rewriter_service
    )