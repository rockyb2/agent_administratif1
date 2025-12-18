from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

"""
Petit helper DB.
Pour l'instant on veut pouvoir démarrer l'agent SANS base de données.
Si DATABASE_URL n'est pas définie, on n'initialise pas d'engine
et les parties qui utilisent la DB devront être adaptées plus tard.
"""

engine = None
SessionLocal = None

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)


def get_db():
    """
    Générateur de session.
    Attention : lèvera une erreur claire si la DB n'est pas configurée.
    """
    if SessionLocal is None:
        raise RuntimeError("Base de données non configurée (DATABASE_URL manquant).")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()