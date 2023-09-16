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
import nltk

import numpy as np
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import numpy as np
import pandas as pd

from nltk.corpus import names
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import ssl
import re


def save_as_csv(data):
    array = np.array(data)

    # Speichern des Arrays als CSV-Datei
    np.savetxt('names.csv', array, delimiter=',')


def save_dict_as_pickle(labels, filename):
    with open(filename, "wb") as handle:
        pickle.dump(labels, handle, protocol=pickle.HIGHEST_PROTOCOL)


def classifierPub(file_path):
    # Check the data type
        # Open the file to read out the content
        with open(file_path) as f:
            file_content = f.read()
            # findRegex(file_content)
            a = findNames(file_content)
            if (a == False):
                return findNamesBylist(file_content)

            if a == False:
                a = nltkNames(file_content)
            return a
            # save_as_csv(names)
def classifierTXT(file_path):
    with open(file_path) as f:
        file_content = f.read()
        #a = findNames(file_content)
        b= containsIBAN(file_content)
        c= containsPhone(file_content)
        d=containsAdress(file_content)
        e=containsMails(file_content)
    if e:
        if b or c or d:
            return True
    return False
def classifierLog(file_path):
    with open(file_path) as f:
        file_content = f.read()
        a = findNames(file_content)
        e=containsMails(file_content)
        b = containsIBAN(file_content)

    if e:

        c = containsPhone(file_content)
        d = containsAdress(file_content)
        if b or c or d:
            return True
    if a:
            return True
    #For md Files
    f=does_next_word_exist(file_content,'number:')
    fe=does_next_word_exist(file_content,'#IBAN:')
    fg = does_next_word_exist(file_content, '#zrnr:')
    g = does_next_word_exist(file_content, '#Client:')
    h= does_next_word_exist(file_content, '#Name:')
    if (f or fe or fg or b) and (g or h):
        return True

    return False
def classifierMd(file_path):
    with open(file_path) as f:
        file_content = f.read()
        a = findNames(file_content)
        e=containsMails(file_content)
        b = containsIBAN(file_content)

    if e:

        c = containsPhone(file_content)
        d = containsAdress(file_content)
        if b or c or d:
            return True
    if a:
            return True
    #For md Files
    f=does_next_word_exist(file_content,'number:')
    fe=does_next_word_exist(file_content,'#IBAN:')
    fg = does_next_word_exist(file_content, '#zrnr:')
    g = does_next_word_exist(file_content, '#Client:')
    h= does_next_word_exist(file_content, '#Name:')
    if (f or fe or fg or b) and (g or h):
        return True
    return False
def findNames(text):
    st = StanfordNERTagger(
        '/Users/janndemond/Downloads/SentiSE-master/edu/stanford/nlp/models/ner/english.all.3class.distsim.crf.ser.gz',
        '/Users/janndemond/PycharmProjects/hackzurich2023/stanford-ner.jar',
        encoding='utf-8')

    # text = 'While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'

    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)

    # Extrahieren der Eigennamen or pos == 'LOCATION'
    names = []
    i =1
    b = containsIBAN(text)
    c = containsPhone(text)
    d = containsAdress(text)

    for i in  range(len(classified_text)-1):
        pos = list(classified_text[i])[1]
        word= list(classified_text[i])[0]
        if i <len(classified_text) and pos == 'PERSON' and list(classified_text[i+1])[1]=='PERSON':
                emails = getMails(text)
                for mail in emails:
                    if findNemesinMail(mail, word) or b or c or d:
                        names.append(word)
                       # print(mail +' ' +word)

        i=i+1;
    if (len(names) > 1):
        return True
    return False

def containsMails(text):
    words = word_tokenize(text)

    # Define a regular expression pattern to match email addresses
    email_pattern =  r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # Definieren Sie das Muster für die deutsche Adresse


    # Find email addresses in the text
    email_addresses = re.findall(email_pattern, text)
    if (len(email_addresses) > 0):

        return True
    return False
