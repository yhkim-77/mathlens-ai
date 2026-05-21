import {createSlice, createAsyncThunk} from '@reduxjs/toolkit';
import {problemsApi} from '../../services/api';

export interface Problem {
  id: string;
  title: string;
  content: string;
  difficulty: string;
  concept_tags: string[];
  subject: string;
}

interface ProblemsState {
  list: Problem[];
  recommended: Problem[];
  loading: boolean;
  error: string | null;
}

const initialState: ProblemsState = {
  list: [],
  recommended: [],
  loading: false,
  error: null,
};

export const fetchProblems = createAsyncThunk(
  'problems/fetch',
  async (token: string) => {
    return await problemsApi.list(token);
  },
);

export const fetchRecommended = createAsyncThunk(
  'problems/recommended',
  async ({userId, token}: {userId: string; token: string}) => {
    return await problemsApi.recommend(userId, token);
  },
);

const problemsSlice = createSlice({
  name: 'problems',
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(fetchProblems.pending, state => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProblems.fulfilled, (state, action) => {
        state.loading = false;
        state.list = action.payload;
      })
      .addCase(fetchProblems.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? '문제 목록을 불러오는데 실패했습니다. 다시 시도해주세요.';
      })
      .addCase(fetchRecommended.fulfilled, (state, action) => {
        state.recommended = action.payload;
      });
  },
});

export default problemsSlice.reducer;
