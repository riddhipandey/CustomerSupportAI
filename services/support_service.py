from services.llm_service import LLMService
from services.embedding_service import EmbeddingService
from repositories.vector_repository import VectorRepository


class SupportService:

    def __init__(
        self, 
        llm_service : LLMService,
        embedding_service : EmbeddingService,
        vector_repository : VectorRepository):

        self.llm_service = llm_service
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository

    async def ask(self, question : str):
        query_embedding = await self.embedding_service.get_embedding(question)
        relevant_documents = await self.vector_repository.search_similar(query_embedding, top_k=8)

        # print("Question:", question)
        # print("Query embedding:", query_embedding)
        # for document in relevant_documents:
        #     print("Relevant document:", document["text"])

        print("Number of relevant documents:", len(relevant_documents))
        if not relevant_documents:
            return {
                "answer" : "I dont have enough information about this question"
            }
        
        context = "\n".join(
            document["text"] for document in relevant_documents
        )
        # print("ABOUT TO CALL LLM")
        # print("QUESTION SENT TO LLM:")
        # print(question)
        # print("CONTEXT SENT TO LLM:")
        # print(context)
        response = await self.llm_service.generate_response(question, context=context)
        return response