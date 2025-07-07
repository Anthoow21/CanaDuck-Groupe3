from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db
from flasgger import Swagger
from functools import wraps
import jwt

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

# app.config["SQLALCHEMY_DATABARE_URI"] = {
#     f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# }
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db.init_app(app)

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

    payload = decode_jwt(token)
    return payload["pseudo"]


@app.route('/channel', methods=['POST'])
@require_role("admin")
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
    return "coucou"

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
    pass

@app.route('/channel/<name>', methods=['PATCH'])
@require_role("moderator")
@require_role("admin")
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
    pass

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
    pass

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