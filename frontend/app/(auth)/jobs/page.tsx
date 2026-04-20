'use client';

import { useEffect, useState } from 'react';
import { fetchWithAuth } from '@/lib/api';
import { JobCard } from '@/components/JobCard';
import { Pagination } from '@/components/Pagination';
import { useAuth } from '@/hooks/useAuth';
import Link from 'next/link';

interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  posted_at: string;
  url: string;
}

const LIMIT = 20;

export default function JobsPage() {
  const { logout } = useAuth();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    setLoading(true);
    const skip = (page - 1) * LIMIT;
    fetchWithAuth(`/jobs?skip=${skip}&limit=${LIMIT}`)
      .then((res) => {
        if (!res.ok) throw new Error('Erro ao carregar vagas');
        return res.json();
      })
      .then(setJobs)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [page]);

  return (
    <div className="min-h-screen bg-zinc-50">
      <nav className="bg-white border-b border-zinc-200 px-4 py-3 flex items-center justify-between">
        <span className="font-semibold text-zinc-900">Vagas</span>
        <div className="flex items-center gap-4 text-sm">
          <Link href="/dashboard" className="text-zinc-600 hover:text-zinc-900">
            Recomendações
          </Link>
          <Link href="/settings" className="text-zinc-600 hover:text-zinc-900">
            Configurações
          </Link>
          <button onClick={logout} className="text-zinc-600 hover:text-zinc-900">
            Sair
          </button>
        </div>
      </nav>

      <main className="max-w-2xl mx-auto px-4 py-8">
        <h1 className="text-xl font-semibold text-zinc-900 mb-6">Todas as vagas</h1>

        {loading && <p className="text-sm text-zinc-500">Carregando...</p>}
        {error && <p className="text-sm text-red-600">{error}</p>}
        {!loading && !error && jobs.length === 0 && (
          <p className="text-sm text-zinc-500">Nenhuma vaga encontrada.</p>
        )}

        <div className="flex flex-col gap-3">
          {jobs.map((job) => (
            <JobCard
              key={job.id}
              title={job.title}
              company={job.company}
              location={job.location}
              date={job.posted_at}
              url={job.url}
            />
          ))}
        </div>

        {!loading && jobs.length > 0 && (
          <Pagination
            page={page}
            hasNext={jobs.length === LIMIT}
            onPrev={() => setPage((p) => p - 1)}
            onNext={() => setPage((p) => p + 1)}
          />
        )}
      </main>
    </div>
  );
}
