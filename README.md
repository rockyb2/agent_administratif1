# Agent2 - Agent IA Assistant avec RAG

Un agent intelligent basé sur l'IA qui peut rechercher dans une base de connaissances, générer des documents (PDF, Word, Excel) et envoyer des emails via une interface conversationnelle intuitive.

## 📋 Description

Agent2 est un assistant IA puissant qui combine :
- **RAG (Retrieval-Augmented Generation)** : Recherche intelligente dans une base de documents vectorielle
- **Génération de documents** : Création automatique de fichiers PDF, Word et Excel professionnels
- **Envoi d'emails** : Support pour l'envoi d'emails avec pièces jointes
- **Interface web** : Interface Gradio pour une interaction conversationnelle fluide

## ✨ Fonctionnalités

- 🔍 **Recherche RAG** : Posez des questions sur votre base de documents et obtenez des réponses précises
- 📄 **Génération de documents Word** : Créez des documents Word formatés professionnellement
- 📊 **Génération de fichiers Excel** : Générez des tableaux Excel avec styles, formules et graphiques
- 📑 **Génération de PDF** : Créez des documents PDF avec mise en page professionnelle
- 📧 **Envoi d'emails** : Envoyez des emails avec support HTML et pièces jointes
- 🌐 **Recherche web** : Accès à DuckDuckGo pour des recherches en ligne
- 💾 **Historique des conversations** : Sauvegarde automatique de l'historique des interactions

## 🛠️ Technologies utilisées

- **Python** : Langage principal
- **smolagents** : Framework pour créer des agents IA
- **Mistral AI** : Modèle de langage (mistral-large-latest)
- **LlamaIndex** : Framework pour RAG et gestion de documents
- **Qdrant** : Base de données vectorielle pour le stockage des embeddings
- **Gradio** : Interface web interactive
- **python-docx** : Génération de documents Word
- **reportlab** : Génération de PDF
- **openpyxl** : Génération de fichiers Excel
- **smtplib** : Envoi d'emails

## 📦 Installation

### Prérequis

- Python 3.8 ou supérieur
- Compte Mistral AI avec clé API
- Instance Qdrant (cloud ou locale)

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/rockyb2/Agent2.git
cd Agent2
```

2. **Créer un environnement virtuel (recommandé)**
```bash
python -m venv venv
# Sur Windows
venv\Scripts\activate
# Sur Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install smolagents gradio python-docx reportlab openpyxl qdrant-client llama-index llama-index-vector-stores-qdrant llama-index-llms-mistralai llama-index-embeddings-huggingface
```

4. **Configurer les variables d'environnement**

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```env
MISTRAL_API_KEY=votre_cle_mistral
QDRANT_URL=votre_url_qdrant
QDRANT_API_KEY=votre_cle_qdrant
```

Ou exportez-les dans votre terminal :
```bash
# Sur Windows (PowerShell)
$env:MISTRAL_API_KEY="votre_cle_mistral"
$env:QDRANT_URL="votre_url_qdrant"
$env:QDRANT_API_KEY="votre_cle_qdrant"

# Sur Linux/Mac
export MISTRAL_API_KEY="votre_cle_mistral"
export QDRANT_URL="votre_url_qdrant"
export QDRANT_API_KEY="votre_cle_qdrant"
```

5. **Indexer les documents (première fois uniquement)**

Placez vos documents dans le dossier `bdc/` puis exécutez :

```bash
python qdrantindex.py
```

Cette étape crée l'index vectoriel dans Qdrant. Vous n'avez besoin de la faire qu'une seule fois (ou lorsque vous ajoutez de nouveaux documents).

## 🚀 Utilisation

### Lancer l'application

```bash
python app.py
```

L'interface Gradio s'ouvrira dans votre navigateur (généralement à l'adresse `http://127.0.0.1:7860`).

### Exemples d'utilisation

#### Recherche dans la base de connaissances
```
Posez une question : "Quels sont les projets prévus pour 2024 ?"
```

#### Générer un document Word
```
Créez un document Word nommé "rapport" avec le titre "Rapport mensuel" 
et le contenu "Voici le contenu du rapport..."
```

#### Générer un fichier Excel
```
Créez un fichier Excel nommé "budget" avec les colonnes ["Mois", "Revenus", "Dépenses"] 
et les données [["Janvier", 5000, 3000], ["Février", 5500, 3200]]
```

#### Générer un PDF
```
Créez un PDF nommé "presentation" avec le titre "Présentation" 
et le contenu "Voici le contenu de la présentation..."
```

#### Envoyer un email
```
Envoyez un email à exemple@email.com avec le sujet "Test" 
et le message "Bonjour, ceci est un test"
```

## 📁 Structure du projet

```
agent2/
├── app.py                 # Application principale avec interface Gradio
├── tools.py               # Outils de génération (Word, PDF, Excel, Email)
├── qdrantindex.py         # Script pour créer l'index vectoriel
├── loadindex.py           # Fonction pour charger l'index existant
├── history.json           # Historique des conversations (généré automatiquement)
├── bdc/                   # Dossier contenant les documents à indexer
│   ├── *.pdf
│   ├── *.docx
│   └── *.csv
└── README.md              # Ce fichier
```

## 🔧 Configuration

### Modèle de langage

Le projet utilise `mistral-large-latest` par défaut. Vous pouvez modifier le modèle dans `app.py` :

```python
model_id= "mistral/mistral-large-latest"
```

### Paramètres de l'agent

Dans `app.py`, vous pouvez ajuster :
- `max_steps` : Nombre maximum d'étapes que l'agent peut effectuer (défaut: 5)

### Collection Qdrant

Le nom de la collection par défaut est `rag_agent1`. Vous pouvez le modifier dans `qdrantindex.py` et `loadindex.py`.

## 📝 Notes importantes

- **Première utilisation** : N'oubliez pas d'exécuter `qdrantindex.py` pour créer l'index vectoriel avant d'utiliser l'application
- **Documents** : Placez tous vos documents à indexer dans le dossier `bdc/`
- **Historique** : L'historique des conversations est sauvegardé dans `history.json`
- **Fichiers générés** : Les fichiers créés (Word, PDF, Excel) sont sauvegardés dans le répertoire racine du projet

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir une issue pour signaler un bug ou proposer une amélioration
- Créer une pull request pour ajouter une fonctionnalité

## 📄 Licence

[Spécifiez votre licence ici]

## 👤 Auteur

[Votre nom]

## 🙏 Remerciements

- Mistral AI pour le modèle de langage
- L'équipe LlamaIndex pour le framework RAG
- L'équipe Qdrant pour la base de données vectorielle
- L'équipe Gradio pour l'interface utilisateur
