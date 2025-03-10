import tiktoken
import numpy as np

def str_count_tokens(text: str, model: str = "gpt-4o") -> int:
    """
    Calcul et affiche le nombre de tokens d'un texte donné en utilisant  
    l'encodage spécifique au modèle gpt-4o. 

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

