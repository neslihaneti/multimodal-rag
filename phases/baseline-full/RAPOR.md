# Baseline: tam indeks (doc1 + doc2 + doc3'ün 200 sayfası), Faz 5c ile

Tarih: 5 Kasım 2026.

- İndeks: 3 belge, 1.164 parça. doc3_sample yerine doc3.pdf'in tamamı.
- Golden: `golden_dev.jsonl` (sha 236b0d3efd8e). doc3 soruları orijinal sayfa numaralarında.
  - Ek sayfa önerisi henüz uygulanmadı: `../doc3-tam-golden-kontrol.md`.
- Raporlar: `reports/20261105-0756-retrieval.*`, `reports/20261105-0849-answers*`.
- Ölçüm tek seferde bitti: bekçi devreye girmedi, devam (resume) gerekmedi. 82 soru ~50 dk sürdü.

## Retrieval (hibrit + reranker)

| Metrik | Faz 5 (doc3 örneği) | Tam indeks | Başarılı |
|---|---|---|---|
| Recall@1 | 0.88 | 0.86 | ≥ 0.80 |
| Recall@6 | 0.94 | 0.94 | ≥ 0.90 |
| MRR | 0.918 | 0.903 | ≥ 0.85 |
| doc3 R@6 / MRR | — | 1.00 / 0.93 | — |

- doc3 160 sayfa büyüdü ama R@6 1.00'da kaldı.
- R@1'deki düşüş üç doc3 sorusundan geliyor (d3q02, d3q03, d3q19 2. sırada).
  - d3q02 ve d3q19 için 1. sıradaki parça, ek sayfa önerisindeki tekrar sayfaları. Golden onaylanırsa bu ikisi büyük
    ihtimalle 1. sıraya çıkar.
- Hâlâ ilk 6'nın dışında kalanlar: q24 (7), d2q03 (8), d2q10 (15), d2q12 (7).

## Cevaplar

| Metrik | Faz 5 | Tam indeks + 5c | Başarılı |
|---|---|---|---|
| answer_correctness | 0.97 | 0.97 | ≥ 0.85 ✅ |
| faithfulness | 0.94 | 0.96 | ≥ 0.92 ✅ |
| citation_precision | 0.84 | 0.82 | ≥ 0.80 ✅ |
| cites_expected_page | 0.90 | 0.90 | ≥ 0.85 ✅ |
| answers_without_citation | 0.00 | 0.00 | ≤ 0.05 ✅ |
| false_refusals | 0.00 | 0.00 | ≤ 0.05 ✅ |
| unanswerable_refused | 1.00 | 1.00 | ≥ 0.90 ✅ |
| unanswerable_with_citation | 0.15 | **0.00** | 0.00 ✅ |
| raw_unanswerable_with_citation (bilgi) | — | 0.15 | — |
| p50 / p95 gecikme | 35.4 / 67.0 sn | 31.4 / 63.5 sn | ≤ 30 / ≤ 60 ❌ |

- **Faz 5c gerçek ölçümde doğrulandı.**
  - Ret atıfı 0.00; ham metinde 0.15 (q42/q45 tipi atıflı ret sürüyor, kullanıcıya gitmiyor).
  - q44, q45 ve d3u03 Türkçe ret aldı.
- Yanlış cevaplar:
  - q24: bağımsız sürüm sorusu. Doğru sayfa 7. sırada.
  - d2q12: Türkçe, doc2. Doğru sayfa 7. sırada.
  - İkisi de retrieval sorunu.
- d3q19 yalnızca s.111'i gösterdi ve cevabın tamamı orada. Golden önerisi onaylanırsa doğru sayılacak.

## E2E testleri

`pytest tests/e2e`: 25/25 geçti (3 dk). Kapsam:

- UI testleri:
  - Türkçe soru, kaynak görselleri.
  - Arama ayrıntıları.
  - İngilizce takip sorusu (ilk kez çalıştı).
  - Türkçe ret (yeni).
- Prompt injection testi.
- Yargıç ret testi (15/15).

## Durum

Başarı tanımındaki cevap ve retrieval eşiklerinin hepsi geçiyor. Kalanlar:

- Gecikme: p50 31.4 sn (hedef ≤ 30), p95 63.5 sn (hedef ≤ 60).
- TTFT: streaming yok.
- Final holdout testi.