def getMails(text):
    words = word_tokenize(text)

    # Define a regular expression pattern to match email addresses
    email_pattern =  r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # Definieren Sie das Muster für die deutsche Adresse


    # Find email addresses in the text
    email_addresses = re.findall(email_pattern, text)

    return email_addresses
def containsAdress(text):
    # Definieren Sie das Muster für die deutsche Adresse
    address_pattern = r"\w+\s+\w+\s+\d+\n\d{4,5}\s+\w+\n\w+"

    # Suchen Sie nach Adressen im Text
    addresses = re.findall(address_pattern, text)
    if (len(addresses) > 0):
        return True
    return False
def containsPhone(text):
    # Definieren Sie das Muster für die deutsche Adresse
    phone_number_pattern = r"((\+?\[49,41,44],\s?)?(\d{2,4}\s?-?){1,4}\d{2,4})\d{6,9}"
    #phone_number_pattern ='(?:(?:\+?[49,41,44]\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d{6-9))?'
    # Suchen Sie nach Adressen im Text
    phone_number_pattern=r"(?:\+49|\+44|\+41)[\s.-]*[1-9]\d{0,3}[\s.-]*\d{1,7}"
    phones = re.findall(phone_number_pattern, text)
    if (len(phones) > 0):
        return True
    return False
def containsIBAN(text):
    # Definieren Sie das Muster für die deutsche Adresse
    #iban_pattern = r"\b[A-Z]{2}[0-9]{2}[A-Z0-9]{4}[0-9]{7}([A-Z0-9]?){0,16}\b"
    iban_pattern = r'\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b'
    # Suchen Sie nach Adressen im Text
    ibans = re.findall(iban_pattern, text)
    if (len(ibans) > 0):
        return True
    return False


def nltkNames(text):
    nltk_results = ne_chunk(pos_tag(word_tokenize(text, language='german')))
    for nltk_result in nltk_results:
        if type(nltk_result) == Tree:
            name = ''
            for nltk_result_leaf in nltk_result.leaves():
                name += nltk_result_leaf[0] + ' '
                if nltk_result_leaf.label() == 'PERSON':
                    print(name + nltk_result.label())
                    return True

    return False


def findRegex(text):
    tokens = []
    patterns = {
        'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}\b',
        'PHONE': r'(?:(?:+\d{1,3}[-.\s]?)?(?\d{3})?[-.\s]?\d{3}[-.\s]?\d{4})',
        'IBAN': r'\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b',
        'GENDER': r'\b(male|female)\b',
        'RSA_PRIVATE_KEY': r'-----BEGIN RSA PRIVATE KEY-----[\s\S]+?-----END RSA PRIVATE KEY-----'
    }
    for tag, pattern in patterns.items():
        for match in re.finditer(pattern, text):
            start_index = match.start()
            end_index = match.end()
            tokens.append((start_index, end_index, tag))
        re.findall(pattern, text)
    print(re.findall(pattern, text))


def findNamesBylist(text):
    male_names = names.words('male.txt')
    female_names = names.words('female.txt')
    all = male_names + female_names;
    text_a = text.split(';')
    i = 0
    if len(text_a) > 2:
        y = 0
        for text_b in text_a:
            y = y + 1
            text_c = text_b.split(' ')
            if len(text_c) > 1:
                for pos_names in text_c:

                    if pos_names in all:
                        i = i + 1

                    else:
                        continue

                    if (i > 0):
                        return True
            else:
                if '@' in text_b:
                    return findNemesinMail(text_b, text_a[y - 2])

    return False


def findNemesinMail(mail, text1):
    mail_part = mail.split('@')
    name_part = mail_part[0].split('.')
    for name in name_part:
        if len(name)>2:
            if name in text1:
                return True
    return False
def does_next_word_exist(text, target_word):
    words = text.split()
    if target_word in words:
        index = words.index(target_word)
        if index < len(words) - 1:
            a = words[index + 1]
            if len(a.strip())>3:
                return True
        if index < len(words) - 2:
            a = words[index + 1]+words[index + 2]
            if len(a.strip()) > 3:
                return True
    return False



