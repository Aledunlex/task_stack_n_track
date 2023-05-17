import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import SupercategoryPage from './SupercategoryPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/:supercategory" element={<SupercategoryPage />} />
      </Routes>
    </Router>
  );
}

export default App;
