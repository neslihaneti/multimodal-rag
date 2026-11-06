# Faz 6b — Reranker skoru yüksekse arama kararını modele sorma

Tarih: 5 Kasım 2026. Rapor: `reports/20261105-1252-answers*`. 6a (896 px) üstüne.

## Değişiklik

- `rag.ENOUGH_SCORE = 0.5`: ilk aramada en iyi parçanın reranker skoru ≥ 0.5 ise "yeterli mi?" kararı (SEARCH_DECISION)
  modele sorulmuyor.
- Gerekçe (tam indeks retrieval verisi):
  - Cevaplanabilir 69 sorunun hepsi zaten tek turda bitiyordu, yani model her seferinde "ENOUGH" diyordu.
  - Bu soruların 62'si 0.5'in üstünde.
  - Cevapsız soruların en yüksek skoru 0.34. Bu sorular hâlâ modele soruluyor ve gerekirse ek arama yapıyor.
- Birim testi: `test_high_rerank_score_skips_the_decision`.

## Sonuç

| Metrik | 6a | 6b |
|---|---|---|
| Cevaplar | — | **82/82 birebir aynı** |
| Kalite metrikleri | correct 0.99, faith 0.91, prec 0.84, cites 0.90 | aynı |
| p50 | 22.5 sn | **21.6 sn** |
| ortalama | 30.7 sn | **29.1 sn** |
| p95 | 55.7 sn | 56.8 sn (gürültü; en yavaşlar q36/q37 döngüsü ve cevapsız sorular) |

- Bekçi bir kez yeniden başlattı (66 GB); yarıda kalan soru yeniden ölçüldü.
- Kazanç küçük (karar çağrısı kısa prompt'ta 1–3 sn), ama çıktıyı değiştirmeden geliyor.

## Faz 6c

Atlandı, kullanıcı kararıyla: 6a + 6b sonrası p50 21.6 ≤ 30 ve p95 56.8 ≤ 60. Riskli sdpa denemesine gerek kalmadı.
Sıradaki adım streaming/TTFT.
