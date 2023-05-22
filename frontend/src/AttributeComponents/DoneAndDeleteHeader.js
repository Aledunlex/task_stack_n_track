import React from 'react';

const DoneAndDeleteHeader = ({ done, handleCheck, handleRemove, title, category }) => {
  const onChange = (event) => {
    handleCheck(title, category, event.target.checked);
  };

  return (
    <div className="title-and-done">
      <div>
        Done: <input type="checkbox" checked={done} onChange={onChange} />
      </div>
      <button className="delete-button" onClick={handleRemove}>X</button>
    </div>
  );
};

export default DoneAndDeleteHeader;
