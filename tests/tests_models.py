from models.llm_models import *
from models.embedding_models import *

prompt = "Fais une blague sur les actuaires"

# test 1
for chunk in llm_4omini.stream(prompt):
    print(chunk.content, end="", flush=True)
    
# test 2
for chunk in llm_4o.stream(prompt):
    print(chunk.content, end="", flush=True)

# test 3
sentence1 = "test"
emb1 = embeddings.embed_query(sentence1)
print(emb1)