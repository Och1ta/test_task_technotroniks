// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';
import Devices from './components/Devices';
import Batteries from './components/Batteries';
import DeviceDetails from './components/DeviceDetails';
import BatteriesDetails from "./components/BatteriesDetails";

function Home() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Выбор между устройством и аккумулятором</h1>
        <div className="button-container">
          <Link to="/devices" className="button">Устройства</Link>
          <Link to="/batteries" className="button">Аккумуляторы</Link>
        </div>
      </header>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/devices" element={<Devices />} />
        <Route path="/devices/:id" element={<DeviceDetails />} />
        <Route path="/batteries" element={<Batteries />} />
        <Route path="/batteries/:id" element={<BatteriesDetails />} />
      </Routes>
    </Router>
  );
}

export default App;
