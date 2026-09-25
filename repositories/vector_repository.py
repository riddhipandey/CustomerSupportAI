import math

class VectorRepository:
    def __init__(self):
        self.records = []

    async def add_records(self, record):
        self.records.append(record)

    async def get_all(self):
        return self.records

    async def search_similar(self, query_embedding, question, top_k = 4):
        # best_record = None
        # best_score = -1
        results = []
        stop_words = {
                    "when", "will", "my", "the", "is",
                    "a", "an", "to", "of", "in", "for"
                }
        words = question.lower().split()

        keywords = [
            word.strip(".,?!")
            for word in words
            if word not in stop_words
        ]
        
        query_magnitude = math.sqrt(
                        sum(q * q for q in query_embedding)
                    )
        
        for record in self.records:
            document_embedding = record["embedding"]
            document_text = record["text"].lower()

            keyword_score = sum(
                1 for word in keywords
                if word in document_text
            )
            keyword_score = keyword_score / len(keywords) if keywords else 0

            # print("Keyword score:", keyword_score)

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
            # print("Document:", record["metadata"]["section"])
            # print("Similarity:", similarity)

            final_score = (0.7 * similarity) + (0.3 * keyword_score)
            # print("Final score:", final_score)

            if similarity >= .30:
                results.append({
                    "text" :record["text"],
                    "embedding" : record["embedding"],
                    "metadata" : record["metadata"],
                    "similarity" : similarity,
                    "keyword_score": keyword_score,
                    "final_score": final_score
                })

        results.sort(
            key=lambda x:x["final_score"],
            reverse=True
        )

        # if best_score < 0.50:
        #     return None

        return results[:top_k]