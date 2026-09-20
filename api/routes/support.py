from fastapi import APIRouter, Depends
from services.support_service import SupportService
from models.requests import SupportRequest
from models.responses import SupportResponse
from services.llm_service import LLMService
from services.embedding_service import EmbeddingService
from repositories.vector_repository import VectorRepository
from dependencies.dependencies import get_support_service


# llm_service=LLMService()
# embedding_service = EmbeddingService()
# vector_repository = VectorRepository()
router = APIRouter()
# support_service = SupportService(llm_service, embedding_service, vector_repository)

@router.post("/support/ask", response_model=SupportResponse)
async def ask_support(
    request : SupportRequest, 
    support_service : SupportResponse = Depends(get_support_service)
):

    response = await support_service.ask(request.question)

    return response

      