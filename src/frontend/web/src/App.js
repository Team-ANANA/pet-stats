import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Route, BrowserRouter,Routes } from "react-router-dom";
import React from 'react';

//navbar
import NavBar from './components/navbar';

//pages
import HeatMapPage from './pages/heatmapPage';
import PieChartPage from './pages/piechartPage';
import LineGraphPage from './pages/lineGraphPage';
import AboutPage from './pages/aboutPage';


function App() {
  return (
    <BrowserRouter>

    <NavBar/>
    <Routes>
      <Route path="/"
             element={<HeatMapPage/>}
      />
      <Route path="/heatmap"
             element={<HeatMapPage/>}
      />
      <Route path="/linegraph"
             element={<LineGraphPage/>}
      />
      <Route path="/piechart"
             element={<PieChartPage/>}
      />
            <Route path="/about"
             element={<AboutPage/>}
      />
    </Routes>

  </BrowserRouter>
  );
}

export default App;
