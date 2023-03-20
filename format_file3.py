import os
from time import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor


dict_files={}
dict_folders={}
dir=""

def format(file):
    if os.path.isdir(file):
        # ab_path='/folder?folder='+row
        ab_path='/folder?folder='+file[1:]
        dict_folders[ab_path]=file.split('/')[-2]+'/'
    else:
        # ab_path='/download?file='+row
        ab_path='/download?file='+file[1:]
        dict_files[ab_path]=file.split('/')[-2]

def mem_clean():
    dict_files.clear()
    dict_folders.clear()

def thread_format(files,directory):
    global dir
    # try:
    # 	mem_clean(dict_files,dict_folders)
    # except:
    # 	print ("error")
    
    
    dict_files.clear()
    dict_folders.clear()
    tc=1
    dir=directory
    s=time()
    # for i in files:
    #     format(i)
    with ThreadPoolExecutor(max_workers=200) as executor:
        executor.map(format,files)
    e=time()
    print(f'Formatting Completed in {e-s}seconds.')
    return dict_files, dict_folders

