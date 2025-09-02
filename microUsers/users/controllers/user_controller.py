from flask import Blueprint, request, jsonify, session
from passlib.hash import sha256_crypt
from users.models.user_model import User

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/api/users/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    username = data.get('username')
    password = sha256_crypt.encrypt(str(data.get('password')))

    if User.create(name, email, username, password):
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    return jsonify({'message': 'El usuario o email ya existe'}), 400

@user_controller.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password_candidate = data.get('password')

    user = User.get_by_username(username)

    if user and sha256_crypt.verify(password_candidate, user['password']):
        # Iniciar sesión
        session['logged_in'] = True
        session['username'] = username
        session['email'] = user['email']
        return jsonify({'message': 'Inicio de sesión exitoso'})
    else:
        return jsonify({'message': 'Usuario o contraseña incorrectos'}), 401

@user_controller.route('/api/users/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Cierre de sesión exitoso'})

@user_controller.route('/api/users/check_session', methods=['GET'])
def check_session():
    if 'logged_in' in session:
        return jsonify({
            'logged_in': True,
            'username': session['username'],
            'email': session['email']
        })
    return jsonify({'logged_in': False})
