import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { toast } from 'react-toastify';
import axios from 'axios';

import './SupercategoryPage.css';
import NewElementForm from './NewElementForm';
import componentMapping from './componentMapping';
import { updateElement, removeElement } from './services/elementService';

const SupercategoryPage = () => {
  const [allElements, setAllElements] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [viewStyle, setViewStyle] = useState('list');
  const { supercategory } = useParams();

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios(`http://localhost:8080/api/${supercategory}`);
      const allElements = result.data.all_elements;
      allElements.forEach(element => {
        element.done = element.done === 'True';
      });
      setAllElements(allElements);
    };

    fetchData();
  }, [supercategory]);

  const getComponentName = (item) => {
    if (item.reward && item.solution) {
      return 'quest';
    }
    if (item.stackable_properties) {
      return 'stackable';
    }
    return 'base';
  };

  // function to toggle view style
  const toggleViewStyle = () => {
    setViewStyle(viewStyle === 'list' ? 'grid' : 'list');
  };

  // determine the class name based on the view style
  const viewStyleClass = viewStyle === 'list' ? 'list-view' : 'grid-view';

  const handleCategoryClick = (category) => {
    setSelectedCategory(category);
  };

  // Créez les boutons de catégorie :
  const categoryButtons = allElements
    .map((item) => item.category)
    .filter((value, index, self) => self.indexOf(value) === index)
    .map((category) => (
      <button key={category} onClick={() => handleCategoryClick(category)}>
        {category}
      </button>
    ));

  categoryButtons.push(
    <button key="all" onClick={() => handleCategoryClick(null)}>
      Voir tout
    </button>
  );

  // Filtrez la liste des éléments à afficher :
  const elementsToDisplay = selectedCategory
    ? allElements.filter((item) => item.category === selectedCategory)
    : allElements;

  const handleCheck = async (title, category, done) => {
    const newDoneStatus = await updateElement(title, category, done);

    // Met à jour l'état local des éléments
    setAllElements((prevElements) =>
      prevElements.map((el) =>
        el.title === title ? { ...el, done: newDoneStatus } : el
      )
    );
  };

  const addNewElement = (newElement) => {
    setAllElements(prevElements => [newElement, ...prevElements]);
  };

  const handleRemove = async (title, category) => {
    const success = await removeElement(title, category);
  
    if (success) {
      toast.success(`Element "${title}" removed`);
      setAllElements((prevElements) =>
        prevElements.filter((element) =>
          !(element.title === title && element.category === category)
        )
      );
    } else {
      toast.error(`Error removing element "${title}"`);
    }
  };

  return (
    <div>
      <h1>{supercategory}</h1>
      <div>{categoryButtons}</div>
      <button onClick={toggleViewStyle}>Switch to {viewStyle === 'list' ? 'Grid' : 'List'} View</button>
      <div className={viewStyleClass}>
        <NewElementForm supercategory={supercategory} addNewElement={addNewElement} />
        {elementsToDisplay.map((item) => {
          const Component = componentMapping[getComponentName(item)];
          return <Component key={item.title} handleCheck={handleCheck} handleRemove={() => handleRemove(item.title, item.category)} {...item} />;
        })}
      </div>
    </div>
  );
  
};

export default SupercategoryPage;
