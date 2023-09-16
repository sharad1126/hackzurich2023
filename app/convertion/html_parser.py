import os
from bs4 import BeautifulSoup
import re

def parse_html_files(path):
    for root,dirs,files in os.walk(path):
        for name in files:
            file_path = os.path.join(root,name)
            extension = file_path.split('.')
            extension = extension[len(extension)-1]
            if extension == "html":
                with open(file_path) as f:
                    soup = BeautifulSoup(f, 'lxml')
                    soup.prettify()
                    if soup.find('div', class_ ='card-body'):
                        p_tag = soup.find_all('p')
                        lenght_p = len(soup.find_all('p'))
                        a_tag = soup.find_all('a')
                        lenght_a = len(soup.find_all('a'))
                        if lenght_p is not None:
                            for a in range(lenght_p):
                                if re.search('IBAN', p_tag[a].text) and (re.search('Name',p_tag[a].text) or re.search('Email',p_tag[a].text)):
                                    print(file_path)
                                    break
                        if lenght_a is not None:
                            for a in range(lenght_a):
                                if re.search('IBAN', a_tag[a].text) and (re.search('Name',a_tag[a].text) or re.search('Email',a_tag[a].text)):
                                    print(file_path)            


parse_html_files('/Users/sharadagarwal/Downloads/sample_set/')                    