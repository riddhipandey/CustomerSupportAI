import math

class VectorRepository:
    def __init__(self):
        self.records = []

    async def add_records(self, record):
        self.records.append(record)

    async def get_all(self):
        return self.records

    async def search_similar(self, query_embedding, top_k = 4):
        # best_record = None
        # best_score = -1
        results = []

        query_magnitude = math.sqrt(
                        sum(q * q for q in query_embedding)
                    )
        
        for record in self.records:
            document_embedding = record["embedding"]
            document_text = record["text"]

            dot_product = sum(
                q * d
                for q, d in zip(query_embedding, document_embedding)
            )

            document_magnitude = math.sqrt(
                sum(d * d for d in document_embedding)
            )

            similarity = (
                dot_product /
                (query_magnitude * document_magnitude)
            )

            # if similarity > best_score:
            #     best_score = similarity
            #     best_record = record

            # print("Query:", query_embedding)
            # print("Document:", document_embedding)
            # print("Document:", document_text)
            # print("Similarity:", similarity)   
            print("Document:", record["metadata"]["section"])
            print("Similarity:", similarity)

            if similarity >= .30:
                results.append({
                    "text" :record["text"],
                    "embedding" : record["embedding"],
                    "metadata" : record["metadata"],
                    "similarity" : similarity
                })

        results.sort(
            key=lambda x:x["similarity"],
            reverse=True
        )

        # if best_score < 0.50:
        #     return None

        return results[:top_k]