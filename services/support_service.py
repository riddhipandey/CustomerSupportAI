from services.llm_service import LLMService
from services.embedding_service import EmbeddingService
from repositories.vector_repository import VectorRepository
from services.reranker_service import RerankerService
from services.query_rewriter_service import QueryRewriterService


class SupportService:

    def __init__(
        self, 
        llm_service : LLMService,
        embedding_service : EmbeddingService,
        vector_repository : VectorRepository,
        reranker_service : RerankerService,
        query_rewriter_service : QueryRewriterService):

        self.llm_service = llm_service
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository
        self.reranker_service = reranker_service
        self.query_rewriter_service = query_rewriter_service

    async def ask(self, question : str):

        sources = []
        original_question = question
        retrieval_question = await self.query_rewriter_service.rewrite(original_question)

        # print("\nOriginal Question : ", original_question, "  \nRetrieval Question:", retrieval_question)

        query_embedding = await self.embedding_service.get_embedding(retrieval_question)
        relevant_documents = await self.vector_repository.search_similar(query_embedding, retrieval_question, top_k=8)

        reranker_documents = self.reranker_service.rerank(retrieval_question, relevant_documents)

        top_documents = reranker_documents[:3]
        # print(top_documents[0])
        # for result in top_documents:
        #     print(
        #     "\nScore:", result["rerank_score"],
        #     "\nSection:", result["metadata"]["section"],
        #     # "\nText:", result["text"]
        #     )
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
            document["text"] for document in top_documents
        )

        print("\nOriginal Question:", original_question)
        print("Retrieval Question:", retrieval_question)

        print("\nTop Documents:")
        for document in top_documents:
            print(
                "\nScore:", document["rerank_score"],
                "\nSection:", document["metadata"]["section"],
                # "\nText:", document["text"]
            )

        # print("\nFinal Context:")
        # print(context)

        # print("\n===== FINAL LLM INPUT =====")
        # print("Original Question:", original_question)
        # print("Context:")
        # print(context)
        # print("===========================\n")
        # print("ABOUT TO CALL LLM")
        # print("QUESTION SENT TO LLM:")
        # print(question)
        # print("CONTEXT SENT TO LLM:")
        # print(context)
        response = await self.llm_service.generate_response(original_question, context=context)

        answer = response["answer"]

        if "don't have enough information" not in answer.lower():
            best_score = top_documents[0]["rerank_score"]
            SOURCE_SCORE_GAP = 1.0

            for document in top_documents:

                    score_difference = best_score - document["rerank_score"]

                    if score_difference <= SOURCE_SCORE_GAP:
                        metadata = document["metadata"]

                        sources.append({
                            "document_name" : metadata["document_name"],
                            "document_title": metadata["document_title"],
                            "document_id": metadata["document_id"],
                            "page_number": metadata["page_number"],
                            "section": metadata["section"]
                            })

        return {
            "answer" : answer,
            "sources" : sources
        }