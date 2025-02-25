import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text_snowball(texte, langue='french'):
    """
    Cette fonction prend en entrée un texte, supprime les stopwords et applique le SnowballStemmer,
    puis retourne le texte prétraité sous forme de chaîne de caractères.
    
    :param texte: Le texte à traiter (chaîne de caractères).
    :param langue: La langue du texte et du stemmer (par défaut 'french').
    :return: Une chaîne de caractères du texte prétraité.
    """
    # Initialisation du stemmer pour la langue spécifiée
    stemmer = SnowballStemmer(langue)
    
    # Chargement des stopwords pour la langue spécifiée
    stop_words = set(stopwords.words(langue))
    
    # Tokenisation du texte
    mots = word_tokenize(texte, language=langue)
    
    # Filtrage des stopwords et racinisation des mots restants
    mots_filtrés_et_racinisés = [
        stemmer.stem(mot) for mot in mots
        if mot.isalnum() and mot.lower() not in stop_words
    ]
    
    # Conversion de la liste de mots en une chaîne de caractères
    texte_pretraite = ' '.join(mots_filtrés_et_racinisés)
    
    return texte_pretraite