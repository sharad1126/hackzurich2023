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

import pickle
import ner
from convertion.txt import *
from convertion.tabular import *
from clasification.classifier import *
from clasification.validation import *

chunk_size = 1000000

ner_categories = {
    'direct': {'PERSON', 'EMAIL', 'ORG', 'RSA_PRIVATE_KEY'},
    'indirect': {'', 'PHONE', 'IBAN'},
    'potential_indirect': {'GENDER'}
}


# def classification_rule(labels):
#     sensitive_combinations = [
#         {'RSA_PRIVATE_KEY'},
#         {'PERSON', 'EMAIL'},
#         {'PERSON', 'IBAN'},
#         {'PERSON', 'PHONE'},
#         {'PERSON', 'ADDRESS'},
#         {'EMAIL', 'IBAN'},
#         {'EMAIL', 'ADDRESS'},
#         {'EMAIL', 'PHONE'}
#     ]
#
#     for combination in sensitive_combinations:
#         if combination.issubset(set(labels)):
#             return True
#
#     return False


def save_dict_as_pickle(labels, filename):
    with open(filename, "wb") as handle:
        pickle.dump(labels, handle, protocol=pickle.HIGHEST_PROTOCOL)


# def classifier(file_path):
#     with open(file_path, encoding="utf8") as f:
#         while True:
#             chunk = f.read(chunk_size)
#
#             if not chunk:
#                 break
#
#             label_tokens = ner(chunk)
#             print(label_tokens)
#             class_out = classification_rule([label for (_, _, _, label) in label_tokens])
#
#             # TODO review
#
#             return "True" if class_out else "False"


def preprocess(file_path: str, output_dir: str):
    file_extension = Path(file_path).suffix.lower()
    try:
        if file_extension == ".docx":
            return convert_docx_to_txt(file_path, output_dir)
        elif file_extension == ".pdf":
            return convert_pdf_to_txt(file_path, output_dir)
        elif file_extension == ".msg":
            return convert_msg_to_txt(file_path, output_dir)
        elif file_extension == ".xlsx":
            return convert_from_excel_to_csv(file_path, output_dir)
        elif file_extension == ".db":
            return convert_from_db_to_csv(file_path, output_dir)
        elif file_extension == ".csv":
            return convert_other_to_csv(file_path, output_dir)
        elif file_extension == ".log":
            return convert_other_to_txt(file_path, output_dir)
    except Exception as e:
        print(f"Could not preprocess {file_path} - {e}")


def classify(script_dir_path):
    preprocessed_dir = script_dir_path / "preprocessed"
    df = pd.read_csv(script_dir_path / 'results' / 'labels.csv')
    labels = {}
    for file_name in os.listdir(preprocessed_dir):
        file_path = preprocessed_dir / file_name
        file_extension = file_path.suffix
        try:
            if file_extension == ".txt":
                result = classifierTXT(preprocessed_dir / file_path)
                validation(os.path.splitext(file_name)[0], result, df)
                labels[file_path] = result

            elif file_extension == ".pub":
                result = classifierPub(preprocessed_dir / file_path)
                validation(os.path.splitext(file_name)[0], result, df)
                labels[file_path] = result

        except Exception as e:
            print(f"Could not classify {file_path} - {e}")


def main():
    # Get the path of the directory where this script is in
    script_dir_path = Path(os.path.realpath(__file__)).parents[1]
    # Get the path containing the files that we want to label
    file_dir_path = script_dir_path / "sample_set"

    if os.path.exists(file_dir_path):
        # Initialize the label dictionary
        labels = {}

        # Create new directory for preproccesed files if it does not exist
        preprocessed_dir = script_dir_path / "preprocessed"
        if not os.path.exists(preprocessed_dir):
            os.mkdir(preprocessed_dir)

        # Loop over all items in the file directory.
        # Do Preprocessing and save in preprocessed directory
        # for file_name in os.listdir(file_dir_path):
        #     # TODO: Check if it does not have an extension
        #     preprocessed_path = preprocess(file_dir_path / file_name, preprocessed_dir)
        #     # classifier(preprocessed_path)

        # Save the label dictionary as a Pickle file
        #save_dict_as_pickle(labels, script_dir_path / 'results' / 'crawler_labels.pkl')
        classify(script_dir_path)
    else:
        print("Please place the files in the corresponding folder:" + str(file_dir_path))


if __name__ == "__main__":
    main()
