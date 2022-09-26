from flask import Flask
from auth.api.auth import auth_blueprint

# 工厂方法
def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()

    app.run(host='0.0.0.0', port=5050)