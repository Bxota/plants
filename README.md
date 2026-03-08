# Mes Plantes

Application web personnelle pour gérer son herbier. Upload une photo → l'IA identifie la plante et remplit les conseils de soin automatiquement.

## Stack

- **Backend** : Python FastAPI + PostgreSQL
- **Frontend** : Vue.js 3 + Vite
- **IA** : Claude Vision (Anthropic)
- **Déploiement** : Docker Compose

## Démarrage rapide

### 1. Configurer l'environnement

```bash
cp .env.example .env
```

Éditer `.env` :

- `DB_PASSWORD` : mot de passe PostgreSQL
- `SECRET_KEY` : clé JWT (`openssl rand -hex 32`)
- `APP_USERNAME` : ton identifiant
- `APP_PASSWORD_HASH` : hash bcrypt de ton mot de passe
- `ANTHROPIC_API_KEY` : clé API Anthropic

**Générer le hash du mot de passe :**
```bash
python3 -c "from passlib.context import CryptContext; print(CryptContext(schemes=['bcrypt']).hash('TON_MOT_DE_PASSE'))"
```

### 2. Lancer l'app

```bash
docker compose up --build
```

Accessible sur [http://localhost:3000](http://localhost:3000)

### 3. Développement local (sans Docker)

**Backend :**
```bash
cd backend
pip install -r requirements.txt
# Créer un .env dans backend/ avec les variables
uvicorn app.main:app --reload
```

**Frontend :**
```bash
cd frontend
npm install
npm run dev
```

## Fonctionnalités

- **Identification par photo** : glisser une photo → Claude identifie la plante et pré-remplit tous les champs
- **CRUD complet** : ajouter, modifier, supprimer des plantes
- **Accès protégé** : login JWT single-user
- **Design fidèle** à l'herbier original

## Déploiement VPS

1. Cloner le repo sur le VPS
2. Créer le `.env` avec les vraies valeurs
3. `docker compose up -d --build`
4. Configurer un reverse proxy (Caddy/Nginx) pour HTTPS
