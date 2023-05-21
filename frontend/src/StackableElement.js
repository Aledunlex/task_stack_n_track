import React from 'react';
import BaseElement from './BaseElement';
import TextAttribute from './AttributeComponents/TextAttribute';

const StackableElement = ({ title, category, done, handleCheck, handleRemove, stackable_properties }) => (
  <BaseElement title={title} category={category} done={done} handleRemove={handleRemove} handleCheck={handleCheck}>
    {Object.entries(stackable_properties).map(([key, value]) => (
      <div key={key}>
        {key}: {value}
      </div>
    ))}
  </BaseElement>
);


export default StackableElement;