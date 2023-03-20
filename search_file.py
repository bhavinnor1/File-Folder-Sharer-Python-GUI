#import threading
import os
from time import time,sleep
from threading import Thread 

#import string
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

#pathdict1={}
dict1={}
def mem_clean():
    dict1.clear()
#directory="/storage/emulated/0/" #Android
#directory="C:/" #Windows C
#directory="D:/" #Windows D
#directory="/home" #linux
#dirc=0
#n=0
def sort_files(directory):
	#print (directory)
	
	#for drive in dletters:
	for root,dirs,files in os.walk(directory):
			root=root.replace('\\','/')
			
			#print ("root: ",root)
		#	print ("dirs: ", dirs)
		#	print ("files: ", files)
			for i in dirs:
				i=i.replace('\\','/')
				small_i=i[0].lower()
				filepath=os.path.join(root,i)
				for j in list(i):
					small_j=j.lower()
					try:
						if dict1[small_j]:
							dict1[small_j].append({filepath:i})
					except:
						#print (e)
						dict1[small_j]=[]
						dict1[small_j].append({filepath:i})
						
			for i in files:
				i=i.replace('\\','/')
				small_i=i[0].lower()
				filepath=os.path.join(root,i)
				for j in list(i):
					small_j=j.lower()
					try:
						if dict1[small_j]:
							dict1[small_j].append({filepath:i})
					except:
						#print (e)
						dict1[small_j]=[]
						dict1[small_j].append({filepath:i})
						
#for i in os.listdir(directory):

def sort_start(directory):
	z=0
	s=time()
	for name in os.listdir(directory):
			name=name.replace('\\','/')
				#print ("root: ",root)
			#	print ("dirs: ", dirs)
			#	print ("files: ", files)
			if os.path.isdir(os.path.join(directory,name)):
					small_i=name[0].lower()
					filepath=os.path.join(directory,name)
					#print (list(name))
					for j in list(name):
						
						small_j=j.lower()
						try:
							if dict1 [small_j]:
								dict1[small_j].append({filepath:name})
						except:
							#print (e)
							dict1[small_j]=[]
							dict1[small_j].append({filepath:name})
					thread = Thread(target=sort_files, args=(os.path.join(directory,name),))
					thread.start()
					continue 
			else:
					small_i=name[0].lower()
					filepath=os.path.join(directory,name)
					#print (list(name))
					for j in list(name):
						
						small_j=j.lower()
						try:
							if dict1 [small_j]:
								dict1[small_j].append({filepath:name})
						except:
							#print (e)
							dict1[small_j]=[]
							dict1[small_j].append({filepath:name})
							
	
	#for i in 
	#thread = Thread(target=sort_files, args=(os.path.join(directory),))
	#thread.start()
	try:				
		thread.join()
	except:
		# print ("no thread")	
		pass
	# print(len(dict1["a"]))
		
	
						
	#print (dict1)
	e=time ()
	# print (f"Total time for sort: {e-s} seconds.")
	#print (f"Total Files:- {n}")
	#print ("Files: ",len(dict1))
	#for i in dict1.values():
	#	print (i)

def loop(directory):
	# while True:
	# 	thread=Thread(target=sort_start,args=(directory,))
	# 	thread.daemon=True
	# 	thread.start()
	# 	sleep(60)
	direct=':'.join(directory.split(':')[1:])
	if len(direct)>0:
		directory=directory
	else:
		directory=direct
	print(directory)
	sort_start(directory)

#print (os.listdir(directory))
#result=[]

def search_cache(query, directory):
	# sort_start(directory)
	result=[]
	search_term=query
	#print (search_term[0].lower())
	# dict112=dict1
	if (search_term[0].lower()) in dict1:
		letter_list=dict1[search_term[0].lower()]
	else:
		letter_list=[]
	# try:
	# 	letter_list=dict1[search_term[0].lower()]
	# except:
	# 	r2=[]
	# 	return []
	# print(letter_list)
	# print (len(letter_list))
	#print (dict1[search_term[0].lower()])
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
	# dict1.clear()
	for i in result:
		for j in i.keys():
			if j in r2:
				continue
			else:
				dohj=j.replace('\\','/')
				r2.append(dohj)
	r2.sort()
	# for i,p in enumerate(r2):
	# 	r2[i]=p.replace(r'\\','/')
	# print(len(r2))
	#dict1={}
	# print('R2: ',r2)
	return r2

def search (query, directory):
	directory=directory
	mem_clean()
	sort_start(directory)
	result=[]#
	search_term=query
	#print (search_term[0].lower())
	try:
		letter_list=dict1[search_term[0].lower()]
	except:
		r2=[]
		return []
	# print (len(letter_list))
	#print (dict1[search_term[0].lower()])
	lowcase_searchterm=search_term.lower()
	for i in letter_list:
		for j in i.values():
			if lowcase_searchterm in j.lower():
				#print ("Filename:- ",i)
				result.append(i)
	r2=[]
	for i in result:
		for j in i.keys():
			if j in r2:
				continue
			else:
				r2.append(j)
	r2.sort()
	for i,p in enumerate(r2):
		r2[i]=p.replace(r'\\','/')
		print(r2[i])
	print('---------------R2---------------\n',r2)
	#dict1={}
	return r2

if __name__=="__main__":
	directory="D:/"
	# thread=Thread(target=loop,args=(directory,))
	# thread.start()
	# thread.daemon=True
	# thread.join()
	sort_start(directory.replace('/','\\'))

	from time import sleep
	sleep(10)
	a= search_cache('bhavin', directory)

	print(a)