export type Ton = "success" | "warning" | "danger" | "info" | "neutral";

interface Etiket {
  etiket: string;
  ton: Ton;
}

export const KATEGORI: Record<string, Etiket> = {
  basit_soru: { etiket: "Basit soru", ton: "info" },
  teknik_sorun: { etiket: "Teknik sorun", ton: "warning" },
  hassas_sikayet: { etiket: "Hassas şikayet", ton: "danger" },
};

export const SONUC: Record<string, Etiket> = {
  otomatik_cevap: { etiket: "Otomatik yanıtlandı", ton: "success" },
  insan_onayli: { etiket: "Onaylandı", ton: "info" },
  eskale_edildi: { etiket: "Temsilciye aktarıldı", ton: "danger" },
};

// Tabloda olmayan bir deger gelirse ham degeri gri rozetle goster
export function etiketBul(tablo: Record<string, Etiket>, deger: string): Etiket {
  return tablo[deger] ?? { etiket: deger, ton: "neutral" };
}