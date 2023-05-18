import React from 'react';
import TitleAttribute from './AttributeComponents/TitleAttribute';
import CheckboxAttribute from './AttributeComponents/CheckboxAttribute';

const BaseElement = ({ title, done, category, handleCheck, handleRemove, children }) => (
  <div>
    {done}
    
    <CheckboxAttribute done={done} handleCheck={handleCheck} title={title} category={category} />
    <button onClick={handleRemove}>Delete</button>
    <TitleAttribute value={title} />
    {children}
  </div>
);

export default BaseElement;
