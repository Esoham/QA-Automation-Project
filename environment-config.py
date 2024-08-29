import os

class Environment:
    @staticmethod
    def get_base_url():
        env = os.getenv('ENVIRONMENT', 'development')
        if env == 'production':
            return 'https://www.greengrocerapp.com'
        elif env == 'staging':
            return 'https://staging.greengrocerapp.com'
        else:
            return 'http://localhost:5000'

    @staticmethod
    def is_production():
        return os.getenv('ENVIRONMENT') == 'production'
