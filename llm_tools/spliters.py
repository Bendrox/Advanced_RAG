
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter_recursive_carac = RecursiveCharacterTextSplitter(
    chunk_size=900 ,
    chunk_overlap=90,
    # Ordre des séparateurs, du plus large au plus fin
    separators=["\n\n", "\n", "."]
)