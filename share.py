# from importlib.resources import path
# from logging import exception
from flask import Flask, render_template, request, send_file, redirect,  stream_with_context, Response
import os
from zipfile import ZipFile
from time import time, sleep
import glob
from werkzeug.utils import secure_filename
import pathlib 
import logging
import search_file3
import format_file3
import search_file
import format_file
from threading import Thread
import urllib
# import requests

app=Flask(__name__, static_url_path='/static')
dir="D:/"
up_dir="D:/"
list_of_mp3=set()
# parent_folder = pathlib.Path(dir)

# logging.basicConfig(filename='error.log', format='%(message)s',filemode='w',level=logging.INFO)
# logging.basicConfig(filename='error.log', format='%(message)s',filemode='w',level=logging.ERROR)
# logging.basicConfig(filename='error.log', format='%(message)s',filemode='w',level=logging.DEBUG)
# logging.basicConfig(filename='error.log', format='%(message)s',filemode='w',level=logging.WARNING)
# logging.basicConfig(filename='error.log', format='%(message)s',filemode='w',level=logging.CRITICAL)
# logging.basicConfig(filename='error.log', format='%(message)s',filemode='w',level=logging.WARN)
# logging.basicConfig(filename='error.log', format='%(message)s',filemode='w',level=logging.NOTSET)
# logging.setLevel(logging.ERROR)
# logging.setLevel(logging.DEBUG)
# logging.setLevel(logging.WARNING)
# logging.setLevel(logging.CRITICAL)
# logging.setLevel(logging.WARN)
# logging.setLevel(logging.BASIC_FORMAT)







n=0
blacklist=["$RECYCLE.BIN", "System Volume Information","Android","sound_recorder"]

list=set()
size=0
# dir=input('Enter dir to share: ')
# dir='/storage/emulated/0/'


# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def index():
    path=dir
    rows=os.listdir(path)
    # print(rows)
    dict_files={}
    dict_folders={}
    for row in rows:
        if os.path.isdir(path+row):
            ab_path='/folder?folder='+row+'/'
            dict_folders[ab_path]=row+"/"
        else:
            ab_path='/download?file='+row
            dict_files[ab_path]=row
        # print(dict_files)
    # print(dict_folders.values())
    return render_template('index.html', spath=[], dict_folders=dict_folders, dict_files=dict_files)

def mem_clean(d1,d2):
    sleep(10)
    d1.clear()
    d2.clear()
    format_file3.mem_clean()
    search_file3.mem_clean()


# @app.route('/search', methods=['POST'])
def search():
    ref=request.referrer
    path=dir
    if "=" in ref and "/search" not in ref:
        linkdir=ref.split("=")[-1]
        path=os.path.join(dir,linkdir)
    # print(path)
    query=request.form['query']
    if not query:
    	return redirect('/')
    else:
        s=time()
        files=search_file3.search_cache(query,path)
        # print(files)
        e=time()
        # print(f'Actual Time for search {e-s}seconds')
        # print (len(files))
        st=time()
        dict_files, dict_folders= format_file3.thread_format(files,dir)
        en=time()
        # print(f'Actual Time for format {en-st}seconds')
        # print(dict_folders)
        return render_template('s.html', query=query, dict_folders=dict_folders, dict_files=dict_files)

@app.route('/search', methods=['POST'])
def search():
    ref=request.referrer
    path=dir
    if "=" in ref and "/search" not in ref:
        linkdir=ref.split("=")[-1]
        path=os.path.join(dir,linkdir)
    # print(path)
    query=request.form['query']
    if not query:
    	return redirect('/')
    else:
        s=time()
        files=search_file.search_cache(query,path)
        if files==[]:
            # print('entered')
            files=search_file.search(query, path)
        print('--------------Files------------\n',files)
        # print(files)
        e=time()
        # print(f'Actual Time for search {e-s}seconds')
        # print (len(files))
        format_file.mem_clean()
        st=time()
        dict_files, dict_folders= format_file.thread_format(files,dir)
        print(dict_files)
        en=time()
        # print(f'Actual Time for format {en-st}seconds')
        # print(dict_folders)
        return render_template('s.html', query=query, dict_folders=dict_folders, dict_files=dict_files)

