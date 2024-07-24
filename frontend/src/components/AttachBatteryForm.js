// src/components/AttachBatteryForm.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AttachBatteryForm = ({ device_id }) => {
  const [batteries, setBatteries] = useState([]);
  const [selectedBattery, setSelectedBattery] = useState('');

  useEffect(() => {
    const fetchBatteries = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/batteries/');
        setBatteries(response.data);
      } catch (error) {
        console.error('Ошибка при загрузке аккумуляторов:', error);
      }
    };

    fetchBatteries();
  }, []);

  const handleAttach = async (event) => {
    event.preventDefault();
    try {
      await axios.post(`http://localhost:8000/api/batteries/${selectedBattery}/attach`, {
        device_id,
      });
      window.location.reload();
    } catch (error) {
      console.error('Ошибка при прикреплении аккумулятора:', error);
    }
  };

  return (
    <form onSubmit={handleAttach}>
      <h3>Прикрепить аккумулятор к устройству</h3>
      <label>
        Выберите аккумулятор:
        <select value={selectedBattery} onChange={(e) => setSelectedBattery(e.target.value)} required>
          <option value="">Выберите аккумулятор</option>
          {batteries.map(battery => (
            <option key={battery.id} value={battery.id}>
              {battery.name}
            </option>
          ))}
        </select>
      </label>
      <button type="submit">Прикрепить</button>
    </form>
  );
};

export default AttachBatteryForm;
