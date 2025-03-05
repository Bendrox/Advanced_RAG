import tiktoken
import numpy as np

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """
    Calcule et affiche le nombre de tokens d'un texte donné en utilisant  
    l'encodage spécifique au modèle OpenAI.  

    Args:  
        text (str): Le texte dont on souhaite compter les tokens.  
        model (str, optional): Le nom du modèle pour lequel l'encodage est choisi.  
                               Par défaut 'gpt-4o'.  

    Returns: Le nombre de tokens du texte.  

    Remarque : La fonction affiche également le nombre de tokens dans la console.  
    """
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    token_count = len(tokens)
    return token_count

def chunk_stat(your_chunks):
    """Produit des stats sur le nombre de tokens par chunks. 
    Pour but d'améliorer les performances 

    Args:your_chunks (_type_)
    """
    chunk_lengths = [count_tokens(chunk) for chunk in your_chunks]
    print("Nombre de chunks :", len(your_chunks))
    print("Longueur moyenne des chunks:", np.mean(chunk_lengths))
    print("Longueur max des chunks:", np.max(chunk_lengths))
    print("Longueur min des chunks:", np.min(chunk_lengths))
