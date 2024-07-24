import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const DeviceForm = ({ onSave, onClose }) => {
  const [name, setName] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.post('http://localhost:8000/api/devices/', { name });
      onSave();
      onClose();
    } catch (error) {
      console.error('Ошибка при создании устройства:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Создать новое устройство</h3>
      <label>
        Название:
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
      </label>
      <button type="submit">Создать</button>
      <button type="button" onClick={onClose}>Отменить</button>
    </form>
  );
};

const Devices = () => {
  const [devices, setDevices] = useState([]);
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    fetchDevices();
  }, []);

  const fetchDevices = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/devices/');
      setDevices(response.data);
    } catch (error) {
      console.error('Ошибка при загрузке устройств:', error);
    }
  };

  const handleSave = () => {
    fetchDevices();
    setIsCreating(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Устройства</h1>
        <button onClick={() => setIsCreating(true)}>
          Создать новое устройство
        </button>
        {isCreating && <DeviceForm onSave={handleSave} onClose={() => setIsCreating(false)} />}
        <ul>
          {devices.map(device => (
            <li key={device.id}>
              <Link to={`/devices/${device.id}/`}>{device.name}</Link>
            </li>
          ))}
        </ul>
      </header>
    </div>
  );
};

export default Devices;
