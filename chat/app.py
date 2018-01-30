# -*- encoding: utf-8 -*-

from flask import Flask, request
from flask_restful import Resource, Api
from flask_uploads import UploadSet, configure_uploads, ALL

app = Flask(__name__)
api = Api(app)
app.debug = True

files = UploadSet('uploads', ALL)
app.config['UPLOADS_DEFAULT_DEST'] = 'files'
configure_uploads(app, files)

app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'
