// pages/_app.js
import { Provider } from 'react-redux';
import store from '../store'; // Подключите ваше Redux хранилище

function MyApp({ Component, pageProps }) {
  return (
    <Provider store={store}>
      <Component {...pageProps} />
    </Provider>
  );
}

export default MyApp;
