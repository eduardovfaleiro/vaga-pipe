const API = process.env.NEXT_PUBLIC_API_URL;

export async function fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
  let token = typeof window !== 'undefined' ? sessionStorage.getItem('access_token') : null;

  const makeRequest = (t?: string | null) =>
    fetch(`${API}${url}`, {
      ...options,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
        ...(t ? { Authorization: `Bearer ${t}` } : {}),
      },
    });

  let res = await makeRequest(token);

  if (res.status === 401) {
    const refreshRes = await fetch(`${API}/auth/refresh`, {
      method: 'POST',
      credentials: 'include',
    });

    if (refreshRes.ok) {
      const { access_token } = await refreshRes.json();
      if (typeof window !== 'undefined') {
        sessionStorage.setItem('access_token', access_token);
      }
      res = await makeRequest(access_token);
    } else {
      if (typeof window !== 'undefined') {
        sessionStorage.removeItem('access_token');
        window.location.href = '/login';
      }
      throw new Error('Session expired');
    }
  }

  return res;
}

type PydanticError = { msg: string; loc?: string[] };

export function extractError(detail: unknown): string {
  if (!detail) return 'Erro desconhecido';
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((e: PydanticError) => e.msg ?? JSON.stringify(e))
      .join('; ');
  }
  return JSON.stringify(detail);
}

export async function apiFetch(url: string, options: RequestInit = {}): Promise<Response> {
  return fetch(`${API}${url}`, {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
}
