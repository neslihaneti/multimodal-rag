# Faz 2 — Kararlılık: uzun prompt'ta çökme → token bütçesi

Tarih: 4 Kasım 2026. Faz 1b'nin cevap değerlendirmesi q43'te iki kez süreç çökmesiyle durmuştu (segfault,
`eager_attention_forward`, 13.298 token'lık prompt). Bu faz atıf oranından önce alındı, çünkü çökme kullanıcı arayüzünü de
etkiliyordu. Ayrıntılı tanı: [ZORLUKLAR.md Z10](../ZORLUKLAR.md), bellek sorunu: Z11.

## Hedef

82 soruluk geliştirme seti çökmeden bitsin; kalite metrikleri Faz 1b'den kötüleşmesin.

## Değişiklik

| Dosya | Ne |
|---|---|
| `model.py` | MPS'te eager attention'da kalındı (sdpa ~9.5k token'dan itibaren çöp üretip sonraki çağrıları da bozuyor). `MAX_INPUT_TOKENS = 10000`: aşan prompt çökme yerine `ValueError` ile reddedilir. `count_tokens()`. Her `generate` sonrası `torch.mps.empty_cache()` (Z11). |
| `rag.py` | `PROMPT_TOKEN_BUDGET = 9000`. `fit_prompt`: önce en düşük sıralı parçalar (en az 3 kalana kadar), sonra sayfa görselleri, en son yine parçalar atılır. Arama-karar prompt'u da aynı bütçeyle kırpılır. |
| testler | `tests/unit/test_prompt_budget.py` (3), `test_decision_prompt_is_kept_under_the_token_budget`. Toplam birim 43, tüm testler 52 geçti. |

## Sonuç (`reports/20261104-1330-answers.md`, 82 soru)

Ölçüm iki parçada bitti. İlk koşu 81. soruya kadar gitti ve d3u03'te **MPS bellek yetersizliğiyle** durdu: eager
attention'ın GB'larca tamponu önbellekte birikiyordu. `empty_cache` eklenip `--resume` ile son soru tamamlandı.
Kontrol: prompt değişmediği için (prompt_sha256 aynı) iki parça aynı sistemi ölçüyor.

| Metrik | Hedef | Faz 1b (ilk 42, doc1) | **Faz 2 (82)** | Faz 2, yalnız doc1 (45) |
|---|---|---|---|---|
| tamamlanan soru | 82 | 42 (çöktü) | **82** ✅ | 45 |
| answer_correctness | ≥ 0.85 | 0.92 | **0.91** ✅ | 0.92 |
| faithfulness | ≥ 0.92 | 0.95 | **0.93** ✅ | 0.95 |
| citation_precision | ≥ 0.80 | — | **0.83** ✅ | — |
| cites_expected_page | ≥ 0.85 | 0.70 | **0.62** ❌ | 0.70 |
| answers_without_citation | ≤ 0.05 | 0.30 | **0.30** ❌ | 0.30 |
| false_refusals | ≤ 0.05 | 0.00 | **0.00** ✅ | — |
| unanswerable_refused | ≥ 0.90 | 1.00 (n=5) | **0.92** ✅ (n=13) | 0.88 |
| gecikme p50 / p95 | ≤ 30 / ≤ 60 sn | 41.7 / 76.4 | **49.9 / 97.8** ❌ | — |

| Belge (n) | correct | faithfulness | cites expected page | atıfsız | cevapsız reddi |
|---|---|---|---|---|---|
| doc1 (45) | 0.92 | 0.95 | 0.70 | 0.30 | 0.88 |
| doc2 (14) | 0.83 | 0.85 | **0.33** | 0.25 | 1.00 |
| doc3 örneği (23) | 0.95 | 0.92 | 0.65 | 0.35 | 1.00 |

Bulgular:

- **Çökme giderildi.** q43 artık doğru reddediliyor (122 sn). doc1 sonuçları Faz 1b ile aynı düzeyde (0.92 / 0.95 / 0.70 / 0.30), yani
  bütçe doc1'de kaliteyi düşürmedi.
- **doc2 zayıf halka.** Atıflarda doğru sayfa yalnızca 0.33; yanlış 6 cevabın 2'si 14 soruluk doc2'de (d2q10, d2q12). Retrieval'daki
  doc2 zayıflığıyla (R@6 0.75) uyumlu: dev parçalar bütçeyle kırpılınca altın sayfa da kırpılabiliyor → Faz 5 (parçalama).
- **Atıfsız cevap oranı 0.30** (en büyük açık). Örnek: d2q06 doğru ama atıfsız ("The 2022 least-squares adjustment
  used 133 input data and 79 adjusted constants."). Kısa tek cümlelik cevaplarda model atıfı atlıyor → Faz 3.
- **q44 (Kubernetes pod, cevapsız):** model önce uydurma bir cümleyi doc2'ye atıfla verip sonra "metinlerde
  açıklanmamıştır" dedi. Reddetme regex'i "açıklanmamış"ı tanımıyor ve cevap kısmen uydurma. Ayrı bir iyileştirme
  adayı (reddetme biçimi); Faz 3'ün prompt'u da etkileyebilir, önce o ölçülecek.
- **Gecikme arttı** (p95 97.8 sn): doc2/doc3 soruları uzun prompt'larla geliyor ve eager attention yavaş. Faz 6.
- Yanlış 6 cevap: q24, q31, q35 (doc1, Faz 1'den beri), d2q10, d2q12, d3q12; ayrıca reddedilmeyen cevapsız q44.

## Sonraki faz

Faz 3 — atıf oranı: ANSWER_PROMPT'ta "her cümleyi atıfla bitir, tek cümlelik cevap dahil" talimatı.
