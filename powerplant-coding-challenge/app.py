from dotenv import load_dotenv
from flask import Flask

from api.routes import api_blueprint
from api.v1.routes import v1_blueprint

load_dotenv()

app = Flask(__name__)
app.register_blueprint(api_blueprint)
app.register_blueprint(v1_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
