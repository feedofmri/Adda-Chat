from flask import Flask, request, render_template, session, redirect
from flask_socketio import SocketIO, leave_room, join_room, send

import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "sdgksdjg"
socketio = SocketIO(app)

with open("data/users.json", "r") as users_file:
    users = json.load(users_file)

with open("data/areas.json", "r") as areas_file:
    areas = json.load(areas_file)

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
        if 'create' in request.form:
            return redirect('/create')
        
        elif 'join' in request.form:
            if area_id in areas:
                return redirect('/area/' + area_id)
            
            else:
                return render_template('join.html', error='Invalid area id!')
    
    return render_template('join.html', username=username)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:  # Access the session keyword
        return redirect('/')
    
    username = session['username']  # Access the session keyword
    
    if request.method == 'POST':
        if 'cancel' in request.form:
            return redirect('/join')
        elif 'create' in request.form:
            area_name = request.form.get('area_name')
            area_id = request.form.get('area_id')
            area_size = request.form.get('area_size')
            areas[area_id] = {"name": area_name, "size": area_size}
            
            
            with open("data/areas.json", "w") as areas_file:
                json.dump(areas, areas_file)
                
            return redirect('/area/' + area_id)
    
    return render_template('create.html', username=username)

@app.route('/area/<area_id>', methods=['GET', 'POST'])
def area(area_id):
    if 'username' not in session:
        return redirect('/')
    if area_id not in areas:
        return redirect('/join')
    
    username = session['username']
    
    if request.method == 'POST':
        if 'leave' in request.form:
            return redirect('/join')
        if 'logout' in request.form:
            return redirect('/')
        
        
    return render_template('area.html', username=username, area_id=area_id, area_name=areas[area_id]['name'], area_size=areas[area_id]['size'])

@socketio.on('connect')
def connect(auth):
    area = request.args.get('area')
    username = request.args.get('username')
    if not area or not username:
        return False
    if area not in areas:
        leave_room(area)
        return False
    join_room(area)
    send(username + ' has joined the area.', room=area)
    print(f"{username} has joined the area {area}")


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
