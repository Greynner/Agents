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

const MODAL_ENDPOINT = process.env.NEXT_PUBLIC_MODAL_ENDPOINT ?? "";

export default function Home() {
  const [requirement, setRequirement] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<HannahResponse | null>(null);

  const isEndpointConfigured = Boolean(MODAL_ENDPOINT);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!isEndpointConfigured) {
      setError("Configura NEXT_PUBLIC_MODAL_ENDPOINT antes de enviar.");
      return;
    }

    if (!requirement.trim()) {
      setError("Ingresa un requerimiento QA antes de enviar.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(MODAL_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ requerimiento: requirement }),
      });

      const data: HannahResponse = await response.json();

      if (!response.ok || data.status !== "success") {
        throw new Error(data.error || "No se pudo generar la matriz.");
      }

      setResult(data);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Error inesperado generando los casos.";
      setError(message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const hasMatrix =
    !!result &&
    Array.isArray(result.matrix_columns) &&
    result.matrix_columns.length > 0 &&
    Array.isArray(result.matrix_data) &&
    result.matrix_data.length > 0;

  return (
    <div className="flex min-h-screen justify-center bg-[#f3f4f6] py-16 px-4 text-slate-900">
      <main className="flex w-full max-w-4xl flex-col gap-10 rounded-3xl border border-slate-200 bg-white p-10 shadow-lg">
        <header className="flex flex-col gap-2">
          <h1 className="text-3xl font-semibold text-slate-900">
            🧠 QA Agent - Analizador de Requerimientos
          </h1>
          <p className="text-base text-slate-600 leading-relaxed">
            Ingresa tu requerimiento QA, lo enviaremos a nuestro backend
            desplegado en Modal y te mostraremos la respuesta generada por el
            agente de IA.
          </p>
        </header>

        <form
          onSubmit={handleSubmit}
          className="flex flex-col gap-4 rounded-2xl border border-slate-200 bg-white p-6 shadow-inner"
        >
          {!isEndpointConfigured && (
            <p className="rounded-xl border border-orange-300 bg-orange-100 p-4 text-sm text-orange-800">
              Falta configurar la variable NEXT_PUBLIC_MODAL_ENDPOINT.
            </p>
          )}
          <label className="flex flex-col gap-2">
            <span className="text-sm font-medium uppercase tracking-wide text-lime-700">
              Requerimiento QA
            </span>
            <textarea
              value={requirement}
              onChange={(event) => setRequirement(event.target.value)}
              rows={6}
              className="w-full rounded-xl border border-slate-200 bg-slate-50 p-4 text-base text-slate-700 shadow-sm outline-none transition focus:border-lime-400 focus:ring focus:ring-lime-200"
              placeholder="Ejemplo: Como usuario de banca digital quiero iniciar sesión con correo y contraseña..."
            />
          </label>
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center justify-center rounded-xl bg-gradient-to-r from-yellow-400 via-orange-400 to-lime-400 px-6 py-3 text-base font-semibold text-slate-900 transition hover:shadow-md disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "Generando con Hannah..." : "Enviar a Hannah"}
          </button>
          {error && (
            <p className="rounded-xl border border-orange-300 bg-orange-100 p-4 text-sm text-orange-800">
              {error}
            </p>
          )}
        </form>

        {result && (
          <section className="flex flex-col gap-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-inner">
            <div>
              <h2 className="text-xl font-semibold text-slate-900">
                Resultado del agente
              </h2>
              <p className="text-sm text-slate-600">
                Status:{" "}
                <span className="font-semibold text-orange-600">
                  {result.status.toUpperCase()}
                </span>
              </p>
            </div>

            {hasMatrix && (
              <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white">
                <table className="min-w-full divide-y divide-slate-200 text-left text-sm text-slate-700">
                  <thead className="bg-lime-50 text-xs uppercase text-lime-700">
                    <tr>
                      {result.matrix_columns.map((column) => (
                        <th key={column} className="px-4 py-3 font-medium">
                          {column}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {result.matrix_data.map((row, index) => (
                      <tr key={index} className="bg-white">
                        {result.matrix_columns.map((column) => (
                          <td key={column} className="px-4 py-3">
                            {row[column]}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {result.gherkin_content && (
              <div className="flex flex-col gap-2">
                <h3 className="text-lg font-semibold text-slate-900">
                  Escenarios Gherkin
                </h3>
                <pre className="whitespace-pre-wrap rounded-xl border border-yellow-200 bg-yellow-50 p-4 text-sm text-slate-700">
                  {result.gherkin_content}
                </pre>
              </div>
            )}

            <details className="rounded-xl border border-slate-200 bg-slate-50">
              <summary className="cursor-pointer px-4 py-3 text-sm font-semibold text-orange-600">
                Ver respuesta completa del backend
              </summary>
              <pre className="max-h-72 overflow-auto whitespace-pre-wrap p-4 text-xs text-slate-600">
                {JSON.stringify(result, null, 2)}
              </pre>
            </details>
          </section>
        )}
      </main>
    </div>
  );
}
