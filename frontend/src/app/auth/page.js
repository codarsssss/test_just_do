// В начале файла добавьте импорт Axios
"use client";
import axios from "axios";
import { useState } from "react";
import { useRouter } from 'next/navigation';
import { jwtDecode } from 'jwt-decode';
import { CookiesProvider, useCookies } from 'react-cookie';



export default function Auth() {
  const router = useRouter();
  const [cookies, setCookie] = useCookies(['jwt'])
  let [isLogin, setIsLogin] = useState(true);
  const [username, setUserName] = useState("");
  const [last_name, setLastName] = useState("");
  const [first_name, setFirstName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  function getCookie(name) {
  let cookies = document.cookie; // Получаем строку всех куки
  let parts = cookies.split('; '); // Разделяем куки на части
  for(let i = 0; i < parts.length; i++) {
    let part = parts[i];
    let [key, value] = part.split('='); // Разделяем каждую часть на ключ и значение
    if (key === name) {
      return value; // Возвращаем значение, если нашли нужный ключ
    }
  }
    return null; // Возвращаем null, если куки с таким ключом нет
  }


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

        setCookie('jwt', response.data.access, { path: '/', httpOnly: true})
        // document.cookie = `${"jwt=" + response.data.access}`
        const decodedToken = jwtDecode(response.data.access);
        localStorage.setItem('isSuperuser', decodedToken.is_superuser)
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
