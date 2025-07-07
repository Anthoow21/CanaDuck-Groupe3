from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db
from flasgger import Swagger
app = Flask(__name__)

swagger = Swagger(app, template_file='swagger.yml')

# app.config["SQLALCHEMY_DATABARE_URI"] = {
#     f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# }
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=5001)