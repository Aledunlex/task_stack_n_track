import React from 'react';
import BaseElement from './BaseElement';
import StackableProperties from '../attributeComponents/StackableProperties';

const StackableElement = ({ title, category, done, handleCheck, handleRemove, stackable_properties }) => (
  <BaseElement title={title} category={category} done={done} handleRemove={handleRemove} handleCheck={handleCheck} transferData={{stackable_properties}}>
    <StackableProperties stackable_properties={stackable_properties} />
  </BaseElement>
);


export default StackableElement;