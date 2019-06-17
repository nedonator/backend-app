import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'Mnw7LSSjVaX7HnMcetHBRBNU557vkjfH'
    SALT = 'wmUVQa68W984zwDZ5pQtUzq9'

    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    MAIL_USERNAME = 'alaska1732@mail.ru'
    MAIL_PASSWORD = 'Purchase1867'
