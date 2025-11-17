"use client";

import { FormEvent, useState } from "react";

type HannahResponse = {
  status: string;
  output: string;
  matrix_data: Record<string, string>[];
  matrix_columns: string[];
  gherkin_content: string;
  error?: string;
};

// Usar el proxy de Vercel (ruta relativa) o variable de entorno como fallback
// El proxy está en /api/modal_proxy.py y reenvía a Modal
const ENDPOINT = process.env.NEXT_PUBLIC_API_ENDPOINT || 
                 (typeof window !== 'undefined' 
                   ? `${window.location.origin}/api/analizar-requerimiento`
                   : '/api/analizar-requerimiento');

export default function Home() {
  const [requirement, setRequirement] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<HannahResponse | null>(null);

  const handleNewRequirement = () => {
    setRequirement("");
    setResult(null);
    setError(null);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!ENDPOINT) {
      setError("Configura NEXT_PUBLIC_MODAL_ENDPOINT.");
      return;
    }

    if (!requirement.trim()) {
      setError("Ingresa un requerimiento.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ requerimiento: requirement }),
      });

      if (!res.ok) {
        const errorText = await res.text();
        let errorData;
        try {
          errorData = JSON.parse(errorText);
        } catch {
          errorData = { error: errorText || `Error ${res.status}: ${res.statusText}` };
        }
        throw new Error(errorData.error || errorData.detail || `Error ${res.status}`);
      }

      const data: HannahResponse = await res.json();

      if (data.status !== "success") {
        throw new Error(data.error || "Error al generar.");
      }

      setResult(data);
    } catch (err) {
      console.error("Error en la solicitud:", err);
      setError(err instanceof Error ? err.message : "Error inesperado.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const hasMatrix = result && result.matrix_columns?.length && result.matrix_data?.length;

  return (
    <div className="flex min-h-screen justify-center bg-black py-16 px-6 text-slate-100">
      <main className="w-full max-w-xl space-y-8 rounded-[32px] border border-white/5 bg-[#0B0B0F] px-10 py-12 shadow-[0_30px_70px_-35px_rgba(0,0,0,0.9)]">
        <header className="flex flex-col gap-4">
          <div className="space-y-3">
            <h1 className="text-3xl font-semibold text-slate-50">
              
       Hannah QA Agent
            </h1>
            <p className="text-base leading-relaxed text-slate-300">
              Generate test matrices and Gherkin scenarios with AI
            </p>
          </div>
          <button
            type="button"
            onClick={handleNewRequirement}
            className="inline-flex items-center justify-center gap-2 rounded-2xl border border-white/5 bg-transparent px-4 py-3 text-sm font-medium text-slate-200 transition hover:border-white/15 hover:bg-white/5 focus:outline-none focus:ring-2 focus:ring-purple-400/40"
          >
            ➕ Add new requirement
          </button>
        </header>

        <form onSubmit={handleSubmit} className="space-y-5">
          {!ENDPOINT && (
            <div className="rounded-xl border border-amber-400/40 bg-amber-500/10 p-4 text-sm text-amber-100">
              ⚠️ Configura NEXT_PUBLIC_API_ENDPOINT o asegúrate de que el proxy esté configurado
            </div>
          )}
          
          <label className="block">
            <span className="mb-3 block text-xs font-semibold tracking-[0.2em] text-slate-400">
              BUSINESS REQUIREMENT
            </span>
            <textarea
              value={requirement}
              onChange={(e) => setRequirement(e.target.value)}
              rows={6}
              className="w-full rounded-2xl border border-white/5 bg-[#050507] p-4 text-base text-slate-100 shadow-[inset_0_0_0_1px_rgba(255,255,255,0.02)] transition focus:border-purple-500/60 focus:ring-2 focus:ring-purple-500/30"
              placeholder="Example: As a user, I want to log in..."
            />
          </label>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-2xl bg-gradient-to-r from-indigo-500 via-fuchsia-500 to-purple-500 px-6 py-3 font-semibold text-white transition hover:shadow-[0_20px_45px_-18px_rgba(192,132,252,0.85)] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "⏳ Generating..." : "🚀 Send to Hannah"}
          </button>
          
          {error && (
            <div className="rounded-xl border border-rose-500/40 bg-rose-500/10 p-4 text-sm text-rose-100">
              ❌ {error}
            </div>
          )}
        </form>

        {result && (
          <section className="space-y-6 rounded-[28px] border border-white/5 bg-[#08080B] p-6">
            <div>
              <h2 className="text-xl font-semibold text-slate-50 mb-1">
                📊 Result
              </h2>
              <p className="text-sm text-slate-300">
                Status: <span className="font-bold text-emerald-300">{result.status.toUpperCase()}</span>
              </p>
            </div>

            {hasMatrix && (
              <div className="overflow-x-auto rounded-2xl border border-white/5 bg-[#050507]">
                <table className="min-w-full divide-y divide-white/5 text-sm text-slate-200">
                  <thead className="bg-white/5 text-xs uppercase tracking-[0.18em] text-slate-300">
                    <tr>
                      {result.matrix_columns.map((col) => (
                        <th key={col} className="px-4 py-3 font-medium tracking-wide">{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {result.matrix_data.map((row, i) => (
                      <tr key={i} className="bg-transparent">
                        {result.matrix_columns.map((col) => (
                          <td key={col} className="px-4 py-3 text-slate-200">{row[col]}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {result.gherkin_content && (
              <div>
                <h3 className="text-lg font-semibold text-slate-50 mb-2">🧾 Gherkin Scenarios</h3>
                <pre className="whitespace-pre-wrap rounded-2xl border border-white/5 bg-[#050507] p-4 text-sm text-indigo-100">
                  {result.gherkin_content}
                </pre>
              </div>
            )}

            <details className="rounded-2xl border border-white/5 bg-transparent">
              <summary className="cursor-pointer px-4 py-3 text-sm font-semibold text-slate-200">
                🔍 View full response
              </summary>
              <pre className="max-h-72 overflow-auto p-4 text-xs text-slate-200">
                {JSON.stringify(result, null, 2)}
              </pre>
            </details>
          </section>
        )}
      </main>
    </div>
  );
}
