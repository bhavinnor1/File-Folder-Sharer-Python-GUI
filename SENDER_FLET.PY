import flet as ft
import os
from flask import Flask, render_template, request, send_file, redirect,  stream_with_context, Response
import os
from zipfile import ZipFile
from time import time, sleep
import glob
from werkzeug.utils import secure_filename
import pathlib 
# import logging
import search_file
import format_file
import search_file3
import format_file3
from threading import Thread
import urllib
import webbrowser

new=1
# url1='https://open.spotify.com/playlist/7c2r3SB5wzIQSpOblrGOKz?si=0ea5971f58cf4285'
# url2='https://open.spotify.com/playlist/4y7sepkiWjeSZ88F3Dn2c7?si=061108600a8a4b14'
# url3='https://open.spotify.com/playlist/5K75kzLTDIhF6rbChxkh4o?si=ecb359fa917d461b'

def openweb(url):
    webbrowser.open(url,new=new)

# from tkinter import Tk, Label, font, Entry,LEFT, Button, StringVar, Text, Listbox, END,Toplevel,BOTH,YES,ttk,Frame,Canvas,Scrollbar
import share
# from tkinter import *
# from threading import Thread
from multiprocessing import Process, active_children
import sys
import threading
from subprocess import Popen, PIPE
import signal



def main(page: ft.Page):
    global new_task,ethernet,wifi,hotspot
    a=[]
    def start():
        directory=new_task.value
        directory=directory.replace("\\","/").replace('D:','').replace('C:','')
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
            print('dir: ',directory)
            thread=Thread(target=share.app.run,args=('0.0.0.0',8080,))
            thread.daemon=True
            thread.start()
        
        

    tlist=[]
    def start_sharing():
        global w
        directory=new_task.value
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
        for i in a:
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
        ipconfig.close()
        # print(dict)
        # print(ips)
        # w.delete(0,END)
        # n=0
        ethernet.value=''
        wifi.value=''
        hotspot.value=''
        for k in ips:
            address='http://'+k+':8080'
            # w.insert(n,address)
            
            if dict[k]=='Wifi Hotspot':
                hotspot.value=f"Connected To this Device's Hotspot?\n{address}"
                
            elif dict[k]=='Ethernet':
                ethernet.value=f'Connected To Ethernet?\n{address}'
                
                # wifi.config(text='')
            elif dict[k]=='Wifi Network':
                wifi.value=f'Connected To the Same Wi-Fi?\n{address}'
                # ethernet.config(text='')
                # hotspot.config(text='')
            # n+=1
        
        print('start')
        thread=Thread(target=start)
        thread.daemon=True
        thread.start()

        page.update()
    def stop_sharing():
	    sys.exit()

    def on_dialog_result(e: ft.FilePickerResultEvent):
        print("Selected files:", e.files)
        print("Selected file or directory:", e.path)
        new_task.value=e.path
        page.update()
    file_picker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)
    page.update()
    def open_repo(e):
        page.launch_url('https://github.com/iqfareez/flet-hello')

    appbar = ft.Text("Flutter using Flet")
    def add():
        a=file_picker.get_directory_path()
        new_task.value=a
        page.update()
    def add_clicked(e):
        tasks_view.controls.append(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        view.update()

    def resp(e):
        if page.width<=505:
            pass
        return
            # pw.update()
    page.on_resize=resp
    new_task = ft.TextField(hint_text="Choose A folder...", expand=True)
    ethernet=ft.Text(
                    "",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    italic=True,
                    )
    wifi=ft.Text(
                    "Browse a Folder and\nClick Start Sharing",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    italic=True,
                    )
    hotspot=ft.Text(
                    "",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    italic=True,
                    )
    a=os.getcwd()
    b=a.split('\\')
    c=""
    for i,folder in enumerate(b):
        try:
            c="\\".join(b[:i])
            os.listdir(c)
            break
        except:
            pass
    # print(dir)
    dir=c+'\\'
    new_task.value=dir
    page.update()
    # print(os.listdir(dir))
    up_dir=dir
    view=ft.Column(
        controls=[
            ft.Row(
                controls=[
                    new_task,
                    ft.FloatingActionButton(icon=ft.icons.FOLDER_OPEN, on_click=lambda _: file_picker.get_directory_path()),
                    # ft.ElevatedButton(icon=ft.icons.FOLDER_OPEN, on_click=lambda _: file_picker.pick_files(allow_multiple=True))
                ],
            ),
            ft.Row(
                controls=[
                    ft.FloatingActionButton(icon=ft.icons.PLAY_ARROW_ROUNDED,text="Start Sharing",expand=True, on_click=lambda _: start_sharing()),
                    ft.FloatingActionButton(icon=ft.icons.STOP,text="Stop Sharing",expand=True, on_click=lambda _: stop_sharing())
                ],
            ),
            ft.Row(
                controls=[
                    ft.Text(
                    "Receiver's Instructions: ",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    italic=True,
                    )
                ],
            ),
            ft.Row(
                controls=[
                    ethernet,
                ],
            ),
            ft.Row(
                controls=[
                    wifi,
                ],
            ),
            ft.Row(
                controls=[
                    hotspot,
                ],
            ),
        ],
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(view)


ft.app(target=main)