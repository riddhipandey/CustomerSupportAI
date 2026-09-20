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

            If the context contains the answer, give the answer directly and clearly.
            Do not say that you lack information when the answer is present in the context.

            If the context truly does not contain enough information to answer the question,
            then say you don't have enough information.
            """

        user_message = f"""
            Context:
            {context}

            Question
            {question}
            """

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
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