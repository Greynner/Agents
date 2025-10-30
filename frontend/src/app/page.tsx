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

const ENDPOINT = process.env.NEXT_PUBLIC_MODAL_ENDPOINT ?? "";

export default function Home() {
  const [requirement, setRequirement] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<HannahResponse | null>(null);

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

      const data: HannahResponse = await res.json();

      if (!res.ok || data.status !== "success") {
        throw new Error(data.error || "Error al generar.");
      }

      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error inesperado.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const hasMatrix = result && result.matrix_columns?.length && result.matrix_data?.length;

  return (
    <div className="flex min-h-screen justify-center bg-gray-100 py-12 px-4">
      <main className="w-full max-w-4xl space-y-8 rounded-2xl border border-gray-200 bg-white p-8 shadow-lg">
        <header>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🧠 Hannah QA Agent
          </h1>
          <p className="text-gray-600">
            Genera matrices de prueba y casos Gherkin con IA
          </p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-4">
          {!ENDPOINT && (
            <div className="rounded-xl border border-orange-300 bg-orange-50 p-4 text-sm text-orange-800">
              ⚠️ Configura NEXT_PUBLIC_MODAL_ENDPOINT
            </div>
          )}
          
          <label className="block">
            <span className="text-sm font-semibold text-green-700 uppercase mb-2 block">
              Requerimiento QA
            </span>
            <textarea
              value={requirement}
              onChange={(e) => setRequirement(e.target.value)}
              rows={6}
              className="w-full rounded-xl border border-gray-200 bg-gray-50 p-4 text-gray-700 focus:border-green-400 focus:ring-2 focus:ring-green-200 outline-none transition"
              placeholder="Ejemplo: Como usuario quiero iniciar sesión..."
            />
          </label>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-gradient-to-r from-yellow-400 via-orange-400 to-green-400 px-6 py-3 font-semibold text-gray-900 transition hover:shadow-md disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {loading ? "⏳ Generando..." : "🚀 Enviar a Hannah"}
          </button>
          
          {error && (
            <div className="rounded-xl border border-red-300 bg-red-50 p-4 text-sm text-red-800">
              ❌ {error}
            </div>
          )}
        </form>

        {result && (
          <section className="space-y-6 rounded-2xl border border-gray-200 bg-gray-50 p-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-1">
                📊 Resultado
              </h2>
              <p className="text-sm text-gray-600">
                Status: <span className="font-bold text-green-600">{result.status.toUpperCase()}</span>
              </p>
            </div>

            {hasMatrix && (
              <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
                <table className="min-w-full divide-y divide-gray-200 text-sm">
                  <thead className="bg-green-50 text-xs uppercase text-green-700">
                    <tr>
                      {result.matrix_columns.map((col) => (
                        <th key={col} className="px-4 py-3 font-medium">{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {result.matrix_data.map((row, i) => (
                      <tr key={i} className="bg-white">
                        {result.matrix_columns.map((col) => (
                          <td key={col} className="px-4 py-3 text-gray-700">{row[col]}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {result.gherkin_content && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">🧾 Casos Gherkin</h3>
                <pre className="whitespace-pre-wrap rounded-xl border border-yellow-200 bg-yellow-50 p-4 text-sm">
                  {result.gherkin_content}
                </pre>
              </div>
            )}

            <details className="rounded-xl border border-gray-200 bg-gray-50">
              <summary className="cursor-pointer px-4 py-3 text-sm font-semibold text-orange-600">
                🔍 Ver respuesta completa
              </summary>
              <pre className="max-h-72 overflow-auto p-4 text-xs">
                {JSON.stringify(result, null, 2)}
              </pre>
            </details>
          </section>
        )}
      </main>
    </div>
  );
}