#@app.route('/search', methods=['POST'])
def search():
    query=request.form['query']
    main_dir=dir
    q="*"+query+"*"
    st=time()
    files=parent_folder.rglob(q)
    en=time()
    #print("\n\n",files)
    # print(f'Search Completed in {en-st}seconds.')
    dict_files={}
    dict_folders={}
    for row in files:
        if os.path.isdir(os.path.join(dir,row)):
            # ab_path='/folder?folder='+row
            ab_path='/folder?folder='+(str(row).replace(main_dir,"")).replace('\\','/')+"/"
            dict_folders[ab_path]=os.path.basename(row)+"/"
        else:
            # ab_path='/download?file='+row
            ab_path='/download?file='+(str(row).replace(main_dir,"")).replace('\\','/')
            dict_files[ab_path]=os.path.basename(row)
    # dict_files={}
    # for row in files:
    #     if os.path.isdir(row):
    #         ab_path='/folder?folder='+(row.replace(main_dir,"")).replace('\\','/')+"/"
    #     else:
    #         ab_path='/download?file='+(row.replace(main_dir,"")).replace('\\','/')
    #     #dict_files[ab_path]=row
    #     dict_files[ab_path]=row.split('\\')[-1]
    return render_template('search2.html', query=query, dict_folders=dict_folders, dict_files=dict_files)



def search():
    query=request.form['query']
    #file="test"
    #D:\Bhavin\hp share\music_finder.py
    main_dir=dir.replace('/','\\')
    path=main_dir+"**\\*"+query+"*"
    st=time()
    files=glob.glob(path, recursive=True)
    en=time()
    #print("\n\n",files)
    # print(f'Search Completed in {en-st}seconds.')
    dict_files={}
    dict_folders={}
    for row in files:
        if os.path.isdir(os.path.join(dir,row)):
            # ab_path='/folder?folder='+row
            ab_path='/folder?folder='+(row.replace(main_dir,"")).replace('\\','/')+"/"
            dict_folders[ab_path]=os.path.basename(row)+"/"
        else:
            # ab_path='/download?file='+row
            ab_path='/download?file='+(row.replace(main_dir,"")).replace('\\','/')
            dict_files[ab_path]=os.path.basename(row)
    # dict_files={}
    # for row in files:
    #     if os.path.isdir(row):
    #         ab_path='/folder?folder='+(row.replace(main_dir,"")).replace('\\','/')+"/"
    #     else:
    #         ab_path='/download?file='+(row.replace(main_dir,"")).replace('\\','/')
    #     #dict_files[ab_path]=row
    #     dict_files[ab_path]=row.split('\\')[-1]
    return render_template('search2.html', query=query, dict_folders=dict_folders, dict_files=dict_files)


@app.route('/back')
def back():
    url = request.referrer
    base_url = url.split('/')
    # print(base_url)
    previous_url = '/'.join(base_url[3:-2])
    # print('previous_url',previous_url)
    if previous_url=='':
        previous_url='/'
    else:
        previous_url+='/'
    return redirect(previous_url)
    # print(base_url)
    # print(previous_url)
    # txt=url+" <br> "+str(base_url)
    # url=request.url
    # folder=url.split('/')
    # print(folder)
    # folder.pop(-1)
    # print(folder)
    # new_url='/'.join(folder)
    # return redirect(new_url)

