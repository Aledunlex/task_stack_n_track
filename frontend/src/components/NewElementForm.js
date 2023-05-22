import React, { useState } from 'react';
import { toast } from 'react-toastify';
import { addElement } from '../services/elementService';
import { QuestElementForm, StackableElementForm } from './ComponentNewElementForm';

const NewElementForm = ({ supercategory, addNewElement }) => {
  const [elementType, setElementType] = useState('');

  const handleTypeChange = (event) => setElementType(event.target.value);

  const handleSubmit = async (newElementData) => {
    const newElement = { ...newElementData, supercategory, done: false };
    const result = await addElement(newElement);
    if (result.success) {
      toast.success(`Item ${result.element.title} successfully created!`);
      addNewElement(result.element);
    } else {
      toast.error('Failed to create new item.');
    }
  };

  let form;
  switch (elementType) {
    case 'stackable':
      form = <StackableElementForm onSubmit={handleSubmit} />;
      break;
    case 'quest':
      form = <QuestElementForm onSubmit={handleSubmit} />;
      break;
    default:
      form = null;
  }

  return (
    <div>
      <select value={elementType} onChange={handleTypeChange}>
        <option value="">--Select element type--</option>
        <option value="stackable">StackableElement</option>
        <option value="quest">QuestElement</option>
      </select>

      {form}
    </div>
  );
};

export default NewElementForm;
