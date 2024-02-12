// pages/dashboard.js
"use client";
import { useState } from 'react';

export default function Dashboard() {
  const [period, setPeriod] = useState('today');

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
      {/* Здесь должна быть логика для отображения статистики в зависимости от выбранного периода */}
      <div>Статистика для периода: {period}</div>
    </div>
  );
}
