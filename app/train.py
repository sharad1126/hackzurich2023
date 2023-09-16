import os
from pathlib import Path
import spacy
import random
from app.ner import ner
import csv


chunk_size = 1000000


def tokenize_training_data():
    script_dir_path = Path(os.path.realpath(__file__)).parents[1]
    file_dir_path_base = script_dir_path / "training_files"
    file_dir_path = file_dir_path_base / "data"

    filename = open(file_dir_path_base / "labels.csv", 'r')
    file = csv.DictReader(filename)
    sensitive = []
    for col in file:
        sensitive.append(col['sensitive'])

    if os.path.exists(file_dir_path):
        for i, file_name in enumerate(os.listdir(file_dir_path)):
            print(f'Processing ({i + 1}/{len(os.listdir(file_dir_path))}): {file_name} => {sensitive[i]}')
            file_path = file_dir_path / file_name

            if file_path.suffix == ".txt":
                labels = []
                with open(file_path, encoding="utf8") as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk: break
                        labels += ner(chunk)
                print(labels)
    else:
        print("Please place the files in the corresponding folder")


def train():
    nlp = spacy.blank("en")

    ner = nlp.add_pipe("ner", config={"labels": ["SENSITIVE_LABEL"]})

    # Define your training data (list of tuples: text and annotations)
    training_data = [
        ("The document contains sensitive information.", {"entities": [(20, 38, "SENSITIVE_LABEL")]}),
        ("Please protect the data in this file.", {"entities": [(26, 30, "SENSITIVE_LABEL")]}),
    ]

    # Define the number of training iterations and batch size
    n_iter = 10
    batch_size = 4

    # Start the training loop
    for _ in range(n_iter):
        random.shuffle(training_data)
        losses = {}
        for batch in spacy.util.minibatch(training_data, size=batch_size):
            texts, annotations = zip(*batch)
            example = []
            # Update the model with iterating each text and annotation
            for i in range(len(texts)):
                doc = nlp.make_doc(texts[i])
                example.append(Example.from_dict(doc, annotations[i]))
            nlp.update(example, losses=losses)
        print("Losses during training:", losses)

    # Save the trained NER model
    nlp.to_disk("./sensitivity_classifier_model.spacy")


if __name__ == '__main__':
    train()
