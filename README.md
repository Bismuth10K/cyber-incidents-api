# cyber-incidents-api

Projet de développement d'une API REST en python sur la base du TP *cyber incidents*.

Projet commun entre bismuth10K et hakaroa-04.

# Comment le lancer chez vous

## Installation
```
git clone https://github.com/Bismuth10K/cyber-incidents-api/
cd cyber-incidents-api
```

## Création de la venv
```
cd src
python -m venv .venv
```

- Windows : 
```bash
.\.venv\Scripts\activate
```
- Linux : 
```bash
source .venv/bin/activate
```

## Installation des dépendances
```bash
pip install -r requirements.txt
```

## Lancement
Cette commande créé la base de données, la remplit, et lance le serveur.
```bash
py app.py
```

# Routes du serveur web
Voici une liste des routes les plus importantes, la console vous indiquera toutes les routes possibles.
- http://localhost:5000/agents
- http://localhost:5000/data/sources
- http://localhost:5000/data/targets
- http://localhost:5000/data/attackers
- http://localhost:5000/login/login
