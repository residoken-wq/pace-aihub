import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen } from "@testing-library/react";
import Home from "@/app/page";
import viMessages from "@/messages/vi.json";

describe("Home Page Component (INF-01a Web Skeleton)", () => {
  const originalFetch = global.fetch;

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  it("renders API ok status when API /healthz responds with ok", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ status: "ok" }),
    });

    const jsx = await Home();
    render(jsx);

    expect(screen.getByTestId("page-title").textContent).toContain(viMessages.app.title);
    expect(screen.getByTestId("api-status-text").textContent).toContain(viMessages.home.api_status_ok);
    expect(screen.getByTestId("icon-ok")).toBeDefined();
    expect(screen.queryByTestId("icon-error")).toBeNull();
  });

  it("renders API error status gracefully when fetch fails or API is down", async () => {
    global.fetch = vi.fn().mockRejectedValueOnce(new Error("Connection refused"));

    const jsx = await Home();
    render(jsx);

    expect(screen.getByTestId("page-title").textContent).toContain(viMessages.app.title);
    expect(screen.getByTestId("api-status-text").textContent).toContain(viMessages.home.api_status_error);
    expect(screen.getByTestId("icon-error")).toBeDefined();
    expect(screen.getByTestId("api-error-hint").textContent).toContain(viMessages.home.api_error_hint);
    expect(screen.queryByTestId("icon-ok")).toBeNull();

    // Ensure internal URL is not leaked to DOM
    expect(document.body.textContent).not.toContain("127.0.0.1:8000");
    expect(document.body.textContent).not.toContain("api:8000");
    expect(document.body.textContent).not.toContain("Connection refused");
  });
});
