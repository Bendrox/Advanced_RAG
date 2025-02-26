
import difflib

def comparer_phrases(phrase1, phrase2):
    mots1 = phrase1.split()
    mots2 = phrase2.split()
    sequence = difflib.SequenceMatcher(None, mots1, mots2)
    differences = []
    for tag, i1, i2, j1, j2 in sequence.get_opcodes():
        if tag == 'replace':
            differences.append(f"Remplacer '{' '.join(mots1[i1:i2])}' par '{' '.join(mots2[j1:j2])}'")
        elif tag == 'delete':
            differences.append(f"Supprimer '{' '.join(mots1[i1:i2])}'")
        elif tag == 'insert':
            differences.append(f"Insérer '{' '.join(mots2[j1:j2])}'")
    return differences