@app.route('/folder')
def folder():
    path=dir
    folder=request.args.get('folder')
    path=path+folder
    index=folder.split("/")
    index=index[:-1]

    # print(folder)
    # print('index: ',index)
    spath=[]
    # for i in index:
    for i in range(0,len(index)):
        subpath=index[:i]
        subpath.append(index[i])
        spath.append("/".join(subpath)+'/')
    rows=os.listdir(path)
    dict_files={}
    dict_folders={}
    for row in rows:
        if os.path.isdir(path+row):
            ab_path='/folder?folder='+folder+row+'/'
            dict_folders[ab_path]=row+"/"
        else:
            ab_path='/download?file='+folder+'/'+row
            dict_files[ab_path]=row
    # print(spath)
    return render_template('index.html', spath=spath, dict_folders=dict_folders, dict_files=dict_files)

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths 

@app.route('/zip')
def zip():
    path=dir
    url = request.referrer
    base_url = url.split('/')
    base_url = '/'.join(base_url[3:])
    # print(base_url)
    txt=url+" <br> "+str(base_url)
    if "=" in base_url:
        if path[-1]!='/':
            folder='/'+base_url.split('=')[-1]
        else:
            folder=base_url.split('=')[-1]
        txt+=" <br> True"
        f=True
    else:
        folder='/'
        txt+=" <br> False"
        f=False
    
    dir_name = path+folder
    
    if f:
        if folder[-1]=='/':
            folder2=folder[:-1]
            fi=((folder2.split('/'))[-1]).replace('%20', " ")
        else:
            fi=((folder.split('/'))[-1]).replace('%20', " ")
        zip_name = 'zip/'+(fi).replace('%20'," ")+".zip"
    else:
        zip_name = 'zip/main.zip'
        fi=dir
    # print ("base_url =",base_url)
    # print ("zip_name =",zip_name)
    dir_name=dir_name.replace("%20"," ")

    try:
        ls=os.listdir('zip')
    except:
        os.mkdir('zip')
        ls=os.listdir('zip')
    same_count=0
    for i in ls:
       if (zip_name.split('/')[-1]).split(".")[0] in i:
          same_count+=1
    if same_count>0:
       zip_name=zip_name.split(".")[0]+f" ({same_count}).zip"

    zip_path=zip_name
    s=time()
    list_of_files= get_all_file_paths(dir_name)
    e=time()
    # print (f"\nSearching Completed in {e-s}seconds.\n")
    s=time()
    # print(list_of_files)
    zip_path=zip_path.replace('/','\\\\')

    with ZipFile(zip_path, 'w') as zipObj:
        for file in list_of_files:
            zipObj.write(filename=file,arcname=fi+file.split(fi)[-1])
    e=time()
    # print (f"\nZipping Completed in {e-s}seconds.\n")
    return send_file(zip_name, as_attachment=True)
    
CHUNK_SIZE = 102400
def read_file_chunks(path):
    with open(path, 'rb') as fd:
        while 1:
            buf = fd.read(CHUNK_SIZE)
            if buf:
                yield buf
            else:
                break

@app.route('/video')
def stream_video():
  filename=request.args.get('file')
  fp=dir+filename
  # Open the video file in binary mode
  file = open(fp, 'rb')

  # Return the file as a stream
  return send_file(
      file,
      mimetype='video/mp4',
      as_attachment=False
  )


def download_file():
  filename=request.args.get('file')
  fp=dir+filename
  # Get the range header from the request
  range_header = request.headers.get('Range')
#   print(range_header)
  if not range_header:
      return send_file(fp)

  # Get the byte range from the range header
  byte_range = range_header.split('=')[1]
  start, end = byte_range.split('-')
  start = int(start)
  if end:
    end = int(end)

  # Open the file and seek to the requested position
  file = open(fp, 'rb')
  file.seek(start)
  if end:
    chunk = file.read(end - start + 1)
  else:
    chunk = file.read(start + 1)

  # Build the response with the appropriate headers
  response = app.make_response(chunk)
  type=filename.split('.')[-1]
  if filename.split('.')[-1] in ['mp4','mkv']:
    response.headers['Content-Type']= 'application/x-mpegURL'

  if end:
    response.headers['Content-Range'] = f'bytes {start}-{end}/{ os.path.getsize(fp)}'
  else:
    response.headers['Content-Range'] = f'bytes {start}-/{ os.path.getsize(fp)}'
  response.headers['Accept-Ranges'] = 'bytes'
  response.status_code = 206

  return response

