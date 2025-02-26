from models.llm_models import llm_4omini, llm_4o
from models.embedding_models import embeddings

prompt = "Réponds en un mot"

# test 1
if not llm_4omini.invoke(prompt):
    raise AssertionError("Error : Gpt4o mini failed test run")
else:
    print("Gpt4o mini succeded test run! ")
    
# test 2    
if not llm_4o.invoke(prompt):
    raise AssertionError("Error : Gpt4o failed test run")
else:
    print("Gpt4o succeded test run !")

# test embedding:
sentence1 = "test"
emb1 = embeddings.embed_query(sentence1)
if not sentence1:
    raise AssertionError("Error : embedding failed test run")
else:
    print(f"Test Embedding succeded !")
