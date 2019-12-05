from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/PlantStore')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()