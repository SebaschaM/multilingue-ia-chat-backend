from app import socketio


@socketio.on('connect')
def handle_connect():
    print("Connected")

@socketio.on('message')
def handle_message(data):
    print("Mensaje recibido en el backend", data)
    socketio.emit('message', data, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    print("Disconnected")
    socketio.emit('disconnected', {'data': 'Disconnected'})
