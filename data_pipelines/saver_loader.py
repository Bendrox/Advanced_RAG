
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