import re

class ChunkingService:

    def create_chunks(
            self, 
            pages, 
            document_name : str, 
            document_title : str, 
            document_id : str, 
            chunk_size=100, 
            overlap=20):

        chunks = []
        chunk_index = 0
        for page in pages:
            page_text = page["text"]
            page_number = page["page_number"]

            sections = re.split(
                r"(?=\n?\d+\.\s+)",
                page_text
            )


            for section in sections:

                if not section or not re.match(r"\d+\.\s+", section):
                    continue

                words = section.split()
                # section_info = re.match(r"\d+\.\s+.*", section).group()
                # print(f"SECTION INFO ",section_info)
                section_info = section.split("\n")[0]
                if len(words) <= chunk_size:
                    chunk = {
                        "text" : section,
                        "metadata" : {
                            "document_name" : document_name,
                            "document_title" : document_title,
                            "document_id" : document_id,
                            "chunk_index" : chunk_index,
                            "page_number" : page_number,
                            "section" : section_info
                        }
                    }
                    chunks.append(chunk)
                    chunk_index +=1
                    continue

                start = 0

                while start < len(words):

                    end = start + chunk_size

                    chunk_text = " ".join(words[start:end])
                    chunk = {
                                        "text" : chunk_text,
                                        "metadata" : {
                                            "document_name" : document_name,
                                            "document_title" : document_title,
                                            "document_id" : document_id,
                                            "chunk_index" : chunk_index,
                                            "page_number" : page_number,
                                            "section" : section_info
                                        }
                                    }
                    chunks.append(chunk)
                    chunk_index += 1
                    start = end - overlap


        # chunks = [
        #     section.strip()
        #     for section in sections if section.strip() and re.match(r"\d+\.\s+", section.strip())
        # ]

        return chunks