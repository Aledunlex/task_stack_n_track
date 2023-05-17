import React from 'react';

const CheckboxAttribute = ({ done, handleCheck, title, category }) => {
  const onChange = (event) => {
    handleCheck(title, category, event.target.checked);
  };

  return (
    <div>
      Done: <input type="checkbox" checked={done} onChange={onChange} />
    </div>
  );
};

export default CheckboxAttribute;
