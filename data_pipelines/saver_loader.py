
import json 

def load_txt(filepath: str):
    """
    Charge un fichier txt local dans une variable str
    
    Args: filepath (str)
    Returns: str
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()
    
   
def save_txt(filepath: str, text: str):
    """
    Sauvegarde le texte donné dans un fichier .txt.
    
    Args:
        filepath (str): Chemin du fichier où sauvegarder le texte.
        text (str): Contenu texte à écrire.
    """
    with open(filepath, "w", encoding="utf-8") as fichier:
        fichier.write(text)

def save_dict_json(filepath: str, dict: dict):
    """sauvgarde un fichier dict (chunks) en json dans un fichier local.

    Args:
        filepath (str): chemin sauvarde du fichier json
        dict (dict): nom de la variable 
    """
    with open(filepath, "w", encoding="utf-8") as fichier:
        json.dump( #écrit le dictionnaire dans un fichier
                dict, 
                fichier, 
                ensure_ascii=False,# garde les accents/caractères spéciaux lisibles
                indent=4) # rend le fichier lisible avec une bonne indentation
        
        
import json

def save_doc_json(filepath: str, dict_obj: dict):
    """Sauvegarde un chunk document en JSON après conversion des objets non sérialisables.

    Args:
        filepath (str): chemin de sauvegarde du fichier json
        dict_obj (dict): dictionnaire à sauvegarder
    """
    def convert(obj):
        # si l'objet est un Document, on le convertit en dictionnaire
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return str(obj)  # fallback pour tout autre type non sérialisable

    with open(filepath, "w", encoding="utf-8") as fichier:
        json.dump(dict_obj, fichier, ensure_ascii=False, indent=4, default=convert)