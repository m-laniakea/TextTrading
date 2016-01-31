import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '124a95b6f97d7181939acacac2950c4b3b014ef6590d362737696fe2e8b2971211aeec99ee6e678170aabc24f404f6d1e73fab4f06ef88b393f318178e'

    @staticmethod
    def init_app(app):
        pass

class devConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

cfg = {
        'development' : devConfig,

        'default' : devConfig
}
