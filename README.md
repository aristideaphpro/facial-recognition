# Système de Reconnaissance Faciale

Système de reconnaissance faciale en temps réel développé en Python. 
Il identifie et authentifie des visages connus à partir d'un flux vidéo webcam, 
accessible via un navigateur web.

## Fonctionnalités

- Détection de visages en temps réel via webcam
- Identification des personnes connues avec affichage du nom
- Affichage "Inconnu" pour les personnes non enregistrées
- Interface accessible depuis n'importe quel navigateur web

## Technologies utilisées

- Python 3.11
- face_recognition — encodage et comparaison de visages
- OpenCV — capture et traitement vidéo
- Flask — serveur web pour le flux vidéo

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/aristideaphpro/facial-recognition.git
cd facial-recognition
```

2. Créer et activer l'environnement virtuel :
```bash
python3.11 -m venv venv
source venv/bin/activate
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Créer le dossier `visages_connus/` à la racine du projet :
```bash
mkdir visages_connus
```

5. Ajouter des photos dans un dossier nommé `visages_connus/` :
- Une photo par personne
- Nommer chaque photo avec le prénom de la personne (ex: `aristide.jpg`)

## Utilisation

1. Lancer le serveur :
```bash
python3 main.py
```

2. Ouvrir un navigateur et aller sur :
http://127.0.0.1:5001

3. Le système charge automatiquement les visages connus et démarre la reconnaissance en temps réel.

## Structure du projet

```
facial-recognition/
├── main.py              # Code principal
├── requirements.txt     # Dépendances Python
├── README.md            # Documentation
└── visages_connus/      # À créer manuellement — photos des personnes à reconnaître
```

## Auteur

Aristide Portal-Hadancourt