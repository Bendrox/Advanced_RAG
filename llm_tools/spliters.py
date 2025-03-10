
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from models.embedding_models import emb_3_large


text_splitter_recursive_carac = RecursiveCharacterTextSplitter(
    chunk_size=900 ,
    chunk_overlap=90,
    # Ordre des séparateurs, du plus large au plus fin
    #separators=["\n\n", "\n", "."]
)

text_splitter_semantic_v2_prc = SemanticChunker(emb_3_large,
                                            breakpoint_threshold_type="percentile",
                                            breakpoint_threshold_amount=40)# default is 95+ de segments.


text_splitter_semantic_v3_gdt = SemanticChunker(emb_3_large,
                                            breakpoint_threshold_type="gradient",
                                            breakpoint_threshold_amount=40) # default is 95 . Diminue + de segments.