@app.route('/download')
def download():
    filename=request.args.get('file')
    # print(filename)
    fp=dir+filename
    size=os.path.getsize(fp)
    fr="filename*=UTF-8''{quoted_filename}".format(quoted_filename=urllib.parse.quote(os.path.basename(fp).encode('utf8')))
    if os.path.exists(fp):
        return Response(
            stream_with_context(read_file_chunks(fp)),
            headers={
                'Content-Disposition': f'attachment; {fr};', 'Content-Length': size,'Content-Type': 'application/octet-stream'
            }
        )
    else:
        raise BufferError

CHUNK_SIZE_VIEW = 20480
def read_file_chunks_view(path,rh):
    with open(path, 'rb') as fd:
        while 1:
            if rh==0:
                buf = fd.read(CHUNK_SIZE_VIEW)
            else:
                buf = fd.read(rh)
            if buf:
                yield buf
            else:
                break

@app.route('/view', methods=['GET'])
def view():
    filename=request.args.get('file')
    fp=dir+filename
    size=os.path.getsize(fp)
    range_header = request.headers.get('Range')
    # print(str(request.headers))
    # print("Range Header",range_header)
    if range_header is not None:
        range_header=int(range_header)
    else:
        range_header=0
    fr="filename*=UTF-8''{quoted_filename}".format(quoted_filename=urllib.parse.quote(os.path.basename(fp).encode('utf8')))
    if os.path.exists(fp):
        return Response(
            stream_with_context(read_file_chunks_view(fp,range_header)),
            headers={
                'Content-Disposition': f'{fr}', 
                'Content-Length': size,
                'Content-Type': 'application/octet-stream'
            }
        )
    else:
        raise BufferError


@app.route('/stream', methods=['GET', 'POST'])
def Music():
    filename=request.args.get('file')
    fp=dir+filename.replace('/','\\')
    size=os.path.getsize(fp)
    range_header = request.headers.get('Range')
    if range_header is not None:
        with open(fp, 'rb') as f:
            partial_file = f.seek(int(range_header))
            return send_file(partial_file, as_attachment=True, conditional=True), 206
        raise Exception("Unknown exception")

    return send_file(fp, as_attachment=True)

def download():
    filename=request.args.get('file')
    path=dir+filename
    return send_file(path,as_attachment=True)

@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
      f = request.files['file']
      ip=request.environ['REMOTE_ADDR']
      if not os.path.exists(up_dir+'uploads/'):
        os.mkdir(os.path.join(up_dir,'uploads/'))
      if not os.path.exists(up_dir+'uploads/'+ip):
        os.mkdir(os.path.join(up_dir,'uploads',ip))
      app.config['UPLOAD_FOLDER'] = os.path.join(os.path.join(up_dir,'uploads'),ip)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
    if "/search" in request.referrer:
    	return redirect ("/")
    return redirect(request.referrer)


#d():

#    filename=request.args.get('file')

#    path=dir+filename

#    return send_file(path,as_attachment=True)

#

#


#def music(format,path):

#    global n

#    n+=1

#    print(n)

#    if path.split("/")[-1] in blacklist:

#        pass

#    else:

#	        path_list=os.listdir(path)

#	    

#	        if path[-1]=="/":

#	            path=path[:-1]

#	        for inpath in path_list:

#	            abs_path=path+"/"+inpath

#	            if os.path.isdir(abs_path):

#	      	
    
