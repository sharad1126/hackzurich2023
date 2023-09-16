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

import numpy as np
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import numpy as np
import pandas as pd
import ssl


def save_as_csv(data):
    array = np.array(data)

    # Speichern des Arrays als CSV-Datei
    np.savetxt('names.csv', array, delimiter=',')
def save_dict_as_pickle(labels, filename):
    with open(filename, "wb") as handle:
        pickle.dump(labels, handle, protocol=pickle.HIGHEST_PROTOCOL)


def classifier(file_path):
    # Check the data type
    if file_path.suffix == ".txt":
        # Open the file to read out the content
        with open(file_path) as f:
            file_content = f.read()
            names= findNames(file_content)
            #save_as_csv(names)

            # If the file contains the word "hello" label it as true
            if file_content.find("hello") != -1:
                return "True"
            else:
                return "False"
    else:
        # If it is not a `.txt` file the set the label to "review"
        return "review"

def findNames(text):
    st = StanfordNERTagger(
        '/Users/janndemond/Downloads/SentiSE-master/edu/stanford/nlp/models/ner/english.all.3class.distsim.crf.ser.gz',
        '/Users/janndemond/PycharmProjects/hackzurich2023/stanford-ner.jar',
        encoding='utf-8')

    # text = 'While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'

    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)

    # Extrahieren der Eigennamen
    names = [word for word, pos in classified_text if (pos == 'PERSON' or pos == 'LOCATION')]
    print(names)
    return names


def main():
    # Get the path of the directory where this script is in
    script_dir_path = Path(os.path.realpath(__file__)).parents[1]
    # Get the path containing the files that we want to label
    file_dir_path = script_dir_path / "files"
    #ssl._create_default_https_context = ssl._create_unverified_context
    #nltk.download()
    os.environ['CLASSPATH'] = "/Users/janndemond/PycharmProjects/hackzurich2023/stanford-ner.jar"
    os.environ['STANFORD_MODELS'] = '/Users/janndemond/Downloads/SentiSE-master/edu/stanford/nlp/models/ner'
    java_path = '/Library/Java/JavaVirtualMachines/jdk-20.jdk/Contents/Home/bin/java'
    os.environ['JAVAHOME'] = java_path

    if os.path.exists(file_dir_path):
        # Initialize the label dictionary
        labels = {}

        # Loop over all items in the file directory
        for file_name in os.listdir(file_dir_path):
            file_path = file_dir_path / file_name
            labels[file_name] = classifier(file_path)

        # Save the label dictionary as a Pickle file
        save_dict_as_pickle(labels, script_dir_path / 'results' / 'crawler_labels.pkl')
    else:
        print("Please place the files in the corresponding folder")


if __name__ == "__main__":
    main()
