# Faz 8: TTFT (Yol 3 + Yol 1)

Kullanıcı kararı (5 Kasım 2026): ret tamponu ~60 karakter (Yol 3) + prompt'ta daha az sayfa görseli (Yol 1); sdpa yok.
TTFT p50 11–14 sn bandına inerse hedef ≤ 15 sn (Yol 4).

## Yol 3: `rag.FIRST_SENTENCE_MAX` 300 → 60

Faz 7'nin 82 ham cevabında 40/50/60/80 karakterlik tamponla ret kararları tam ilk cümleyle verilenle birebir aynı.
Birim testi eklendi (`test_stream_starts_before_a_long_first_sentence_ends`); birim + entegrasyon 80 geçti.

## Yol 1: görsel sayısı taraması (`sweep8.json`, 22 şekil/tablo/seçili soru, tampon 60)

| Görsel | Doğruluk | Doğru sayfa atfı | TTFT p50 / p95 | Toplam p50 |
|---|---|---|---|---|
| 3 | 22/22 | 20 | 13.5 / 25.7 | 16.6 |
| 2 | 22/22 | 20 | 11.5 / 23.1 | 14.6 |
| 1 | 22/22 | 20 | 10.6 / 22.0 | 12.4 |

## Tam ölçüm (82 soru)

| | Faz 7 (3 görsel, tampon 300) | Faz 8 (1 görsel) | **Faz 8b (2 görsel)** |
|---|---|---|---|
| answer_correctness | 0.99 | 0.96 | **0.97** |
| faithfulness (yargıç) | 0.91 | 0.93 | 0.90 |
| citation_precision | 0.84 | 0.86 | 0.84 |
| cites_expected_page | 0.90 | 0.90 | 0.90 |
| answers_without_citation / false_refusals | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 |
| unanswerable_refused / with_citation | 1.00 / 0.00 | 1.00 / 0.00 | 1.00 / 0.00 |
| gecikme p50 / p95 | 19.9 / 56.1 | 14.6 / 37.7 | 17.8 / 52.4 |
| TTFT p50 / p95 | 17.7 / 37.5 | 10.8 / 31.1 | **12.9 / 36.4** |

- 1 görsel: q24 ve q29 yeni yanlış (q24 uydurma "test cases or inputs"; q29 içindekiler tablosunu döngüyle sayıp
  olmayan parçalara [7]–[11] atıf). İki soru > gerileme sınırı. Ayrı deneme deterministik: 1 görsel ikisi ❌,
  2 görsel yalnız q24 ❌, 3 görsel ikisi ✅. → **`MAX_PAGE_IMAGES = 2`** (onaylı Yol 1 "1–2 görsel").
- 8b: yanlışlar q24 (yeni, 1 soru = sınır içinde) ve d2q12 (eskiden beri). TTFT p50 12.9 → BASARI_TANIMI TTFT p50
  hedefi ≤ 15 sn yapıldı (Yol 4, kullanıcı onaylı).
- Sadakat: yargıç 0.90 (< 0.92). 6a'nın insan etiketleri birebir aynı iddialara uygulanınca 0.914. Etiketsiz 11
  "desteklenmiyor" iddiası: `reports/20261105-1812-answers-judgments-unsupported-to-label.jsonl` → **kullanıcı etiketi bekleniyor**;
  final holdout bu karardan sonra (final bir kez koşulur, sonrasında ayar değişmemeli).
