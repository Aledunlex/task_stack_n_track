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

  const handleSubmit = (formData) => {
    onSubmit({ ...formData, type:'stackable' });
  };

  return (
    <BaseElementForm onSubmit={handleSubmit}>
      <button type="submit">Add element</button>
    </BaseElementForm>
  );
};
