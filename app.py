from flask import Flask
from config import Config
from models import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

from routes import main

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
