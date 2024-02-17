// reducers.js
import { combineReducers } from 'redux';
import userReducer from './userReducer'; // Подключите редюсер пользователя и другие редюсеры, если есть

const rootReducer = combineReducers({
  user: userReducer,
  // Другие редюсеры...
});

export default rootReducer;
