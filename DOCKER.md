# 🐳 Docker - Agent Administratif

## 1. Construire l'image

Depuis le dossier `agent2` :

```bash
docker build -t agent_administratif .
```

## 2. Lancer uniquement l'API (sans PostgreSQL)

```bash
docker run --rm -p 8000:8000 --env-file .env agent_administratif
```

Puis ouvre dans ton navigateur :
- `http://localhost:8000/docs`

## 3. Lancer l'API + PostgreSQL avec docker-compose

```bash
docker-compose up --build
```

Cela démarre :
- `api` sur `http://localhost:8000`
- `db` PostgreSQL sur le port `5432`

Assure-toi que ta variable `DATABASE_URL` dans `.env` correspond bien à :

```env
DATABASE_URL=postgresql://agent_user:agent_password@db:5432/agent_administratif
```

## 4. Arrêter les conteneurs

```bash
docker-compose down
```

## 5. Résumé rapide

- Dockerfile : image Python + installation des dépendances + lancement de `mcp_server.py`
- docker-compose.yml : API FastAPI + PostgreSQL
- `.dockerignore` : évite d'envoyer les gros fichiers/documents dans l'image


