from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from flask import Flask, render_template, request, send_file, redirect,  stream_with_context, Response
import os
from zipfile import ZipFile
from time import time, sleep
import glob
from werkzeug.utils import secure_filename
import pathlib 
# import logging
import search_file3
import format_file3
from threading import Thread
import urllib

# from tkinter import Tk, Label, font, Entry,LEFT, Button, StringVar, Text, Listbox, END,Toplevel,BOTH,YES,ttk,Frame,Canvas,Scrollbar
import share
# from tkinter import *
# from threading import Thread
from multiprocessing import Process, active_children
import sys
import threading
from subprocess import Popen, PIPE
import signal
import search_file
# import os
# import ks_ip_search
# from bs4 import BeautifulSoup
# import requests

win = Tk()
win.minsize(300,200)
win.title("Sharer")
win.iconbitmap('send-message.ico')

def browse():
	a=filedialog.askdirectory()
	# print(a)
	userentry.delete(0,"end")
	userentry.insert(0,a)



a=[]


def start():
	global a
	import ctypes, sys

	def is_admin():
		try:
			return ctypes.windll.shell32.IsUserAnAdmin()
		except:
			return False

	if is_admin():
		try:
			directory=userentry.get()
			directory=directory.replace("\\","/").replace('D:','').replace('C:','')
			thread=Thread(target=search_file.loop,args=(directory,))
			thread.daemon=True
			thread.start()
			if directory[-1]!='/':
				directory=directory+'/'
			if os.path.isdir(directory):
				share.dir=directory
				share.up_dir=directory
				share.app.run('0.0.0.0',port=8080,threaded=True)
		except Exception as e:
			msg=f'{e}\nError: No Such Directory!\n{directory}'
			messagebox.showerror('Not a Folder Error', msg)
	else:
		# Re-run the program with admin rights
		ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
	
def start():
	directory=userentry.get()
	directory=directory.replace("\\","/")
	thread=Thread(target=search_file.loop,args=(directory,))
	thread.daemon=True
	thread.start()
    # thread.join()
    # Thread(search_file3.sort_start(dir))
	# n=0
	blacklist=["$RECYCLE.BIN", "System Volume Information","Android","sound_recorder"]

    # list=set()
	size=0
	if directory[-1]!='/':
		directory=directory+'/'
	if os.path.isdir(directory):
		share.dir=directory
		share.up_dir=directory
		share.app.run('0.0.0.0',port=8080,threaded=True)

