# doc3 tam indeks: geliştirme seti kontrolü (5 Kasım 2026)

doc3.pdf'in tamamı indekslendi: 200 sayfa, 562 parça. Geliştirme setindeki doc3 soruları örnek PDF'ten (40 sayfa)
yazılmıştı. Tüm metinde iki şey kontrol edildi:

1. Cevapsız sorular hâlâ cevapsız mı?
2. Cevaplanabilir soruların başka geçerli sayfası var mı?

Kaynak: indeksteki OCR metni (`rag_pages.ocr_text`).

## Cevapsız sorular: değişiklik gerekmiyor

| id | soru | 200 sayfada arama |
|---|---|---|
| d3u01 | LOT için NASA bütçesi kaç dolar? | LOT için hiçbir tutar yok. Tek dolar tutarı balon programına ait: "about \$2.0 million for the three-year period" (s.170). LOT tablosunda yalnızca "Approved by NASA, but not funded" yazıyor (s.29). |
| d3u02 | Hubble Uzay Teleskobu ne zaman fırlatıldı? | "Hubble" yalnızca "Hubble radius" (s.151) ve "Hubble constant" (s.198) olarak geçiyor. |
| d3u03 | Pulsarların keşfi | "pulsar" hiç geçmiyor (rapor 1965, keşif 1967). Nötron yıldızı tartışması var (s.147, s.149), pulsar yok. |

## Ek geçerli sayfalar: ÖNERİ (kullanıcı onayı bekliyor)

Rapor önerileri hem özet bölümünde hem çalışma grubu bölümünde neredeyse aynı cümleyle tekrarlıyor.

| id | şu anki sayfa | önerilen ek | kanıt |
|---|---|---|---|
| d3q01 | 4 | **39** | "the Solar Astronomy Working Group met at Woods Hole, Massachusetts, from June 21 to July 3, 1965" (yer + tarih) |
| d3q02 | 11 | **24** | Recommendation 8: "with a resolution corresponding to an aperture of at least 120 inches" (golden cevapla birebir) |
| d3q09 | 157 (şekil) | **156** | "The reflecting surfaces of the objective were a paraboloid and a hyperboloid. A ray diagram for these two surfaces is shown in Figure 4." |
| d3q14 | 102 | **111** | Recommendation 2: "aperture of the order of 20 km … With larger apertures, effects due to irregularities in the interplanetary medium …" |
| d3q19 | 102 + 103 (ikisi birden gerekli) | **111** (tek başına yeterli) | s.111 tam metni içeriyor: "within about ten years … a design study, of perhaps two years' duration". |
| d3q07 | 140 (şekil) | 139 (sınırda) | Şeklin anlatıldığı metin: "a concentration toward the galactic plane, which implies that the sources are galactic objects". Soru "summary figure" diyor; eklemek isteğe bağlı. |

d3q19 için golden biçimi sorun çıkarıyor. `pages` + `needs_all_pages` "ya {102, 103} ya {111}" diyemiyor. Önerim:
`pages: [102, 103, 111]`, `needs_all_pages: false`. Böylece "tüm sayfalar" metriğinden çıkar, Recall@k'ta herhangi biri
yeter.

Değişiklik önerilmeyen yakın eşleşmeler:

- d3q16 s.181: "high vacuum, gravity-free condition, and low temperature". Kısmi; düşük basınç ve zayıf alan yok.
- d3q17 s.51: "11 years at least and may be as long as 22 years". Döngü tanımı değil, alet ömrü.
- d3q20 s.149: "proton-antiproton annihilation". Farklı süreç.
