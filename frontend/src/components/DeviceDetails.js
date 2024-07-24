import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const DeviceEditForm = ({ device, onSave, onClose }) => {
  const [name, setName] = useState(device ? device.name : '');
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.put(`http://localhost:8000/api/devices/${device.id}/`, { name });
      onSave();
      onClose();
    } catch (error) {
      console.error('Ошибка при обновлении устройства:', error);
      setError('Ошибка при обновлении устройства');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Редактировать устройство</h3>
      {error && <p className="error">{error}</p>}
      <label>
        Название:
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </label>
      <button type="submit">Обновить</button>
      <button type="button" onClick={onClose}>Отменить</button>
    </form>
  );
};

const DeviceDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [device, setDevice] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [batteries, setBatteries] = useState([]);
  const [selectedBattery, setSelectedBattery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        await Promise.all([fetchDevice(), fetchBatteries()]);
      } catch (error) {
        setError('Ошибка при загрузке данных');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchData();
    }
  }, [id]);

  const fetchDevice = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/devices/${id}/`);
      setDevice(response.data);
    } catch (error) {
      console.error('Ошибка при загрузке устройства:', error);
      setError('Ошибка при загрузке устройства');
    }
  };

  const fetchBatteries = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/batteries/');
      setBatteries(response.data);
    } catch (error) {
      console.error('Ошибка при загрузке аккумуляторов:', error);
      setError('Ошибка при загрузке аккумуляторов');
    }
  };

  const handleDelete = async () => {
    try {
      await axios.delete(`http://localhost:8000/api/devices/${id}/`);
      navigate('/devices/');
    } catch (error) {
      console.error('Ошибка при удалении устройства:', error);
      setError('Ошибка при удалении устройства');
    }
  };

  const handleSave = () => {
    fetchDevice();
    setIsEditing(false);
  };

  const handleAttachBattery = async () => {
    if (!selectedBattery) {
      setError('Выберите аккумулятор для привязки');
      return;
    }

    try {
      await axios.post(`http://localhost:8000/api/devices/${id}/batteries/${selectedBattery}/attach`);
      fetchDevice();
      setSelectedBattery('');
      setError('');
    } catch (error) {
      console.error('Ошибка при привязке аккумулятора:', error);
      setError('Ошибка при привязке аккумулятора');
    }
  };

  if (loading) {
    return (
      <div className="App">
        <header className="App-header">
          <p>Загрузка...</p>
        </header>
      </div>
    );
  }

  if (error) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>{error}</h1>
          <button onClick={() => navigate('/devices/')}>Назад к списку устройств</button>
        </header>
      </div>
    );
  }

  if (device === null) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Устройство не найдено</h1>
          <button onClick={() => navigate('/devices/')}>Назад к списку устройств</button>
        </header>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Детали устройства</h1>
        {device ? (
          <>
            {isEditing ? (
              <DeviceEditForm device={device} onSave={handleSave} onClose={() => setIsEditing(false)} />
            ) : (
              <div>
                <h2>{device.name}</h2>
                <button onClick={() => setIsEditing(true)}>Редактировать</button>
                <button onClick={handleDelete}>Удалить</button>
              </div>
            )}
            <div>
              <h3>Подключенные аккумуляторы</h3>
              <ul>
                {device.batteries && device.batteries.length > 0 ? (
                  device.batteries.map((battery) => (
                    <li key={battery.id}>{battery.name}</li>
                  ))
                ) : (
                  <p>Нет подключенных аккумуляторов</p>
                )}
              </ul>
              <h3>Добавить аккумулятор</h3>
              <select
                value={selectedBattery}
                onChange={(e) => setSelectedBattery(e.target.value)}
              >
                <option value="">Выберите аккумулятор</option>
                {batteries.map((battery) => (
                  <option key={battery.id} value={battery.id}>
                    {battery.name}
                  </option>
                ))}
              </select>
              <button onClick={handleAttachBattery} disabled={!selectedBattery}>
                Добавить аккумулятор
              </button>
            </div>
          </>
        ) : (
          <p>Загрузка...</p>
        )}
      </header>
    </div>
  );
};

export default DeviceDetails;
