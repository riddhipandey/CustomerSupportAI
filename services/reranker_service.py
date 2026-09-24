from sentence_transformers import CrossEncoder

class RerankerService:

    def __init__(self):
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, question, documents):
        pairs = [
            [question, document["text"]]
            for document in documents
        ]

        scores = self.model.predict(pairs)

        for document, score in zip(documents, scores):
            document["rerank_score"] = float(score)

        return sorted(
            documents,
            key=lambda x: x["rerank_score"],
            reverse=True
        )




# if __name__ == "__main__":

#     service = RerankerService()

#     question = "When will my shipment arrive?"

#     documents = [
#         {
#             "text": "Standard Shipping takes 3 to 5 business days."
#         },
#         {
#             "text": "Customers can update their shipping address before processing."
#         },
#         {
#             "text": "Overnight shipping takes 1 business day."
#         }
#     ]

#     results = service.rerank(question, documents)

#     for result in results:
#         print(
#             result["rerank_score"],
#             "->",
#             result["text"]
#         )