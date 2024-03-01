from flask import Flask, request, render_template, redirect, url_for, session, jsonify, send_from_directory

from flask_socketio import SocketIO, join_room, leave_room, send
from werkzeug.utils import secure_filename
from utils import generate_room_code
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'SDKFJSDFOWEIOF'
socketio = SocketIO(app)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif'}
rooms = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
def home():
    session.clear()

    if request.method == "POST":
        name = request.form.get('name')
        create = request.form.get('create', False)
        code = request.form.get('code')
        join = request.form.get('join', False)

        if not name:
            return render_template('home.html', error="Name is required", code=code)

        if create != False:
            room_code = generate_room_code(6, list(rooms.keys()))
            new_room = {
                'members': 0,
                'messages': []
            }
            rooms[room_code] = new_room

        if join != False:
            # no code
            if not code:
                return render_template('home.html', error="Please enter a room code to enter a chat room", name=name)
            # invalid code
            if code not in rooms:
                return render_template('home.html', error="Room code invalid", name=name)

            room_code = code

        session['room'] = room_code
        session['name'] = name
        return redirect(url_for('room'))
    else:
        return render_template('home.html')


@app.route('/room')
def room():
    room = session.get('room')
    name = session.get('name')

    if name is None or room is None or room not in rooms:
        return redirect(url_for('home'))

    messages = rooms[room]['messages']
    return render_template('room.html', room=room, user=name, messages=messages)


@socketio.on('connect')
def handle_connect(auth):
    name = session.get('name')
    room = session.get('room')

    if name is None or room is None:
        return

    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({
        "sender": "",
        "message": f"{name} has entered the chat"
    }, to=room)
    
    if room in rooms:
        rooms[room]["members"] += 1



@socketio.on('message')
def handle_message(payload):
    room = session.get('room')
    name = session.get('name')

    if room not in rooms:
        return
    
    if 'file_name' in payload:
        # If the payload contains 'file_name', it is a file message
        message = {
            "sender": name,
            "message": payload["file_name"],
            "file": True,  # Add a flag to indicate it's a file message
            "file_path": f"/uploads/{payload['file_name']}"  # Update with the correct file path
        }
    else:
        message = {
            "sender": name,
            "message": payload["message"]
        }

    send(message, to=room)
    rooms[room]["messages"].append(message)

@socketio.on('file_upload')
def handle_file_upload(data):
    room = session.get('room')
    name = session.get('name')

    if room not in rooms:
        return

    file_name = data['file_name']
    # Additional: Send the file path to the client
    file_path = url_for('uploaded_file', filename=file_name)
    print("Upload Folder:", app.config['UPLOAD_FOLDER'])
    socketio.emit('file_path', {'file_name': file_name, 'file_path': file_path, 'sender': name}, to=room)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


   
@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file part"})

        file = request.files['file']

        if file.filename == '':
            return jsonify({"status": "error", "message": "No selected file"})

        if file and allowed_file(file.filename):
            # Ensure that you are saving the file to the correct path
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return jsonify({"status": "success", "message": "File uploaded successfully"})
        else:
            return jsonify({"status": "error", "message": "Unsupported file format"})

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Exception during file upload: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"})

@socketio.on('disconnect')
def handle_disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({
        "message": f"{name} has left the chat",
        "sender": ""
    }, to=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)
