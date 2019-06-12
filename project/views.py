import os, json

from flask import Flask, request, Response, jsonify, json
from flask import render_template, url_for, redirect, send_from_directory
from flask import make_response, abort, session
from werkzeug.utils import secure_filename

from project import app

from cbir.indexing import Indexing
from cbir.colordescriptor import ColorDescriptor
from cbir.searcher import Searcher
from cbir.search import Search

# Web Profile
@app.route('/')
def index():
    return redirect(url_for('flowercolor_image'))

# flowercolor Image Search
@app.route('/flowercolor/image/')
def flowercolor_image():
    return render_template('flowercolor/image.html', title="Flowers Image")

@app.route('/flowercolor/image/features/')
def features():
    data = None
    with open('dataset_features.json') as f:
        data = json.load(f)
        f.close()

    return render_template('flowercolor/features.html', title="Image Feature", data=data)

@app.route('/flowercolor/image/process_features/')
def process_features():
    indexer = Indexing.indexer()

    return redirect('/flowercolor/image/features/')

@app.route('/flowercolor/image/result', methods=['GET', 'POST'])
def image_result():
    result = None
    if request.method == 'POST':
        f = request.files['search']
        name = secure_filename(f.filename)
        img = f.read()
        
        # query by color
        s = Search(img, name)

        result, query = s.query_search()
    return render_template('flowercolor/result_image.html', title=name, data=result, query=query['query'])