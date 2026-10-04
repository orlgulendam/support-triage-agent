\# ADR-0003: Riske Göre AI'ın Rolünün Farklılaştırılması



\## Durum

Kabul edildi



\## Bağlam

Sistemde üç farklı noktada Claude API'ye başvuruluyor: sınıflandırma

(`classify`/`retry\_classify`), müşteriye doğrudan cevap üretme

(`draft\_response`), ve bir insan temsilciye yardımcı brifing üretme

(`finalize\_human`, eskalasyon durumunda). Bu üç kullanımın AI'a verdiği

"yetki" aynı değil — soru şuydu: AI her durumda nihai cevabı mı üretsin,

yoksa bazı durumlarda sadece bir insana mı yardımcı olsun?



\## Karar

AI'ın rolü, talebin risk seviyesine göre bilinçli olarak farklılaştırıldı:



| Durum | AI'ın rolü |

|---|---|

| Düşük risk (`basit\_soru`) | AI, müşteriye gidecek cevabı \*\*doğrudan\*\* yazıyor |

| Yüksek risk, insan onayladı | AI'a sorulmuyor, sabit bir kayıt tutuluyor |

| Yüksek risk, insan reddetti, deneme hakkı var (`deneme\_sayisi < 2`) | AI, \*\*farklı bir açıdan\*\* tekrar sınıflandırma deniyor (`retry\_classify`) |

| Yüksek risk, deneme hakkı bitti (`deneme\_sayisi >= 2`) | AI, müşteriye değil \*\*insan temsilciye\*\* özet + risk nedeni + önerilen yaklaşım içeren bir brifing yazıyor |



`MAX\_RETRY = 2` sınırı bilinçli olarak seçildi: sınırsız yeniden deneme

hem API maliyetini artırır hem de insanın "sistem hiç bitmiyor" hissi

yaşamasına yol açar; hiç yeniden deneme olmaması ise retry mekanizmasının

anlamını ortadan kaldırır. 2, bu ikisi arasında bilinçli bir denge noktası

olarak seçildi, deneysel olarak optimize edilmedi.



\## Sonuçlar

\- (+) Hassas/belirsiz durumlarda AI, müşteriye doğrudan temas etmiyor —

&#x20; risk, AI'ın özerkliğiyle orantılı tutuluyor.

\- (+) İnsana "boş bir talep" değil, bağlamı hazırlanmış bir talep

&#x20; düşüyor — temsilcinin karar süresi kısalıyor.

\- (+) Sistem kendi belirsizliğini fark edip (2 kez reddedilme) bunu

&#x20; açıkça işaretliyor (`\[ESKALE EDILDI]` etiketi) — sessizce "en son

&#x20; tahmini" doğru kabul etmiyor.

\- (-) `MAX\_RETRY = 2` deneysel olarak ayarlanmadı; gerçek bir üretim

&#x20; sisteminde bu, ret oranı/maliyet verisiyle optimize edilmesi gereken

&#x20; bir parametre olurdu.

\- (-) Brifing kalitesi test edilmedi (örn. insanın gerçekten daha hızlı

&#x20; karar verip vermediği ölçülmedi) — bu, projenin doğal bir sonraki

&#x20; adımı (kullanıcı testi) olurdu.

