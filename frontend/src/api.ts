import type { Ticket, TicketResponse, Stats, PendingTicket } from "./types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";
const TOKEN_ANAHTARI = "panel_token";

export function tokenAl(): string {
  return sessionStorage.getItem(TOKEN_ANAHTARI) ?? "";
}

export function tokenKaydet(token: string) {
  sessionStorage.setItem(TOKEN_ANAHTARI, token);
}

export function tokenSil() {
  sessionStorage.removeItem(TOKEN_ANAHTARI);
}

async function istek<T>(yol: string, secenekler: RequestInit = {}): Promise<T> {
  const response = await fetch(`${BASE_URL}${yol}`, {
    ...secenekler,
    headers: {
      ...(secenekler.headers ?? {}),
      "X-Panel-Token": tokenAl(),
    },
  });
  if (!response.ok) {
    throw new Error(`Sunucu hatası: ${response.status}`);
  }
  return response.json();
}

function postSecenekleri(veri: unknown): RequestInit {
  return {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(veri),
  };
}

export async function createTicket(talep: string): Promise<TicketResponse> {
  return istek<TicketResponse>("/tickets", postSecenekleri({ talep }));
}

export async function reviewTicket(
  ticketId: string,
  karar: "onay" | "red"
): Promise<TicketResponse> {
  return istek<TicketResponse>(
    `/tickets/${ticketId}/review`,
    postSecenekleri({ karar })
  );
}

export async function fetchTickets(): Promise<Ticket[]> {
  return istek<Ticket[]>("/tickets");
}

export async function fetchStats(): Promise<Stats> {
  return istek<Stats>("/stats");
}

export async function fetchPending(): Promise<PendingTicket[]> {
  return istek<PendingTicket[]>("/tickets/pending");
}

export async function panelGirisKontrol(): Promise<boolean> {
  try {
    await istek<{ ok: boolean }>("/panel/auth");
    return true;
  } catch {
    return false;
  }
}
