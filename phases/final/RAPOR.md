# Final holdout ölçümü (5 Kasım 2026)

`eval/golden_final.jsonl`: 72 soru (57 cevaplanabilir, 15 cevapsız), kullanıcı yazdı, geliştirme boyunca açılmadı.
Bir kez koşuldu; sonucuna göre ayar yapılmadı. Ayarlar: Faz 8b (896 px, 2 sayfa görseli, ret tamponu 60 kr,
ENOUGH_SCORE 0.5). Raporlar: `reports/20261105-1921-retrieval.*`, `reports/20261105-1952-answers.*`.
Bellek koruyucu hiç devreye girmedi; koşu kesintisiz.

## Retrieval (hibrit + reranker)

| Metrik | Başarılı | Final | |
|---|---|---|---|
| Recall@6 | ≥ 0.90 | 0.98 | ✅ (hedef ≥ 0.95 de) |
| Recall@1 | ≥ 0.80 | 0.89 | ✅ |
| MRR | ≥ 0.85 | 0.934 | ✅ (hedef ≥ 0.92 de) |
| All pages@6 (multi_page n=8) | ≥ 0.70 | 1.00 | ✅ |
| Tür başına Recall@6 (en düşük) | ≥ 0.85 | turkish 0.90 | ✅ |
| Reranker skor ayrımı | ≥ 0.50 | 0.949 − 0.366 = 0.58 | ✅ |

## Cevaplar

| Metrik | Başarılı | Final | |
|---|---|---|---|
| faithfulness (yargıç) | ≥ 0.92 | 0.94 | ✅ |
| answer_correctness | ≥ 0.85 | 0.91 | ✅ |
| cites_expected_page | ≥ 0.85 | 0.95 | ✅ |
| citation_precision | ≥ 0.80 | 0.87 | ✅ |
| answers_without_citation | ≤ 0.05 | 0.00 | ✅ |
| unanswerable_refused (n=15) | ≥ 0.90 | 1.00 | ✅ |
| unanswerable_with_citation | 0.00 | 0.00 | ✅ (ham: 0.07, bilgi amaçlı) |
| false_refusals | ≤ 0.05 | 0.02 (f51) | ✅ |
| gecikme p50 / p95 | ≤ 30 / ≤ 60 sn | 22.2 / 40.4 | ✅ |
| TTFT p50 | ≤ 15 sn | **15.2** (p95 30.5) | ❌ 0.2 sn farkla |

Yanlışlar (5/57): f39 (figure), f44 (multi_page), f49, f51 (yanlış ret), f54 (turkish). Türkçe sorularda doğruluk
0.70 ve doğru sayfa atfı 0.70: en zayıf alt küme (tür bazında doğruluk eşiği yok, bilgi amaçlı).

## Sonuç

- 17 kalite/retrieval ölçütünün tamamı final sette geçti.
- TTFT p50 15.2 sn, ≤ 15 hedefini 0.2 sn kaçırdı (dev 12.9). Final, ayar değiştirilmeden kayıt altına alındı;
  bu ölçüt **geçmedi** olarak raporlanır.
- Henüz tamamlanmayanlar (BASARI_TANIMI §3–4): final sette yargıç kalibrasyonu (kullanıcı etiketi, kappa) ve
  GitHub CI (kullanıcı onayı gerekli). Bu ikisi olmadan "başarı" tam ilan edilemez.

## Kararlar (kullanıcı, 5 Kasım 2026)

- TTFT p50 15.2 sn: 0.2 sn fark donanım/işletim sistemi varyansı olarak kabul edildi; ayar değiştirilmedi.
- Yargıç kalibrasyonu: `reports/20261105-1952-answers-judgments-to-label.jsonl` (90 satır: tür başına yargıcın tüm nadir kararları + rastgele, seed 0) kullanıcı etiketine verildi.

## Yargıç kalibrasyonu (BASARI_TANIMI §3; etiketler kullanıcıdan, 90 satır)

| Tür | n | Uyum (≥ 0.85) | Kappa (≥ 0.70) | |
|---|---|---|---|---|
| claim_supported | 30 | 0.93 | 0.79 | ✅ |
| correct | 30 | 1.00 | 1.00 | ✅ |
| refusal | 30 | 1.00 | 1.00 | ✅ |

Etiketlerle final sadakati 0.94 → 0.958. Yargıcın correctness kararlarıyla hiçbir anlaşmazlık yok, yani 0.91 doğruluk insan etiketiyle de aynı.

## Nihai sonuç

Final holdout setinde retrieval (6/6), cevap kalitesi (11/11) ve yargıç güvenilirliği (3/3) ölçütleri geçti; TTFT p50
15.2 sn kullanıcı kararıyla kabul edildi. Birim + entegrasyon 80/80, e2e 25/25 (Faz 7). **Başarı tanımı karşılandı**,
tek açık madde: GitHub'a gönderim ve CI (§4), kullanıcı onayı bekliyor.
