import { useState } from 'react';

import componentMapping from './componentMapping';

const Workbench = ({ workbenchItems, setWorkbenchItems }) => {
  const [isWorkbenchVisible, setIsWorkbenchVisible] = useState(true);

  const handleToggleWorkbench = () => {
    setIsWorkbenchVisible((prevState) => !prevState);
  };

  const getComponentName = (item) => {
    if (item.reward && item.solution) {
      return 'quest';
    }
    if (item.stackable_properties) {
      return 'stackable';
    }
    return 'base';
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const data = JSON.parse(e.dataTransfer.getData("application/json"));
    if (workbenchItems.find((item) => item.title === data.title)) {
      return;
    }
    // if the source or the target are not StackableElements, add the element to the workbench
    if (!data.stackable_properties || !workbenchItems.some((item) => item.stackable_properties)) {
      setWorkbenchItems((prevItems) => [...prevItems, data]);
      return;
    }
    // if the source and the target are StackableElements, merge them on the element already on the workbench
    const target = workbenchItems.find((item) => item.stackable_properties);
    handleStack(target, data);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleRemove = (title) => {
    setWorkbenchItems((prevItems) =>
      prevItems.filter((item) => item.title !== title)
    );
  };

  const mergeStackableProperties = (obj1, obj2) => {
  const result = { ...obj1 };
  for (const key in obj2) {
    if (result.hasOwnProperty(key)) {
      result[key] = (parseInt(result[key]) + parseInt(obj2[key])).toString();
    } else {
      result[key] = obj2[key];
    }
  }
  return result;
};

  // If the source and the target are StackableElements, merge them on the element already on the workbench
  const handleStack = (target, source) => {
    const targetIndex = workbenchItems.findIndex(
      (item) => item.title === target.title
    );
    const newTitle = `${target.title} + ${source.title}`;
    const newStackableProperties = mergeStackableProperties(
      target.stackable_properties,
      source.stackable_properties
    );
    // sort the stackable properties by value when they're numerical, then alphabetically by key
    const sortedStackableProperties = Object.fromEntries(
      Object.entries(newStackableProperties).sort(([, a], [, b]) => {
        if (isNaN(a) || isNaN(b)) {
          return a.localeCompare(b);
        }
        return parseInt(b) - parseInt(a);
      })
    );
    const newWorkbenchItems = [...workbenchItems];
    newWorkbenchItems[targetIndex] = {
      ...target,
      title: newTitle,
      stackable_properties: sortedStackableProperties,
    };
    setWorkbenchItems(newWorkbenchItems);
  };
  
    

  return (
    <div
      className={`workbench ${isWorkbenchVisible ? '' : 'workbench--hidden'}`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      <button className='toggle-workbench' onClick={handleToggleWorkbench}>
        {isWorkbenchVisible ? 'Cacher le workbench' : 'Afficher le workbench'}
      </button>
      {workbenchItems.map((item) => {
        const Component = componentMapping[getComponentName(item)];
        return <Component key={item.title} {...item}  handleCheck={() => console.log(item.title)} handleRemove={() => handleRemove(item.title)} {...item} />;
      })}
    </div>
  );
  
};

export default Workbench;