from services.llm_service import LLMService
import asyncio

class QueryRewriterService:
    def __init__(self, llm_service : LLMService):
        self.llm_service = llm_service

    async def rewrite(self, question):

        prompt = f"""
            Rewrite the following user question into a concise search query
            that would help retrieve relevant information from a knowledge base.

            Requirements:
                - Preserve the original intent of the question.
                - Keep important domain concepts from the original question.
                - Preserve useful terms related to the subject, such as shipping,
                shipment, delivery, estimated delivery time, etc., when relevant.
                - You may slightly expand the query if it helps match information
                that may appear in the knowledge base.
                - Do not answer the question.
                - Return only the rewritten search query.

            User question:
            {question}

            Return only the rewritten search query.
            """

        response = await self.llm_service.generate_response(
                        prompt,
                        context=""
                    )

        return response["answer"]

# if __name__ == "__main__" :
#     question = "Do you deliver to Canada?"

#     from dotenv import load_dotenv

#     load_dotenv()
#     llm_service = LLMService()
#     service = QueryRewriterService(llm_service=llm_service)
#     retrival_question = asyncio.run(service.rewrite(question))

#     print("\n Original Question : ", question , "\n Retrival Question : ", retrival_question)


