"use client";
import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [period, setPeriod] = useState('today');

  useEffect(() => {
    // Создаем новое WebSocket соединение
    const socket = new WebSocket('ws://127.0.0.1:8000/ws/notifications/');

    socket.onopen = () => {
      console.log('Connected to server');
    };

    socket.onmessage = (event) => {
      // Обрабатываем сообщения, полученные от сервера
      console.log('Message from server ', event.data);
    };

    socket.onclose = () => {
      console.log('Disconnected from server');
    };

    socket.onerror = (error) => {
      console.log('WebSocket error: ', error);
    };

    // Очистка при размонтировании компонента
    return () => {
      socket.close();
    };
  }, []); // Пустой массив зависимостей гарантирует, что эффект выполнится один раз после монтирования компонента

  return (
    <div className="p-8">
      <h1 className="text-xl mb-4">Дашборд</h1>
      <select
        value={period}
        onChange={(e) => setPeriod(e.target.value)}
        className="mb-4 px-4 py-2 border rounded"
      >
        <option value="lastHour">За последний час</option>
        <option value="today">Сегодня</option>
        <option value="yesterday">Вчера</option>
        <option value="lastWeek">За последнюю неделю</option>
        <option value="lastMonth">За последний месяц</option>
      </select>
      <div>Статистика для периода: {period}</div>
    </div>
  );
}