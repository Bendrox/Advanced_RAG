from data_pipelines.str_diff_tools import comparer_phrases
from models.llm_models import llm_41_mini, llm_4omini


def get_eu_data_3p(llm_model, reglement_ue, fr_old_version, fr_new_version):
    prompt_LCQA_3p = f""" 
        Tu es un juriste expert avec au moins 10 ans d expérience.
        Tu as une double expertise a la fois dans la réglementation francaise et dans les textes européens.
        Tu as travaillé a plusieurs reprises sur la transposition des textes européens dans la réglementation francaise.
        
        Ta tâche :
        -   Analyser les changements réglementaires dans la loi francaise avec pour objectif de trouver la ou les parties
        de la directive UE (article ou articles) a l origine de ce(s) changement(s).
        
        Régles : 
        - Tu te baseras uniquement sur les informations fournies pour faire ton analyse.
        - Tu feras ton analyse de la facon la plus conconcieuse et précise 
        - Tu ne pas pas reciter le contenu de la loi francaise avant et après modification
        
        Voici le text européen {reglement_ue}
        Voici le texte de loi francais dans sa version avant l'entree en vigueur du text européen: {fr_old_version}
        Voici le texte de loi francais dans sa version après l'entree en vigueur du text européen: {fr_new_version}
"""

    output = llm_model.invoke(prompt_LCQA_3p)
    output= output.content
    return output

def get_eu_data_4p(llm_model, reglement_ue, fr_old_version, fr_new_version):
    changement_derter= comparer_phrases(fr_old_version, fr_new_version)
    prompt_LCQA_4p = f""" 
            Tu es un juriste expert avec au moins 10 ans d expérience.
            Tu as une double expertise a la fois dans la réglementation francaise et dans les textes européens.
            Tu as travaillé a plusieurs reprises sur la transposition des textes européens dans la réglementation francaise.
            
            
            Ta tâche :
            -   Analyser les changements réglementaires dans la loi francaise et de trouver la ou les parties
            de la directive UE (article ou articles) a l origine de ce changement réglementaire.
            
            Régles : 
            - Tu te baseras uniquement sur les informations fournies pour faire ton analyse.
            - Tu feras ton analyse de la facon la plus conconcieuse et précise 
            
            Voici le text européen {reglement_ue}
            Voici le texte de loi francais dans sa version avant l'entree en vigueur du text européen: {fr_old_version}
            Voici le texte de loi francais dans sa version après l'entree en vigueur du text européen: {fr_new_version}
            Voici une indication des changements entre les deux version du texte francais sur la quelle tu t appuieras pour
            trouver la partie du texte europeen a l origine de ce changement : {changement_derter}

    """

    output = llm_model.invoke(prompt_LCQA_4p)
    output= output.content
    return output
        
                    
        
        