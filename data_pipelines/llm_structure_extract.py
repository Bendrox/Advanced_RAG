
def extract_structure_with_llm(model,document):
    prompt_structure_extract_json = f""" 
            You are an expert data scientist and data engineer with an expertise in law .
            That means that you have a deep knowlage of law.
            
            To do: 
            - Extract the whole structure of this document to prepare to make the best and most reliable embedding.
            - The output is a tabular Json. 
            Example de contenu a mettre en accollade : 
            'article 1er', 'paragraphe n°3', 'contenu': "3. Aux fins de la présente directive, sont 
            criminelle, dans le but de dissimuler ou de déguiser l'origine illicite de ces biens ...".
            
            Rules: 
            - Be as acurate as possible.
            - Do not ommit information.
            - You will be starting from the "Article"
            - Do not omit the structure under "Article" until the last "Article".
            - Do not translate the text : {document} 
            
    """
    for chunk in model.stream(prompt_structure_extract_json):
        print(chunk.content, end="", flush=True) 
        result = chunk.content
        

