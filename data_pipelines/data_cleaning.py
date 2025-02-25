

def supr_avant_directive_mrk(texte):
    start_phrase = "ONT ADOPTÉ LA PRÉSENTE DIRECTIVE:\n\nCHAPITRE I"
    index_debut = texte.find(start_phrase)
    if index_debut != -1:
        return texte[index_debut:]
    else:
        return "Le texte ne contient pas la phrase spécifiée."
    

def supr_apres_directive_mrk(texte):
    end_phrase = "Par le Parlement européen\n\nLe président\n"
    index_fin = texte.find(end_phrase)
    if index_fin != -1:
        return texte[:index_fin + len(end_phrase)]
    else:
        return texte  

import re

def nettoyer_markdown(texte):
    # Supprimer les tableaux Markdown
    texte = re.sub(r'\|.*?\|', '', texte)
    texte = re.sub(r'\|\s*---\s*\|', '', texte)
    
    # Supprimer les liens Markdown
    texte = re.sub(r'\[.*?\]\(.*?\)', '', texte)
    
    # Supprimer les annotations de type [texte][numéro]
    texte = re.sub(r'\[.*?\]\[\d+\]', '', texte)
    
    # Supprimer les espaces multiples et les lignes vides consécutives
    texte = re.sub(r'\n\s*\n', '\n', texte)
    texte = re.sub(r'[ ]{2,}', ' ', texte)
    
    # Supprimer les caractères spéciaux isolés comme '|'
    texte = re.sub(r'\|', '', texte)
    
    return texte.strip()


def weird_carac_remove(variable):
    variable_1 = variable.replace("\xa0", " ")
    variable_2 = variable_1.replace("\n", " ")
    return variable_2

def supr_avant_reglement_mrk(texte):
    start_phrase = "ONT ADOPTÉ LE PRÉSENT RÈGLEMENT"
    index_debut = texte.find(start_phrase)
    if index_debut != -1:
        return texte[index_debut:]
    else:
        return "Le texte ne contient pas la phrase spécifiée."
    
def supr_apres_reglement_mrk(texte):
    end_phrase = "Par le Parlement européen"
    index_fin = texte.find(end_phrase)
    if index_fin != -1:
        return texte[:index_fin + len(end_phrase)]
    else:
        return texte  
