# Reebike Compatibility Widget v1.0

Widget de compatibilité pour évaluer automatiquement la compatibilité des vélos avec les kits de motorisation Reebike.

## 🚀 Fonctionnalités v1.0

- ✅ Interface utilisateur simple (marque + modèle)
- ✅ API Flask mock avec données JSON locales
- ✅ 3 états de compatibilité (compatible/incertain/incompatible)
- ✅ Intégration Shopify 2.0 native
- ✅ Tests unitaires JavaScript et Python
- ✅ Design responsive et moderne

## 📁 Structure du projet

```
reebike-compatibility-widget/
├── shopify/
│   ├── sections/
│   │   └── kit-compatibility.liquid    # Section Shopify 2.0
│   └── assets/
│       └── custom-kit.js              # Widget JavaScript
├── backend/
│   ├── app.py                         # API Flask
│   ├── mock_bikes.json               # Base de données mock
│   ├── requirements.txt              # Dépendances Python
│   └── wsgi.py                       # Point d'entrée WSGI
├── tests/
│   ├── test_compatibility.py         # Tests Python
│   └── test_frontend.js              # Tests JavaScript
└── README.md
```

## 🛠️ Installation

### Backend (API Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

L'API sera disponible sur `http://localhost:5000`

### Frontend (Shopify)

1. Copier `shopify/sections/kit-compatibility.liquid` dans le dossier `sections/` de votre thème
2. Copier `shopify/assets/custom-kit.js` dans le dossier `assets/` de votre thème
3. Ajouter la section dans une page via l'éditeur Shopify

## 🧪 Tests

### Tests Python
```bash
cd backend
python -m pytest test_compatibility.py -v
```

### Tests JavaScript
```bash
npm test
```

## 📡 API Endpoints

### `GET /api/compat`
Vérification de compatibilité

**Paramètres :**
- `brand` (string) : Marque du vélo
- `model` (string) : Modèle du vélo

**Réponse :**
```json
{
  "status": "compatible|unknown|incompatible",
  "kits": ["Cosmopolit", "Urban", "Explorer"],
  "recommendation_url": "/products/kit-urban",
  "notes": "Description de la compatibilité"
}
```

### `GET /api/health`
Vérification de l'état de l'API

### `GET /api/brands`
Liste des marques disponibles

## 🎨 Utilisation Shopify

1. Dans l'éditeur de thème, ajouter la section "Kit Compatibility Checker"
2. Personnaliser le titre et la description
3. Configurer l'URL de l'API si nécessaire
4. Publier les modifications

## 🔧 Configuration

### Variables d'environnement (optionnel)
```bash
FLASK_ENV=development
API_BASE_URL=http://localhost:5000
```

### Personnalisation CSS
Le widget utilise des classes CSS préfixées `.kit-compatibility-*` pour éviter les conflits.

## 📊 Base de données mock

Le fichier `mock_bikes.json` contient :
- 15 modèles de vélos de marques populaires
- Spécifications techniques (axe, entraxe, longueur tube, etc.)
- Matrice de compatibilité pour les 3 kits Reebike

## 🚦 États de compatibilité

### Compatible ✅
- Vélo compatible avec au moins un kit
- Affichage des kits compatibles
- Lien vers la page produit recommandée

### Incertain ⚠️
- Données manquantes ou modèle non reconnu
- Redirection vers le support client
- Message d'aide personnalisé

### Incompatible ❌
- Vélo non compatible (axe traversant, entraxe non standard)
- Explication claire des raisons
- Suggestions alternatives

## 🔄 Roadmap

### v1.1 - Autocomplétion
- Autocomplétion des marques et modèles
- Amélioration de l'UX de saisie

### v1.2 - Intégration GeometryGeeks
- API externe pour données vélos
- Fallback sur base locale

### v1.3 - Optimisations UX
- Interface responsive avancée
- Analytics et logs

### v1.4 - Production
- Déploiement O2SWITCH
- Intégration Shopify App (optionnel)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Distribué sous licence MIT. Voir `LICENSE` pour plus d'informations.

## 📞 Support

Pour toute question ou problème :
- Email : support@reebike.com
- Documentation : [docs.reebike.com](https://docs.reebike.com)
- Issues GitHub : [github.com/reebike/compatibility-widget/issues](https://github.com/reebike/compatibility-widget/issues)