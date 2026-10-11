import type { Ticket, TicketResponse, Stats } from "./types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

async function istek<T>(yol: string, secenekler?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${yol}`, secenekler);
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