import os
import logging

from openai import AsyncOpenAI
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger(__name__)

class EmbeddingService:

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key = os.getenv("OPENAI_API_KEY")
        )

        self.cache = {}

    async def get_embedding(self, text : str):

        if text in self.cache:
            logger.info("CACHE HIT")
            return self.cache[text]

        logger.info("CACHE MISS - CALLING OPENAI")
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        embedding = response.data[0].embedding
        self.cache[text] = embedding

        return embedding







# # OUTSIDE the class
# async def test():

#     service = EmbeddingService()

#     embedding = await service.get_embedding(
#         "Customers can request a refund within 30 days."
#     )

#     print("Embedding length:", len(embedding))
#     print("First 5 values:", embedding[:5])


# # OUTSIDE the class
# if __name__ == "__main__":
    # asyncio.run(test())  
    # async def get_embedding(self, text : str):
    #     if "order" in text.lower():
    #         return [0.90, 0.10, 0.80, 0.20, -0.30]

    #     if "refund" in text.lower():
    #         return [0.20, 0.90, 0.10, -0.40, 0.70]

    #     if "password" in text.lower():
    #         return [-0.30, 0.20, 0.90, 0.70, 0.10]

    #     return [0.10, 0.10, 0.10, 0.10, 0.10]
