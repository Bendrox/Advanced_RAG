

# step 1: 

def pipe_1_url_to_pdf(url, save_path):
    """Optimized pipeline Transform local URL eurlex to a local file PDF

    Args:
        url (_type_): url of eurlex , exemple: http://publications.europa.eu/resource/celex/32013R0575
        save_path (_type_): give your local path
    """
    response = requests.get(url, 
                            headers={"Accept": "application/pdf"})
    # tres important pour ne pas renvoyer rdf ou autre format...
    with open(save_path, "wb") as f:
        f.write(response.content)
        

# step 3: 

def pipe_3_nettoyer_texte(texte):
    # 1. Supprime les caractères de coupure de mot suivis de retour à la ligne
    texte = re.sub(r'\xad\n', '', texte)

    # 2. \ndénommé -> dénommé, \nEn -> En
    texte = re.sub(r'\n(?=\w)', '', texte)

    # 3. Supprime les retours à la ligne devant une parenthèse contenant des chiffres (\n(2) -> (2))
    texte = re.sub(r'\n(?=\(\d+\))', '', texte)

    # 4. Remplace les apostrophes échappées (l\'Union -> l'Union)
    texte = re.sub(r"\\'", "'", texte)

    # 5. Supprime tout autre backslash isolé non nécessaire
    texte = re.sub(r'\\', '', texte)

    return texte