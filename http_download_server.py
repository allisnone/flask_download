# -*- coding: utf-8 -*-
# Author: allisnone
# basic upload and download function for flask framework
import os
import sys
import glob
from flask import Flask, render_template, send_from_directory,request
from werkzeug import secure_filename   # 获取上传文件的文件名
 
DOWNLOAD_PATH='./download/'
#DOWNLOAD_PATH = 'C:/Users/Administrator/Downloads/' 
UPLOAD_PATH = './upload/'   # 上传路径
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','doc'])   # 允许上传的文件类型
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH


def get_download_file_maps(dir='./download/',pattern='*.dll'): 
    maps ={}
    for fname in glob.glob(dir+pattern):
        if os.path.isfile(fname):
            key = fname.split('\\')[-1]
            maps[key]= os.path.getsize(fname)/1024
    return maps

@app.route('/')
def index():
    return '<a href="/download"> 文件下载 </a>'
 
@app.route('/download')
def filelist():
    return render_template('download.html', files=get_download_file_maps(dir=DOWNLOAD_PATH,pattern='*.dll') )
 
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(DOWNLOAD_PATH, filename, mimetype='application/octet-stream')


def allowed_file(filename):   # 验证上传的文件名是否符合要求，文件名必须带点并且符合允许上传的文件类型要求，两者都满足则返回 true
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':   # 如果是 POST 请求方式
        file = request.files['file']   # 获取上传的文件
        if file:  # 如果文件存在
            filename = secure_filename(file.filename)   # 获取上传文件的文件名
            if allowed_file(file.filename):   # 如果文件存在并且符合要求则为 true
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   # 保存文件
                return '{} upload successed!'.format(filename)   # 返回保存成功的信息
            else:
                return '{} Not supported file type!'.format(filename)   # 返回保存成功的信息
        else:
            pass
    # 使用 GET 方式请求页面时或是上传文件失败时返回上传文件的表单页面
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    ''' 
@app.route('/upload_nolimit', methods=['GET', 'POST'])
def upload_file_nolimit():
    if request.method == 'POST':   # 如果是 POST 请求方式
        file = request.files['file']   # 获取上传的文件
        if file:  # 如果文件存在
            filename = secure_filename(file.filename)   # 获取上传文件的文件名
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   # 保存文件
            return '{} upload successed!'.format(filename)   # 返回保存成功的信息
        else:
            pass
    # 使用 GET 方式请求页面时或是上传文件失败时返回上传文件的表单页面
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    ''' 

@app.route('/uploaded')
def uploaded_file_list():
    return render_template('download_uploaded.html', files=get_download_file_maps(dir=UPLOAD_PATH,pattern='*') )

 
@app.route('/uploaded/<filename>')
def download_uploaded(filename):
    return send_from_directory(UPLOAD_PATH, filename, mimetype='application/octet-stream')
    
if __name__ == '__main__':
    #app.run(debug=True, port=80)
    if os.path.exists(DOWNLOAD_PATH):
        pass
    else:
        os.mkdir(DOWNLOAD_PATH)#,755)
    if os.path.exists(UPLOAD_PATH):
        pass
    else:
        os.mkdir(UPLOAD_PATH)#,755)
    app.run(debug=True, host='0.0.0.0', port=5000)
