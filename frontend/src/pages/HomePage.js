import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

import './HomePage.css';

const HomePage = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios(
        'http://localhost:8080/api/supercategories',
      );
	setData(result.data.supercategories);
    };
 
    fetchData();
  }, []);
  
  return (
    <div>
      <h1>Supercatégories</h1>
      {data.map(item => (
        <div key={item.value}>
          <Link to={`/${item.value}`} className="link-button">{item.value}</Link>
        </div>
      ))}
    </div>
  );
}

export default HomePage;
