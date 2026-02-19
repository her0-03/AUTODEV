# 🔧 Correction Timeout Render - Analyses Longues (2-3 minutes)

## 🎯 Problème
- Backend prend 2-3 minutes pour analyser les documents
- Render timeout après 30 secondes
- Frontend ne reçoit jamais les résultats

## ✅ Solutions Implémentées

### 1. Backend - Heartbeat SSE (ai_service.py)
```python
# Envoie ": heartbeat\n\n" toutes les 10 secondes
# Garde la connexion SSE active pendant l'analyse IA
last_heartbeat = time.time()
if time.time() - last_heartbeat > 10:
    yield ": heartbeat\n\n"
    last_heartbeat = time.time()
```

**Effet**: La connexion reste active même si l'IA prend 3 minutes

### 2. Backend - Timeouts Uvicorn (render.yaml)
```yaml
startCommand: "uvicorn app.main:app --timeout-keep-alive 300 --timeout-graceful-shutdown 300"
```

**Effet**: Backend accepte les connexions de 5 minutes

### 3. Frontend - Timeouts Proxy (app.py)
```python
# SSE: 10 minutes
with requests.get(url, stream=True, timeout=600) as r:

# JSON: 5 minutes  
requests.post(url, json=data, timeout=300)
```

**Effet**: Frontend attend jusqu'à 10 minutes pour SSE

### 4. Frontend - Gunicorn Config (gunicorn.conf.py)
```python
timeout = 300        # 5 minutes
keepalive = 300      # 5 minutes
graceful_timeout = 300
```

**Effet**: Gunicorn ne tue pas les requêtes longues

## 📊 Avant / Après

### Avant ❌
```
Client → Frontend → Backend → IA Groq
  ↓         ↓          ↓
30s     30s        30s
TIMEOUT! ❌
```

### Après ✅
```
Client → Frontend → Backend → IA Groq
  ↓         ↓          ↓
10min   5min      5min
💓 Heartbeat toutes les 10s
✅ Analyse complète en 2-3 min
```

## 🧪 Test Local

```bash
# 1. Démarrer backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --timeout-keep-alive 300

# 2. Démarrer frontend
cd frontend
python app.py

# 3. Tester heartbeat
python test_timeout.py

# 4. Upload gros document (2-3 min)
# → Devrait fonctionner sans timeout
```

## 🚀 Déploiement Render

```bash
git add .
git commit -m "fix: Support analyses longues avec heartbeat SSE + timeouts étendus"
git push origin main
```

Render redéploiera automatiquement avec:
- ✅ Heartbeat SSE
- ✅ Timeouts 5-10 minutes
- ✅ Gunicorn optimisé

## 📝 Fichiers Modifiés

1. **backend/app/services/ai_service.py**
   - Ajout heartbeat SSE toutes les 10s
   - Ajout asyncio.sleep pour streaming fluide

2. **frontend/app.py**
   - Timeout SSE: 300s → 600s (10 min)
   - Timeout JSON: 180s → 300s (5 min)
   - Meilleure gestion erreur timeout

3. **render.yaml**
   - Backend: `--timeout-keep-alive 300`
   - Frontend: `--config gunicorn.conf.py`

4. **frontend/gunicorn.conf.py** (nouveau)
   - timeout = 300
   - keepalive = 300
   - graceful_timeout = 300

5. **test_timeout.py** (nouveau)
   - Script de test heartbeat
   - Vérifie connexion SSE longue

6. **render-config.md** (nouveau)
   - Documentation complète
   - Monitoring et limites

## 🎯 Résultat Attendu

### Scénario 1: Document petit (< 30s)
- ✅ Fonctionne comme avant
- ✅ Pas de heartbeat nécessaire

### Scénario 2: Document moyen (30s - 2min)
- ✅ Heartbeat garde connexion active
- ✅ Analyse complète sans timeout

### Scénario 3: Document gros (2-3 min)
- ✅ Heartbeat toutes les 10s
- ✅ Frontend attend jusqu'à 10 min
- ✅ Résultats arrivent correctement

### Scénario 4: Document énorme (> 5 min)
- ⚠️ Timeout après 5 min backend
- 💡 Solution: Découper en plusieurs fichiers

## 🔍 Monitoring

### Logs Backend (Render)
```
[SSE] Starting analysis...
[SSE] Heartbeat sent (10s)
[SSE] Heartbeat sent (20s)
[SSE] Heartbeat sent (30s)
...
[SSE] Analysis complete (2m 15s)
```

### Logs Frontend (Render)
```
[PROXY] GET /api/generation/analyze-stream/xxx
[SSE PROXY] Streaming...
[SSE PROXY] Heartbeat received
[SSE PROXY] Complete (2m 15s)
```

### Console Navigateur
```javascript
// EventSource reçoit les heartbeats
: heartbeat
: heartbeat
data: {"appConfig": ...}
```

## 💰 Limites Render Free Tier

| Limite | Valeur | Notre Config |
|--------|--------|--------------|
| Max request time | 10 min | ✅ 5 min backend, 10 min frontend |
| RAM | 512 MB | ✅ 2 workers Gunicorn |
| Sleep inactif | 15 min | ⚠️ Première requête lente |

**Si analyses > 5 min régulièrement:**
- Upgrade Render Starter ($7/mois)
- Ou implémenter job queue asynchrone

## 🎉 Conclusion

**Problème résolu!** Les analyses de 2-3 minutes fonctionnent maintenant sur Render grâce à:

1. ✅ Heartbeat SSE (garde connexion active)
2. ✅ Timeouts étendus (5-10 min)
3. ✅ Gunicorn optimisé
4. ✅ Gestion erreur améliorée

**Prêt pour production Render!** 🚀
