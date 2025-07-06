# Reebike Compatibility Widget

## Objectif
Créer une section Shopify 2.0 qui permet aux clients de renseigner la marque et le modèle de leur vélo musculaire pour évaluer automatiquement la compatibilité avec les kits de motorisation Reebike (Cosmopolit, Urban, Explorer). Le système s'appuie sur une API open source (GeometryGeeks) ou une base de données locale hébergée sur O2SWITCH. En cas d'incertitude, un appel à l'action permet de contacter le support.

## Architecture

### Frontend (Shopify 2.0)
- Section personnalisée (Liquid)
- Champ texte unique : `Marque + Modèle`
- Bouton : `Analyser la compatibilité`
- JS dans `assets/custom-kit.js` :
  - Requête vers backend via `fetch`
  - Récupération de l'évaluation de compatibilité
  - Affichage d'un des 3 états :
    - Compatible avec lien vers produit
    - Incertitude (redirection support)
    - Incompatible

### Backend (API REST légère)
- Développée en Flask (Python) sur serveur O2SWITCH
- Route : `GET /api/compat?brand=X&model=Y`
- Fonctionnalités :
  - Rechercher les caractéristiques du modèle (via API ou JSON local)
  - Appliquer la matrice de compatibilité
  - Retourner une réponse JSON claire

## Données vélo requises

| Champ                   | Utilité                              | Source           |
|------------------------|----------------------------------------|------------------|
| wheel_axle_front       | Axe traversant ?                       | GeometryGeeks    |
| fork_spacing_mm        | Entraxe avant                         | GeometryGeeks    |
| down_tube_length_mm    | Longueur pour batterie (30cm mini)    | GeometryGeeks    |
| seat_tube_length_mm    | Longueur alternative pour batterie    | GeometryGeeks    |
| brake_type             | Type de frein (info non bloquante)    | GeometryGeeks    |

## ✅ Matrice de compatibilité Reebike (version simplifiée)

1. **Critères bloquants :**
   - Si `wheel_axle_front` != "QR" ou `fork_spacing_mm` != 100 → **incompatible**

2. **Compatibilité de base :**
   - Si les deux critères ci-dessus sont valides → ✅ **Cosmopolit**

3. **Compatibilité avancée :**
   - Si `down_tube_length_mm >= 300` ou `seat_tube_length_mm >= 300` → ajouter ✅ **Urban** et ✅ **Explorer**

4. **Données manquantes :**
   - Si une des données est manquante → résultat = **unknown** avec le message : "Certaines données sont manquantes, contactez notre équipe."

## 🔗 Sources de données : API GeometryGeeks

### API GeometryGeeks
- Site : https://geometrygeeks.bike
- Type : API REST non officielle (retour JSON)
- Endpoint principal : `https://geometrygeeks.bike/api/bikes`
- Données utiles récupérables :
  - `brand`
  - `model`
  - `year`
  - `fork_spacing_mm`
  - `wheel_axle_front`
  - `down_tube_length_mm`
  - `seat_tube_length_mm`
  - `brake_type`
- Remarque : certaines valeurs peuvent être absentes ou partielles → prévoir fallback JSON local

## Réponses API types

Consultez le fichier DEVPLAN pour les exemples de structure JSON.

## Bonnes pratiques Shopify 2.0
- Utiliser une `section` dédiée avec `schema` JSON
- Charger JS via `defer` depuis `assets`
- Isoler CSS dans un fichier scoping `.kit-compatibility`
- Ne pas demander plus d’infos au client que `marque + modèle`
- Gestion des 3 états sans rechargement de page
