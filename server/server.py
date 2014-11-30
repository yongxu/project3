from flask import Flask, url_for, redirect, render_template, send_from_directory
from flask.ext.socketio import SocketIO, emit
import os
import json
import time
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

client_connected=False

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    print path
    return app.send_static_file(path)

@socketio.on('client request', namespace='/tile')
def client_message(message):
    receive_client_message(message)

def push_to_client(message,state='update'):
    emit('server response', {'state':'update','data': message})

@socketio.on('connect', namespace='/tile')
def client_connect():
    emit('server response', {'state' : 'connected'})
    client_connected=True
    push_to_client({'state':'update','apple':{'x':3,'y':3}})

@socketio.on('disconnect', namespace='/tile')
def client_disconnect():
    client_connected=False
    print('Client disconnected')

def receive_client_message(message):
    pass

if __name__ == '__main__':
    from gevent import monkey
    monkey.patch_all()

    app.debug=True
    socketio.run(app)


    def background_thread():
        count = 0
        while True:
            time.sleep(1)
            count += 1
            if client_connected:
                push_to_client({'state':'update','apple':{'x':count%20,'y':count%20}})



    thread = Thread(target=background_thread)
    thread.start()
