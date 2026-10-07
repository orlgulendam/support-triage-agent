import type { Ticket, TicketResponse, Stats } from "./types";

const BASE_URL = "http://127.0.0.1:8000";

export async function createTicket(talep: string): Promise<TicketResponse> {
  const response = await fetch(`${BASE_URL}/tickets`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ talep }),
  });
  return response.json();
}

export async function reviewTicket(
  ticketId: string,
  karar: "onay" | "red"
): Promise<TicketResponse> {
  const response = await fetch(`${BASE_URL}/tickets/${ticketId}/review`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ karar }),
  });
  return response.json();
}

export async function fetchTickets(): Promise<Ticket[]> {
  const response = await fetch(`${BASE_URL}/tickets`);
  return response.json();
}

export async function fetchStats(): Promise<Stats> {
  const response = await fetch(`${BASE_URL}/stats`);
  return response.json();
}