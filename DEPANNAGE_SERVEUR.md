# 🔧 Guide de Dépannage - Serveur MCP

## Problème : Le serveur ne répond pas à http://127.0.0.1:8000

### ✅ Solution 1 : Vérifier que le serveur démarre correctement

1. **Lancez le serveur avec le script de démarrage** :
```bash
cd agent2
python start_server.py
```

Ou manuellement :
```bash
uvicorn mcp_server:app --reload --host 127.0.0.1 --port 8000
```

2. **Vérifiez les messages dans le terminal** :
   - ✅ Vous devriez voir : `INFO:     Uvicorn running on http://127.0.0.1:8000`
   - ❌ Si vous voyez des erreurs, notez-les

### ✅ Solution 2 : Tester les endpoints

Une fois le serveur démarré, testez ces URLs dans votre navigateur :

1. **Endpoint racine** : http://127.0.0.1:8000
   - Devrait retourner : `{"status":"ok","message":"Serveur MCP Agent IA fonctionnel","agent_ready":true}`

2. **Endpoint de santé** : http://127.0.0.1:8000/health
   - Devrait retourner : `{"status":"healthy","agent_ready":true}`

3. **Documentation API** : http://127.0.0.1:8000/docs
   - Devrait afficher l'interface Swagger de FastAPI

### ✅ Solution 3 : Vérifier les erreurs courantes

#### Erreur : `ModuleNotFoundError: No module named 'fastapi'`

**Solution** : Installez les dépendances
```bash
pip install fastapi uvicorn
```

#### Erreur : `ModuleNotFoundError: No module named 'agent_core'`

**Solution** : Vérifiez que vous êtes dans le bon répertoire
```bash
cd agent2
python start_server.py
```

#### Erreur : `Port 8000 is already in use`

**Solution** : Changez le port
```bash
uvicorn mcp_server:app --reload --host 127.0.0.1 --port 8001
```

Puis mettez à jour l'URL dans le frontend (`src/services/api.js`) :
```javascript
const API_BASE_URL = 'http://localhost:8001';
```

#### Erreur : `agent_ready: false` dans la réponse

**Solution** : L'agent n'a pas pu s'initialiser. Vérifiez :
1. Les variables d'environnement sont définies :
   ```bash
   # Windows PowerShell
   $env:MISTRAL_API_KEY="votre_cle"
   $env:QDRANT_URL="votre_url"
   $env:QDRANT_API_KEY="votre_cle"
   ```

2. L'index RAG est créé :
   ```bash
   python qdrantindex.py
   ```

### ✅ Solution 4 : Vérifier les imports

Si vous avez des erreurs d'import, vérifiez que tous les fichiers existent :

- ✅ `agent_core.py` existe
- ✅ `tools.py` existe
- ✅ `loadindex.py` existe
- ✅ `models.py` existe
- ✅ `app.py` existe (pour l'import de `RagTool`)

### ✅ Solution 5 : Tester avec curl (optionnel)

Si vous avez `curl` installé, testez la connexion :

```bash
# Test endpoint racine
curl http://127.0.0.1:8000/

# Test endpoint de santé
curl http://127.0.0.1:8000/health

# Test endpoint chat (POST)
curl -X POST http://127.0.0.1:8000/mcp/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test123","message":"Bonjour"}'
```

### ✅ Solution 6 : Vérifier le firewall

Parfois Windows Firewall bloque les connexions. Vérifiez que le port 8000 n'est pas bloqué.

### 📝 Checklist de diagnostic

- [ ] Le serveur démarre sans erreur dans le terminal
- [ ] http://127.0.0.1:8000 retourne une réponse JSON
- [ ] http://127.0.0.1:8000/health retourne `{"status":"healthy","agent_ready":true}`
- [ ] http://127.0.0.1:8000/docs affiche la documentation Swagger
- [ ] Les variables d'environnement sont définies
- [ ] L'index RAG est créé dans Qdrant
- [ ] Le frontend utilise la bonne URL (http://localhost:8000)

### 🆘 Si rien ne fonctionne

1. **Vérifiez les logs du serveur** dans le terminal
2. **Ouvrez la console du navigateur** (F12) et regardez les erreurs
3. **Vérifiez que le serveur écoute bien** :
   ```bash
   # Windows
   netstat -an | findstr 8000
   
   # Linux/Mac
   netstat -an | grep 8000
   ```

Si le port 8000 n'apparaît pas, le serveur n'écoute pas correctement.

