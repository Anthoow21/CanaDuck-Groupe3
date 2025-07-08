from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db
from flasgger import Swagger
from functools import wraps
import jwt
import os
from dotenv import load_dotenv
load_dotenv()


JWT_SECRET = "on-ny-arrivera-jamais-enfin-peut-etre"

def decode_jwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Token manquant"}), 401

            token = auth_header.split(" ")[1]
            payload = decode_jwt(token)
            if not payload:
                return jsonify({"error": "Token invalide"}), 401

            roles = payload.get("roles", [])
            if required_role not in roles:
                return jsonify({"error": f"Rôle '{required_role}' requis"}), 403

            request.user = payload  # pour un accès facile dans la route
            return f(*args, **kwargs)
        return wrapper
    return decorator

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Channel Service API',
    'uiversion': 3,
    'definitions': {
        'Channel': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'name': {'type': 'string'},
                'private': {'type': 'boolean'},
                'topic': {'type': 'string'},
                'owner': {'type': 'string'},
                'created_at': {'type': 'string', 'format': 'date-time'},
                'modes': {
                    'type': 'array',
                    'items': {'type': 'string'}
                },
                'moderators': {
                    'type': 'array',
                    'items': {'type': 'string'}
                },
                'banned': {
                    'type': 'array',
                    'items': {'type': 'string'}
                },
                'invited': {
                    'type': 'array',
                    'items': {'type': 'string'}
                },
                'members': {
                    'type': 'array',
                    'items': {'type': 'string'}
                }
            }
        }
    }
}

swagger = Swagger(app)

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/channel', methods=['GET'])
def list_channels():
    """
    Lister les canaux publics
    ---
    tags:
      - Channel
    responses:
      200:
        description: Liste des canaux publics
        schema:
          type: array
          items:
            $ref: '#/definitions/Channel'
    """
    # Appel à la bdd pour retourner la liste des canaux
    channels = db.session.query(Channel).filter_by(private=False).all()
    return jsonify([channel.to_dict() for channel in channels]), 200


@app.route('/channel', methods=['POST'])
@require_role("owner")
@require_role("moderator")
def create_channel():
    """
    Créer un nouveau canal
    ---
    tags:
      - Channel
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - private
          properties:
            name:
              type: string
            private:
              type: boolean
          example:
            name: "tech"
            private: false
    responses:
      201:
        description: Canal créé avec succès
      409:
        description: Canal déjà existant
    """
    data = request.get_json()
    if not data or 'name' not in data or 'private' not in data:
        return jsonify({"error": "Nom et statut privé requis"}), 400
    name = data['name']
    private = data['private']
    existing_channel = db.session.query(Channel).filter_by(name=name).first()
    if existing_channel:
        return jsonify({"error": "Canal déjà existant"}), 409
    new_channel = Channel(name=name, private=private, owner=request.user['username'])
    db.session.add(new_channel)
    db.session.commit()
    return jsonify(new_channel.to_dict()), 201

@app.route('/channel/<name>/users', methods=['GET'])
def list_users_in_channel(name):
    """
    Lister les utilisateurs d’un canal
    ---
    tags:
      - Channel
    parameters:
      - name: name
        in: path
        required: true
        type: string
    responses:
      200:
        description: Liste des utilisateurs
        schema:
          type: array
          items:
            type: string
    """
    # Appel à la bdd pour retourner la liste des utilisateurs dans le canal
    channel = db.session.query(Channel).filter_by(name=name).first()
    if not channel:
        return jsonify({"error": "Canal non trouvé"}), 404
    return jsonify({"usernames": channel.members}), 200

@app.route('/channel/<name>', methods=['PATCH'])
@require_role("moderator")
@require_role("owner")
def update_channel(name):
    """
    Modifier le sujet et/ou les modes d’un canal
    ---
    tags:
      - Channel
    parameters:
      - name: name
        in: path
        type: string
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            topic:
              type: string
            mode:
              type: string
          example:
            topic: "Nouveau sujet"
            mode: "+r"
    responses:
      200:
        description: Modification réussie
      403:
        description: Non autorisé
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données manquantes"}), 400
    channel = db.session.query(Channel).filter_by(name=name).first()
    if not channel:
        return jsonify({"error": "Canal non trouvé"}), 404
    if 'topic' in data:
        channel.topic = data['topic']
    if 'mode' in data:
        mode = data['mode']
        if mode not in channel.modes:
            channel.modes.append(mode)
        else:
            return jsonify({"error": "Mode déjà présent"}), 409
    db.session.commit()
    return jsonify(channel.to_dict()), 200

@app.route('/channel/<name>', methods=['DELETE'])
def delete_channel(name):
    """
    Supprimer un canal
    ---
    tags:
      - Channel
    parameters:
      - name: name
        in: path
        required: true
        type: string
    responses:
      200:
        description: Canal supprimé
      403:
        description: Non autorisé
    """
    pass

@app.route('/channel/<name>/topic', methods=['POST'])
def update_topic(name):
    """
    Modifier uniquement le sujet d’un canal
    ---
    tags:
      - Channel
    parameters:
      - name: name
        in: path
        required: true
        type: string
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [topic]
          properties:
            topic:
              type: string
          example:
            topic: "Nouveau topic cool"
    responses:
      200:
        description: Sujet mis à jour
      403:
        description: Non autorisé
    """
    data = request.get_json()
    if not data or 'topic' not in data:
        return jsonify({"error": "Sujet requis"}), 400
    channel = db.session.query(Channel).filter_by(name=name).first()
    if not channel:
        return jsonify({"error": "Canal non trouvé"}), 404
    channel.topic = data['topic']
    db.session.commit()
    return jsonify(channel.to_dict()), 200

@app.route('/channel/<name>/mode', methods=['POST'])
def add_mode(name):
    """
    Ajouter un mode à un canal
    ---
    tags:
      - Channel
    parameters:
      - name: name
        in: path
        required: true
        type: string
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [mode]
          properties:
            mode:
              type: string
          example:
            mode: "+m"
    responses:
      201:
        description: Mode ajouté
      409:
        description: Mode déjà présent
    """
    pass

@app.route('/channel/<name>/config', methods=['GET'])
def get_config(name):
    """
    Récupérer la configuration complète d’un canal
    ---
    tags:
      - Channel
    parameters:
      - name: name
        in: path
        required: true
        type: string
    responses:
      200:
        description: Config du canal
        schema:
          $ref: '#/definitions/Channel'
    """
    pass

@app.route('/channel/<name>/invite', methods=['POST'])
def invite_user(name):
    """
    Inviter un utilisateur dans un canal
    ---
    tags:
      - Channel
    parameters:
      - name: name
        in: path
        type: string
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [pseudo]
          properties:
            pseudo:
              type: string
          example:
            pseudo: "roger"
    responses:
      200:
        description: Utilisateur invité
      403:
        description: Non autorisé
    """
    pass

@app.route('/channel/<name>/ban', methods=['POST'])
def ban_user(name):
    """
    Bannir un utilisateur d’un canal
    ---
    tags:
      - Channel
    parameters:
      - name: name
        in: path
        type: string
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [pseudo, reason]
          properties:
            pseudo:
              type: string
            reason:
              type: string
          example:
            pseudo: "spammer"
            reason: "Spam excessif"
    responses:
      200:
        description: Utilisateur banni
      403:
        description: Non autorisé
    """
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')