import './SupercategoryPage.css';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import componentMapping from './componentMapping';
import axios from 'axios';
import { updateElement } from './services/elementService';

const SupercategoryPage = () => {
  const [allElements, setAllElements] = useState([]);
  const [viewStyle, setViewStyle] = useState('list'); // initial view style is 'list'
  const { supercategory } = useParams();

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios(`http://localhost:8080/api/${supercategory}`);
      const allElements = result.data.all_elements;
      allElements.forEach(element => {
        element.done = element.done === 'True';  // Convert 'done' to boolean
      });
      setAllElements(allElements);
    };

    fetchData();
  }, [supercategory]);

  const getComponentName = (item) => {
    if (item.reward && item.solution) {
      return 'quest';
    }

    return 'base';
  };

  // function to toggle view style
  const toggleViewStyle = () => {
    setViewStyle(viewStyle === 'list' ? 'grid' : 'list');
  };

  // determine the class name based on the view style
  const viewStyleClass = viewStyle === 'list' ? 'list-view' : 'grid-view';

  const handleCheck = async (title, category, done) => {
    console.log(done);
    const newDoneStatus = await updateElement(title, category, done);
    console.log(newDoneStatus);

    // Met à jour l'état local des éléments
    setAllElements((prevElements) =>
      prevElements.map((el) =>
        el.title === title ? { ...el, done: newDoneStatus } : el
      )
    );
  };

  return (
    <div>
      <h1>{supercategory}</h1>
      <button onClick={toggleViewStyle}>Switch to {viewStyle === 'list' ? 'Grid' : 'List'} View</button>
      <div className={viewStyleClass}>
        {allElements.map((item) => {
          const Component = componentMapping[getComponentName(item)];
          return <Component key={item.title} handleCheck={handleCheck} {...item} />;
        })}
      </div>
    </div>
  );
};

export default SupercategoryPage;
