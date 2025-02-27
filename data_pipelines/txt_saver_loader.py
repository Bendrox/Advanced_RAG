

def load_txt(filepath: str):
    """
    Charge un fichier txt dans une variable str

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

# Utilisation :
save_txt("resultat_extraction.txt", "Ceci est mon texte extrait et nettoyé.")

