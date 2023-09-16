import re
import spacy


relevant_categories = ['PERSON', 'EMAIL', 'RSA_PRIVATE_KEY', 'PHONE', 'IBAN', 'ADDRESS']


def ner(text):
    nlp = spacy.load("en_core_web_sm")
    # nlp = spacy.load("de_core_news_sm")
    # nlp = spacy.load("xx_ent_wiki_sm")

    patterns = {
        'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        'PHONE': r'^(?:\+49|\+44|\+41)[\s.-]*[1-9]\d{0,3}[\s.-]*\d{1,7}$',
        'IBAN': r'\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b',
        # 'GENDER': r'\b(male|female)\b',
        'RSA_PRIVATE_KEY': r'-----BEGIN RSA PRIVATE KEY-----[\s\S]+?-----END RSA PRIVATE KEY-----',
        'ADDRESS': r'\w+\s+\w+\s+\d+\n\d{4,5}\s+\w+\n\w+'
    }

    doc = nlp(text)

    tokens = []

    for ent in doc.ents:
        if ent.label_ in relevant_categories:
            tokens.append((ent.text, ent.start_char, ent.end_char, ent.label_))

    for tag, pattern in patterns.items():
        for match in re.finditer(pattern, text):
            matched_text = match.group()
            start_index = match.start()
            end_index = match.end()
            tokens.append((matched_text, start_index, end_index, tag))

    return tokens
