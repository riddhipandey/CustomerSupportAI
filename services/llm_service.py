import os

from openai import AsyncOpenAI

class LLMService:

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    async def generate_response(self, question : str, context : str):
        system_message = """
            You are a helpful customer support assistant.

            Answer the user's question using ONLY the information provided in the context.

            Rules:
            - Use only information explicitly stated in the context.
            - Do not use outside knowledge.
            - Do not make assumptions or infer facts that are not supported by the context.
            - Only consider a fact supported if the context explicitly states it.
            - Do not use geographic, logical, or common-knowledge reasoning to fill in missing information.
            - For questions about a specific country, product, service, date, price, etc.,
            do not assume it is included merely because its broader category or region is mentioned.
            - If the context contains the answer, give the answer directly and clearly.
            - If the context contains only part of the answer, provide only what is explicitly supported.
            - If the context does not contain enough information to answer the question,
            say that you don't have enough information.

            Do not invent information.
            """

        user_message = f"""
            Context:
            {context}

            Question
            {question}
            """

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages = [
                {
                    "role" : "system",
                    "content" : system_message
                },
                {
                    "role" : "user",
                    "content" : user_message
                }
            ]
        )
        answer = response.choices[0].message.content

        # fake_llm_response = {
        #     "system" : system_message,
        #     "user" : user_message,
        #     "answer" : answer
        # }

        return {
            "answer" : answer
        }