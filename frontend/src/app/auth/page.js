// В начале файла добавьте импорт Axios
"use client";
import axios from "axios";
import { useState } from "react";
import { useRouter } from 'next/navigation'
export default function Auth() {
  const router = useRouter();

  let [isLogin, setIsLogin] = useState(true);
  const [username, setUserName] = useState("");
  const [last_name, setLastName] = useState("");
  const [first_name, setFirstName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    const user = {
      username,
      first_name,
      last_name,
      email,
      password,
    };

    try {
      if (!isLogin) {
        // Make the request to the Next.js API route proxy
        const response = await axios.post("http://localhost:8000/api/users/", user);
        console.log("Регистрация успешна:", response.data);
        setIsLogin(true)
        // Handle successful registration
      } else {
        const user = {
          email,
        password
        }
        const response = await axios.post("http://localhost:8000/api/auth/jwt/create/", user)
        // Handle login logic
        console.log("Авторизация успешна:", response.data);
        document.cookie = `${"jwt=" + response.data.access}`
        router.push('/dashboard');
      }
    } catch (error) {
      console.error("Ошибка при регистрации:", error.response ? error.response.data : error);
      // Handle errors
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-100">
      <div className="p-8 bg-white shadow-md rounded">
        <h2 className="text-xl mb-4">
          {isLogin ? "Вход в систему" : "Регистрация"}
        </h2>
        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <>
              <input
                type="text"
                placeholder="Никнейм"
                className="mb-4 px-4 py-2 border rounded w-full"
                value={username}
                onChange={(e) => setUserName(e.target.value)}
              />
              <input
                type="firstName"
                placeholder="Имя"
                className="mb-4 px-4 py-2 border rounded w-full"
                value={first_name}
                onChange={(e) => setFirstName(e.target.value)}
              />
              <input
                type="secondName"
                placeholder="Фамилия"
                className="mb-4 px-4 py-2 border rounded w-full"
                value={last_name}
                onChange={(e) => setLastName(e.target.value)}
              />
            </>
          )}

          <input
            type="email"
            placeholder="Email"
            className="mb-4 px-4 py-2 border rounded w-full"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Пароль"
            className="mb-4 px-4 py-2 border rounded w-full"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded w-full"
          >
            {isLogin ? "Войти" : "Зарегистрироваться"}
          </button>
        </form>
        <button
          onClick={() => setIsLogin(!isLogin)}
          className="mt-4 text-sm text-blue-500"
        >
          {isLogin ? "Создать аккаунт" : "У меня уже есть аккаунт"}
        </button>
      </div>
    </div>
  );
}
