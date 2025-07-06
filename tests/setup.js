/**
 * Jest setup file for frontend tests
 */

// Mock DOM APIs
global.fetch = jest.fn();

// Mock scrollIntoView
Element.prototype.scrollIntoView = jest.fn();

// Mock console methods to reduce noise in tests
global.console = {
  ...console,
  log: jest.fn(),
  warn: jest.fn(),
  error: jest.fn(),
};

// Setup DOM environment
beforeEach(() => {
  document.body.innerHTML = '';
  fetch.mockClear();
});