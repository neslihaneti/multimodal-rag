# Faz 6a — Sayfa görseli 1280 → 896 piksel

Tarih: 5 Kasım 2026. Kullanıcı onayı: Faz 6 sırası 6a → 6b → (gerekirse) 6c.

- Tarama: `sweep6a.json` (23 soru × 1280/1024/896).
- Tam ölçüm: `reports/20261105-1206-answers*`.
- Golden: ek doc3 sayfalarıyla (sha 6cab820cb2f0). Baseline bu golden ile yeniden puanlandı: cites 0.913, precision 0.848.

## Tarama (şekil ve tablo sorularının hepsi + sayı, Türkçe, ret ve iki sayfa soruları)

| boyut | doğru | doğru sayfa atfı | p50 | ortalama | prompt token (medyan) |
|---|---|---|---|---|---|
| 1280 | 22/22 | 19 | 32.3 sn | 37.1 sn | 5.294 |
| 1024 | 22/22 | 19 | 23.6 sn | 28.4 sn | 4.142 |
| 896 | 22/22 | 20 | 20.9 sn | 26.0 sn | 3.614 |

Şekil ve tablo cevaplarındaki sayılar tek tek karşılaştırıldı; hepsi aynı.

## Tam ölçüm

| Metrik | Baseline (yeni golden) | 6a | Başarılı |
|---|---|---|---|
| answer_correctness | 0.97 | **0.99** | ≥ 0.85 ✅ |
| faithfulness | 0.96 | **0.91** | ≥ 0.92 ❌ |
| citation_precision | 0.85 | 0.84 | ≥ 0.80 ✅ |
| cites_expected_page | 0.91 | 0.90 | ≥ 0.85 ✅ |
| unanswerable_refused / with_citation | 1.00 / 0.00 | 1.00 / 0.00 | ✅ |
| raw_unanswerable_with_citation | 0.15 | 0.00 | bilgi |
| p50 / p95 | 31.4 / 63.5 sn | **22.5 / 55.7 sn** | ≤ 30 / ≤ 60 ✅ |

**Gecikme hedefi sağlandı.** Ancak sadakat eşiğin altına düştü. Düşüşün ayrıştırması:

- **Tekrar döngüsü geri geldi: q36 ve q37 (Türkçe), ~3.100 karakter, 140–190 sn.**
  - Sadakate etkisi küçük: döngüler baseline değeriyle sayılınca 0.907 → 0.912.
  - p95'in kuyruğunu da bunlar oluşturuyor.
- **Kalan düşüş: yeniden ifade edilen cevaplarda yargıcın iddia kararları değişti.**
  - Yargıç 16 iddiayı "desteklenmiyor" saydı.
  - Elle bakıldığında birçoğu atıf yapılan parçada açıkça var. Örnekler:
    - q07: F1 formülü sözle anlatılmış.
    - d3q08: "inverse-square law".
    - d3q14: "irregularities in the interplanetary medium".
    - d3q18: "prototype 1976".
  - Yargıcın kalibre edilmiş anlaşma oranı 0.93; 69 soruda birkaç iddialık oynama bu aralıkta.
  - Karar kullanıcı etiketiyle verilecek:
    `reports/20261105-1206-answers-judgments-unsupported-to-label.jsonl` (16 satır).
- d3q14'te cevap "about 43 km" dedi (golden: 20 km). Uydurma değil: s.108'de "At 1 MHz … not be more than 43 km in
  aperture" yazıyor. Belgede iki farklı rakam var.

Bellek: tam ölçüm sırasında üreticideki MPS sızıntısı (Z13) 64 GB'a ve 10 GB swap'a yol açtı.

- Bu sırada d2q02–d2q07'nin süreleri şişti (d2q06 568 sn). Bu satırlar silinip temiz bir işlemle yeniden ölçüldü.
- Bekçi 48 GB'a indirildiğinde d2q11 tek başına 50–58 GB'a çıktığı için ölçüm ilerleyemedi. Sınır 66 GB yapıldı.
- Ders: bekçi sınırı, tek bir sorunun tepe kullanımının üstünde olmalı.

## Karar (geçici)

896 tutuldu: gecikme hedefi sağlandı, doğruluk arttı. Sadakat için kullanıcı etiketi bekleniyor.

- Etiketler yargıç hatasını doğrularsa 6a kesinleşir.
- Doğrulamazsa seçenekler: 1024 piksel ya da q36/q37 döngüsüne ayrı bir çözüm.

## İnsan etiketi (5 Kasım 2026)

Kullanıcı yargıcın "desteklenmiyor" dediği 16 iddiayı etiketledi: 7'si destekleniyor (yargıcın yanlış negatifleri: q07, q20, q29 ×2, d3q07, d3q08, d3q14), 9'u desteklenmiyor (çoğu komşu sayfaya atıf; d2q09, d2q12). Etiketlerle soru başına sadakat **0.907 → 0.95** (≥ 0.92). **896 px kesinleşti.**
