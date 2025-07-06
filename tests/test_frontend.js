/**
 * Tests unitaires JavaScript pour le widget de compatibilité
 * Version 1.0
 */

// Mock DOM elements for testing
function createMockDOM() {
  document.body.innerHTML = `
    <div id="bike-input"></div>
    <button id="analyze-btn">
      <span class="btn-text">Analyser</span>
      <span class="btn-loader" style="display: none;">Loading...</span>
    </button>
    <div id="compatibility-result" style="display: none;"></div>
  `;
}

// Test suite
describe('KitCompatibilityWidget', () => {
  let widget;
  
  beforeEach(() => {
    createMockDOM();
    // Assuming KitCompatibilityWidget is loaded
    widget = new KitCompatibilityWidget();
  });
  
  afterEach(() => {
    document.body.innerHTML = '';
  });
  
  test('should parse bike input correctly', () => {
    const result1 = widget.parseBikeInput('Trek Domane SL 2023');
    expect(result1.brand).toBe('Trek');
    expect(result1.model).toBe('Domane SL 2023');
    
    const result2 = widget.parseBikeInput('Specialized');
    expect(result2.brand).toBe('Specialized');
    expect(result2.model).toBe('');
  });
  
  test('should handle loading state correctly', () => {
    const button = document.getElementById('analyze-btn');
    const btnText = button.querySelector('.btn-text');
    const btnLoader = button.querySelector('.btn-loader');
    
    // Test loading state
    widget.setLoadingState(button, true);
    expect(btnText.style.display).toBe('none');
    expect(btnLoader.style.display).toBe('inline-flex');
    expect(button.disabled).toBe(true);
    
    // Test normal state
    widget.setLoadingState(button, false);
    expect(btnText.style.display).toBe('inline');
    expect(btnLoader.style.display).toBe('none');
    expect(button.disabled).toBe(false);
  });
  
  test('should get correct status color', () => {
    expect(widget.getStatusColor('compatible')).toBe('#10b981');
    expect(widget.getStatusColor('unknown')).toBe('#f59e0b');
    expect(widget.getStatusColor('incompatible')).toBe('#ef4444');
    expect(widget.getStatusColor('invalid')).toBe('#6b7280');
  });
  
  test('should generate mock response correctly', () => {
    const response1 = widget.getMockResponse('trek', 'domane');
    expect(response1.status).toBe('compatible');
    expect(response1.kits.length).toBeGreaterThan(0);
    
    const response2 = widget.getMockResponse('unknown', 'model');
    expect(response2.status).toBe('unknown');
    expect(response2.kits.length).toBe(0);
  });
  
  test('should display error correctly', () => {
    const message = 'Test error message';
    widget.showError(message);
    
    const result = document.getElementById('compatibility-result');
    expect(result.style.display).toBe('block');
    expect(result.innerHTML).toContain(message);
    expect(result.innerHTML).toContain('result-incompatible');
  });
  
  test('should display compatible result correctly', () => {
    const mockResponse = {
      status: 'compatible',
      kits: ['Cosmopolit', 'Urban'],
      recommendation_url: '/products/kit-cosmopolit',
      notes: 'Test compatibility notes'
    };
    
    widget.displayResult(mockResponse);
    
    const result = document.getElementById('compatibility-result');
    expect(result.style.display).toBe('block');
    expect(result.innerHTML).toContain('result-compatible');
    expect(result.innerHTML).toContain('Vélo compatible !');
    expect(result.innerHTML).toContain('Cosmopolit');
    expect(result.innerHTML).toContain('Urban');
    expect(result.innerHTML).toContain('Test compatibility notes');
  });
  
  test('should display unknown result correctly', () => {
    const mockResponse = {
      status: 'unknown',
      kits: [],
      recommendation_url: null,
      notes: 'Unknown bike model'
    };
    
    widget.displayResult(mockResponse);
    
    const result = document.getElementById('compatibility-result');
    expect(result.style.display).toBe('block');
    expect(result.innerHTML).toContain('result-unknown');
    expect(result.innerHTML).toContain('Vérification nécessaire');
    expect(result.innerHTML).toContain('Unknown bike model');
  });
  
  test('should display incompatible result correctly', () => {
    const mockResponse = {
      status: 'incompatible',
      kits: [],
      recommendation_url: null,
      notes: 'Bike not compatible'
    };
    
    widget.displayResult(mockResponse);
    
    const result = document.getElementById('compatibility-result');
    expect(result.style.display).toBe('block');
    expect(result.innerHTML).toContain('result-incompatible');
    expect(result.innerHTML).toContain('Vélo non compatible');
    expect(result.innerHTML).toContain('Bike not compatible');
  });
});

// Integration tests
describe('Integration Tests', () => {
  test('should handle full analysis workflow', async () => {
    createMockDOM();
    const widget = new KitCompatibilityWidget();
    
    const input = document.getElementById('bike-input');
    input.value = 'Trek Domane SL 2023';
    
    // Mock the API call
    const originalCall = widget.callCompatibilityAPI;
    widget.callCompatibilityAPI = jest.fn().mockResolvedValue({
      status: 'compatible',
      kits: ['Cosmopolit', 'Urban'],
      recommendation_url: '/products/kit-cosmopolit',
      notes: 'Compatible bike'
    });
    
    await widget.analyzeBike();
    
    const result = document.getElementById('compatibility-result');
    expect(result.style.display).toBe('block');
    expect(result.innerHTML).toContain('compatible');
    
    // Restore original method
    widget.callCompatibilityAPI = originalCall;
  });
});

console.log('Frontend tests defined. Run with Jest or similar test runner.');