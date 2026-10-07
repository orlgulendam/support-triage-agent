export interface Ticket {
  id: number;
  zaman: string;
  talep: string;
  kategori: string;
  sonuc_tipi: string;
  cevap: string;
}

export interface TicketResponse {
  ticket_id: string;
  durum: "beklemede" | "tamamlandi";
  kategori: string;
  cevap?: string;
}

export interface StatDagilim {
  tip: string;
  adet: number;
}

export interface Stats {
  toplam: number;
  dagilim: StatDagilim[];
}