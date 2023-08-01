from aider_app.extensions import db


def init_app_endpoints(app):

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

        @app.route('/config')
        def config():
            return {
                'config': app.config,
                'status': 200
            }

        @app.route('/config/<key>')
        def config_key(key):
            return {
                'config': app.config[key],
                'status': 200
            }
