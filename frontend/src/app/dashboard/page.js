"use client";
import { useState } from 'react';
import useWebSocket from 'react-use-websocket';

export default function Dashboard() {
  const [period, setPeriod] = useState('today');

  // Настройка WebSocket соединения
  const { lastMessage, sendJsonMessage, readyState } = useWebSocket('ws://127.0.0.1:8000/ws/notifications/', {
    onOpen: () => console.log('Connected to server'),
    // Параметры reconnect позволяют автоматически переподключаться
    shouldReconnect: (closeEvent) => true, // Будет пытаться переподключиться при любом закрытии соединения
    reconnectInterval: 3000, // Переподключение каждые 3000 мс
    reconnectAttempts: 10, // Максимальное количество попыток переподключения
  });

  // Функция для отправки сообщений на сервер (при необходимости)
  const sendMessage = () => {
    sendJsonMessage({ message: 'Привет сервер!' });
  };

  // Обработка полученных сообщений
  const message = lastMessage ? lastMessage.data : null;

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
      <div>Последнее сообщение: {message}</div>
      {/* Пример кнопки для отправки сообщений */}
      <button onClick={sendMessage} disabled={readyState !== WebSocket.OPEN}>Отправить сообщение</button>
    </div>
  );
}

