import {createSlice, createAsyncThunk} from '@reduxjs/toolkit';
import {analysisApi} from '../../services/api';

export interface AnalysisResult {
  submission_id: string;
  is_correct: boolean;
  error_type?: string;
  error_step?: number;
  feedback: string;
  correct_solution?: string;
  concept_tags?: string[];
}

interface AnalysisState {
  current: AnalysisResult | null;
  history: AnalysisResult[];
  loading: boolean;
  error: string | null;
}

const initialState: AnalysisState = {
  current: null,
  history: [],
  loading: false,
  error: null,
};

export const submitAnalysis = createAsyncThunk(
  'analysis/submit',
  async ({
    imageBase64,
    recognizedLatex,
    userId,
    grade,
    token,
  }: {
    imageBase64: string;
    recognizedLatex: string;
    userId: string;
    grade: string;
    token: string;
  }) => {
    return await analysisApi.analyze(imageBase64, recognizedLatex, userId, grade, token);
  },
);

const analysisSlice = createSlice({
  name: 'analysis',
  initialState,
  reducers: {
    clearCurrent(state) {
      state.current = null;
    },
  },
  extraReducers: builder => {
    builder
      .addCase(submitAnalysis.pending, state => {
        state.loading = true;
        state.error = null;
      })
      .addCase(submitAnalysis.fulfilled, (state, action) => {
        state.loading = false;
        state.current = action.payload;
        state.history.unshift(action.payload);
      })
      .addCase(submitAnalysis.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? '풀이 분석에 실패했습니다. 네트워크 연결을 확인하고 다시 시도해주세요.';
      });
  },
});

export const {clearCurrent} = analysisSlice.actions;
export default analysisSlice.reducer;
