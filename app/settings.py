class Config(object):
    SECRET_KEY = "sslirfhoerondslknfmlksdnflknsdf"
    FACEBOOK_APP_ID = '291411834375925'
    FACEBOOK_APP_SECRET = 'da574af948206ecefeba35883c739447'
    debug = False


class Production(Config):
    debug = True
