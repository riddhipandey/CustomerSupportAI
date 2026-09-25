from evaluation.evaluation_dataset import evaluation_dataset
from dependencies.dependencies import get_vector_repository, get_embedding_service, get_query_rewriter_service, get_reranker_service
from main import initialize_documents
import asyncio
import pandas as pd

## Did we find our all relevant documents in top k retrieved documents.
def calculate_recall(expected_sections, retrieved_documents, k):

    top_k_documents = retrieved_documents[:k]

    retrieved_sections = {
        document["metadata"]["section"]
        for document in top_k_documents
    }

    if not expected_sections:
        return None

    matched_sections = [
        section 
        for section in expected_sections
        if section in retrieved_sections
    ]

    return len(matched_sections) / len(expected_sections)

##How many irrelevant document did we find with our relevant documents.
def calculate_precision(expected_sections, retrieved_documents, k):

    top_k_documents = retrieved_documents[:k]

    retrieved_sections = {
        document["metadata"]["section"]
        for document in top_k_documents
    }

    if not expected_sections:
        return None

    relevant_document_count = sum(
        1 
        for section in expected_sections
        if section in retrieved_sections
    )
        
    return relevant_document_count/ len(top_k_documents)

#mrr -  Mean Reciprocal Rank - if we found relevant document at which position its present.
def calculate_mrr(expected_sections, retrieved_documents, k): 

    top_k_documents = retrieved_documents[:k]

    if not expected_sections:
        return None

    for index, document in enumerate(top_k_documents, start = 1):

        section = document["metadata"]["section"]

        if section in expected_sections:
            return 1 / index

    return 0.0

## did we find at leat one relevant document in the retrieved top k documents.
def calculate_hit_rate(expected_sections, retrieved_documents, k): 

    top_k_documents = retrieved_documents[:k]

    if not expected_sections:
        return None

    retrieved_sections = {
        document["metadata"]["section"] 
        for document in top_k_documents
    }

    for section in expected_sections:
        if section in retrieved_sections:
            return 1.0

    return 0.0



async def evaluate_question(question, expected_sections):

    embedidng_service = get_embedding_service()
    vector_repository = get_vector_repository()
    query_rewriter_service = get_query_rewriter_service()
    reranker_service = get_reranker_service()

    retrieval_question = await query_rewriter_service.rewrite(question=question)
    question_embedding =await embedidng_service.get_embedding(retrieval_question)

    documents = await vector_repository.search_similar(
                 question_embedding, question, top_k = 8
        )

    recall = calculate_recall(expected_sections, documents, 8)
    precision = calculate_precision(expected_sections, documents, 8)
    mrr = calculate_mrr(expected_sections, documents, 8)
    hit_rate = calculate_hit_rate(expected_sections, documents, 8)

    reranked_documents = reranker_service.rerank(retrieval_question, documents)
    top_3_reranked_documents = reranked_documents[:3]

    reranked_recall = calculate_recall(expected_sections, top_3_reranked_documents, 3)
    reranked_precision = calculate_precision(expected_sections, top_3_reranked_documents, 3)
    reranked_mrr = calculate_mrr(expected_sections, top_3_reranked_documents, 3)
    reranked_hit_rate = calculate_hit_rate(expected_sections, top_3_reranked_documents, 3)
    
    return {
        "question": question,
        "expected_sections": ", ".join(expected_sections),
        "recall@8": recall,
        "precision@8": precision,
        "mrr@8": mrr,
        "hit_rate@8": hit_rate,
        "rerank_recall@3": reranked_recall,
        "rerank_precision@3": reranked_precision,
        "rerank_mrr@3": reranked_mrr,
        "rerank_hit_rate@3": reranked_hit_rate,
    }
    # print("\nQuestion:", question)
        
        # print("\nRetrieved sections:")
        
        # for document in documents:
        #     print(document["metadata"]["section"])
        
        # print("\nRecall@8:", recall)
        # print("\nPrecision@8:", precision)
        
    
    #Reranked details print
    # print("\nRewritten Question:", retrieval_question)
    
    # print("\nReranked Retrieved sections:")
    
    # for document in top_3_reranked_documents:
    #     print(document["metadata"]["section"])
    
    # print("\nRerank_Precision@3:", reranked_precision)


async def run_evaluation():

    await initialize_documents()
    results = []

    for item in evaluation_dataset:
        
        result = await evaluate_question(
            item["question"],
            item["expected_sections"]
        )

        results.append(result)

    df = pd.DataFrame(results)
    print(df.to_string(index=False))
    df.to_csv(
        "evaluation/evaluation_results.csv",
        index=False
    )
    average_metrics = (
        df[
            [
                "recall@8",
                "precision@8",
                "mrr@8",
                "hit_rate@8",
                "rerank_recall@3",
                "rerank_precision@3",
                "rerank_mrr@3",
                "rerank_hit_rate@3",

            ]
        ]
        .mean()
        .mul(100)
        .map(lambda x : f"{x:.2f} %")
    )
    


    print("\nAverage Metrics:")
    print(average_metrics)


if __name__ == "__main__":

    asyncio.run(
        run_evaluation()
    )

# if __name__ == "__main__":

#     retrieved_documents = [
#         {
#             "metadata": {
#                 "section": "3. Domestic Shipping Options and Delivery Rates"
#             }
#         },
#         {
#             "metadata": {
#                 "section": "4. Delivery to P.O. Boxes and Military Addresses"
#             }
#         },
#         {
#             "metadata": {
#                 "section": "5. International Shipping, Customs, and Duties"
#             }
#         }
#     ]

#     score = calculate_recall(
#         ["3. Domestic Shipping Options and Delivery Rates"],
#         retrieved_documents,
#         3
#     )

#     print("Recall@3:", score)
