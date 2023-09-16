import xml.etree.ElementTree as ET
import re
import os
from lxml import etree
#from more_itertools import locate

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


#root_node = ET.parse(r'C:\Users\sirot\Downloads\hackzh23-scan-the-bank-main\hackzh23-scan-the-bank-main\files\within-resource.xml').getroot()
#get the current directory
cdir = os.getcwd() 
#get the parent directory
pdir = os.path.dirname(cdir)
# assign directory
directory = os.path.join(pdir,'files')


# iterate over files in that directory
for filename in os.listdir(directory):
    #get the filepath
    f = os.path.join(directory, filename)
    #print(f)

    filename_stripped, extension = os.path.splitext(filename)

    if extension == ".xml":
        parser = etree.XMLParser(recover=True)
        with open(f, 'r', encoding='unicode_escape') as file:
            xml_content = file.read()
        #tree = ET.parse(xml_content, parser=parser)
        #root = tree.getroot()
        root_node = ET.fromstring(xml_content)
        #root_node = ET.parse(f).getroot()

        for k in range(len(root_node)):
            c = 0
            mail = False
            iban = False
            address = False
            phone = False
            for x in root_node[k]:
                tags = []
                values = []
                tags.append(x.tag)
                values.append(x.text) 
                for tag in tags:
                    if re.search('name',tag):
                        x = tags.index(tag)
                        if values[x]:
                            #print('name: ' + values[x])
                            c = c + 1
                    if re.search('mail',tag):
                        y=tags.index(tag)
                        if values[y]:
                            if containsMails(values[y]):
                                #print('mail:' + values[y])
                                mail = True
                    if re.search('iban',tag) or re.search('IBAN',tag):
                        z=tags.index(tag)
                        if values[z]:
                            if containsIBAN(values[z]):
                                #print('iban: ' + values[z])
                                iban = True
                    if re.search('phone',tag):
                        b=tags.index(tag)
                        if values[b]:
                            if containsPhone(values[b]):
                                #print('phone: ' + values[b])
                                phone = True
                    if re.search('ddress',tag):
                        a=tags.index(tag)
                        if values[a]:
                            if containsAdress(values[a]):
                                #print('address: ' + values[a])	
                                address = True
            if (((c == 2) and (mail or iban or phone or address)) or (mail and (iban or address or phone))):	
                print('sensitive ' + f)	
                break