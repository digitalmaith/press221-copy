# PRESS 221 — API de Gestion de Pressing

API REST professionnelle construite avec **FastAPI**, **PostgreSQL** et **SQLAlchemy (ORM)**.

---

## 🏗️ Architecture du projet

```
press221/
├── main.py                        # Point d'entrée FastAPI
├── requirements.txt
├── .env.example                   # Variables d'environnement
├── Dockerfile
├── docker-compose.yml
├── alembic.ini                    # Config migrations
├── alembic/
│   ├── env.py
│   └── versions/                  # Fichiers de migration générés
└── app/
    ├── core/
    │   └── config.py              # Settings (Pydantic)
    ├── db/
    │   └── session.py             # Engine + SessionLocal + get_db
    ├── models/                    # Modèles SQLAlchemy (POO)
    │   ├── employe.py
    │   ├── client.py
    │   ├── type_service.py
    │   └── depot.py
    ├── schemas/                   # Schémas Pydantic (validation)
    │   ├── employe.py
    │   ├── client.py
    │   ├── type_service.py
    │   └── depot.py
    ├── services/                  # Logique métier (POO)
    │   ├── employe_service.py
    │   ├── client_service.py
    │   ├── type_service_service.py
    │   └── depot_service.py
    └── api/v1/
        ├── router.py              # Agrégateur des routes
        └── endpoints/             # Contrôleurs REST
            ├── employes.py
            ├── clients.py
            ├── services.py
            └── depots.py
```

---

## 🚀 Démarrage rapide

### Option 1 — Docker Compose (recommandé)

```bash
docker-compose up --build
```

L'API sera disponible sur : http://localhost:8000

### Option 2 — Local

**1. Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

**2. Installer les dépendances**
```bash
pip install -r requirements.txt
```

**3. Configurer l'environnement**
```bash
cp .env.example .env
# Modifier DATABASE_URL selon votre config PostgreSQL
```

**4. Lancer PostgreSQL et créer la base**
```sql
CREATE DATABASE press221;
```

**5. Lancer les migrations (optionnel si create_all est activé)**
```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

**6. Démarrer l'API**
```bash
uvicorn main:app --reload
```

---

## 📖 Documentation Swagger

- Swagger UI : http://localhost:8000/docs
- ReDoc      : http://localhost:8000/redoc

---

## 📡 Endpoints disponibles

### Employés — `/api/v1/employes`
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/` | Lister tous les employés |
| GET | `/{id}` | Obtenir un employé |
| POST | `/` | Créer un employé |
| PUT | `/{id}` | Modifier un employé |
| DELETE | `/{id}` | Supprimer (si aucun dépôt en cours) |

### Clients — `/api/v1/clients`
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/` | Lister tous les clients |
| GET | `/{id}` | Obtenir un client |
| POST | `/` | Créer un client |
| PUT | `/{id}` | Modifier un client |
| DELETE | `/{id}` | Supprimer (si aucun dépôt non retiré) |

### Types de service — `/api/v1/services`
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/` | Lister tous les services |
| GET | `/{id}` | Obtenir un service |
| POST | `/` | Créer un service |
| PUT | `/{id}` | Modifier un service |
| DELETE | `/{id}` | Supprimer (si aucun dépôt lié) |

### Dépôts — `/api/v1/depots`
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/` | Lister tous les dépôts |
| GET | `/{id}` | Obtenir un dépôt |
| POST | `/` | Enregistrer un dépôt |
| PATCH | `/{id}/statut` | Mettre à jour le statut |

---

## 🔒 Règles métier appliquées

- Email unique pour employés et clients
- Poste obligatoire : `repasseur`, `nettoyeur`, `accueil`
- Code unique pour les types de service
- Prix > 0 et délai > 0 pour les services
- `dateDepot` ≤ aujourd'hui
- `dateRetraitPrevue` = `dateDepot` + délai du service (en heures)
- Statut initial d'un dépôt : `DEPOSE`
- Suppression bloquée si contraintes d'intégrité métier non respectées
