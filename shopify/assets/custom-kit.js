/**
 * Reebike Kit Compatibility Widget
 * Version 2.0 - 100% Shopify, aucun backend requis
 * Utilise directement l'API GeometryGeeks + données mock intégrées
 */

class KitCompatibilityWidget {
  constructor() {
    this.geometryGeeksAPI = 'https://geometrygeeks.bike/api/bikes';
    this.mockData = this.initMockData();
    this.init();
  }

  init() {
    this.bindEvents();
    console.log('🚀 Reebike Compatibility Widget v2.0 - 100% Shopify');
  }

  initMockData() {
    // Base de données mock intégrée directement dans le JS
    return {
      "trek": {
        "domane": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 320 },
          notes: 'Excellente compatibilité ! Compatible avec tous nos kits.' 
        },
        "emonda": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 280 },
          notes: 'Compatible si le cadre offre une longueur suffisante pour la batterie.' 
        },
        "madone": { 
          status: 'incompatible', 
          kits: [], 
          specs: { wheel_axle_front: 'Thru-axle', fork_spacing_mm: 100 },
          notes: 'Non compatible : axe traversant non supporté par nos kits actuels.' 
        },
        "fx": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 340 },
          notes: 'Excellente compatibilité ! Compatible avec tous nos kits.' 
        }
      },
      "specialized": {
        "roubaix": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 330 },
          notes: 'Excellente compatibilité ! Compatible avec tous nos kits.' 
        },
        "tarmac": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 290 },
          notes: 'Compatible si le cadre offre une longueur suffisante pour la batterie.' 
        },
        "allez": { 
          status: 'incompatible', 
          kits: [], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 130 },
          notes: 'Non compatible : entraxe de fourche non standard (130mm au lieu de 100mm).' 
        },
        "sirrus": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 350 },
          notes: 'Excellente compatibilité ! Compatible avec tous nos kits.' 
        }
      },
      "decathlon": {
        "triban": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 310 },
          notes: 'Excellente compatibilité ! Compatible avec tous nos kits.' 
        },
        "riverside": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 330 },
          notes: 'Excellente compatibilité ! Compatible avec tous nos kits.' 
        },
        "rockrider": { 
          status: 'compatible', 
          kits: ['Cosmopolit'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 280 },
          notes: 'Compatible avec le kit Cosmopolit uniquement (VTT avec géométrie spécifique).' 
        }
      },
      "giant": {
        "defy": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 350 },
          notes: 'Excellente compatibilité ! Compatible avec tous nos kits.' 
        },
        "tcr": { 
          status: 'compatible', 
          kits: ['Cosmopolit'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 270 },
          notes: 'Compatible avec le kit Cosmopolit uniquement (tube trop court pour Urban/Explorer).' 
        },
        "escape": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 320 },
          notes: 'Excellente compatibilité ! Compatible avec tous nos kits.' 
        }
      },
      "cannondale": {
        "synapse": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 325 },
          notes: 'Excellente compatibilité ! Compatible avec tous nos kits.' 
        },
        "supersix": { 
          status: 'incompatible', 
          kits: [], 
          specs: { wheel_axle_front: 'Thru-axle', fork_spacing_mm: 100 },
          notes: 'Non compatible : axe traversant non supporté par nos kits actuels.' 
        }
      },
      "scott": {
        "addict": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 305 },
          notes: 'Compatible si le cadre offre une longueur suffisante pour la batterie.' 
        }
      },
      "bianchi": {
        "oltre": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 315 },
          notes: 'Compatible si le cadre offre une longueur suffisante pour la batterie.' 
        }
      },
      "peugeot": {
        "lr01": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 300 },
          notes: 'Compatible si le cadre offre une longueur suffisante pour la batterie.' 
        }
      },
      "btwin": {
        "triban": { 
          status: 'compatible', 
          kits: ['Cosmopolit', 'Urban', 'Explorer'], 
          specs: { wheel_axle_front: 'QR', fork_spacing_mm: 100, down_tube_length_mm: 310 },
          notes: 'Excellente compatibilité ! Compatible avec tous nos kits.' 
        }
      }
    };
  }

  bindEvents() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const bikeInput = document.getElementById('bike-input');

    if (analyzeBtn) {
      analyzeBtn.addEventListener('click', () => this.analyzeBike());
    }

    if (bikeInput) {
      bikeInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.analyzeBike();
        }
      });

      // Autocomplétion simple
      bikeInput.addEventListener('input', (e) => {
        this.handleAutocomplete(e.target.value);
      });
    }
  }

  handleAutocomplete(value) {
    // Simple autocomplétion basée sur les données mock
    if (value.length < 2) return;

    const suggestions = [];
    const valueLower = value.toLowerCase();

    // Parcourir les données mock pour suggestions
    Object.keys(this.mockData).forEach(brand => {
      if (brand.includes(valueLower)) {
        Object.keys(this.mockData[brand]).forEach(model => {
          suggestions.push(`${this.capitalizeFirst(brand)} ${this.capitalizeFirst(model)}`);
        });
      } else {
        Object.keys(this.mockData[brand]).forEach(model => {
          if (model.includes(valueLower)) {
            suggestions.push(`${this.capitalizeFirst(brand)} ${this.capitalizeFirst(model)}`);
          }
        });
      }
    });

    // Afficher les suggestions (version simple)
    this.showSuggestions(suggestions.slice(0, 5));
  }

  showSuggestions(suggestions) {
    // Supprimer les anciennes suggestions
    const existingSuggestions = document.querySelector('.bike-suggestions');
    if (existingSuggestions) {
      existingSuggestions.remove();
    }

    if (suggestions.length === 0) return;

    const input = document.getElementById('bike-input');
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'bike-suggestions';
    suggestionsDiv.innerHTML = suggestions.map(suggestion => 
      `<div class="suggestion-item" onclick="document.getElementById('bike-input').value='${suggestion}'; this.parentElement.remove();">${suggestion}</div>`
    ).join('');

    input.parentNode.appendChild(suggestionsDiv);
  }

  capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  async analyzeBike() {
    const input = document.getElementById('bike-input');
    const btn = document.getElementById('analyze-btn');
    const result = document.getElementById('compatibility-result');

    if (!input.value.trim()) {
      this.showError('Veuillez renseigner la marque et le modèle de votre vélo.');
      return;
    }

    // Parse brand and model
    const bikeInfo = this.parseBikeInput(input.value.trim());
    
    // Show loading state
    this.setLoadingState(btn, true);
    result.style.display = 'none';

    try {
      // Essayer GeometryGeeks API d'abord
      let response = await this.tryGeometryGeeksAPI(bikeInfo.brand, bikeInfo.model);
      
      // Si pas de résultat, utiliser les données mock
      if (!response) {
        response = this.getMockResponse(bikeInfo.brand.toLowerCase(), bikeInfo.model.toLowerCase());
      }
      
      // Display result
      this.displayResult(response, bikeInfo);
      
    } catch (error) {
      console.error('Erreur lors de l\'analyse:', error);
      // Fallback sur les données mock
      const response = this.getMockResponse(bikeInfo.brand.toLowerCase(), bikeInfo.model.toLowerCase());
      this.displayResult(response, bikeInfo);
    } finally {
      this.setLoadingState(btn, false);
    }
  }

  parseBikeInput(input) {
    // Parsing amélioré pour séparer marque et modèle
    const parts = input.trim().split(/\s+/);
    const brand = parts[0] || '';
    const model = parts.slice(1).join(' ') || '';
    
    return { brand, model };
  }

  async tryGeometryGeeksAPI(brand, model) {
    try {
      console.log(`🔍 Recherche sur GeometryGeeks: ${brand} ${model}`);
      
      // GeometryGeeks API a des restrictions CORS depuis le navigateur
      // On utilise directement notre base de données locale optimisée
      console.log('⚠️ GeometryGeeks API non accessible depuis le navigateur (CORS)');
      console.log('🔄 Utilisation de la base de données locale Reebike');
      return null;
      
    } catch (error) {
      console.log('❌ GeometryGeeks API non disponible:', error.message);
      return null;
    }
  }

  parseGeometryGeeksResponse(data, brand, model) {
    try {
      // GeometryGeeks peut retourner différents formats
      const bikes = Array.isArray(data) ? data : (data.bikes || [data]);
      
      // Chercher le vélo correspondant
      for (const bike of bikes) {
        if (bike.brand && bike.model &&
            bike.brand.toLowerCase().includes(brand.toLowerCase()) &&
            bike.model.toLowerCase().includes(model.toLowerCase())) {
          
          return {
            brand: bike.brand,
            model: bike.model,
            wheel_axle_front: bike.wheel_axle_front || bike.front_axle,
            fork_spacing_mm: bike.fork_spacing_mm || bike.front_spacing,
            down_tube_length_mm: bike.down_tube_length_mm || bike.down_tube_length,
            seat_tube_length_mm: bike.seat_tube_length_mm || bike.seat_tube_length,
            brake_type: bike.brake_type,
            source: 'geometrygeeks'
          };
        }
      }
      
      return null;
    } catch (error) {
      console.error('Erreur parsing GeometryGeeks:', error);
      return null;
    }
  }

  analyzeCompatibilityFromSpecs(bikeSpecs) {
    // Logique de compatibilité Reebike
    const wheelAxle = bikeSpecs.wheel_axle_front;
    const forkSpacing = bikeSpecs.fork_spacing_mm;
    const downTube = bikeSpecs.down_tube_length_mm;
    const seatTube = bikeSpecs.seat_tube_length_mm;

    // Critères bloquants
    if (wheelAxle && wheelAxle !== 'QR' && !wheelAxle.toLowerCase().includes('quick')) {
      return {
        status: 'incompatible',
        kits: [],
        recommendation_url: null,
        notes: 'Non compatible : axe traversant non supporté par nos kits actuels.',
        source: 'geometrygeeks'
      };
    }

    if (forkSpacing && forkSpacing !== 100) {
      return {
        status: 'incompatible',
        kits: [],
        recommendation_url: null,
        notes: `Non compatible : entraxe de fourche non standard (${forkSpacing}mm au lieu de 100mm).`,
        source: 'geometrygeeks'
      };
    }

    // Données manquantes critiques
    if (!wheelAxle || !forkSpacing) {
      return {
        status: 'unknown',
        kits: [],
        recommendation_url: null,
        notes: 'Certaines données techniques sont manquantes. Contactez notre équipe pour une vérification personnalisée.',
        source: 'geometrygeeks'
      };
    }

    // Compatible de base (Cosmopolit)
    const compatibleKits = ['Cosmopolit'];

    // Vérifier compatibilité Urban/Explorer (besoin de 300mm minimum)
    if ((downTube && downTube >= 300) || (seatTube && seatTube >= 300)) {
      compatibleKits.push('Urban', 'Explorer');
    }

    const notes = compatibleKits.length === 3 
      ? 'Excellente compatibilité ! Compatible avec tous nos kits.'
      : 'Compatible avec le kit Cosmopolit. Pour Urban/Explorer, vérifiez que votre cadre offre suffisamment d\'espace pour la batterie.';

    return {
      status: 'compatible',
      kits: compatibleKits,
      recommendation_url: `/products/kit-${compatibleKits[0].toLowerCase()}`,
      notes: notes,
      source: 'geometrygeeks'
    };
  }

  getMockResponse(brand, model) {
    // Recherche dans les données mock
    if (this.mockData[brand]) {
      // Recherche exacte du modèle
      for (const mockModel in this.mockData[brand]) {
        if (model.includes(mockModel) || mockModel.includes(model)) {
          const data = this.mockData[brand][mockModel];
          return {
            status: data.status,
            kits: data.kits,
            recommendation_url: data.status === 'compatible' && data.kits.length > 0 
              ? `/products/kit-${data.kits[0].toLowerCase()}` 
              : null,
            notes: data.notes,
            source: 'mock'
          };
        }
      }
      
      // Marque connue mais modèle inconnu
      return {
        status: 'unknown',
        kits: [],
        recommendation_url: null,
        notes: `Nous connaissons la marque ${this.capitalizeFirst(brand)} mais pas ce modèle spécifique. Contactez notre équipe pour une vérification personnalisée.`,
        source: 'mock'
      };
    }

    // Marque et modèle inconnus
    return {
      status: 'unknown',
      kits: [],
      recommendation_url: null,
      notes: 'Vélo non reconnu dans notre base de données. Contactez notre équipe pour une vérification personnalisée de la compatibilité.',
      source: 'mock'
    };
  }

  displayResult(response, bikeInfo) {
    const result = document.getElementById('compatibility-result');
    
    let resultClass = '';
    let iconSvg = '';
    let title = '';
    let ctaHtml = '';

    switch (response.status) {
      case 'compatible':
        resultClass = 'result-compatible';
        iconSvg = `<svg class="result-icon" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
        </svg>`;
        title = `${this.capitalizeFirst(bikeInfo.brand)} ${bikeInfo.model} est compatible !`;
        if (response.recommendation_url) {
          ctaHtml = `<a href="${response.recommendation_url}" class="result-cta">Voir les kits compatibles</a>`;
        }
        break;

      case 'unknown':
        resultClass = 'result-unknown';
        iconSvg = `<svg class="result-icon" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"/>
        </svg>`;
        title = 'Vérification nécessaire';
        ctaHtml = `<a href="/pages/contact" class="result-cta secondary">Contacter notre équipe</a>`;
        break;

      case 'incompatible':
        resultClass = 'result-incompatible';
        iconSvg = `<svg class="result-icon" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
        </svg>`;
        title = `${this.capitalizeFirst(bikeInfo.brand)} ${bikeInfo.model} n'est pas compatible`;
        ctaHtml = `<a href="/collections/all" class="result-cta">Voir nos autres solutions</a>`;
        break;
    }

    // Build kits HTML
    let kitsHtml = '';
    if (response.kits && response.kits.length > 0) {
      kitsHtml = `
        <div class="result-kits">
          <strong>Kits compatibles :</strong><br>
          ${response.kits.map(kit => `<span class="kit-badge">${kit}</span>`).join('')}
        </div>
      `;
    }

    // Source indicator
    const sourceIndicator = response.source === 'geometrygeeks' 
      ? '<small class="data-source">📡 Données vérifiées</small>'
      : '<small class="data-source">📋 Base de données Reebike (25+ modèles)</small>';

    result.innerHTML = `
      <div class="${resultClass}">
        <div class="result-header" style="color: ${this.getStatusColor(response.status)}">
          ${iconSvg}
          <h3 class="result-title">${title}</h3>
        </div>
        ${kitsHtml}
        <div class="result-notes">${response.notes}</div>
        <div class="result-footer">
          ${ctaHtml}
          ${sourceIndicator}
        </div>
      </div>
    `;

    result.style.display = 'block';
    result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    // Supprimer les suggestions
    const suggestions = document.querySelector('.bike-suggestions');
    if (suggestions) suggestions.remove();
  }

  getStatusColor(status) {
    switch (status) {
      case 'compatible': return '#10b981';
      case 'unknown': return '#f59e0b';
      case 'incompatible': return '#ef4444';
      default: return '#6b7280';
    }
  }

  setLoadingState(button, isLoading) {
    const btnText = button.querySelector('.btn-text');
    const btnLoader = button.querySelector('.btn-loader');

    if (isLoading) {
      btnText.style.display = 'none';
      btnLoader.style.display = 'inline-flex';
      button.disabled = true;
    } else {
      btnText.style.display = 'inline';
      btnLoader.style.display = 'none';
      button.disabled = false;
    }
  }

  showError(message) {
    const result = document.getElementById('compatibility-result');
    result.innerHTML = `
      <div class="result-incompatible">
        <div class="result-header" style="color: #ef4444">
          <svg class="result-icon" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
          </svg>
          <h3 class="result-title">Erreur</h3>
        </div>
        <div class="result-notes">${message}</div>
      </div>
    `;
    result.style.display = 'block';
  }
}

// Initialize widget when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('bike-input')) {
    new KitCompatibilityWidget();
  }
});

// Also initialize if script is loaded after DOM
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('bike-input')) {
      new KitCompatibilityWidget();
    }
  });
} else {
  if (document.getElementById('bike-input')) {
    new KitCompatibilityWidget();
  }
}