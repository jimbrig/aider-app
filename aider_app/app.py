from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/ping')
    def ping():
        return 'success', 200

    @app.route('/healthcheck')
    def healthcheck():
        return 'healthy', 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
