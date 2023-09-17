import os 
import magic 
from pathlib import Path

def get_extensions(input_dir: str):
    for root,dirs,files in os.walk(input_dir):
            for name in files:
                    file_path=os.path.join(root,name)   
                    if len(file_path.split('.'))<2: 
                        if magic.from_file(file_path, mime=True).split('/')[1] == 'plain' or magic.from_file(file_path, mime=True).split('/')[1] == 'x-ms-regedit':
                            extension = '.txt'
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'mpeg':   
                            extension = '.mpeg' 
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'mp3':   
                            extension = '.mp3'     
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'mp4':   
                            extension = '.mp4' 
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'wav':   
                            extension = '.wav' 
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'html':   
                            extension = '.html'           
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'csv':
                            extension = '.csv'
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                            extension = '.xlsx'    
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'xml':
                            extension = '.xml'
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'pdf':
                            extension = '.pdf'        
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'vnd.openxmlformats-officedocument.wordprocessingml.document':
                            extension = '.docx'
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'vnd.sqlite3':
                            extension = '.db'
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'jpeg':
                            extension = '.jpg'    
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'png':
                            extension = '.png'   
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'vnd.ms-outlook':
                            extension = '.msg' 
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'x-script.python':
                            extension = '.py' 
                        elif magic.from_file(file_path, mime=True).split('/')[1] == 'zip':
                            extension = '.zip'
                        else:
                            extension = '.txt'       
                        os.rename(file_path, file_path+extension)