from flask import Flask, request, render_template, session, redirect
from flask_socketio import join_room, leave_room, send, emit, SocketIO
import random
from string import ascii_letters, digits

app = Flask(__name__)
app.config["SECRET_KEY"] = "sdgksdjg"
socketio = SocketIO(app)

users = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3",
    "user4": "password4",
    "user5": "password5",
    "user6": "password6",
    "user7": "password7",
    "user8": "password8",
    "user9": "password9",
    "user10": "password10"
}

area_ids = {
    "area1": "id1",
    "area2": "id2",
    "area3": "id3",
    "area4": "id4",
    "area5": "id5",
}

areas = {}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('home.html', error='Please fill in all fields!')
        
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/join')
        else:
            return render_template('home.html', error='Invalid username or password!')
    
    return render_template('home.html')

@app.route('/join', methods=['GET', 'POST'])
def join():
    if 'username' not in session:
        return redirect('/')
    
    username = session['username']
    
    if request.method == 'POST':
        area_id = request.form.get('area_id')
        
        if area_id in area_ids and area_ids[area_id] == 'id':
            return render_template('area.html', username=username)
        elif 'create' in request.form:
            return redirect('/create')
        else:
            return render_template('join.html', error='Invalid area id!')
    
    return render_template('join.html', username=username)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect('/')
    
    username = session['username']
    
    if request.method == 'POST':
        if 'cancel' in request.form:
            return redirect('/join')
        elif 'create' in request.form:
            area_name = request.form.get('area_name')
            area_id = request.form.get('area_id')
            area_size = request.form.get('area_size')
            print(area_name, area_id, area_size)
            areas[area_id] = {"name": area_name, "size": area_size}
            return render_template('area.html', username=username)
    
    return render_template('create.html', username=username)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
