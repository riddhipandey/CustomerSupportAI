from repositories.document_repository import DocumentRepository
from services.embedding_service import EmbeddingService
from repositories.vector_repository import VectorRepository


class DocumentService:
    def __init__(
            self,
            document_repository = DocumentRepository,
            embedding_service = EmbeddingService,
            vector_repository = VectorRepository
            ):
        self.document_repository = document_repository
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository


    async def get_document_embeddings(self, chunks):
        # documents = await self.document_repository.get_documents()
        # document_records = []

        for chunk in chunks:
            embedding = await self.embedding_service.get_embedding(chunk["text"])
            record = {
                "text" : chunk["text"],
                "embedding" : embedding,
                "metadata" : chunk["metadata"]
            }

            await self.vector_repository.add_records(record)

        return await self.vector_repository.get_all()