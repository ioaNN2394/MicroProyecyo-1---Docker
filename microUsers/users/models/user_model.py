# users/models/user_model.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @classmethod
    def create(cls, name, email, username, password):
        # Verificar si ya existe un usuario con ese email o username
        existing_user = cls.query.filter(
            (cls.email == email) | (cls.username == username)
        ).first()

        if existing_user:
            return False

        # Crear nuevo usuario
        new_user = cls(
            name=name,
            email=email,
            username=username,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        return True

    @classmethod
    def get_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        if user:
            # Devolver datos como diccionario (para que encaje con el controller)
            return {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'username': user.username,
                'password': user.password
            }
        return None
