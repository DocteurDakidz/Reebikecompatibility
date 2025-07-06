/**
 * Reebike Kit Compatibility Widget
 * Version 1.0 - Mock implementation
 */

class KitCompatibilityWidget {
  constructor() {
    this.apiEndpoint = '/api/compat';
    this.init();
  }

  init() {
    this.bindEvents();
    this.setupAutocomplete();
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
    }
  }

  setupAutocomplete() {
    // Version 1.0: Pas d'autocomplétion, sera ajoutée en v1.1
    console.log('Autocomplete will be implemented in v1.1');
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
      // Call API
      const response = await this.callCompatibilityAPI(bikeInfo.brand, bikeInfo.model);
      
      // Display result
      this.displayResult(response);
      
    } catch (error) {
      console.error('API Error:', error);
      this.showError('Une erreur est survenue. Veuillez réessayer ou contacter notre support.');
    } finally {
      this.setLoadingState(btn, false);
    }
  }

  parseBikeInput(input) {
    // Simple parsing: first word = brand, rest = model
    const parts = input.split(' ');
    const brand = parts[0] || '';
    const model = parts.slice(1).join(' ') || '';
    
    return { brand, model };
  }

  async callCompatibilityAPI(brand, model) {
    // Try real API first, fallback to mock if needed
    try {
      const response = await fetch(`${this.apiEndpoint}?brand=${encodeURIComponent(brand)}&model=${encodeURIComponent(model)}`);
      
      if (response.ok) {
        return await response.json();
      } else {
        console.warn('API call failed, using mock data');
        return this.getMockResponse(brand.toLowerCase(), model.toLowerCase());
      }
    } catch (error) {
      console.warn('API call error, using mock data:', error);
      return this.getMockResponse(brand.toLowerCase(), model.toLowerCase());
    }
  }

  async callCompatibilityAPIMock(brand, model) {
    // Fallback mock implementation
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock response based on brand (for demo purposes)
    return this.getMockResponse(brand.toLowerCase(), model.toLowerCase());
  }

  getMockResponse(brand, model) {
    // Mock data for demonstration
    const mockDatabase = {
      'trek': {
        'domane': { status: 'compatible', kits: ['Cosmopolit', 'Urban', 'Explorer'], notes: 'Compatible si le cadre offre une longueur suffisante pour la batterie.' },
        'emonda': { status: 'compatible', kits: ['Cosmopolit', 'Urban', 'Explorer'], notes: 'Compatible si le cadre offre une longueur suffisante pour la batterie.' },
        'madone': { status: 'incompatible', kits: [], notes: 'Le vélo n\'est pas compatible avec nos kits actuels (axe traversant ou entraxe non standard).' }
      },
      'specialized': {
        'roubaix': { status: 'compatible', kits: ['Cosmopolit', 'Urban', 'Explorer'], notes: 'Compatible si le cadre offre une longueur suffisante pour la batterie.' },
        'tarmac': { status: 'compatible', kits: ['Cosmopolit', 'Urban', 'Explorer'], notes: 'Compatible si le cadre offre une longueur suffisante pour la batterie.' },
        'allez': { status: 'incompatible', kits: [], notes: 'Le vélo n\'est pas compatible avec nos kits actuels (axe traversant ou entraxe non standard).' }
      },
      'giant': {
        'defy': { status: 'compatible', kits: ['Cosmopolit', 'Urban', 'Explorer'], notes: 'Compatible si le cadre offre une longueur suffisante pour la batterie.' },
        'tcr': { status: 'unknown', kits: [], notes: 'Certaines données sont manquantes, contactez notre équipe.' }
      },
      'cannondale': {
        'synapse': { status: 'compatible', kits: ['Cosmopolit', 'Urban', 'Explorer'], notes: 'Compatible si le cadre offre une longueur suffisante pour la batterie.' },
        'supersix': { status: 'incompatible', kits: [], notes: 'Le vélo n\'est pas compatible avec nos kits actuels (axe traversant ou entraxe non standard).' }
      }
    };

    // Try to find exact match
    if (mockDatabase[brand] && mockDatabase[brand][model]) {
      const data = mockDatabase[brand][model];
      return {
        status: data.status,
        kits: data.kits,
        recommendation_url: data.status === 'compatible' && data.kits.length > 0 ? '/products/kit-' + data.kits[0].toLowerCase() : null,
        notes: data.notes
      };
    }

    // Try partial match on brand
    if (mockDatabase[brand]) {
      return {
        status: 'unknown',
        kits: [],
        recommendation_url: null,
        notes: 'Certaines données sont manquantes, contactez notre équipe.'
      };
    }

    // No match found
    return {
      status: 'unknown',
      kits: [],
      recommendation_url: null,
      notes: 'Certaines données sont manquantes, contactez notre équipe.'
    };
  }

  displayResult(response) {
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
        title = 'Vélo compatible !';
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
        title = 'Vélo non compatible';
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

    result.innerHTML = `
      <div class="${resultClass}">
        <div class="result-header" style="color: ${this.getStatusColor(response.status)}">
          ${iconSvg}
          <h3 class="result-title">${title}</h3>
        </div>
        ${kitsHtml}
        <div class="result-notes">${response.notes}</div>
        ${ctaHtml}
      </div>
    `;

    result.style.display = 'block';
    result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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