import {configureStore} from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import analysisReducer from './slices/analysisSlice';
import problemsReducer from './slices/problemsSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    analysis: analysisReducer,
    problems: problemsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
