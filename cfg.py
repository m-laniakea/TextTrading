##
# Standard configuration file
##

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    ##
    # Secret key used for cookies to validate user sessions
    ## Set SECRET_KEY environment variable before running on production 
    #
    # UNIX
    #  export SECRET_KEY="something long and random"
    #
    # WINDOWS
    #  set SECRET_KEY="something long and random"
    ##
    SECRET_KEY = os.getenv('SECRET_KEY') or '124a95b6f97d7181939acacac2950c4b3b014ef6590d362737696fe2e8b2971211aeec99ee6e678170aabc24f404f6d1e73fab4f06ef88b393f318178e'

    # Automatically commit on db action
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

    RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
    RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'


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
