import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL = 'project3-db-server.postgres.database.azure.com'  #TODO: Update value
    POSTGRES_USER = 'azureadmin@project3-db-server' #TODO: Update value
    POSTGRES_PW = 'admin12345@'   #TODO: Update value
    POSTGRES_DB = 'techconfdb'   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING = 'Endpoint=sb://project3-services-bus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=y0ANkl+4dO18re0/AjLBfx3ExwmhNCWDh+ASbGV6YWs=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'minhhieudn98@gmail.com'
    SENDGRID_API_KEY = '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' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False