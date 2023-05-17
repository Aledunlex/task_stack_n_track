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

export const deleteElement = async (title, category) => {
  await axios.delete(`http://localhost:8080/api/deleteElement`, {
    data: { title: title, category: category },
  });
};

export const addElement = async (element) => { // ajouter supercategory?
  const response = await axios.post(`http://localhost:8080/api/addElement`, element);
  return response.data;
};
