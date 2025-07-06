# Guide de déploiement - Reebike Compatibility Widget

## 🚀 Déploiement Backend (O2SWITCH)

### Prérequis
- Compte O2SWITCH avec accès SSH
- Python 3.8+ installé sur le serveur
- Accès au gestionnaire de fichiers cPanel

### Étapes de déploiement

#### 1. Préparation des fichiers
```bash
# Créer l'archive de déploiement
tar -czf reebike-api.tar.gz backend/
```

#### 2. Upload sur O2SWITCH
```bash
# Via SSH
scp reebike-api.tar.gz user@server.o2switch.net:~/
ssh user@server.o2switch.net
cd ~/
tar -xzf reebike-api.tar.gz
```

#### 3. Installation des dépendances
```bash
cd backend
pip3 install --user -r requirements.txt
```

#### 4. Configuration Apache (.htaccess)
Créer un fichier `.htaccess` dans le dossier public :
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ wsgi.py/$1 [QSA,L]

# CORS Headers
Header always set Access-Control-Allow-Origin "*"
Header always set Access-Control-Allow-Methods "GET, POST, OPTIONS"
Header always set Access-Control-Allow-Headers "Content-Type, Authorization"
```

#### 5. Test de l'API
```bash
curl https://votre-domaine.com/api/health
```

## 🛍️ Déploiement Frontend (Shopify)

### Via l'éditeur de code Shopify

#### 1. Accès à l'éditeur
1. Admin Shopify → Online Store → Themes
2. Actions → Edit code

#### 2. Upload des fichiers
1. **Section Liquid :**
   - Sections → Add a new section
   - Nommer : `kit-compatibility`
   - Coller le contenu de `kit-compatibility.liquid`

2. **JavaScript :**
   - Assets → Add a new asset
   - Nommer : `custom-kit.js`
   - Coller le contenu du fichier JS

#### 3. Configuration de l'API
Dans la section Liquid, modifier l'URL de l'API :
```liquid
"default": "https://votre-domaine.com/api/compat"
```

#### 4. Ajout à une page
1. Customize → Pages → Sélectionner une page
2. Add section → Kit Compatibility Checker
3. Configurer titre et description
4. Save

### Via Shopify CLI (optionnel)

```bash
# Installation Shopify CLI
npm install -g @shopify/cli @shopify/theme

# Connexion au store
shopify auth login

# Upload du thème
shopify theme push
```

## 🔧 Configuration avancée

### Variables d'environnement
Créer un fichier `.env` sur le serveur :
```bash
FLASK_ENV=production
API_BASE_URL=https://votre-domaine.com
CORS_ORIGINS=https://votre-store.myshopify.com
```

### Monitoring et logs
```bash
# Créer le dossier de logs
mkdir -p logs

# Configuration logrotate
sudo nano /etc/logrotate.d/reebike-api
```

### SSL/HTTPS
O2SWITCH fournit automatiquement SSL via Let's Encrypt.

## 🧪 Tests de déploiement

### Test API
```bash
# Health check
curl https://votre-domaine.com/api/health

# Test compatibilité
curl "https://votre-domaine.com/api/compat?brand=Trek&model=Domane"

# Test CORS
curl -H "Origin: https://votre-store.myshopify.com" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS https://votre-domaine.com/api/compat
```

### Test Frontend
1. Ouvrir la page avec le widget
2. Tester avec différents modèles :
   - `Trek Domane SL 2023` (compatible)
   - `Trek Madone SLR 2023` (incompatible)
   - `Marque Inconnue` (unknown)

## 🔄 Mise à jour

### Backend
```bash
# Backup de l'ancienne version
cp -r backend backend_backup_$(date +%Y%m%d)

# Upload nouvelle version
scp -r backend/ user@server.o2switch.net:~/

# Redémarrage (si nécessaire)
touch wsgi.py
```

### Frontend
1. Backup du thème actuel
2. Upload des nouveaux fichiers
3. Test sur thème de développement
4. Publication

## 🚨 Rollback

### Backend
```bash
# Restaurer la version précédente
rm -rf backend
mv backend_backup_YYYYMMDD backend
touch wsgi.py
```

### Frontend
1. Admin Shopify → Themes
2. Actions → Duplicate (sur la version stable)
3. Actions → Publish

## 📊 Monitoring

### Métriques à surveiller
- Temps de réponse API
- Taux d'erreur
- Utilisation CPU/RAM
- Logs d'erreur

### Outils recommandés
- Google Analytics (frontend)
- Logs serveur O2SWITCH
- Shopify Analytics

## 🔐 Sécurité

### Bonnes pratiques
- Utiliser HTTPS uniquement
- Valider tous les inputs
- Limiter les requêtes (rate limiting)
- Logs des accès

### Configuration CORS
```python
CORS(app, origins=[
    'https://votre-store.myshopify.com',
    'https://checkout.shopify.com'
])
```

## 📞 Support déploiement

En cas de problème :
1. Vérifier les logs : `tail -f logs/app.log`
2. Tester l'API manuellement
3. Vérifier la configuration CORS
4. Contacter le support O2SWITCH si nécessaire

## ✅ Checklist de déploiement

### Backend
- [ ] Fichiers uploadés sur O2SWITCH
- [ ] Dépendances installées
- [ ] Configuration .htaccess
- [ ] Variables d'environnement
- [ ] Test API health
- [ ] Test CORS
- [ ] Logs configurés

### Frontend
- [ ] Section Liquid uploadée
- [ ] JavaScript uploadé
- [ ] URL API configurée
- [ ] Section ajoutée à une page
- [ ] Test widget complet
- [ ] Responsive testé
- [ ] Analytics configuré