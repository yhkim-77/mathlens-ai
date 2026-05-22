const BASE_URL = process.env.API_BASE_URL ?? 'http://10.0.2.2:8000';

async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
    ...options,
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error((body as {detail?: string}).detail ?? res.statusText);
  }

  return res.json() as Promise<T>;
}

function authHeader(token: string): {Authorization: string} {
  return {Authorization: `Bearer ${token}`};
}

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

interface UserResponse {
  id: string;
  email: string;
  display_name?: string;
  grade?: string;
}

export const authApi = {
  async login(email: string, password: string): Promise<TokenResponse> {
    const body = new URLSearchParams();
    body.append('username', email);
    body.append('password', password);
    const res = await fetch(`${BASE_URL}/api/v1/auth/token`, {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: body.toString(),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error((data as {detail?: string}).detail ?? res.statusText);
    }
    return res.json() as Promise<TokenResponse>;
  },

  async register(
    email: string,
    password: string,
    displayName?: string,
    grade?: string,
  ): Promise<TokenResponse> {
    return request<TokenResponse>('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify({email, password, display_name: displayName, grade}),
    });
  },

  async me(token: string): Promise<UserResponse> {
    return request<UserResponse>('/api/v1/auth/me', {
      headers: authHeader(token),
    });
  },
};

interface AnalysisResponse {
  submission_id: string;
  is_correct: boolean;
  error_type?: string;
  error_step?: number;
  feedback: string;
  correct_solution?: string;
  concept_tags?: string[];
}

export const analysisApi = {
  async analyze(
    imageBase64: string,
    recognizedLatex: string,
    userId: string,
    grade: string,
    token: string,
  ): Promise<AnalysisResponse> {
    return request<AnalysisResponse>('/api/v1/analyze', {
      method: 'POST',
      headers: authHeader(token),
      body: JSON.stringify({
        image_base64: imageBase64,
        recognized_latex: recognizedLatex,
        user_id: userId,
        student_grade: grade,
      }),
    });
  },
};

interface Problem {
  id: string;
  title: string;
  content: string;
  difficulty: string;
  concept_tags: string[];
  subject: string;
}

export const problemsApi = {
  async list(token: string): Promise<Problem[]> {
    return request<Problem[]>('/api/v1/problems', {
      headers: authHeader(token),
    });
  },

  async recommend(userId: string, token: string): Promise<Problem[]> {
    return request<Problem[]>(
      `/api/v1/problems/recommend?user_id=${userId}`,
      {headers: authHeader(token)},
    );
  },
};
