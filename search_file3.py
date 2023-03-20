#import threading
import os
from time import time 
from threading import Thread 
from concurrent.futures import ThreadPoolExecutor

# import string
#from ctypes import windll

#def get_drives():
#    drives = []
#    bitmask = windll.kernel32.GetLogicalDrives()
#    for letter in string.uppercase:
#        if bitmask & 1:
#            drives.append(letter)
#        bitmask >>= 1

#    return drives

#dletters=get_drives()
#print (dletters)

#pathdict={}
dict={}
def mem_clean():
    dict.clear()
#directory="/storage/emulated/0/" #Android
#directory="C:/" #Windows C
#directory="D:/" #Windows D
#directory="/home" #linux
#dirc=0
n=0
def sort_files(directory):
	# print ("directory: ",directory)
	# print(os.walk(directory))
	#for drive in dletters:
	for root,dirs,files in os.walk(directory):
			#print ("root: ",root)
			# print ("dirs: ", dirs)
		#	print ("files: ", files)
			root=root.replace('\\', '/')
			# print(root)
			
			for i in dirs:
				# small_i=i[0].lower()
				# print(i)
				
				filepath=root+'/'+i+'/'
				# print(filepath)
				for j in list(i):
					small_j=j.lower()
					try:
						if dict[small_j]:
							dict[small_j].append({filepath:i})
					except:
						#print (e)
						dict[small_j]=[]
						dict[small_j].append({filepath:i})
						
			for i in files:
				# small_i=i[0].lower()
				filepath=root+'/'+i+'/'
				for j in list(i):
					small_j=j.lower()
					try:
						if dict[small_j]:
							dict[small_j].append({filepath:i})
					except:
						#print (e)
						dict[small_j]=[]
						dict[small_j].append({filepath:i})
						
#for i in os.listdir(directory):

def sort_start(directory):
	z=0
	s=time()
	subfolders = [ f.path.replace('\\', '/') for f in os.scandir(directory) if f.is_dir() ]
	with ThreadPoolExecutor(max_workers=20) as executor:
		executor.map(sort_files,subfolders)
	for name in os.listdir(directory):
				#print ("root: ",root)
			#	print ("dirs: ", dirs)
			#	print ("files: ", files)
			if os.path.isdir(os.path.join(directory,name)):
					# small_i=name[0].lower()
					# filepath=
					# #print (list(name))
					# for j in list(name):
						
					# 	small_j=j.lower()
					# 	try:
					# 		if dict [small_j]:
					# 			dict[small_j].append({filepath:name})
					# 	except:
					# 		#print (e)
					# 		dict[small_j]=[]
					# 		dict[small_j].append({filepath:name})
					# thread = Thread(target=sort_files, args=(os.path.join(directory,name),))
					# thread.start()
					continue 
			else:
					small_i=name[0].lower()
					filepath=directory+'/'+name+'/'
					#print (list(name))
					for j in list(name):
						small_j=j.lower()
						try:
							if dict [small_j]:
								dict[small_j].append({filepath:name})
						except:
							#print (e)
							dict[small_j]=[]
							
							dict[small_j].append({filepath:name})
							
	
	#for i in 
	#thread = Thread(target=sort_files, args=(os.path.join(directory),))
	#thread.start()
	# try:				
	# 	thread.join()
	# except:
	# 	print ("no thread")	
		
	
						
	#print (dict)
	e=time ()
	print (f"Total time for sort: {e-s} seconds.")
	#print (f"Total Files:- {n}")
	#print ("Files: ",len(dict))
	#for i in dict.values():
	#	print (i)

#print (os.listdir(directory))
#result=[]
def search (query, directory):
	sort_start(directory)
	result=[]#
	search_term=query
	#print (search_term[0].lower())
	letter_list=dict[search_term[0].lower()]
	print (len(letter_list))
	#print (dict[search_term[0].lower()])
	lowcase_searchterm=search_term.lower()
	n=0
	for i in letter_list:
		if n>500:
			break
		for j in i.values():
			if lowcase_searchterm in j.lower():
				#print ("Filename:- ",i)
				result.append(i)
				n+=1
	r2=[]
	letter_list=[]
	dict.clear()
	for i in result:
		for j in i.keys():
			if j in r2:
				continue
			else:
				r2.append(j)
	r2.sort()
	#dict={}
	return r2

def search_cache(query, directory):
	# sort_start(directory)
	result=[]
	search_term=query
	#print (search_term[0].lower())
	letter_list=dict[search_term[0].lower()]
	# print(letter_list)
	print (len(letter_list))
	#print (dict[search_term[0].lower()])
	lowcase_searchterm=search_term.lower()
	n=0
	for i in letter_list:
		if n>500:
			break
		for j in i.values():
			if lowcase_searchterm in j.lower():
				#print ("Filename:- ",i)
				result.append(i)
				n+=1
	r2=[]
	letter_list=[]
	# dict.clear()
	for i in result:
		for j in i.keys():
			if j in r2:
				continue
			else:
				r2.append(j)
	r2.sort()
	#dict={}
	print('R2: ',r2)
	return r2