from flask import render_template, request
from model import KeyLog

def register_routes(app, db):
    
    @app.route('/')
    def index():
        logs: list[KeyLog] = KeyLog.query.all()
        return str(logs)