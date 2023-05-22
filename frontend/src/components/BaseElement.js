import React from 'react';
import './BaseElement.css';
import TitleAttribute from '../attributeComponents/TitleAttribute';
import DoneAndDeleteHeader from '../attributeComponents/DoneAndDeleteHeader';

const BaseElement = ({ title, done, category, handleCheck, handleRemove, children, transferData }) => (
  <div className="base-element"
       draggable="true"
       onDragStart={(e) => {
        const data = JSON.stringify({title, category, done, ...transferData});
        e.dataTransfer.setData("application/json", data);
       }}
  >
    <DoneAndDeleteHeader done={done} handleCheck={handleCheck} handleRemove={handleRemove} title={title} category={category} />
    <TitleAttribute value={title} />
    {children}
  </div>
);

export default BaseElement;
