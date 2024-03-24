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

    
@app.route('/', methods=['GET', 'POST'])
def home():
    home = True
    join = False
    create = False
    area = False
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        area_id = request.form.get('area_id')
        
        if not username or not password:
            return render_template('home.html', error='Please fill in all fields!')
        
        if home and 'login' in request.form:
            if username in users and users[username] == password:
                session['username'] = username
                join = True
                home = False
                return render_template('join.html', username=username)
            else:
                return render_template('home.html', error='Invalid username or password!')
            
        if join and 'join' in request.form:
            if area_ids[area_id] == id:
                area_ids[area_id] = id
                create = True
                join = False
                return render_template('create.html', username=username)
            else:
                return render_template('join.html', error='Invalid area id!')
            
        if join and 'create' in request.form:
            return render_template('create.html', username=username)
    
    if home:
        return render_template('home.html')
    elif join:
        return render_template('join.html')
    elif create:
        return render_template('create.html')
    elif area:
        return render_template('area.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)