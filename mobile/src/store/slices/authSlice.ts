import {createSlice, createAsyncThunk} from '@reduxjs/toolkit';
import {authApi} from '../../services/api';

interface User {
  id: string;
  email: string;
  display_name?: string;
  grade?: string;
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  accessToken: null,
  refreshToken: null,
  loading: false,
  error: null,
};

export const login = createAsyncThunk(
  'auth/login',
  async ({email, password}: {email: string; password: string}) => {
    const tokens = await authApi.login(email, password);
    const user = await authApi.me(tokens.access_token);
    return {tokens, user};
  },
);

export const register = createAsyncThunk(
  'auth/register',
  async ({
    email,
    password,
    displayName,
    grade,
  }: {
    email: string;
    password: string;
    displayName?: string;
    grade?: string;
  }) => {
    const tokens = await authApi.register(email, password, displayName, grade);
    const user = await authApi.me(tokens.access_token);
    return {tokens, user};
  },
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout(state) {
      state.user = null;
      state.accessToken = null;
      state.refreshToken = null;
    },
    clearError(state) {
      state.error = null;
    },
  },
  extraReducers: builder => {
    builder
      .addCase(login.pending, state => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.accessToken = action.payload.tokens.access_token;
        state.refreshToken = action.payload.tokens.refresh_token;
        state.user = action.payload.user;
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? '로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.';
      })
      .addCase(register.pending, state => {
        state.loading = true;
        state.error = null;
      })
      .addCase(register.fulfilled, (state, action) => {
        state.loading = false;
        state.accessToken = action.payload.tokens.access_token;
        state.refreshToken = action.payload.tokens.refresh_token;
        state.user = action.payload.user;
      })
      .addCase(register.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? '회원가입에 실패했습니다. 다시 시도해주세요.';
      });
  },
});

export const {logout, clearError} = authSlice.actions;
export default authSlice.reducer;
