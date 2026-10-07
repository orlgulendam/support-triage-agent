import type { Ticket } from "../types";

interface Props {
  ticket: Ticket;
}

export default function TicketDetail({ ticket }: Props) {
  return (
    <div className="ticket-detail">
      <h3>{ticket.kategori}</h3>
      <p>
        <strong>Zaman:</strong> {ticket.zaman}
      </p>
      <p>
        <strong>Talep:</strong> {ticket.talep}
      </p>
      <p>
        <strong>Sonuc:</strong> {ticket.sonuc_tipi}
      </p>
      <p>
        <strong>Cevap:</strong> {ticket.cevap}
      </p>
    </div>
  );
}