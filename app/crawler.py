"""
This is a simple crawler that you can use as a boilerplate for your own
implementation. The crawler labels `.txt` files that contain the word
"hello" as "true", `.txt` files without "hello" as "false" and every other
item as "review". Try to modify this simple implementation so that it finds
some sensitive data and then expand your crawler from there.

You can change the code however you want, just make sure that following
things are satisfied:

- Grab the files from the directory "../files" relative to this script
- If you use Python packages, add a "requirements.txt" to your submission
- If you need to download larger files, e.g. NLP models, don't add them to
  the `app` folder. Instead, download them when the Docker image is build by
  changing the Docker file.
- Save your labels as a pickled dictionary in the `../results` directory.
  Use the filename as the key and the label as the value for each file.
- Your code cannot the internet during evaluation. Design accordingly.
"""

import os
from pathlib import Path
import pickle
import spacy
import re

from app.ner import ner

chunk_size = 1000000


ner_categories = {
    'direct': {'PERSON', 'EMAIL', 'ORG', 'RSA_PRIVATE_KEY'},
    'indirect': {'', 'PHONE', 'IBAN'},
    'potential_indirect': {'GENDER'}
}


def classification_rule(labels):
    if 'RSA_PRIVATE_KEY' in labels:
        return True

    n_direct = len(set(labels).intersection(ner_categories['direct']))
    n_indirect = len(set(labels).intersection(ner_categories['indirect']))
    n_potential_indirect = len(set(labels).intersection(ner_categories['potential_indirect']))

    if n_direct >= 2:
        return True
    if n_direct > 0 and (n_indirect > 0 or n_potential_indirect > 0):
        return True

    return False


def save_dict_as_pickle(labels, filename):
    with open(filename, "wb") as handle:
        pickle.dump(labels, handle, protocol=pickle.HIGHEST_PROTOCOL)


def classifier(file_path):
    # Check the data type
    if file_path.suffix == ".txt":
        # Open the file to read out the content
        with open(file_path, encoding="utf8") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk: break
                print(ner(chunk))
            # if file_content.find("hello") != -1:
            #     return "True"
            # else:
            #     return "False"
    else:
        # If it is not a `.txt` file the set the label to "review"
        return "review"


def main():
    # Get the path of the directory where this script is in
    script_dir_path = Path(os.path.realpath(__file__)).parents[1]
    # Get the path containing the files that we want to label
    file_dir_path = script_dir_path / "files"

    if os.path.exists(file_dir_path):
        # Initialize the label dictionary
        labels = {}

        # Loop over all items in the file directory
        for i, file_name in enumerate(os.listdir(file_dir_path)):
            print(f'Processing ({i + 1}/{len(os.listdir(file_dir_path))}): {file_name}')
            file_path = file_dir_path / file_name
            labels[file_name] = classifier(file_path)

        # Save the label dictionary as a Pickle file
        save_dict_as_pickle(labels, script_dir_path / 'results' / 'crawler_labels.pkl')
    else:
        print("Please place the files in the corresponding folder")


def ner___(text):
    nlp = spacy.load("en_core_web_sm")

    patterns = {
        'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        'PHONE': r'(?:(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})',
        'IBAN': r'\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b',
        'GENDER': r'\b(male|female)\b',
        'RSA_PRIVATE_KEY': r'-----BEGIN RSA PRIVATE KEY-----[\s\S]+?-----END RSA PRIVATE KEY-----'
    }

    # text = 'Please contact support@example.com for assistance.'
    # text = 'John,Doe,John Doe,john.doe@gmail.com,Apple Inc.,CH0214047068029644243,42nd street NYC USA,+36(12)1234567,American,male,45,software engineer'
    doc = nlp(text)

    identified_labels = set([ent.label_ for ent in doc.ents])

    # for ent in doc.ents:
    #     print(ent.text, ent.start_char, ent.end_char, ent.label_)

    for tag, pattern in patterns.items():
        if len(re.findall(pattern, text)) != 0:
            identified_labels.add(tag)

        # for match in re.finditer(pattern, text):
        #     start_index = match.start()
        #     end_index = match.end()
        #     matched_text = match.group()
        #     print(matched_text, start_index, end_index, tag)

    print(identified_labels)


if __name__ == "__main__":
    main()
