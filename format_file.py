import os
from time import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

dict_files={}
dict_folders={}
dir=""

def format(file):
    if os.path.isdir(os.path.join(dir,file)):
        # ab_path='/folder?folder='+row
        # print('file: ',str(file).replace('\\','/'),)
        ab_path='/folder?folder='+(str(file).replace('\\','/')).replace(dir,"").replace('\\','/')+"/"
        dict_folders[ab_path]=os.path.basename(file)+"/"
    else:
        # ab_path='/download?file='+row
        ab_path='/download?file='+(str(file).replace('\\\\','/').replace(dir,""))[1:].replace('\\','/')
        dict_files[ab_path]=os.path.basename(file)

def mem_clean():
    dict_files.clear()
    dict_folders.clear()

def thread_format(files,directory):
    global dir
    # print(directory)
    tc=1
    dir=directory
    print("format:-",dir)
    s=time()
    # for i in files:
    #     format(i)
    with ThreadPoolExecutor(max_workers=200) as executor:
        executor.map(format,files)
    e=time()
    # print(f'Formatting Completed in {e-s}seconds.')
    return dict_files, dict_folders

