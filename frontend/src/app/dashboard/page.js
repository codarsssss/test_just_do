"use client";
import { useState, useEffect } from 'react';
import useWebSocket from 'react-use-websocket';
import {jwtDecode} from "jwt-decode";
import axios from "axios";

export default function Dashboard() {
  const [period, setPeriod] = useState('today');
  const [notificationType, setNotificationType] = useState('info');
  const [notificationMessage, setNotificationMessage] = useState('');
  const [recipientID, setRecipientID] = useState(0);
  const [notifications, setNotifications] = useState({});

  const isSuperuser = localStorage.getItem('isSuperuser') === 'true';

  // Настройка WebSocket соединения
  const { lastMessage, sendJsonMessage, readyState } = useWebSocket('ws://127.0.0.1:8000/ws/notifications/', {
    onOpen: () => console.log('Connected to server'),
    // Параметры reconnect позволяют автоматически переподключаться
    shouldReconnect: (closeEvent) => true, // Будет пытаться переподключиться при любом закрытии соединения
    reconnectInterval: 3000, // Переподключение каждые 3000 мс
    reconnectAttempts: 10, // Максимальное количество попыток переподключения
  });

  // Функция для отправки сообщений на сервер
  const sendMessage = () => {
    sendJsonMessage({ message: notificationMessage, status: notificationType, recipient_id: recipientID ? recipientID : null });
  };

  // Запрос на получение данных о уведомлениях с бэкенда
  useEffect(() => {
    async function fetchNotifications() {
      try {
        const response = await axios.get('http://localhost:8000/api/notifications/',  {withCredentials: true,
  credentials: 'include', mode: 'no-cors', headers: {'Access-Control-Allow-Origin': '*',}, });
        if (!response.ok) {
          console.log(response)
          throw new Error('Ошибка загрузки данных о уведомлениях');
        }
        const data = await response.json();
        setNotifications(data);
      } catch (error) {
        console.error(error);
      }
    }

    fetchNotifications();
  }, []); // [] - пустой массив зависимостей, чтобы запрос отправлялся только один раз при загрузке страницы

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
      {isSuperuser && (
        <div className='admin-form'>
          <input type="number" value={recipientID} onChange={(e) => setRecipientID(e.target.value)} />
          <input type="text" value={notificationMessage} onChange={(e) => setNotificationMessage(e.target.value)} />
          <select value={notificationType} onChange={(e) => setNotificationType(e.target.value)}>
            <option value="info">Информационное</option>
            <option value="warning">Оповещение</option>
            <option value="error">Ошибка</option>
          </select>
          <button onClick={sendMessage}>Отправить</button>
        </div>
      )}
    </div>
  );
}
