# 🔧 Guide de Maintenance & Évolution - AutoDev

## 📋 Table des Matières
1. [Maintenance Quotidienne](#maintenance-quotidienne)
2. [Monitoring & Alertes](#monitoring--alertes)
3. [Débogage](#débogage)
4. [Ajout de Fonctionnalités](#ajout-de-fonctionnalités)
5. [Optimisations](#optimisations)
6. [Sécurité](#sécurité)
7. [Backup & Recovery](#backup--recovery)

---

## 🔄 Maintenance Quotidienne

### Checklist Matinale (5 min)
```bash
# 1. Vérifier le statut des services
curl https://autodev-backend.onrender.com/health
curl https://autodev-frontend.onrender.com/

# 2. Vérifier les logs (dernières 24h)
# Render Dashboard → Logs → Filter by ERROR

# 3. Vérifier les métriques
# - Temps de réponse API
# - Taux d'erreur
# - Nombre d'utilisateurs actifs
```

### Checklist Hebdomadaire (30 min)
- [ ] Analyser les logs d'erreur
- [ ] Vérifier l'espace disque
- [ ] Mettre à jour les dépendances
- [ ] Vérifier les backups
- [ ] Tester les fonctionnalités critiques

### Checklist Mensuelle (2h)
- [ ] Audit de sécurité
- [ ] Optimisation base de données
- [ ] Nettoyage fichiers temporaires
- [ ] Mise à jour documentation
- [ ] Review des performances

---

## 📊 Monitoring & Alertes

### Métriques Clés à Surveiller

#### 1. Performance
```python
# backend/app/middleware/monitoring.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Métriques
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
active_users = Gauge('active_users', 'Number of active users')

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    request_duration.observe(duration)
    
    return response
```

#### 2. Alertes Email
```python
# backend/app/utils/alerts.py
import smtplib
from email.mime.text import MIMEText

def send_alert(subject: str, message: str):
    """Envoyer une alerte par email"""
    msg = MIMEText(message)
    msg['Subject'] = f"[AutoDev Alert] {subject}"
    msg['From'] = "alerts@autodev.com"
    msg['To'] = "admin@autodev.com"
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASS'))
        server.send_message(msg)

# Utilisation
if error_rate > 5:
    send_alert("High Error Rate", f"Error rate: {error_rate}%")
```

#### 3. Dashboard Grafana
```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## 🐛 Débogage

### Logs Structurés
```python
# backend/app/utils/logger.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# Configuration
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("autodev")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Utilisation
logger.info("User logged in", extra={"user_id": user.id})
logger.error("Generation failed", extra={"job_id": job_id, "error": str(e)})
```

### Debug Mode
```python
# backend/main.py
if os.getenv("DEBUG") == "true":
    app.add_middleware(
        DebugMiddleware,
        show_error_details=True,
        show_sql_queries=True
    )
```

### Profiling
```python
# backend/app/utils/profiler.py
import cProfile
import pstats
from functools import wraps

def profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(20)
        
        return result
    return wrapper

# Utilisation
@profile
def generate_project(spec: dict):
    # Code à profiler
    pass
```

---

## ➕ Ajout de Fonctionnalités

### Template: Nouvelle Feature

#### 1. Backend Endpoint
```python
# backend/app/api/new_feature.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.user import User
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/new-feature", tags=["new-feature"])

@router.post("/")
async def create_feature(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new feature
    
    - **data**: Feature data
    """
    # Business logic
    result = process_feature(data)
    return {"status": "success", "data": result}

# Enregistrer le router
# backend/main.py
from app.api import new_feature
app.include_router(new_feature.router)
```

#### 2. Frontend Template
```html
<!-- frontend/templates/new_feature.html -->
{% extends "base.html" %}

{% block content %}
<div class="container mx-auto px-6 py-8">
    <h1 class="text-3xl font-bold mb-6">Nouvelle Fonctionnalité</h1>
    
    <form onsubmit="submitFeature(event)">
        <input type="text" id="featureInput" class="border p-2 rounded">
        <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">
            Soumettre
        </button>
    </form>
    
    <div id="result"></div>
</div>

<script>
async function submitFeature(e) {
    e.preventDefault();
    const data = { value: document.getElementById('featureInput').value };
    
    const response = await fetch('/api/new-feature/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(data)
    });
    
    const result = await response.json();
    document.getElementById('result').textContent = JSON.stringify(result);
}
</script>
{% endblock %}
```

#### 3. Tests
```python
# backend/tests/test_new_feature.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_feature():
    response = client.post(
        "/api/v1/new-feature/",
        json={"value": "test"},
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_create_feature_unauthorized():
    response = client.post("/api/v1/new-feature/", json={"value": "test"})
    assert response.status_code == 401
```

#### 4. Documentation
```python
# backend/app/api/new_feature.py
@router.post("/", response_model=FeatureResponse)
async def create_feature(
    data: FeatureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new feature
    
    ## Request Body
    - **value** (string, required): Feature value
    - **options** (object, optional): Additional options
    
    ## Response
    - **status** (string): Operation status
    - **data** (object): Created feature data
    
    ## Errors
    - **400**: Invalid input
    - **401**: Unauthorized
    - **500**: Server error
    
    ## Example
    ```json
    {
        "value": "example",
        "options": {"enabled": true}
    }
    ```
    """
    pass
```

---

## ⚡ Optimisations

### 1. Database Query Optimization
```python
# Avant (N+1 queries)
projects = db.query(Project).all()
for project in projects:
    print(project.user.email)  # Query pour chaque projet

# Après (1 query)
projects = db.query(Project).options(
    joinedload(Project.user)
).all()
for project in projects:
    print(project.user.email)  # Pas de query supplémentaire
```

### 2. Caching
```python
# backend/app/utils/cache.py
from functools import lru_cache
from typing import Optional
import redis

# Redis cache
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(ttl: int = 3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Check cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            redis_client.setex(cache_key, ttl, json.dumps(result))
            
            return result
        return wrapper
    return decorator

# Utilisation
@cache_result(ttl=3600)
def get_expensive_data(user_id: str):
    # Opération coûteuse
    return expensive_operation(user_id)
```

### 3. Async Processing
```python
# backend/app/tasks/celery_app.py
from celery import Celery

celery_app = Celery(
    'autodev',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def generate_project_async(job_id: str):
    """Génération asynchrone"""
    generator = CodeGenerator()
    result = generator.generate(job_id)
    return result

# Utilisation
from app.tasks.celery_app import generate_project_async

@router.post("/generate")
def generate_code(job_id: str):
    # Lancer la tâche en arrière-plan
    task = generate_project_async.delay(job_id)
    return {"task_id": task.id, "status": "processing"}
```

### 4. Frontend Optimization
```javascript
// Lazy loading images
<img src="placeholder.jpg" data-src="real-image.jpg" class="lazy">

<script>
document.addEventListener("DOMContentLoaded", function() {
    const lazyImages = document.querySelectorAll('.lazy');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
});
</script>
```

---

## 🔒 Sécurité

### 1. Audit de Sécurité
```bash
# Scan des dépendances
pip install safety
safety check

# Scan du code
pip install bandit
bandit -r backend/

# Scan des secrets
pip install detect-secrets
detect-secrets scan > .secrets.baseline
```

### 2. Rate Limiting Avancé
```python
# backend/app/middleware/rate_limit.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/hour"]
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Par endpoint
@app.post("/api/v1/generation/job")
@limiter.limit("10/minute")
async def create_job(request: Request):
    pass
```

### 3. Input Sanitization
```python
# backend/app/utils/sanitize.py
import bleach
from html import escape

def sanitize_html(text: str) -> str:
    """Nettoyer le HTML"""
    allowed_tags = ['p', 'br', 'strong', 'em']
    return bleach.clean(text, tags=allowed_tags, strip=True)

def sanitize_sql(text: str) -> str:
    """Échapper les caractères SQL"""
    return text.replace("'", "''").replace(";", "")

def sanitize_filename(filename: str) -> str:
    """Nettoyer les noms de fichiers"""
    return "".join(c for c in filename if c.isalnum() or c in "._- ")
```

---

## 💾 Backup & Recovery

### 1. Backup Automatique
```bash
#!/bin/bash
# scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup database
pg_dump $DATABASE_URL > "$BACKUP_DIR/db_$DATE.sql"

# Backup files
tar -czf "$BACKUP_DIR/files_$DATE.tar.gz" /tmp/generated_projects

# Upload to S3
aws s3 cp "$BACKUP_DIR/db_$DATE.sql" s3://autodev-backups/
aws s3 cp "$BACKUP_DIR/files_$DATE.tar.gz" s3://autodev-backups/

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -mtime +30 -delete

echo "Backup completed: $DATE"
```

### 2. Cron Job
```bash
# Ajouter au crontab
crontab -e

# Backup quotidien à 2h du matin
0 2 * * * /path/to/scripts/backup.sh >> /var/log/backup.log 2>&1
```

### 3. Recovery
```bash
#!/bin/bash
# scripts/restore.sh

BACKUP_FILE=$1

# Restore database
psql $DATABASE_URL < $BACKUP_FILE

# Restore files
tar -xzf files_backup.tar.gz -C /tmp/generated_projects

echo "Restore completed"
```

---

## 📚 Ressources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Flask Docs](https://flask.palletsprojects.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Render Docs](https://render.com/docs)

### Outils
- [Postman](https://www.postman.com/) - Test API
- [pgAdmin](https://www.pgadmin.org/) - Database management
- [Sentry](https://sentry.io/) - Error tracking
- [New Relic](https://newrelic.com/) - APM

### Support
- 📧 Email: dev@autodev.com
- 💬 Slack: #autodev-dev
- 📚 Wiki: wiki.autodev.com

---

**Dernière mise à jour**: 2025-01-XX  
**Version**: 1.0.0  
**Mainteneur**: Équipe DevOps AutoDev
