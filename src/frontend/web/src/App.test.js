import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event'
import {BrowserRouter, MemoryRouter} from 'react-router-dom'
import App from './App';

test('renders title of our website', () => {
  render(<App test={true}/>);
  const title = screen.getByText(/Pet Adoption Data Visualizer/i);
  expect(title).toBeInTheDocument();
});

test('renders navbar to 3 visualizations', () => {
  render(<App test={true}/>);
  const heatmap = screen.getByText("Map");
  expect(heatmap).toBeInTheDocument();
  const linegraph = screen.getByText("Line Graph");
  expect(linegraph).toBeInTheDocument();
  const piechart = screen.getByText("Pie Chart");
  expect(piechart).toBeInTheDocument();
});

describe('Heatmap page is routed and displays', () => {
  beforeEach(() => {
      const renderWithRouter = (ui, { route = '/heatmap' } = {}) => {
          window.history.pushState({}, 'Test page', route);

          return render(ui);
      };
      renderWithRouter(<App test={true}/>);
  });
  test('should render without crashing', () => {});
  test('should render heat map page', () => {
      const heatmapPage = screen.getByText('Heat Map Visualizer');
      expect(heatmapPage).toBeInTheDocument();
  });
  test('should render filters', () => {
    const Filter = screen.getByText(/Breed/i);
    expect(Filter).toBeInTheDocument();
    const advanceSearch = screen.getByText(/Advance Search/i);
    expect(advanceSearch).toBeInTheDocument();
});
});


describe('Piechart page is routed and displays', () => {
  beforeEach(() => {
      const renderWithRouter = (ui, { route = '/piechart' } = {}) => {
          window.history.pushState({}, 'Test page', route);

          return render(ui);
      };
      renderWithRouter(<App test={true}/>);
  });
  test('should render without crashing', () => {});
  test('should render pie chart page', () => {
      const piechartPage = screen.getByText('Pie Chart Visualizer');
      expect(piechartPage).toBeInTheDocument();
  });
  test('should render filters', () => {
    const Filter = screen.getByText(/Gender/i);
    expect(Filter).toBeInTheDocument();
    const advanceSearch = screen.getByText(/Advance Search/i);
    expect(advanceSearch).toBeInTheDocument();
});
});

