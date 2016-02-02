##
# Standard configuration file
##

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key used for cookies to validate user sessions
    ## Don't use this on the production server
    #
    SECRET_KEY = '124a95b6f97d7181939acacac2950c4b3b014ef6590d362737696fe2e8b2971211aeec99ee6e678170aabc24f404f6d1e73fab4f06ef88b393f318178e'
    # Automatically commit on db action
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

##
# Define various configurations to load
# Depending on environment
##
class devConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class testConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')

##
# Production Configuration
##
class prodConfig(Config):
    SQL_ALCHEMY_DATABASE_URI = 'mysql://eir@somesqlserver.com/db'
    


cfg = {
        'dev'  : devConfig,
        'test' : testConfig,
        'prod' : prodConfig,

        'default' : devConfig
}
