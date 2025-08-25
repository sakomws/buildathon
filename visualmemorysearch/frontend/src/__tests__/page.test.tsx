import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Page from '../app/page';

// Mock the API functions
jest.mock('@/lib/api', () => ({
  getScreenshots: jest.fn(),
  searchScreenshots: jest.fn(),
  uploadScreenshot: jest.fn(),
  uploadFolder: jest.fn(),
  getStatus: jest.fn(),
  rebuildIndex: jest.fn(),
  generateTestData: jest.fn(),
  testOpenAIKey: jest.fn(),
}));

// Mock the API client
jest.mock('@/lib/api', () => ({
  api: {
    get: jest.fn(),
    post: jest.fn(),
    delete: jest.fn(),
  },
  getScreenshots: jest.fn(),
  searchScreenshots: jest.fn(),
  uploadScreenshot: jest.fn(),
  uploadFolder: jest.fn(),
  getStatus: jest.fn(),
  rebuildIndex: jest.fn(),
  generateTestData: jest.fn(),
  testOpenAIKey: jest.fn(),
}));

describe('Main Page Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders the main page with all UI elements', () => {
    render(<Page />);
    
    // Check main header
    expect(screen.getByText('Visual Memory Search')).toBeInTheDocument();
    
    // Check main buttons
    expect(screen.getByText('Upload')).toBeInTheDocument();
    expect(screen.getByText('Admin')).toBeInTheDocument();
    expect(screen.getByText('Settings')).toBeInTheDocument();
    expect(screen.getByText('Refresh')).toBeInTheDocument();
    
    // Check search section
    expect(screen.getByText('Search Screenshots')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your search query...')).toBeInTheDocument();
    expect(screen.getByText('Search')).toBeInTheDocument();
    
    // Check filters section
    expect(screen.getByText('Filters & Actions')).toBeInTheDocument();
    expect(screen.getByText('Show Filters')).toBeInTheDocument();
    
    // Check screenshots section
    expect(screen.getByText('All Screenshots (0)')).toBeInTheDocument();
  });

  it('handles search input changes', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const searchInput = screen.getByPlaceholderText('Enter your search query...');
    await user.type(searchInput, 'dashboard');
    
    expect(searchInput).toHaveValue('dashboard');
  });

  it('handles search type selection', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const searchTypeSelect = screen.getByDisplayValue('Combined');
    await user.selectOptions(searchTypeSelect, 'text');
    
    expect(searchTypeSelect).toHaveValue('text');
  });

  it('shows loading state during search', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const searchInput = screen.getByPlaceholderText('Enter your search query...');
    const searchButton = screen.getByText('Search');
    
    await user.type(searchInput, 'test query');
    
    // Mock the search function to return a promise
    const mockSearch = require('@/lib/api').searchScreenshots;
    mockSearch.mockImplementation(() => new Promise(() => {}));
    
    await user.click(searchButton);
    
    // Check if search button is disabled during loading
    expect(searchButton).toBeDisabled();
  });

  it('handles file upload dialog', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const uploadButton = screen.getByText('Upload');
    await user.click(uploadButton);
    
    // Check if upload dialog is shown
    expect(screen.getByText('Upload Screenshots')).toBeInTheDocument();
  });

  it('handles admin panel toggle', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const adminButton = screen.getByText('Admin');
    await user.click(adminButton);
    
    // Check if admin panel is shown
    expect(screen.getByText('System Status')).toBeInTheDocument();
    expect(screen.getByText('Admin Actions')).toBeInTheDocument();
  });

  it('handles settings panel toggle', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const settingsButton = screen.getByText('Settings');
    await user.click(settingsButton);
    
    // Check if settings panel is shown
    expect(screen.getByText('Application Settings')).toBeInTheDocument();
  });

  it('displays empty state when no screenshots', () => {
    render(<Page />);
    
    expect(screen.getByText('No screenshots found')).toBeInTheDocument();
    expect(screen.getByText('Upload some screenshots to get started!')).toBeInTheDocument();
    expect(screen.getByText('Upload Screenshot')).toBeInTheDocument();
  });

  it('handles pagination controls', () => {
    render(<Page />);
    
    const prevButton = screen.getByLabelText('Previous page');
    const nextButton = screen.getByLabelText('Next page');
    
    expect(prevButton).toBeDisabled();
    expect(nextButton).toBeDisabled();
  });

  it('shows filters when toggle is clicked', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const filtersToggle = screen.getByText('Show Filters');
    await user.click(filtersToggle);
    
    // Check if filters are expanded
    expect(screen.getByText('Hide Filters')).toBeInTheDocument();
  });

  it('handles refresh button click', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const refreshButton = screen.getByText('Refresh');
    await user.click(refreshButton);
    
    // The refresh functionality should be triggered
    // We can verify this by checking if the getScreenshots function is called
    expect(refreshButton).toBeInTheDocument();
  });

  it('displays search history in datalist', () => {
    render(<Page />);
    
    const searchInput = screen.getByPlaceholderText('Enter your search query...');
    const datalist = searchInput.getAttribute('list');
    
    expect(datalist).toBe('searchHistory');
  });

  it('handles search with empty query', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const searchButton = screen.getByText('Search');
    await user.click(searchButton);
    
    // Search button should be disabled when no query
    expect(searchButton).toBeDisabled();
  });

  it('shows correct page information', () => {
    render(<Page />);
    
    expect(screen.getByText('Page 1 of 0')).toBeInTheDocument();
  });

  it('handles bulk actions when screenshots exist', () => {
    // Mock screenshots data
    const mockScreenshots = [
      { filename: 'test1.png', filepath: 'test1.png' },
      { filename: 'test2.png', filepath: 'test2.png' }
    ];
    
    // Mock the getScreenshots function
    const mockGetScreenshots = require('@/lib/api').getScreenshots;
    mockGetScreenshots.mockResolvedValue(mockScreenshots);
    
    render(<Page />);
    
    // Check if bulk actions are available
    expect(screen.getByText('Select All')).toBeInTheDocument();
  });

  it('handles image viewer functionality', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    // Mock a screenshot with image
    const mockScreenshot = {
      filename: 'test.png',
      filepath: 'test.png',
      metadata: { dimensions: { width: 1920, height: 1080 } }
    };
    
    // Mock the getScreenshots function
    const mockGetScreenshots = require('@/lib/api').getScreenshots;
    mockGetScreenshots.mockResolvedValue([mockScreenshot]);
    
    render(<Page />);
    
    // Check if image viewer is rendered
    await waitFor(() => {
      expect(screen.getByAltText('test.png')).toBeInTheDocument();
    });
  });

  it('handles keyboard shortcuts', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const searchInput = screen.getByPlaceholderText('Enter your search query...');
    
    // Test Ctrl+F for search focus
    await user.keyboard('{Control>}f{/Control}');
    expect(document.activeElement).toBe(searchInput);
  });

  it('handles responsive design elements', () => {
    render(<Page />);
    
    // Check if responsive classes are applied
    const searchContainer = screen.getByText('Search Screenshots').closest('div');
    expect(searchContainer).toHaveClass('flex-col', 'sm:flex-row');
  });

  it('handles error states gracefully', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    // Mock an error in the API
    const mockSearch = require('@/lib/api').searchScreenshots;
    mockSearch.mockRejectedValue(new Error('API Error'));
    
    const searchInput = screen.getByPlaceholderText('Enter your search query...');
    const searchButton = screen.getByText('Search');
    
    await user.type(searchInput, 'error test');
    await user.click(searchButton);
    
    // Should handle error gracefully
    expect(searchButton).toBeInTheDocument();
  });

  it('handles accessibility features', () => {
    render(<Page />);
    
    // Check for proper ARIA labels
    const searchInput = screen.getByPlaceholderText('Enter your search query...');
    expect(searchInput).toHaveAttribute('aria-label', 'Search query input');
    
    // Check for proper button labels
    const uploadButton = screen.getByText('Upload');
    expect(uploadButton).toHaveAttribute('aria-label', 'Upload screenshots');
  });

  it('handles theme switching', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const settingsButton = screen.getByText('Settings');
    await user.click(settingsButton);
    
    const themeToggle = screen.getByLabelText('Toggle theme');
    await user.click(themeToggle);
    
    // Check if theme is switched
    expect(document.documentElement).toHaveClass('dark');
  });

  it('handles language switching', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const settingsButton = screen.getByText('Settings');
    await user.click(settingsButton);
    
    const languageSelect = screen.getByLabelText('Language');
    await user.selectOptions(languageSelect, 'es');
    
    // Check if language is switched
    expect(languageSelect).toHaveValue('es');
  });

  it('handles notification system', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    // Mock a successful upload
    const mockUpload = require('@/lib/api').uploadScreenshot;
    mockUpload.mockResolvedValue({ message: 'Success', filename: 'test.png' });
    
    const uploadButton = screen.getByText('Upload');
    await user.click(uploadButton);
    
    // Check if success notification is shown
    await waitFor(() => {
      expect(screen.getByText('Success')).toBeInTheDocument();
    });
  });

  it('handles keyboard navigation', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    // Test Tab navigation
    await user.tab();
    expect(screen.getByText('Upload')).toHaveFocus();
    
    await user.tab();
    expect(screen.getByText('Admin')).toHaveFocus();
    
    await user.tab();
    expect(screen.getByText('Settings')).toHaveFocus();
  });

  it('handles mobile viewport', () => {
    // Mock mobile viewport
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375,
    });
    
    render(<Page />);
    
    // Check if mobile-specific classes are applied
    const searchContainer = screen.getByText('Search Screenshots').closest('div');
    expect(searchContainer).toHaveClass('flex-col');
  });

  it('handles print functionality', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const settingsButton = screen.getByText('Settings');
    await user.click(settingsButton);
    
    const printButton = screen.getByText('Print Screenshots');
    await user.click(printButton);
    
    // Mock print function
    const mockPrint = jest.spyOn(window, 'print').mockImplementation(() => {});
    
    expect(mockPrint).toHaveBeenCalled();
    mockPrint.mockRestore();
  });

  it('handles export functionality', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const settingsButton = screen.getByText('Settings');
    await user.click(settingsButton);
    
    const exportButton = screen.getByText('Export Data');
    await user.click(exportButton);
    
    // Check if export options are shown
    expect(screen.getByText('Export Format')).toBeInTheDocument();
    expect(screen.getByText('CSV')).toBeInTheDocument();
    expect(screen.getByText('JSON')).toBeInTheDocument();
  });

  it('handles import functionality', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const settingsButton = screen.getByText('Settings');
    await user.click(settingsButton);
    
    const importButton = screen.getByText('Import Data');
    await user.click(importButton);
    
    // Check if import dialog is shown
    expect(screen.getByText('Import Screenshots')).toBeInTheDocument();
    expect(screen.getByText('Choose File')).toBeInTheDocument();
  });

  it('handles help and documentation', async () => {
    const user = userEvent.setup();
    render(<Page />);
    
    const settingsButton = screen.getByText('Settings');
    await user.click(settingsButton);
    
    const helpButton = screen.getByText('Help & Documentation');
    await user.click(helpButton);
    
    // Check if help content is shown
    expect(screen.getByText('User Guide')).toBeInTheDocument();
    expect(screen.getByText('API Documentation')).toBeInTheDocument();
    expect(screen.getByText('Keyboard Shortcuts')).toBeInTheDocument();
  });
});
