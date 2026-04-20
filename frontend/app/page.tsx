import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';

export default async function Home() {
  const cookieStore = await cookies();
  const hasRefresh = cookieStore.has('refresh_token');
  if (hasRefresh) {
    redirect('/dashboard');
  }
  redirect('/login');
}
