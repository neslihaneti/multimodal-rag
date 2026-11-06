# Faz 1b — Üç belgeli indeksle yeni başlangıç ölçümü

Tarih: 4 Kasım 2026. Faz 1 yalnızca doc1 ile ölçülmüştü; başarı tanımı doc2 ve doc3'ü kapsadığı için (BASARI_TANIMI §0.2)
aynı kodla, üç belgeli indekste yeni baseline alındı.

## Ne değişti (kod değil, veri)

| | Faz 1 | Faz 1b |
|---|---|---|
| İndeks | doc1 (99 sayfa, 276 parça) | + doc2 (CODATA 2022, 62 sayfa metin katmanı, 269 parça) + doc3 örneği (1966 taranmış rapor, 40 sayfa Chandra OCR, 112 parça) |
| Geliştirme seti | `golden_doc1.jsonl` 45 soru | `golden_dev.jsonl` 82 soru (doc2 14, doc3 23; doc3'te 5 tablo, 4 şekil, 2 çok sayfalı) |
| Rapor | tür kırılımı | + belge kırılımı |

doc3 soruları indekslenmiş Chandra metninden yazıldı ve kilit ifadeleri metinde doğrulandı; `orig_pages` alanı orijinal
doc3 sayfasını tutar (indeksteki sayfa numarası örnek PDF'in sayfasıdır, `eval/doc3_sample_pages.json`).

## Retrieval (`reports/20261104-1019-retrieval.md`, 69 cevaplanabilir soru)

| Yöntem | R@1 | R@6 | MRR | All pages@6 (n=5) |
|---|---|---|---|---|
| vector | 0.81 | 0.94 | 0.867 | 0.40 |
| keyword | 0.07 | 0.29 | 0.169 | 0.00 |
| hybrid (RRF) | 0.41 | 0.83 | 0.548 | 0.00 |
| vector + reranker | 0.81 | 0.96 | 0.879 | 0.60 |
| **hybrid + reranker (canlı)** | **0.81** | **0.96** | **0.880** | 0.60 |

| Belge (n) | canlı R@6 / MRR |
|---|---|
| doc1 (37) | 1.00 / 0.94 |
| doc2 (12) | **0.75 / 0.55** |
| doc3 örneği (20) | 1.00 / 0.97 |

Bulgular:

- **doc3 (taranmış, OCR) beklenenden iyi:** 20 sorunun 18'inde doğru sayfa 1. sırada; tablo ve şekil soruları dahil.
  Chandra'nın şekil açıklamaları (`![Figure 1: …]`) şekil sorularını aranabilir yapıyor.
- **doc2 zayıf halka:** d2q03 (G sabiti, tablo) 29. sırada, d2q10 (paraphrase) 14., d2q12 7. doc2'de parçalar 6.104
  karaktere kadar uzun (tablolar ve LaTeX); reranker uzun parçanın yalnızca başını değerlendirebiliyor → Faz 5
  (parçalama) adayı.
- **Keyword araması neredeyse işe yaramıyor (R@6 0.29)** ve RRF canlı sistemde vektör sırasını bozuyor (hibrit R@1 0.41
  < vektör 0.81). Neden (GPU'suz deneyle ayrıştırıldı): sorgu "what/the/does…" gibi dolgu kelimeleri dahil tüm
  kelimeleri OR'luyor ve `ts_rank_cd` çok terimli OR sorgularında uzun parçaları kayırıyor. Dolgu kelimesi listesi +
  `ts_rank(tsv, q, 1)` ile keyword R@6 0.29 → **0.86** → Faz 4.
- Başarı eşikleri (geliştirme setinde, canlı sistem): R@6 0.96 ≥ 0.90 ✅, R@1 0.81 ≥ 0.80 ✅ (sınırda), MRR 0.88 ≥ 0.85 ✅,
  tür başına R@6 (n ≥ 8): factual 1.00, paraphrase 0.91, table 0.91, turkish 0.92 ✅.

## Cevaplar — kısmi (q01–q42, hepsi doc1) ve çökme

Değerlendirme 43. soruda (q43, cevapsız "What is the capital of Australia?") iki kez süreç çökmesiyle durdu:
`Segmentation fault` in `eager_attention_forward`. Prompt 13.298 token'dı (doc2'nin dev parçaları + 3 görsel). Ayrıntı ve
hipotez testleri: [ZORLUKLAR.md Z9, Z10](../ZORLUKLAR.md). **Baseline sistemi, uzun bağlam gerektiren her soruda
(kullanıcı arayüzü dahil) çöküyordu** — Faz 2 bu yüzden atıf oranının önüne alındı.

İlk 42 sorunun sonuçları (`reports/20261104-answers-partial-42.jsonl`; Faz 1 ile aynı sorular, şimdi çok belgeli indeksle):

| Metrik | Faz 1 (45 soru) | Faz 1b (ilk 42) |
|---|---|---|
| answer_correctness | 0.92 | 0.92 |
| faithfulness | 0.96 | 0.95 |
| cites_expected_page | 0.73 | 0.70 |
| answers_without_citation | 0.24 | **0.30** (11 soru) |
| false_refusals | 0.00 | 0.00 |
| unanswerable_refused | 1.00 | 1.00 (n=5) |
| gecikme p50 / p95 | — / — | 41.7 / 76.4 sn |

Çok belgeli indeks doc1 cevaplarını belirgin bozmadı (çeldirici etkisi küçük); atıfsız kısa cevap sorunu sürüyor.

## Sonraki fazlar

1. **Faz 2 — kararlılık:** prompt token bütçesi (çökmeyi önlemek).
2. **Faz 3 — atıf oranı** (Faz 1'den beri ilk sıradaki iyileştirme).
3. **Faz 4 — keyword araması** (dolgu kelimeleri + `ts_rank`).
4. **Faz 5 — parçalama** (uzun liste/tablo bölme, `rechunk_document`).
5. **Faz 6 — gecikme** (p50 41.7 sn > 30 hedef).
