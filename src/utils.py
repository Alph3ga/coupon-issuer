import mongoengine

from src.settings import DB_URI


def dbSetup():
    assert DB_URI
    mongoengine.connect(host=DB_URI, db="test")
