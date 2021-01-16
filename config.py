#!/usr/bin/env python3
from os import environ, path
import os
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Set Flask Configuration variables"""
    FLASK_ENV = 'development'
    TESTING = True
    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database
    DATABASE="./yasmp.sqlite"
    # SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # TODO Add GCE/Aws Secrets depending on the ones we want to use
