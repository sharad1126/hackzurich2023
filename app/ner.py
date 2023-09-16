import re
import spacy


relevant_categories = ['PERSON', 'EMAIL', 'ORG', 'RSA_PRIVATE_KEY', 'PHONE', 'IBAN', 'GENDER']


def ner(text):
    nlp = spacy.load("en_core_web_sm")

    patterns = {
        'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        'PHONE': r'(?:(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})',
        'IBAN': r'\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b',
        'GENDER': r'\b(male|female)\b',
        'RSA_PRIVATE_KEY': r'-----BEGIN RSA PRIVATE KEY-----[\s\S]+?-----END RSA PRIVATE KEY-----'
    }

    doc = nlp(text)

    tokens = []

    for ent in doc.ents:
        if ent.label_ in relevant_categories:
            tokens.append((ent.start_char, ent.end_char, ent.label_))

    for tag, pattern in patterns.items():
        for match in re.finditer(pattern, text):
            start_index = match.start()
            end_index = match.end()
            tokens.append((start_index, end_index, tag))

    return tokens
