# Faz 5 — Parçalama: uzun liste/tablo/satır bölme + yeniden parçalama

Tarih: 5 Kasım 2026. Raporlar: `reports/20261105-0019-retrieval.md`, `reports/20261105-0116-answers.md`.

## Değişiklik

- `chunk_markdown` uzun listeleri, tabloları ve satırları 1500 karakter sınırında bölüyor; tablo başlığı her parçada
  tekrar ediliyor. Eskiden xfail olan `test_long_bullet_list_respects_max_chars` artık geçiyor.
- `indexer.rechunk_document`: OCR yapmadan, saklı sayfa metninden yeniden parçalıyor (sayfa başına transaction,
  tekrar çalıştırılabilir).
- Yalnızca bölünmesi değişen sayfalar yeniden yazıldı: doc1 24 sayfa (6 dk), doc2 28 sayfa (32 dk), doc3_sample
  5 sayfa (2.5 dk).
  - Parça sayısı 657'den 713'e çıktı: doc1 298, doc2 304, doc3_sample 111.
  - En uzun parça 6.104 karakterden 1.500'e indi.
- Yedek: `backups/pre-faz5-20261104-2306.dump` (git dışında).

Aynı ölçümde iki değişiklik daha var:

- **Golden:** kullanıcı doc2'de 7 soruya ikinci geçerli sayfayı ekledi (Faz J raporu).
- **Bellek düzeltmesi Z13:** embedder ve reranker girdileri 128'in katlarına dolduruluyor. Skor farkı en çok 0.00017.

Golden'ın etkisi aşağıda ayrıca hesaplandı. Yargıç Faz J ile aynı (`judge_sha256` c2301e4f60d7).

## Retrieval (canlı sistem: hibrit + reranker)

| Metrik | Faz 4 | Faz 5 | Başarılı eşiği |
|---|---|---|---|
| Recall@1 | 0.81 | **0.88** | ≥ 0.80 |
| Recall@6 | 0.96 | 0.94 | ≥ 0.90 |
| MRR | 0.879 | **0.918** | ≥ 0.85 |
| doc2 R@1 / R@6 | 0.33 / 0.83 | 0.67 / 0.75 | — |
| Türkçe R@1 | 0.75 | 0.92 | — |

- R@6'daki düşüş tek bir sorudan geliyor: d2q03 6. sıradan 8. sıraya indi.
- doc2 R@1'deki artışın bir kısmı golden'a eklenen sayfalardan geliyor.
- Vektör araması tek başına da iyileşti (R@6 0.94 → 0.97). Kısa parçaların embedding'i konuyu daha net taşıyor.

## Cevaplar

| Metrik | Faz J | Faz 5 | Başarılı eşiği |
|---|---|---|---|
| answer_correctness | 0.94 | **0.97** | ≥ 0.85 |
| faithfulness | 0.93 | **0.94** | ≥ 0.92 |
| cites_expected_page | 0.83 (yeni golden ile 0.93) | 0.90 | ≥ 0.85 |
| citation_precision | 0.77 (yeni golden ile 0.87) | 0.84 | ≥ 0.80 |
| answers_without_citation | 0.00 | 0.00 | ≤ 0.05 |
| unanswerable_refused | 1.00 | 1.00 | ≥ 0.90 |
| unanswerable_with_citation | 0.00 | **0.15** ❌ | 0.00 |
| false_refusals | 0.00 | 0.00 | ≤ 0.05 |
| p50 / p95 gecikme | 39.6 / 103.9 sn | 35.4 / 67.0 sn | ≤ 30 / ≤ 60 sn |

**İyileşmeler:**

- **Tekrar döngüleri kayboldu.** Faz J'de q33, q36, q37 ve d2q10 aynı cümleyi 6–40 kez tekrar ediyordu (175–208 sn).
  Faz 5'te en uzun cevap 2.500 karakterin altında, en yavaş soru 81 sn.
  - p95 104 sn'den 67 sn'ye indi.
  - q33 ve q36 artık doğru, Türkçe doğruluk 0.75'ten 0.92'ye çıktı.
  - Döngüleri uzun parçaların (LaTeX yoğun, 3.5–6 bin karakter) tetiklediği anlaşılıyor.
- Ölçüm bekçiye takılmadan, tek seferde bitti (Z13 düzeltmesi).

**Gerilemeler:**

- **Atıf:** golden etkisi çıkarılınca, yani Faz J yeni golden ile yeniden puanlanınca, cites_expected_page 0.928'den
  0.899'a, citation_precision 0.872'den 0.843'e indi. Bu yaklaşık iki soru (q26, q33 doğru sayfayı artık göstermiyor).
  - Kural 0.4'teki "> 0.03" sınırının altında kaldığı için anlamlı gerileme sayılmıyor, ama sınırda.
  - Bilinçli kabul: doğruluk, sadakat ve gecikmedeki kazanç daha büyük.
- **Ret cümlesi atıflı (0.15):** q42 ve q45 "The documents do not contain information about this [1][2][3][4][5][6]."
  yazıyor. Prompt aynı; yalnızca bulunan parçalar değişti. Yani Faz 3c'nin sep_rule'u kırılgan.
  - Kullanıcıya giden cevapta bu atıflar kaynak olarak görünmüyor, çünkü ret regex'i yakalıyor. Ama ham metin
    metriği hedefi kaçırıyor.
  - Faz 5b taramasına eklendi: `[1][2]…[6]` dizisi de bir tekrar biçimi, n-gram engeli ya da tekrar cezası
    düzeltebilir.

## Karar

Faz 5 tutuldu. Retrieval, doğruluk, sadakat ve gecikme iyileşti. Atıftaki iki soruluk düşüş sınırın altında.
unanswerable_with_citation Faz 5b'de ele alınıyor.
