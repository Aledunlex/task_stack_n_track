import React, { useState } from 'react';

export const BaseElementForm = ({ onSubmit, children }) => {
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('');

  const handleTitleChange = (event) => setTitle(event.target.value);
  const handleCategoryChange = (event) => setCategory(event.target.value);

  const handleSubmit = (event) => {
    event.preventDefault();

    onSubmit({ title, category });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={title} onChange={handleTitleChange} placeholder="Title" />
      <input type="text" value={category} onChange={handleCategoryChange} placeholder="Category" />
      {children}
    </form>
  );
};

export const QuestElementForm = ({ onSubmit }) => {
  const [solution, setSolution] = useState('');
  const [reward, setReward] = useState('');

  const handleSolutionChange = (event) => setSolution(event.target.value);
  const handleRewardChange = (event) => setReward(event.target.value);

  const handleSubmit = (formData) => {
    onSubmit({ ...formData, type:'quest', solution, reward });
  };

  return (
    <BaseElementForm onSubmit={handleSubmit}>
      <input type="text" value={solution} onChange={handleSolutionChange} placeholder="Solution" />
      <input type="text" value={reward} onChange={handleRewardChange} placeholder="Reward" />
      <button type="submit">Add element</button>
    </BaseElementForm>
  );
};

export const StackableElementForm = ({ onSubmit }) => {
  const [propertyName, setPropertyName] = useState('');
  const [propertyValue, setPropertyValue] = useState('');
  const [properties, setProperties] = useState({});

  const handlePropertyNameChange = (event) => setPropertyName(event.target.value);
  const handlePropertyValueChange = (event) => setPropertyValue(event.target.value);

  const handleAddProperty = (event) => {
    event.preventDefault();
    setProperties({ ...properties, [propertyName]: propertyValue });
    setPropertyName('');
    setPropertyValue('');
  };

  const handleRemoveProperty = (propertyToRemove) => {
    setProperties(Object.fromEntries(Object.entries(properties).filter(([property]) => property !== propertyToRemove)));
  };

  const handleSubmit = (formData) => {
    onSubmit({ ...formData, type: 'stackable', stackable_properties: properties });
  };

  return (
    <BaseElementForm onSubmit={handleSubmit}>
      <div>
        <input type="text" value={propertyName} onChange={handlePropertyNameChange} placeholder="Property name" />
        <input type="text" value={propertyValue} onChange={handlePropertyValueChange} placeholder="Property value" />
        <button onClick={handleAddProperty}>Add property</button>
      </div>
      <ul>
        {Object.entries(properties).map(([property, value]) => (
          <li key={property}>
            {property}: {value}
            <button onClick={() => handleRemoveProperty(property)}>Remove</button>
          </li>
        ))}
      </ul>
      <button type="submit">Create Stackable</button>
    </BaseElementForm>
  );
};


