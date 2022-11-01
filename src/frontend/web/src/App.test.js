import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event'
import {BrowserRouter, MemoryRouter} from 'react-router-dom'
import App from './App';

test('renders title of our website', () => {
  render(<App />);
  const title = screen.getByText(/Pet Adoption Data Visualization/i);
  expect(title).toBeInTheDocument();
});

test('renders navbar to 3 visualizations', () => {
  render(<App />);
  const heatmap = screen.getByText("Map");
  expect(heatmap).toBeInTheDocument();
  const linegraph = screen.getByText("Line Graph");
  expect(linegraph).toBeInTheDocument();
  const piechart = screen.getByText("Pie Chart");
  expect(piechart).toBeInTheDocument();
});

describe('Piechart page is routed and displays', () => {
  beforeEach(() => {
      const renderWithRouter = (ui, { route = '/piechart' } = {}) => {
          window.history.pushState({}, 'Test page', route);

          return render(ui);
      };
      renderWithRouter(<App />);
  });
  test('should render without crashing', () => {});
  test('should render home page', () => {
      const piechartPage = screen.getByText('Pie Chart Page');
      expect(piechartPage).toBeInTheDocument();
  });
});

