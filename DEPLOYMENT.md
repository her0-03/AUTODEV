# 🚀 Déploiement sur Render

## Méthode 1: Déploiement Automatique (Recommandé)

### 1. Préparer le Repository
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <votre-repo-github>
git push -u origin main
```

### 2. Déployer sur Render
1. Allez sur [render.com](https://render.com)
2. Connectez votre compte GitHub
3. Cliquez sur "New" → "Blueprint"
4. Sélectionnez votre repository
5. Render détectera automatiquement `render.yaml`
6. Cliquez sur "Apply"

### 3. Configurer les Variables d'Environnement
Dans le dashboard Render, ajoutez:

**Backend:**
- `GROQ_API_KEY`: Votre clé API Groq
- `DATABASE_URL`: (auto-généré si vous ajoutez une base PostgreSQL)

**Frontend:**
- Les autres variables sont auto-générées

### 4. Accéder à l'Application
- Backend: `https://autodev-backend.onrender.com`
- Frontend: `https://autodev-frontend.onrender.com`

---

## Méthode 2: Déploiement Manuel

### Backend

1. **Créer un Web Service**
   - Type: Web Service
   - Environment: Python 3
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Variables d'environnement:**
   ```
   DATABASE_URL=sqlite:///./dev.db
   JWT_SECRET=<générer-une-clé-secrète>
   GROQ_API_KEY=<votre-clé-groq>
   GENERATED_DIR=/tmp/generated_projects
   UPLOAD_DIR=/tmp/uploads
   ```

### Frontend

1. **Créer un Web Service**
   - Type: Web Service
   - Environment: Python 3
   - Build Command: `cd frontend && pip install -r requirements.txt`
   - Start Command: `cd frontend && gunicorn app:app --bind 0.0.0.0:$PORT`

2. **Variables d'environnement:**
   ```
   SECRET_KEY=<générer-une-clé-secrète>
   BACKEND_API_URL=https://autodev-backend.onrender.com
   ```

---

## 🔧 Configuration PostgreSQL (Optionnel)

Pour une base de données persistante:

1. Créez une base PostgreSQL sur Render
2. Copiez l'URL de connexion
3. Mettez à jour `DATABASE_URL` dans le backend
4. Ajoutez dans `backend/requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   ```

---

## 📝 Notes Importantes

### Plan Gratuit Render
- ✅ 750h/mois par service
- ✅ SSL automatique
- ⚠️ Les services s'endorment après 15min d'inactivité
- ⚠️ Premier démarrage peut prendre 30-60s

### Limitations
- `/tmp` est effacé au redémarrage
- Pas de stockage persistant sur le plan gratuit
- Pour les fichiers générés, utilisez un service comme AWS S3

### Optimisations
1. **Ajouter un fichier `.slugignore`** pour réduire la taille:
   ```
   *.pyc
   __pycache__/
   .git/
   .env
   ```

2. **Utiliser Redis pour le cache** (optionnel):
   - Ajoutez un service Redis sur Render
   - Configurez l'URL dans les variables d'environnement

---

## 🐛 Dépannage

### Service ne démarre pas
- Vérifiez les logs dans le dashboard Render
- Assurez-vous que toutes les variables d'environnement sont définies

### Erreur de connexion Backend/Frontend
- Vérifiez que `BACKEND_API_URL` pointe vers l'URL correcte du backend
- Utilisez HTTPS, pas HTTP

### Base de données
- SQLite fonctionne mais les données sont perdues au redémarrage
- Utilisez PostgreSQL pour la production

---

## 🚀 Commandes Utiles

```bash
# Voir les logs
render logs <service-name>

# Redémarrer un service
render restart <service-name>

# Mettre à jour depuis Git
git push origin main
# Render redéploie automatiquement
```

---

## 📊 Monitoring

Render fournit:
- ✅ Métriques CPU/RAM
- ✅ Logs en temps réel
- ✅ Alertes par email
- ✅ Historique des déploiements

---

## 💡 Alternatives

Si Render ne convient pas:
- **Railway**: Similar à Render
- **Fly.io**: Plus de contrôle
- **Heroku**: Plus cher mais stable
- **DigitalOcean App Platform**: Bon rapport qualité/prix

---

**Fait avec ❤️ par AutoDev**
