from models.llm_models import llm_4omini, llm_4o
from models.embedding_models import embeddings

prompt = "Réponds en un mot"

# test 1
if not llm_4omini.invoke(prompt):
    raise AssertionError("Erreur : Gpt 4o mini succeded test run.")
else:
    print("Gpt 4o mini fonctionne avec succès")
    
# test 2    
if not llm_4o.invoke(prompt):
    raise AssertionError("Erreur : Gpt 4o succeded test run.")
else:
    print("Gpt 4o fonctionne avec succès")

# test embedding:
sentence1 = "test"
emb1 = embeddings.embed_query(sentence1)
if not sentence1:
    raise AssertionError("Erreur : la phrase d'entrée pour l'embedding est vide.")
else:
    print(f"Test Embedding généré avec succès")