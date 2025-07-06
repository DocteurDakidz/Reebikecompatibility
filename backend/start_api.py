#!/usr/bin/env python3
"""
Script de démarrage pour l'API Reebike
Démarre automatiquement l'API avec la bonne configuration
"""

import os
import sys
from app import app

def main():
    """Démarre l'API avec configuration automatique"""
    print("🚀 Démarrage de l'API Reebike Compatibility...")
    print("📡 GeometryGeeks API: Activée")
    print("🔄 Fallback local: Activé")
    print("🌐 CORS: Configuré pour Shopify")
    print("📊 Logging: Activé")
    print()
    print("API disponible sur: http://localhost:5000")
    print("Health check: http://localhost:5000/api/health")
    print("Test: http://localhost:5000/api/compat?brand=Trek&model=Domane")
    print()
    print("Appuyez sur Ctrl+C pour arrêter")
    print("-" * 50)
    
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n🛑 API arrêtée")
        sys.exit(0)

if __name__ == '__main__':
    main()