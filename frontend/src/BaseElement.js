import React from 'react';
import TitleAttribute from './AttributeComponents/TitleAttribute';
import CheckboxAttribute from './AttributeComponents/CheckboxAttribute';

const BaseElement = ({ title, done, category, handleCheck, children }) => (
  <div>
    {done}
    <TitleAttribute value={title} />
    <CheckboxAttribute done={done} handleCheck={handleCheck} title={title} category={category} />
    {children}
  </div>
);

export default BaseElement;
