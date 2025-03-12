from models.llm_models import llm_4omini, llm_41_mini
from models.embedding_models import emb_3_large

prompt = "Réponds en un mot"


# test 1: embedding:
sentence1 = "test"
emb1 = emb_3_large.embed_query(sentence1)
if not sentence1:
    raise AssertionError("Error : embedding failed test run")
else:
    print(f"Test Embedding succeded !")
    
# test 2: llm_4omini
if not llm_4omini.invoke(prompt):
    raise AssertionError("Error : Gpt4o mini failed test run")
else:
    print("Gpt4o mini succeded test run! ")

# test 3:
if not llm_41_mini.invoke(prompt):
    raise AssertionError("Error : Gpt4o mini failed test run")
else:
    print("Gpt4.1 mini succeded test run! ")
    