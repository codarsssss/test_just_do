import { createStore } from 'redux';
import rootReducer from './reducers'; // Подключите корневой редюсер

const store = createStore(rootReducer);

export default store;
