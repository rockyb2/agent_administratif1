from sqlalchemy import create_engine
import os
# Remplacez 'user' par 'postgres' (ou votre vrai nom d'utilisateur)
DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)
conn = engine.connect()
print("Connexion réussie !")
conn.close()
