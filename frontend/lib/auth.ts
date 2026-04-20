export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return sessionStorage.getItem('access_token');
}

export function setToken(token: string): void {
  sessionStorage.setItem('access_token', token);
}

export function clearToken(): void {
  sessionStorage.removeItem('access_token');
}

export function getUserId(): string | null {
  if (typeof window === 'undefined') return null;
  const token = sessionStorage.getItem('access_token');
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.sub ?? null;
  } catch {
    return null;
  }
}
