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

const ENDPOINT = process.env.NEXT_PUBLIC_MODAL_ENDPOINT_MS;

function downloadText(content: string, filename: string, mime = "text/plain") {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

function matrixToCSV(columns: string[], rows: Record<string, string>[]) {
  const header = columns.map((c) => `"${c}"`).join(",");
  const body = rows.map((row) =>
    columns.map((col) => `"${(row[col] ?? "").replace(/"/g, '""')}"`).join(",")
  );
  return [header, ...body].join("\n");
}

export default function MicroservicesPage() {
  const [requirement, setRequirement] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<HannahResponse | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!ENDPOINT) {
      setError("Configura la variable NEXT_PUBLIC_MODAL_ENDPOINT_MS.");
      return;
    }

    if (!requirement.trim()) {
      setError("Ingresa un requerimiento.");
      return;
    }

    if (requirement.length > 5000) {
      setError("El requerimiento no puede superar 5000 caracteres.");
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
            🤖 Hannah MS Agent
          </h1>
          <p className="text-gray-600">
            Genera casos de prueba especializados para microservicios (API REST)
          </p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-4">
          {!ENDPOINT && (
            <div className="rounded-xl border border-orange-300 bg-orange-50 p-4 text-sm text-orange-800">
              ⚠️ Configura NEXT_PUBLIC_MODAL_ENDPOINT_MS
            </div>
          )}

          <label className="block">
            <span className="text-sm font-semibold text-blue-700 uppercase mb-2 block">
              Requerimiento de Microservicio
            </span>
            <textarea
              value={requirement}
              onChange={(e) => setRequirement(e.target.value)}
              rows={6}
              maxLength={5000}
              className="w-full rounded-xl border border-gray-200 bg-gray-50 p-4 text-gray-700 focus:border-blue-400 focus:ring-2 focus:ring-blue-200 outline-none transition"
              placeholder="Ejemplo: Validar que el endpoint GET /api/v1/clientes/{id} retorne 200 con datos válidos y 404 si el cliente no existe."
            />
            <span className="mt-1 block text-right text-xs text-gray-400">
              {requirement.length}/5000
            </span>
          </label>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-gradient-to-r from-blue-400 via-purple-400 to-indigo-400 px-6 py-3 font-semibold text-white transition hover:shadow-md disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {loading ? "⏳ Generando..." : "🚀 Generar Casos de Prueba MS"}
          </button>

          {error && (
            <div className="rounded-xl border border-red-300 bg-red-50 p-4 text-sm text-red-800">
              ❌ {error}
            </div>
          )}
        </form>

        {result && (
          <section className="space-y-6 rounded-2xl border border-gray-200 bg-gray-50 p-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-1">
                  📊 Resultado
                </h2>
                <p className="text-sm text-gray-600">
                  Status:{" "}
                  <span className="font-bold text-green-600">
                    {result.status.toUpperCase()}
                  </span>
                </p>
              </div>
              <div className="flex gap-2">
                {hasMatrix && (
                  <button
                    type="button"
                    onClick={() =>
                      downloadText(
                        matrixToCSV(result.matrix_columns, result.matrix_data),
                        "matriz_pruebas_ms.csv",
                        "text/csv"
                      )
                    }
                    className="rounded-xl border border-gray-300 bg-white px-3 py-2 text-xs font-medium text-gray-700 transition hover:bg-gray-50"
                  >
                    ⬇ CSV
                  </button>
                )}
                {result.gherkin_content && (
                  <button
                    type="button"
                    onClick={() =>
                      downloadText(result.gherkin_content, "casos_ms.feature")
                    }
                    className="rounded-xl border border-gray-300 bg-white px-3 py-2 text-xs font-medium text-gray-700 transition hover:bg-gray-50"
                  >
                    ⬇ .feature
                  </button>
                )}
              </div>
            </div>

            {hasMatrix && (
              <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
                <table className="min-w-full divide-y divide-gray-200 text-sm">
                  <thead className="bg-blue-50 text-xs uppercase text-blue-700">
                    <tr>
                      {result.matrix_columns.map((col) => (
                        <th key={col} className="px-4 py-3 font-medium">
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {result.matrix_data.map((row, i) => (
                      <tr key={i} className="bg-white">
                        {result.matrix_columns.map((col) => (
                          <td key={col} className="px-4 py-3 text-gray-700">
                            {row[col]}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {result.gherkin_content && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  🧾 Casos Gherkin
                </h3>
                <pre className="whitespace-pre-wrap rounded-xl border border-purple-200 bg-purple-50 p-4 text-sm">
                  {result.gherkin_content}
                </pre>
              </div>
            )}

            <details className="rounded-xl border border-gray-200 bg-gray-50">
              <summary className="cursor-pointer px-4 py-3 text-sm font-semibold text-indigo-600">
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
