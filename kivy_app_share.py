from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
import share
from plyer import filechooser
from threading import Thread
import search_file
import os
import socket
from multiprocessing import Process
import sys
from kivy.lang import Builder
from time import sleep
from kivy.clock import mainthread


class Demo(MDApp):
    
    def build(self):
        # def log_print(self):
        #     while True:
        #         f=open('error.log')
        #         log=f.read()
        #         f.close()
        #         self.txt.text=str(log)
        #         edit(self,log)
        #         # print('logger')
        #         # print(log)
        #         sleep(0.5)
        # @mainthread
        # def edit(self,log):
        #     self.txt.ids.label_to_change.text=str(log)
        # defining label with all the parameters
        screen = Screen()
        l = MDLabel(text="HI PEOPLE!", halign='center',
                    theme_text_color="Custom",
                    text_color=(0.5, 0, 0.5, 1),
                    font_style='Caption')
        
        # defining Text field with all the parameters
        self.path_share = MDTextField(text="Folder Path Appears Here...", pos_hint={
                                    'center_x': 0.5, 'center_y': 0.9})
        btn2 = MDRectangleFlatButton(text="Select Folder", pos_hint={
                                    'center_x': 0.5, 'center_y': 0.8},
                                    on_release=self.file_manager_open)
        # defining Button with all the parameters
        btn = MDRectangleFlatButton(text="Start Sharing", pos_hint={
                                    'center_x': 0.5, 'center_y': 0.7},
                                    on_release=self.btnfunc)
        btn3 = MDRectangleFlatButton(text="Stop Sharing", pos_hint={
                                    'center_x': 0.5, 'center_y': 0.4},
                                    on_release=self.stop)

        logs = MDLabel(text="Reciever's Instructions:", halign='center',
                    theme_text_color="Custom",
                    text_color=(0.5, 0, 0.5, 1),
                    font_style='Caption',pos_hint={
                                    'center_x': 0.5, 'center_y': 0.6})
        self.l = MDLabel(text="Browse a Folder and\nClick Start Sharing", halign='center',
                    theme_text_color="Custom",
                    text_color=(0.5, 0, 0.5, 1),
                    font_style='Caption',pos_hint={
                                    'center_x': 0.5, 'center_y': 0.5})
        KV = '''
MDScreen

    MDTextField:
        text: "abc"
        size_hint_x: .5
        hint_text: "Logs:- "
        max_height: "200dp"
        mode: "fill"
        id: label_to_change
        fill_color: 0, 0, 0, .4
        multiline: True
        pos_hint: {"center_x": 0.5, "center_y": 0.2}
'''
        # self.txt=Builder.load_string(KV)
        # self.txt.text='ytu'
        
        # adding widgets to screen
        screen.add_widget(self.path_share)
        screen.add_widget(btn2)
        screen.add_widget(btn)
        screen.add_widget(btn3)
        screen.add_widget(self.l)
        screen.add_widget(logs)
        # screen.add_widget(self.txt)
        # thread=Thread(target=log_print,args=(self,))
        # thread.daemon=True
        # thread.start()
        
        # returning the screen
        return screen
    def file_manager_open(self,obj):
        path = filechooser.choose_dir()[0] 
        self.path_share.text=path
        # this method returns a list with the first index
        # being the path of the file selected
        # toast(path)

    def stop(self,obj):
        return sys.exit()
    
    def btnfunc(self, obj):
        def extract_ip():
            st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:       
                st.connect(('10.255.255.255', 1))
                IP = st.getsockname()[0]
            except Exception:
                IP = '127.0.0.1'
            finally:
                st.close()
            return str(IP)
        ## importing socket module
        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ip2 = extract_ip()
        ## printing the hostname and ip_address
        a=f"Hostname: {hostname}"
        a+=f"\nPut this address in your browser:-\nhttp://{ip_address}:8080\nhttp://{ip2}:8080"
        self.l.text=a

        def start(self):
            directory=directory=self.path_share.text
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
                # p = Thread(target=share.app.run, args=('0.0.0.0',8080))
                # p.daemon=True
                # p.start()
                share.app.run('0.0.0.0',port=8080,threaded=True)
        
        thread=Thread(target=start,args=(self,))
        thread.daemon=True
        thread.start()
    
        

if __name__ == "__main__":
    Demo().run()
    

