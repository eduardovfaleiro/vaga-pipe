'use client';

interface PaginationProps {
  page: number;
  hasNext: boolean;
  onPrev: () => void;
  onNext: () => void;
}

export function Pagination({ page, hasNext, onPrev, onNext }: PaginationProps) {
  return (
    <div className="flex items-center gap-3 justify-center mt-6">
      <button
        onClick={onPrev}
        disabled={page <= 1}
        className="px-4 py-1.5 text-sm border border-zinc-900 rounded hover:bg-zinc-100 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
      >
        Anterior
      </button>
      <span className="text-sm text-zinc-600">Página {page}</span>
      <button
        onClick={onNext}
        disabled={!hasNext}
        className="px-4 py-1.5 text-sm bg-zinc-900 text-white rounded hover:bg-zinc-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
      >
        Próxima
      </button>
    </div>
  );
}
