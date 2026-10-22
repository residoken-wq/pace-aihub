import { CheckCircle2, AlertCircle } from "lucide-react";
import vi from "@/messages/vi.json";

async function getApiHealth(): Promise<"ok" | "error"> {
  const apiUrl = process.env.API_INTERNAL_URL || "http://127.0.0.1:8000";
  try {
    const res = await fetch(`${apiUrl}/healthz`, { cache: "no-store" });
    if (!res.ok) {
      return "error";
    }
    const data = await res.json();
    return data && data.status === "ok" ? "ok" : "error";
  } catch {
    return "error";
  }
}

export default async function Home() {
  const apiStatus = await getApiHealth();
  const isHealthy = apiStatus === "ok";

  return (
    <main className="flex-1 flex flex-col items-center justify-center p-6 sm:p-12">
      <div className="w-full max-w-2xl bg-white rounded-xl border border-slate-200 shadow-sm p-8 space-y-6">
        <div className="space-y-2 border-b border-slate-100 pb-5">
          <div className="flex items-center justify-between">
            <h1 data-testid="page-title" className="text-2xl font-bold tracking-tight text-slate-900">
              {vi.app.title}
            </h1>
            <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-semibold text-slate-700">
              INF-01a
            </span>
          </div>
          <p className="text-sm text-slate-600">{vi.home.welcome}</p>
          <p className="text-xs text-slate-400">{vi.home.placeholder_notice}</p>
        </div>

        <div className="space-y-3">
          <h2 className="text-sm font-semibold text-slate-800 uppercase tracking-wider">
            {vi.home.system_status}
          </h2>
          <div
            data-testid="api-status-container"
            className={`flex items-start gap-3 p-4 rounded-lg border ${
              isHealthy
                ? "bg-emerald-50/60 border-emerald-200 text-emerald-900"
                : "bg-red-50/60 border-red-200 text-red-900"
            }`}
          >
            {isHealthy ? (
              <CheckCircle2
                data-testid="icon-ok"
                className="h-5 w-5 text-emerald-600 shrink-0 mt-0.5"
                aria-hidden="true"
              />
            ) : (
              <AlertCircle
                data-testid="icon-error"
                className="h-5 w-5 text-red-600 shrink-0 mt-0.5"
                aria-hidden="true"
              />
            )}
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-slate-700">
                  {vi.home.api_status_label}
                </span>
                <span
                  data-testid="api-status-text"
                  className={`text-sm font-semibold ${
                    isHealthy ? "text-emerald-700" : "text-red-700"
                  }`}
                >
                  {isHealthy ? vi.home.api_status_ok : vi.home.api_status_error}
                </span>
              </div>
              {!isHealthy && (
                <p data-testid="api-error-hint" className="text-xs text-red-600 leading-relaxed">
                  {vi.home.api_error_hint}
                </p>
              )}
            </div>
          </div>
        </div>

        <div className="pt-2 text-center text-xs text-slate-400">
          <span>{vi.app.description}</span>
        </div>
      </div>
    </main>
  );
}
