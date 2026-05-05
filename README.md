# Mes Plantes

Application web personnelle pour gérer un herbier : upload d'une photo, identification (IA) et conseils de soin.

**Stack**
- Backend : Python + FastAPI
- Base de données : PostgreSQL
- Frontend : Vue 3 + Vite
- IA : Anthropic (Claude Vision)
- Conteneurisation : Docker / Docker Compose

**Objectif**
Permettre la gestion simple de plantes (CRUD), l'upload de photos et l'aide à l'identification/entretien via IA.

## Prérequis
- Git
- Docker & Docker Compose
- Python 3.10+ (pour le dev backend local)
- Node 16+ / npm (pour le dev frontend local)

## Démarrage rapide (Docker)

1. Copier l'exemple d'environnement :

```bash
cp .env.example .env
```

2. Éditer `.env` et renseigner au minimum :

- DB_PASSWORD : mot de passe PostgreSQL
- SECRET_KEY : clé secrète pour JWT (ex: `openssl rand -hex 32`)
- APP_USERNAME / APP_PASSWORD_HASH : compte admin initial (voir backend/ pour détails)
- ANTHROPIC_API_KEY : clé API pour l'IA

3. Lancer les services :

```bash
docker compose up --build
```

Cette commande lance la stack de développement avec hot reload côté backend et frontend.
L'application frontend est accessible sur http://localhost:3000 par défaut.

Pour l'image de production, utiliser :

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

## Développement local (sans Docker)

Backend :

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Ajuster backend/.env puis
uvicorn app.main:app --reload --port 8000
```

Frontend :

```bash
cd frontend
npm install
npm run dev
```

## Base de données & migrations
- Les scripts SQL initiaux se trouvent dans le dossier `backend/migrations/`.
- En Docker, la migration initiale est appliquée via l'image/postgres et les scripts d'init.

## Variables d'environnement importantes
- `DB_PASSWORD`, `DATABASE_URL` (si utilisée)
- `SECRET_KEY` (JWT)
- `ANTHROPIC_API_KEY` (API IA)

Consultez `backend/config.py` pour la liste complète et les valeurs attendues.

## Tests
- Aucun jeu de tests automatisés n'est inclus actuellement. Ajouter `pytest` côté backend est recommandé.

## Contribution
- Ouvrir une issue pour discuter des grosses modifications.
- Faire une branche par feature et proposer une merge request.

## Fichiers utiles
- Backend : [backend](backend)
- Frontend : [frontend](frontend)

## Déploiement
Utiliser `docker compose -f docker-compose.prod.yml up -d --build` et configurer un reverse-proxy (Nginx/Caddy) pour HTTPS.

---
Si tu veux, je peux :
- ajouter une section « Variables d'environnement détaillées » avec un exemple `.env.example` mis à jour,
- ou créer un guide de déploiement plus complet pour un VPS.
