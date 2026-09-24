from pydantic import BaseModel

class Source(BaseModel):
    document_name : str
    document_title : str
    document_id : str
    page_number : int
    section : str

class SupportResponse(BaseModel):
    answer : str
    sources : list[Source]