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
    address_pattern = r"\w+\s+\w+\s+\d+\n\d{4,5}\s+\w+\n\w+"

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
                            text_to_check = p_tag[a].text.replace(" ","")
                            if re.search('Email',text_to_check):
                                if containsMails(text_to_check):
                                    print(file_path + ' contains Email')    
                                    if re.search('Name',text_to_check) or re.search('IBAN', text_to_check) or re.search('Phone',text_to_check) or re.search('ddress',text_to_check):
                                        if containsMails(text_to_check) or containsIBAN(text_to_check) or containsPhone(text_to_check) or containsAdress(text_to_check):
                                            print(file_path + ' Sensitive')
                                            break
                            if re.search('Name',text_to_check):
                                #if containsName(p_tag[a].text):
                                print(file_path + ' contains Name')
                                if re.search('Email',text_to_check) or re.search('IBAN', text_to_check) or re.search('Phone',text_to_check) or re.search('ddress',text_to_check):
                                    if containsMails(text_to_check) or containsIBAN(text_to_check) or containsPhone(text_to_check) or containsAdress(text_to_check):
                                        print(file_path + ' Sensitive')
                                        break
                                    
                    if lenght_a is not None:
                        for a in range(lenght_a):
                            text_to_check = a_tag[a].text.replace(" ","")
                            if re.search('mail',text_to_check):
                                if containsMails(text_to_check):
                                    print(file_path + ' contains Email')    
                                    if re.search('Name',text_to_check) or re.search('IBAN', text_to_check) or re.search('Phone',text_to_check) or re.search('ddress',text_to_check):
                                        if containsMails(text_to_check) or containsIBAN(text_to_check) or containsPhone(text_to_check) or containsAdress(text_to_check):
                                            print(file_path + ' Sensitive')
                                            break
                            if re.search('Name',a_tag[a].text):
                                #if containsName(p_tag[a].text):
                                print(file_path + ' contains Name')
                                if re.search('mail',text_to_check) or re.search('IBAN', text_to_check) or re.search('Phone',text_to_check) or re.search('ddress',text_to_check):
                                    if containsMails(text_to_check) or containsIBAN(text_to_check) or containsPhone(text_to_check) or containsAdress(text_to_check):
                                        print(file_path + ' Sensitive')
                                        break
                            
parse_html_files('/Users/sharadagarwal/Downloads/sample_set/')                    