// pages/admin.js
'use client';
import Dashboard from '../dashboard/page'; // Используйте компонент Dashboard как основу

export default function Admin() {
  const handleSubmit = (event) => {
    event.preventDefault();
    // Логика отправки сообщения
    console.log("Сообщение отправлено");
  };

  return (
    <div>
      <Dashboard />
      <div className="p-8">
        <h2 className="text-xl mb-4">Отправка сообщения</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Имя пользователя (опционально)"
            className="mb-4 px-4 py-2 border rounded w-full"
          />
          <textarea
            placeholder="Сообщение"
            className="mb-4 px-4 py-2 border rounded w-full"
          ></textarea>
          <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
            Отправить
          </button>
        </form>
      </div>
    </div>
  );
}
