from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/ping')
    def ping():
        return {
            'message': 'pong',
            'status': 200
        }

    @app.route('/health')
    def healthcheck():
        return {
            'message': 'healthy',
            'status': 200
        }

    @app.route('/version')
    def version():
        return {
            'version': '0.0.1',
            'status': 200
        }

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
