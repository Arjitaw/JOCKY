import { createFileRoute } from "@tanstack/react-router";
import { useCallback, useEffect, useState } from "react";
import {
  API_BASE_URL,
  checkHealth,
  sendCommand,
  type CommandResponse,
} from "@/services/api";

export const Route = createFileRoute("/")({
  component: Index,
  head: () => ({
    meta: [
      { title: "JOCKY — Digital Forensics Command Center" },
      {
        name: "description",
        content:
          "JOCKY is a digital forensics command-line tool with a clean graphical interface for analyzing evidence.",
      },
      { property: "og:title", content: "JOCKY — Digital Forensics Command Center" },
      {
        property: "og:description",
        content:
          "Run forensic commands and view execution results in a modern dark-themed interface.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
});

type CommandResult = {
  status: string;
  command: string;
  output: string;
};

type RecentCommand = {
  command: string;
  status: string;
};

const INITIAL_RECENT: RecentCommand[] = [
];

function Index() {
  const [command, setCommand] = useState("");
  const [result, setResult] = useState<CommandResult | null>(null);
  const [recent, setRecent] = useState<RecentCommand[]>(INITIAL_RECENT);
  const [loading, setLoading] = useState(false);
  const [apiConnected, setApiConnected] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const refreshHealth = useCallback(async () => {
    const healthy = await checkHealth();
    setApiConnected(healthy);
    return healthy;
  }, []);

  useEffect(() => {
    let cancelled = false;
    const run = () => {
      checkHealth().then((healthy) => {
        if (!cancelled) setApiConnected(healthy);
      });
    };
    run();
    const interval = setInterval(run, 15_000);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  const handleExecute = async () => {
    const trimmed = command.trim();
    if (!trimmed) return;

    setLoading(true);
    setApiError(null);

    try {
      const data: CommandResponse = await sendCommand(trimmed);

      setApiConnected(true);
      setResult({
        status: data.status ?? "Success",
        command: data.command ?? trimmed,
        output: data.output ?? "",
      });

      setRecent((prev) => {
        const next = [{ command: trimmed, status: data.status ?? "Success" }, ...prev];
        return next.slice(0, 6);
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : "Could not reach the Flask API.";
      setApiError(message);
      setResult(null);
      void refreshHealth();
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleExecute();
    }
  };

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <nav className="sticky top-0 z-10 border-b border-border bg-background/80 backdrop-blur">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-4">
          <div>
            <h1 className="text-xl font-bold tracking-tight text-foreground">JOCKY</h1>
            <p className="text-xs text-muted-foreground">Digital Forensics Tool</p>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span
              className={`h-2 w-2 rounded-full ${apiConnected ? "bg-primary" : "bg-destructive"}`}
              aria-hidden="true"
            />
            <span>{apiConnected ? "API Connected" : "API Disconnected"}</span>
          </div>
        </div>
      </nav>

      <main className="mx-auto w-full max-w-4xl flex-1 px-4 py-8 sm:py-12">
        <div className="mb-8 space-y-2 sm:mb-10">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Digital Forensics Command Center
          </h2>
          <p className="text-base text-muted-foreground sm:text-lg">
            &ldquo;Analyze digital evidence using simple JOCKY forensic commands.&rdquo;
          </p>
        </div>

        <div className="grid gap-6">
          <section className="rounded-xl border border-border bg-card p-5 shadow-sm sm:p-6">
            <h3 className="mb-4 text-lg font-semibold text-card-foreground">Command Center</h3>
            <label htmlFor="command" className="mb-2 block text-sm font-medium text-card-foreground">
              Enter JOCKY Command
            </label>
            <input
              id="command"
              type="text"
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="HASH FILE evidence.txt"
              className="w-full rounded-lg border border-input bg-background px-4 py-3 text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <button
              onClick={handleExecute}
              disabled={loading}
              className="mt-4 inline-flex items-center justify-center rounded-lg bg-primary px-6 py-2.5 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-background disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Executing..." : "Execute Command"}
            </button>

            <div className="mt-6">
              <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Examples
              </p>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li className="font-mono">HASH FILE evidence.txt</li>
                <li className="font-mono">SYSTEM INFO</li>
                <li className="font-mono">LIST FILES</li>
              </ul>
            </div>
          </section>

          <section className="rounded-xl border border-border bg-card p-5 shadow-sm sm:p-6">
            <h3 className="mb-4 text-lg font-semibold text-card-foreground">Execution Result</h3>
            {apiError ? (
              <div className="space-y-1">
                <p className="text-sm text-destructive">{apiError}</p>
              </div>
            ) : result ? (
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-muted-foreground">Status:</span>
                  <span className="font-medium text-primary">{result.status}</span>
                </div>
                <div className="text-sm">
                  <span className="text-muted-foreground">Command:</span>{" "}
                  <span className="font-mono text-card-foreground">{result.command}</span>
                </div>
                <div className="rounded-lg border border-border bg-background p-3">
                  <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    Result
                  </p>
                  <pre className="whitespace-pre-wrap font-mono text-sm text-card-foreground">
                    {result.output}
                  </pre>
                </div>
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">No command executed yet.</p>
            )}
          </section>

          <section>
            <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
              Recent Commands
            </h3>
            <div className="rounded-xl border border-border bg-card p-4 shadow-sm">
              <ul className="space-y-2">
                {recent.map((item, index) => (
                  <li
                    key={`${item.command}-${index}`}
                    className="flex items-center justify-between text-sm"
                  >
                    <span className="font-mono text-card-foreground">{item.command}</span>
                    <span className="text-xs font-medium text-primary">{item.status}</span>
                  </li>
                ))}
              </ul>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