tlist=[]
def start_sharing():
	global w
	directory=userentry.get()
	if os.path.isdir(directory):
		pass
	else:
		msg=f'Error: No Such Directory!\n{directory}'
		messagebox.showerror('Not a Folder Error', msg)
		return 
	ipconfig=os.popen('ipconfig','r',1)
	a=ipconfig.readlines()
	ips=[]
	name=""
	dict={}
	# name=[]
	for i in a:
		# if i[0]!==' ':
		# 	title=i.split(' ')
		# 	header=[['Wireless', 'LAN', 'adapter', 'Local' ,'Area' ,'Connection'],['Ethernet', 'adapter', 'Ethernet'],['Wireless', 'LAN' ,'adapter', 'Wi-Fi']]
		# 	for numi in range(0,len(title)):
		# 		for lineh in range(0,len(header)):
		# 			b=False
		# 			for wordh in range(0,len(header[lineh])):
		# 				if title[numi]==header[wordh]:
		# 					b=True
		# 					continue
		# 				else:
		# 					b=False
		# 					break
		# 			if b==True:
		# 				dict[lineh]
		


			# for p in header:
			# 	for word in p:
			# 		if word in a:
			# 			b=False
			# 		else:
			# 			b=True
			# 			# break
			# 	if b==True:
			# 		if p==['Wireless', 'LAN', 'adapter', 'Local' ,'Area' ,'Connection']:
			# 			name='Wifi Hotspot'
			# 		elif p==['Ethernet', 'adapter', 'Ethernet']:
			# 			name='Ethernet'
			# 		elif p==['Wireless', 'LAN' ,'adapter', 'Wi-Fi']:
			# 			name='Wifi Network'
					# print(p,name)
		for j in range(0,len(i)):
			# print(i[0])
			if i[0]!='' and i[0]!=' ' and i[0]!='\n':
				a=i.split(' ')
				# print(a)
				b=False
				header=[['Wireless', 'LAN', 'adapter', 'Local' ,'Area' ,'Connection'],['Ethernet', 'adapter', 'Ethernet'],['Wireless', 'LAN' ,'adapter', 'Wi-Fi']]
				if 'Local' in a and 'Area' in a and 'Wireless' in a:
					name='Wifi Hotspot'
				if 'Ethernet' in a and 'adapter' in a:
					print('Ethernet')
					name='Ethernet'
				if 'Wireless' in a and 'LAN' in a and 'Wi-Fi:\n' in a:
					name='Wifi Network'
			if i[j]=='I':
				# print('['+i[j:j+12]+']')
				if i[j:j+12]=='IPv4 Address':
					ip=''
					for num in range(j+12,len(i)):
						if i[num].isdigit():
							# print(i[num:-1])
							ips.append(i[num:-1])
							
							dict[i[num:-1]]=name
							# print(name,dict[name])
							break
	print(dict)
	ipconfig.close()
	# print(dict)
	# print(ips)
	# w.delete(0,END)
	# n=0
	ethernet.config(text='')
	wifi.config(text='')
	hotspot.config(text='')
	ne=0
	nh=0
	nw=0
	for k in ips:
		address='http://'+k+':8080'
		# w.insert(n,address)
		
		if dict[k]=='Wifi Hotspot':
			if nh>0:
				htextinfo=hotspot.cget("text")+'\n'+address
				hotspot.config(text=htextinfo)
			else:	
				hotspot.config(text=f"Connected To this Device's Hotspot?\n{address}")
			nh+=1
		elif dict[k]=='Ethernet':
			if ne>0:
				etextinfo=ethernet.cget("text")+'\n'+address
				ethernet.config(text=etextinfo)
			else:	
				ethernet.config(text=f'Connected To Ethernet?\n{address}')
			ne+=1
			
			# wifi.config(text='')
		elif dict[k]=='Wifi Network':
			if nw>0:
				wtextinfo=wifi.cget("text")+'\n'+address
				wifi.config(text=wtextinfo)
			else:	
				wifi.config(text=f'Connected To the Same Wi-Fi?\n{address}')
			nw+=1
			
			# ethernet.config(text='')
			# hotspot.config(text='')
		# n+=1
	thread=Thread(target=start)
	thread.daemon=True
	thread.start()

def stop_sharing():
	sys.exit()

def page1(win):
	global wifi,hotspot,ethernet,userentry
	sender = Label(text="Sender")
	sender.pack()
	userentry= Entry(win, width=39, bg="#fafafa")
	userentry.pack()
	showb=Button(win,text="Browse", bg="#3897f1",fg="white", activebackground="white",activeforeground="#3897f1",command=browse)
	showb.pack()
	start=Button(win,text="Start Sharing", bg="#3897f1",fg="white", activebackground="white",activeforeground="#3897f1",command=start_sharing)
	start.pack()
	logs = Label(text="Reciever's Instructions:")
	logs.pack()
	wifi = Label(text="")
	wifi.pack()
	hotspot = Label(text="Browse a Folder and\nClick Start Sharing")
	hotspot.pack()
	ethernet = Label(text="")
	ethernet.pack()
	# search=Button(win,text="Search PC's", bg="#3897f1",fg="white", activebackground="white",activeforeground="#3897f1",command=start_searching)
	# search.pack()
	
	# w = Listbox(win)
	# w.pack()
	# openpc=Button(win,text="Open Files", bg="#3897f1",fg="white", activebackground="white",activeforeground="#3897f1",command=pc)
	# openpc.pack()

	stop=Button(win,text="Stop Sharing", bg="#3897f1",fg="white", activebackground="white",activeforeground="#3897f1",command=stop_sharing)
	stop.pack()
	
	# log_text=Text(win, height=5, width=15)
	# log_text.pack()


page1(win)
win.mainloop()