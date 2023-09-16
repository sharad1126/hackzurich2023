import os
from bs4 import BeautifulSoup
import re

def containsMails(text):

    # Define a regular expression pattern to match email addresses
    email_pattern =  r'\b[A-Za-z0-9.%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}\b'

    # Find email addresses in the text
    email_addresses = re.findall(email_pattern, text)
    if (len(email_addresses) > 0):
        return True
    return False

def containsAdress(text):
    address_pattern = r"\w+\s+\w+\s+\d+\n\d{5}\s+\w+\n\w+"

    addresses = re.findall(address_pattern, text)
    if (len(addresses) > 0):
        return True
    return False

def containsPhone(text):
    phone_number_pattern = r"^(?:\+49|\+44|\+41)[\s.-]*[1-9]\d{0,3}[\s.-]*\d{1,7}$"

    phones = re.findall(phone_number_pattern, text)
    if (len(phones) > 0):
        return True
    return False

def containsIBAN(text):
    iban_pattern = r"\b[A-Z]{2}[0-9]{2}[A-Z0-9]{4}[0-9]{7}([A-Z0-9]?){0,16}\b"

    ibans = re.findall(iban_pattern, text)
    if (len(ibans) > 0):
        return True
    return False

def parse_html_files(path):
    for root,dirs,files in os.walk(path):
        for name in files:
            file_path = os.path.join(root,name)
            extension = file_path.split('.')
            extension = extension[len(extension)-1]
            if extension == "html":
                with open(file_path) as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    p_tag = soup.findAll('p')
                    lenght_p = len(soup.find_all('p'))
                    a_tag = soup.find_all('a')
                    lenght_a = len(soup.find_all('a'))
                    if lenght_p is not None:
                        for a in range(lenght_p):
                            if re.search('Name',p_tag[a].text):
                                print(file_path + ' contains Name')
                                if re.search('Email',p_tag[a].text) or re.search('IBAN', p_tag[a].text) or re.search('Phone',p_tag[a].text):
                                    if containsMails(p_tag[a].text) or containsIBAN(p_tag[a].text) or containsPhone(p_tag[a].text):
                                        print(file_path + ' contains Email IBAN or Phone')
                                        break
                            if re.search('Email',p_tag[a].text):
                                print(file_path + ' contains Email')    
                                if re.search('Name',p_tag[a].text) or re.search('IBAN', p_tag[a].text) or re.search('Phone',p_tag[a].text):
                                    if containsMails(p_tag[a].text) or containsIBAN(p_tag[a].text) or containsPhone(p_tag[a].text):
                                        print(file_path + ' contains Email or IBAN or Phone')
                                        break
                                    
                    if lenght_a is not None:
                        for a in range(lenght_a):
                            if re.search('Name',a_tag[a].text):
                                print(file_path + ' contains Name')
                                if re.search('Email',a_tag[a].text) or re.search('IBAN', a_tag[a].text) or re.search('Phone',a_tag[a].text):
                                    if containsMails(a_tag[a].text) or containsIBAN(a_tag[a].text) or containsPhone(a_tag[a].text):
                                        print(file_path + ' contains Email IBAN or Phone')
                                        break
                            if re.search('Email',a_tag[a].text):
                                print(file_path + ' contains Email')    
                                if re.search('Name',a_tag[a].text) or re.search('IBAN', a_tag[a].text) or re.search('Phone',a_tag[a].text):
                                    if containsMails(a_tag[a].text) or containsIBAN(a_tag[a].text) or containsPhone(a_tag[a].text):
                                        print(file_path + ' contains Email or IBAN or Phone')
                                        break         

parse_html_files('/Users/sharadagarwal/Downloads/sample_set/')                    