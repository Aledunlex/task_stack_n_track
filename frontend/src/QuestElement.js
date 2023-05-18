import React from 'react';
import BaseElement from './BaseElement';
import TextAttribute from './AttributeComponents/TextAttribute';

const QuestElement = ({ title, category, done, handleCheck, handleRemove, reward, solution }) => (
  <BaseElement title={title} category={category} done={done} handleRemove={handleRemove} handleCheck={handleCheck}>
    <TextAttribute value={reward} />
    <TextAttribute value={solution} />
  </BaseElement>
);

export default QuestElement;
