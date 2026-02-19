# Configuration Render pour Longues Analyses

## Problème Résolu
- ❌ Timeout après 30 secondes sur Render
- ✅ Support analyses de 2-3 minutes avec SSE

## Solutions Implémentées

### 1. Timeouts Uvicorn (Backend)
```bash
uvicorn app.main:app --timeout-keep-alive 300 --timeout-graceful-shutdown 300
```
- Keep-alive: 5 minutes
- Graceful shutdown: 5 minutes

### 2. Timeouts Frontend
- SSE: 600 secondes (10 minutes)
- JSON: 300 secondes (5 minutes)
- Form/Files: 180 secondes (3 minutes)

### 3. Heartbeat SSE
- Envoie `: heartbeat\n\n` toutes les 10 secondes
- Garde la connexion active pendant l'analyse IA
- Évite les timeouts proxy Render

### 4. Configuration Render
```yaml
services:
  - type: web
    name: autodev-backend
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 300 --timeout-graceful-shutdown 300"
```

## Test Local

```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --timeout-keep-alive 300

# Terminal 2 - Frontend
cd frontend
python app.py

# Test avec gros document (2-3 minutes)
# La connexion SSE reste active grâce au heartbeat
```

## Déploiement Render

```bash
git add .
git commit -m "fix: Support analyses longues avec heartbeat SSE"
git push origin main
```

Render redéploiera automatiquement avec les nouveaux timeouts.

## Monitoring

### Logs Backend
```
[SSE] Heartbeat sent (10s)
[SSE] Heartbeat sent (20s)
[SSE] Analysis complete (2m 15s)
```

### Logs Frontend
```
[SSE PROXY] Streaming...
[SSE PROXY] Heartbeat received
[SSE PROXY] Complete
```

## Limites Render Free Tier

- ⏱️ Max request: 10 minutes (on a 5 min)
- 💾 RAM: 512 MB
- 🔄 Sleep après 15 min inactivité

Si analyses > 5 minutes → Upgrade Render Starter ($7/mois)

## Alternative: Analyse Asynchrone

Si problèmes persistent, implémenter:

1. **Job Queue** (Celery + Redis)
   - Upload → Crée job → Retourne job_id
   - Frontend poll `/api/job/{id}/status` toutes les 5s
   - Pas de timeout SSE

2. **WebSocket** (au lieu de SSE)
   - Connexion bidirectionnelle
   - Meilleure gestion reconnexion

3. **Chunking Documents**
   - Analyser par morceaux de 500 KB
   - Combiner résultats
   - Chaque chunk < 30s

## Vérification

✅ Heartbeat SSE toutes les 10s
✅ Timeout backend 5 min
✅ Timeout frontend 10 min
✅ Gestion erreur timeout explicite
✅ Logs détaillés

**Status: Prêt pour production Render**
