import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';


const BatteriesEditForm = ({ batteries, onSave, onClose }) => {
  const [name, setName] = useState(batteries ? batteries.name : '');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.put(`http://localhost:8000/api/batteries/${batteries.id}/`, { name });
      onSave();
      onClose();
    } catch (error) {
      console.error('Ошибка при обновлении аккумулятора:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Редактировать аккумулятор</h3>
      <label>
        Название:
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
      </label>
      <button type="submit">Обновить</button>
      <button type="button" onClick={onClose}>Отменить</button>
    </form>
  );
};

const BatteriesDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [batteries, setBatteries] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    if (id) {
      fetchBatteries();
    }
  }, [id]);

  const fetchBatteries = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/batteries/${id}/`);
      setBatteries(response.data);
    } catch (error) {
      console.error('Ошибка при загрузке аккумулятора:', error);
      setBatteries(null);
    }
  };

  const handleDelete = async () => {
    try {
      await axios.delete(`http://localhost:8000/api/batteries/${id}/`);
      navigate('/batteries/');
    } catch (error) {
      console.error('Ошибка при удалении аккумулятора:', error);
    }
  };

  const handleSave = () => {
    fetchBatteries();
    setIsEditing(false);
  };

  if (batteries === null) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Аккумулятор не найден</h1>
          <button onClick={() => navigate('/batteries/')}>Назад к списку аккумуляторов</button>
        </header>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Детали аккумулятора</h1>
        {batteries ? (
          <>
            {isEditing ? (
              <BatteriesEditForm batteries={batteries} onSave={handleSave} onClose={() => setIsEditing(false)} />
            ) : (
              <div>
                <h2>{batteries.name}</h2>
                <button onClick={() => setIsEditing(true)}>Редактировать</button>
                <button onClick={handleDelete}>Удалить</button>
              </div>
            )}
          </>
        ) : (
          <p>Загрузка...</p>
        )}
      </header>
    </div>
  );
};

export default BatteriesDetails;
