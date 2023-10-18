from flask import Flask, render_template, request
import requests
import os
from get_sub_names_in_subdirectories import get_subjects_from_folder
app=Flask(__name__)

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
    return "abc"

if __name__ == '__main__':
    app.run(debug=True)