# def music(format,path):
#     global size
#     if path.split("/")[-1] in blacklist:
#         pass
#     else:
#         path_list=os.listdir(path)
#         if path[-1]=="/":
#             path=path[:-1]
#         for inpath in path_list:
#             abs_path=path+"/"+inpath
#             if os.path.isdir(abs_path):
#                 music(format,abs_path)
#             if inpath.split(".")[-1]==format:
#                 list.add(inpath)
#                 if len(list)>size:
#                     list_of_mp3.add(path+"/"+inpath)
#                 size=len(list)
	                


#   list.add(inpath)

#	                if len(list)>size:

#	                	list_of_mp3.add(path+"/"+inpath)

#	                size=len(list)

#	                

#

#

#def zip(list_of_mp3):

#  

def zip_arc(list_of_files):
	zip_path="zip/music.zip"
	zipObj = ZipFile(zip_path, 'w')
	for file in list_of_files:
		zipObj.write(filename=file,arcname="\\"+file.split("\\")[-1])
	return zip_path

@app.route("/music_zip")
def music_zip():
    list_of_mp3.clear()
    st=time()
    files=glob.glob(dir+"**/*.mp3", recursive=True)
    en=time()
    # print(f'Searching completed in {en-st} seconds')
    # print (list_of_mp3)
    s=time()
    zip_path=zip_arc(files)
    e=time()
    # print(f'Zipping completed in {e-s} seconds')
    return send_file(zip_path, as_attachment=True)


def stop():
    raise ModuleNotFoundError

if __name__=='__main__':
    a=os.getcwd()
    b=a.split('/')
    c=""
    for i,folder in enumerate(b):
    	try:
    		c="/".join(b[:i])
    		os.listdir(c)
    		break
    	except:
    		pass
    # print(dir)
    dir='/'
    # print(os.listdir(dir))
    up_dir=dir
    # print('dir: ',dir)
    list_of_mp3=set()
    list_of_mp3=set()
    # parent_folder = pathlib.Path('D:\\')
    thread=Thread(target=search_file.loop,args=(dir.replace("/","\\"),))
    thread.daemon=True
    thread.start()
    # thread.join()
    # Thread(search_file3.sort_start(dir))
    n=0
    blacklist=["$RECYCLE.BIN", "System Volume Information","Android","sound_recorder"]

    # list=set()
    size=0
    app.run('0.0.0.0',port=8080,debug=True)

"""
<!-- <form action="{{ url_for('upload') }}">
            <div class="sticky">
                <a href="" class="upload"><img class="img" src="{{ url_for('static', filename='file.png') }}" alt="">Upload</a>
            </div>
        </form> -->


{% if value[1]=="folder" %}
            <a href="{{ key }}"><img class="img" src="{{ url_for('static', filename='icons/folder-fill.svg') }}" alt=""></a>
            {% endif %}
            {% if value[1] in ["apng", "png", "avif", "jpg", "jpeg", "jfif", "pjpeg", "pjp", "webp", "bmp", "svg", "ico", "cur", "tif", "tiff"] %}
            <a href="{{ key }}"><img class="img" src="{{ url_for('static', filename='icons/file-image-fill.svg') }}" alt="img"></a>
            {% endif %}
            {% if value[1]=="folder" %}
            <a href="{{ key }}"><img class="img" src="{{ url_for('static', filename='icons/folder-fill.svg') }}" alt=""></a>
            {% endif %}
            {% if value[1]=="folder" %}
            <a href="{{ key }}"><img class="img" src="{{ url_for('static', filename='icons/folder-fill.svg') }}" alt=""></a>
            {% endif %}
            {% if value[1]=="folder" %}
            <a href="{{ key }}"><img class="img" src="{{ url_for('static', filename='icons/folder-fill.svg') }}" alt=""></a>
            {% endif %}
            {% if value[1]=="folder" %}
            <a href="{{ key }}"><img class="img" src="{{ url_for('static', filename='icons/folder-fill.svg') }}" alt=""></a>
            {% endif %}
"""
