

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
    