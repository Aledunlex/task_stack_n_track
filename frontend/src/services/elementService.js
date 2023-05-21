import axios from 'axios';

export const updateElement = async (title, category, done) => {
  const newDoneStatus = done;

  await axios.put(`http://localhost:8080/api/updateElement`, {
    title: title,
    category: category,
    done: newDoneStatus
  });

  return newDoneStatus;
};

export const removeElement = async (title, category) => {
  try {
  const response = await axios.delete(`http://localhost:8080/api/removeElement`, {
    data: {
      title: title,
      category: category 
    }
  });
  
  return response.data.success;
  } catch (error) {
    return error;
  }
};

export const addElement = async (element) => {
  const response = await axios.post(`http://localhost:8080/api/addElement`, element);
  return response.data;
};
