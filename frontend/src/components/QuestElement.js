import React from 'react';
import BaseElement from './BaseElement';
import TextAttribute from '../attributeComponents/TextAttribute';

const QuestElement = ({ title, category, done, handleCheck, handleRemove, reward, solution }) => (
  <BaseElement title={title} category={category} done={done} handleRemove={handleRemove} handleCheck={handleCheck} transferData={{ reward, solution }}>
    <TextAttribute value={reward} />
    <TextAttribute value={solution} />
  </BaseElement>
);

export default QuestElement;
