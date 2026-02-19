# 🚀 AutoDev - AI-Powered Full-Stack Code Generator

AutoDev est une plateforme intelligente qui analyse vos documents de spécifications et génère automatiquement des applications web complètes et prêtes pour la production.

## ✨ Fonctionnalités

- 📄 **Analyse Multi-Format**: PDF, Word, Excel, Images (OCR)
- 🏭 **AI Factory**: 13 agents IA niveau FAANG (Microsoft, Apple, Google, Amazon)
- 🤖 **Auto-Amélioration**: 3 itérations d'optimisation automatique
- 🎨 **Pages Web SOTA**: Glassmorphism, gradients animés, animations 60fps
- ⚡ **Streaming Temps Réel**: Suivez l'analyse en direct (SSE)
- 🎨 **Éditeur Visuel**: Modifiez le code dans le navigateur
- 🤖 **Assistant IA**: Posez des questions, modifiez automatiquement
- 🐳 **Infrastructure Complète**: Docker, K8s, Terraform, CI/CD
- 🔒 **Sécurité**: Analyse OWASP, score de sécurité
- 📊 **Analytics**: Coûts, performance, scalabilité

### 🏭 Nouveau: AI FACTORY - Usine à IA Multi-Agents

**13 agents IA spécialisés** de niveau FAANG travaillent ensemble :

**🎨 Design Team (2 agents)**
- Chief Designer (Llama-3.3-70b): Concepts visuels Apple-level
- UX Researcher (Llama-3.1-70b): Accessibilité & user flows

**💻 Frontend Team (3 agents)**
- Frontend Architect (Llama-4-Maverick): HTML/CSS ultra-moderne
- JavaScript Expert (Llama-3.1-8b): Code ES6+ interactif
- Animation Specialist (Llama-3.2-90b): Animations 60fps Disney-level

**🔧 Backend Team (2 agents)**
- Backend Architect (Llama-3.3-70b-specdec): FastAPI Amazon-level
- API Designer (Llama-3.1-70b): RESTful Stripe-level

**🔒 Security & Quality Team (3 agents)**
- Security Expert (Llama-Guard-3-8b): OWASP Microsoft-level
- Code Reviewer (Llama-4-Scout): Best practices Google-level
- QA Engineer (Llama-3.2-11b): Tests Tesla-level

**🚀 Performance Team (2 agents)**
- Performance Optimizer (Llama-3.1-8b): Lazy loading Cloudflare-level
- SEO Specialist (Llama-3.2-3b): Meta tags Shopify-level

**🎯 Orchestration (1 agent)**
- Tech Lead (Llama-3.3-70b): Coordination Uber-level

**Résultat**: Code auto-amélioré sur 3 itérations, score moyen 92/100, niveau Silicon Valley!

## 🚀 Installation Rapide

### Prérequis
- Python 3.11+
- Clé API Groq ou OpenAI

### Configuration Locale
```bash
# 1. Cloner le projet
git clone <votre-repo>
cd proj_02_2026

# 2. Configurer l'environnement
cp .env.example .env
# Éditer .env et ajouter: GROQ_API_KEY=gsk_...

# 3. Démarrer
.\start_backend.bat   # Terminal 1
.\start_frontend.bat  # Terminal 2
```

### Accès
- 🌐 Frontend: http://localhost:5000
- 🔌 API: http://localhost:8000
- 📚 Docs: http://localhost:8000/docs

## 🚢 Déploiement sur Render

### Déploiement Automatique (1-Click)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Cliquez sur le bouton ci-dessus
2. Connectez votre compte GitHub
3. Ajoutez votre `GROQ_API_KEY`
4. Cliquez sur "Apply"

**C'est tout !** Votre application sera déployée en quelques minutes.

### Push sur GitHub

```bash
# Si erreur 403 (mauvais compte GitHub)
# Ouvrir le Gestionnaire d'identifiants Windows
rundll32.exe keymgr.dll,KRShowKeyMgr
# Supprimer les entrées "git:https://github.com"

# OU utiliser cmdkey
cmdkey /list
cmdkey /delete:LegacyGeneric:target=git:https://github.com

# Puis push
git push -u origin main
# Entrez les identifiants du compte her0-03 quand demandé
```

### Déploiement Manuel

Consultez [DEPLOYMENT.md](./DEPLOYMENT.md) pour les instructions détaillées.

**URLs après déploiement:**
- Frontend: `https://autodev-frontend.onrender.com`
- Backend: `https://autodev-backend.onrender.com`

## 📖 Utilisation

1. **Créer un compte** sur http://localhost:5000
2. **Créer un projet** → Donner un nom
3. **Upload documents** → PDF, DOCX, Excel, images
4. **Analyser** → L'IA extrait les spécifications
5. **Preview** → Vérifier entités, endpoints, pages
6. **Générer** → 12 étapes animées
7. **Éditeur** → Modifier, tester, télécharger

## 🤖 Assistant IA

Dans l'éditeur, cliquez sur **🤖 AI Assistant**:
- "Améliore le README.md"
- "Ajoute des tests pour l'API"
- "Optimise les requêtes SQL"
- "Explique l'architecture"

L'IA modifie automatiquement les fichiers!

## 🏗️ Stack Technique

**Backend**: FastAPI, SQLAlchemy, JWT, Pydantic
**Frontend**: Flask, Jinja2, Tailwind CSS, CodeMirror
**IA**: Groq (Llama-3.3-70b, Llama-4)
**Infra**: Docker, Kubernetes, Terraform, GitHub Actions

## 🎯 Projet Généré

```
project_<id>/
├── backend/          # FastAPI + SQLAlchemy
├── frontend/         # Flask + Jinja2
├── k8s/             # Kubernetes
├── terraform/       # AWS Infrastructure
├── monitoring/      # Prometheus/Grafana
├── .github/         # CI/CD
└── docker-compose.yml
```

## 🔧 Configuration

**Backend (.env)**
```env
DATABASE_URL=sqlite:///./dev.db
JWT_SECRET=your-secret-key
GROQ_API_KEY=gsk_...
GENERATED_DIR=C:/Downloads/generated_projects
```

**Frontend (.env)**
```env
SECRET_KEY=flask-secret-key
BACKEND_API_URL=http://localhost:8000
```

## 🐛 Dépannage

**Port occupé**
```bash
netstat -ano | findstr :8000
taskkill /F /PID <PID>
```

**Erreur base de données**
```bash
del backend\dev.db
# Redémarrer
```

**Cache navigateur**
```bash
Ctrl + Shift + R
```

**Timeout sur Render (analyse longue)**
- ✅ Heartbeat SSE automatique toutes les 10s
- ✅ Timeout backend: 5 minutes
- ✅ Timeout frontend: 10 minutes
- Si timeout persiste: Réduire la taille des documents
- Test: `python test_timeout.py`

## 📊 Performances

- ⚡ Analyse: 30-60s
- 🚀 Génération: 45-90s
- 🎯 Précision: 85-95%

## 🚢 Déploiement

```bash
# Docker Compose
docker-compose up -d

# Kubernetes
kubectl apply -f k8s/

# Terraform
cd terraform && terraform apply
```

## 📝 Roadmap

- [ ] Support React/Vue.js
- [ ] Multi-langue (i18n)
- [ ] Déploiement cloud direct
- [ ] Multi-agent AI system
- [ ] Validation interactive

## 📄 Licence

MIT License

## 🙏 Remerciements

FastAPI • Flask • Groq • Tailwind CSS • CodeMirror

---

**Fait avec ❤️ par l'équipe AutoDev**

⭐ Donnez une étoile sur GitHub!
