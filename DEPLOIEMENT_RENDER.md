# 🚀 Guide de Déploiement sur Render

Ce guide vous explique comment déployer votre agent IA sur Render.

## 📋 Prérequis

1. Un compte Render (gratuit) : https://render.com
2. Un compte Qdrant Cloud (pour la base vectorielle)
3. Une clé API Mistral AI
4. Votre code dans un repository Git (GitHub, GitLab, ou Bitbucket)

## 🔧 Étapes de Déploiement

### 1. Préparer le Repository

Assurez-vous que votre repository contient :
- ✅ `requirements.txt` (dépendances Python)
- ✅ `mcp_server.py` (fichier principal du serveur)
- ✅ Tous les fichiers nécessaires (`agent_core.py`, `tools.py`, `loadindex.py`, etc.)
- ✅ `render.yaml` (configuration optionnelle)

### 2. Créer un Nouveau Service Web sur Render

1. **Connectez-vous à Render** : https://dashboard.render.com
2. Cliquez sur **"New +"** → **"Web Service"**
3. Connectez votre repository Git
4. Sélectionnez le repository contenant votre code

### 3. Configurer le Service

#### Configuration de Base

- **Name** : `agent-administratif` (ou le nom de votre choix)
- **Environment** : `Python 3`
- **Region** : Choisissez la région la plus proche
- **Branch** : `main` (ou votre branche principale)
- **Root Directory** : Laissez vide (ou `agent2` si votre code est dans un sous-dossier)
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `uvicorn mcp_server:app --host 0.0.0.0 --port $PORT`

#### Variables d'Environnement

Ajoutez les variables d'environnement suivantes dans l'onglet **"Environment"** :

```
MISTRAL_API_KEY=votre_cle_mistral_ici
QDRANT_URL=https://votre-cluster.qdrant.io
QDRANT_API_KEY=votre_cle_qdrant_ici
DATABASE_URL=postgresql://user:password@host:port/database
```

**Note** : Pour `DATABASE_URL`, vous pouvez :
- Créer une base PostgreSQL sur Render (gratuite)
- Ou utiliser une base externe

### 4. Créer la Base de Données PostgreSQL (Optionnel)

Si vous utilisez une base de données :

1. Dans Render Dashboard, cliquez sur **"New +"** → **"PostgreSQL"**
2. Configurez :
   - **Name** : `agent-db`
   - **Database** : `agent_administratif`
   - **User** : `agent_user`
   - **Plan** : `Free` (pour commencer)
3. Une fois créée, copiez la **"Internal Database URL"**
4. Ajoutez-la comme variable d'environnement `DATABASE_URL` dans votre service web

### 5. Déployer

1. Cliquez sur **"Create Web Service"**
2. Render va automatiquement :
   - Cloner votre repository
   - Installer les dépendances
   - Démarrer votre application
3. Attendez que le déploiement se termine (2-5 minutes)

### 6. Vérifier le Déploiement

Une fois déployé, vous obtiendrez une URL comme : `https://agent-administratif.onrender.com`

Testez les endpoints :
- **Racine** : `https://votre-url.onrender.com/`
- **Santé** : `https://votre-url.onrender.com/health`
- **Documentation** : `https://votre-url.onrender.com/docs`

## 🔒 Configuration CORS pour Production

Mettez à jour `mcp_server.py` pour autoriser votre domaine frontend :

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Développement local
        "https://votre-frontend.vercel.app",  # Votre frontend en production
        "https://votre-frontend.netlify.app",  # Ou autre
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📝 Notes Importantes

### Index RAG

⚠️ **Important** : L'index RAG doit être créé **avant** le déploiement ou lors du premier démarrage.

Options :
1. **Créer l'index localement** et s'assurer qu'il est dans Qdrant
2. **Ajouter un script de build** qui crée l'index au démarrage (peut ralentir le démarrage)

### Fichiers Générés

Les fichiers générés (Word, PDF, Excel) seront stockés dans le système de fichiers temporaire de Render. Pour la production, considérez :
- Utiliser un service de stockage (S3, Cloudinary, etc.)
- Ou retourner les fichiers en base64 dans la réponse

### Timeout Render

Les requêtes sur le plan gratuit ont un timeout de 30 secondes. Si votre agent prend plus de temps, considérez :
- Passer au plan payant
- Optimiser le temps de réponse de l'agent
- Utiliser des tâches asynchrones

## 🐛 Dépannage

### Le service ne démarre pas

1. Vérifiez les **logs** dans Render Dashboard
2. Vérifiez que toutes les variables d'environnement sont définies
3. Vérifiez que `requirements.txt` contient toutes les dépendances

### Erreur "Module not found"

Ajoutez le module manquant dans `requirements.txt` et redéployez.

### Erreur de connexion à Qdrant

1. Vérifiez que `QDRANT_URL` et `QDRANT_API_KEY` sont corrects
2. Vérifiez que votre cluster Qdrant est accessible depuis Render
3. Vérifiez les règles de firewall de Qdrant

### Erreur de connexion à la base de données

1. Vérifiez que `DATABASE_URL` est correct
2. Si vous utilisez une base Render, utilisez l'**"Internal Database URL"** (pas l'externe)
3. Vérifiez que la base est bien créée et accessible

## 🔄 Mise à Jour

Pour mettre à jour votre application :

1. Poussez vos changements sur votre repository Git
2. Render détectera automatiquement les changements
3. Un nouveau déploiement sera lancé automatiquement

Ou manuellement :
1. Dans Render Dashboard, cliquez sur **"Manual Deploy"**
2. Sélectionnez la branche et le commit

## 📊 Monitoring

Render fournit des logs en temps réel :
- Accédez aux **"Logs"** dans votre service
- Surveillez les erreurs et les performances

## 💰 Coûts

- **Plan Gratuit** : 
  - Service web gratuit (peut s'endormir après 15 min d'inactivité)
  - Base PostgreSQL gratuite (90 jours)
  - 750 heures/mois

- **Plan Starter** ($7/mois) :
  - Service toujours actif
  - Pas de timeout
  - Plus de ressources

## 🎯 Prochaines Étapes

1. ✅ Déployez votre service
2. ✅ Testez les endpoints
3. ✅ Configurez votre frontend pour utiliser l'URL de production
4. ✅ Configurez un domaine personnalisé (optionnel)
5. ✅ Configurez les alertes et monitoring

## 📞 Support

- Documentation Render : https://render.com/docs
- Support Render : support@render.com
- Community : https://community.render.com

