import { render, screen } from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});

test('mock test', () => {
  console.log("we just ran a test!\n");
  console.log("The react tester is working hard to test the app!\n");
});
