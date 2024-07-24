import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const BatteriesForm = ({ onSave, onClose }) => {
  const [name, setName] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.post('http://localhost:8000/api/batteries/', { name });
      onSave();
      onClose();
    } catch (error) {
      console.error('Ошибка при создании аккумулятора:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Создать новый аккумулятор</h3>
      <label>
        Название:
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
      </label>
      <button type="submit">Создать</button>
      <button type="button" onClick={onClose}>Отменить</button>
    </form>
  );
};

const Batteries = () => {
  const [batteries, setDevices] = useState([]);
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    fetchBatteries();
  }, []);

  const fetchBatteries = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/batteries/');
      setDevices(response.data);
    } catch (error) {
      console.error('Ошибка при загрузке аккумулятора:', error);
    }
  };

  const handleSave = () => {
    fetchBatteries();
    setIsCreating(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Аккумуляторы</h1>
        <button onClick={() => setIsCreating(true)}>
          Создать новый аккумулятор
        </button>
        {isCreating && <BatteriesForm onSave={handleSave} onClose={() => setIsCreating(false)} />}
        <ul>
          {batteries.map(batteries => (
            <li key={batteries.id}>
              <Link to={`/batteries/${batteries.id}/`}>{batteries.name}</Link>
            </li>
          ))}
        </ul>
      </header>
    </div>
  );
};

export default Batteries;
