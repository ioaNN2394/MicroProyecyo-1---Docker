from flask import Flask, jsonify
from flask_cors import CORS # Necesitamos importar CORS aquí
from users.controllers.user_controller import user_controller
from users.models.user_model import db
from utils import register_service
import os

app = Flask(__name__)
CORS(app, supports_credentials=True) # Y activarlo

# Configuración para la conexión a la base de datos con SQLAlchemy
DB_USER = os.environ.get('MYSQL_USER')
DB_PASSWORD = os.environ.get('MYSQL_PASSWORD')
DB_HOST = os.environ.get('MYSQL_HOST')
DB_NAME = os.environ.get('MYSQL_DB')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tu_clave_secreta_aqui'

# Inicializar la base de datos con la aplicación
db.init_app(app)

# Registrar el blueprint
app.register_blueprint(user_controller)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    register_service('users', 5001)
    app.run(host='0.0.0.0', port=5001, debug=True)
