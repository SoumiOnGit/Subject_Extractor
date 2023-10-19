from flask import Flask, render_template, request , redirect
import requests
import os
from get_sub_names_in_subdirectories import get_subjects_from_folder
from os import listdir
app=Flask(__name__ , static_folder="uploads")
#to set static folder


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/1')
def sub():
    print(os.getcwd())
    path = os.path.join(os.getcwd(),"uploads")
    all_subjects = get_subjects_from_folder(path)
    print(all_subjects)
    print(path)
    return redirect('/extracts')


@app.route('/upload', methods = ['POST' , 'GET'] )
def upload():
    if request.method == 'POST':
        uploads = os.listdir(os.path.join(os.getcwd(),"uploads"))
        for file in uploads:
            os.remove(os.path.join(os.getcwd(),"uploads",file))
        uploaded_file = request.files['file']
        print(uploaded_file)
        print(uploaded_file.filename)
        uploaded_file.save(os.path.join(os.getcwd(),"uploads",uploaded_file.filename))
        return redirect('/1')
    return render_template('uploads.html')

@app.route('/extracts')
def show_extracts():
    upload_path = os.path.join(os.getcwd(),"uploads")
    extract_path = os.path.join(upload_path,"extracts")
    print(extract_path)
    folders = os.listdir(extract_path)
    print(folders)
    
    extracts = os.listdir(os.path.join(os.getcwd(),"uploads","extracts"))
    print(extracts)

    extractdict= {}

    for folder in extracts:
        file = os.listdir(os.path.join(os.getcwd(),"uploads","extracts",folder))[0]

        extractdict[folder] = os.path.join(folder,file)
    print(extractdict)
    return render_template('extracts.html', folders = folders, extract_path = extract_path, extractdict=extractdict)


extracts = os.listdir(os.path.join(os.getcwd(),"uploads","extracts"))
print(extracts)

extractdict= {}

for folder in extracts:
    file = os.listdir(os.path.join(os.getcwd(),"uploads","extracts",folder))[0]

    extractdict[folder] = os.path.join(os.getcwd(),"uploads","extracts",folder,file)
print(extractdict)
if __name__ == '__main__':
    app.run(debug=True)


#from music app tutorial , while uploading it shiuld get store din the uploads folder 
#before each upload , the uploads folder should be emptied.. from yt donwloader 
#one more path , show_extracts , which will show extracts in the extracts folder
