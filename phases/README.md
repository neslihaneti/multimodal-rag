# Fazlar: ölç → düzelt → tekrar ölç

Hedef: [`BASARI_TANIMI.md`](BASARI_TANIMI.md). Fazlar bu tanım final test setinde karşılanana kadar sürer.

Her iyileştirme ayrı bir fazdır. Bir faz şu adımlardan oluşur:

1. **Hedef:** hangi sorunu çözüyoruz, hangi ölçümün değişmesini bekliyoruz (önceki fazın raporundan).
2. **Değişiklik:** koddaki tek bir iyileştirme (birden fazla değişiklik etkiyi karıştırır).
3. **Tekrar ölçüm:** `pytest`, `pytest tests/e2e`, `python3 evaluate.py retrieval`, gerekirse `python3 evaluate.py answers`.
4. **Karşılaştırma:** önceki fazın tablolarıyla yan yana; iyileşti mi, başka bir şey bozuldu mu (regresyon)?
5. **Kayıt:** `faz-N/RAPOR.md` + ölçüm raporlarının kopyası `faz-N/reports/`; çıkan zorluklar [`ZORLUKLAR.md`](ZORLUKLAR.md)'ye.

| Faz | Konu | Durum | Rapor |
|---|---|---|---|
| 1 | Test altyapısı kuruldu, başlangıç (baseline) ölçümü | ✅ 4 Kasım 2026 | [faz-1/RAPOR.md](faz-1/RAPOR.md) |
| 1b | Üç belgeli indeks (doc1 + doc2 + doc3 örneği), 82 soruluk geliştirme seti, yeni baseline; q43'te çökme bulundu | ✅ 4 Kasım 2026 | [faz-1b/RAPOR.md](faz-1b/RAPOR.md) |
| 2 | Kararlılık: uzun prompt'ta segfault → token bütçesi + MPS önbellek boşaltma; 82/82 tamamlandı | ✅ 4 Kasım 2026 | [faz-2/RAPOR.md](faz-2/RAPOR.md) |
| 3 | Atıf oranı: atıfsız 0.30→0.00, doğru sayfa 0.62→0.87 (yan etki: reddederken atıf 0.38) | ✅ 4 Kasım 2026 | [faz-3/RAPOR.md](faz-3/RAPOR.md) |
| 3b | Reddetme cümlesi atıfsız (prompt'ta istisna): etkisiz (0.38 → 0.38), geri alındı | ❌ 4 Kasım 2026 | [faz-3b/RAPOR.md](faz-3b/RAPOR.md) |
| 3c | Reddetme: 5 prompt varyantı hızlı taramada; sabit ret cümlesi seçildi (taramada 5 → 0 atıf) | ✅ 4 Kasım 2026 (tam ölçüm Faz J'de) | [faz-3c/RAPOR.md](faz-3c/RAPOR.md) |
| J | Yargıç: cümle = iddia, atıflı parçayla kontrol, correctness ve çapraz dil prompt'ları (kullanıcı kalibrasyonundan) | ✅ 4 Kasım 2026 (correctness 0.94, ret atıfı 0.38→0.00; kalibrasyon: claim κ 0.61→0.86, üç tür de geçer; doc2 golden düzeltildi) | [faz-j/RAPOR.md](faz-j/RAPOR.md) |
| 4 | Keyword araması: keyword R@6 0.29→0.86, hibrit R@1 0.41→0.71; canlı sistem nötr | ✅ 4 Kasım 2026 | [faz-4/RAPOR.md](faz-4/RAPOR.md) |
| 5 | Parçalama (uzun liste/tablo bölme, yeniden parçalama): R@1 0.81→0.88, correct 0.97, p95 104→67 sn, döngüler kayboldu; ret atıfı 0.15 | ✅ 5 Kasım 2026 | [faz-5/RAPOR.md](faz-5/RAPOR.md) |
| 5b | Tekrar engeli taraması: HF n-gram sayıları bozuyor (2017→2020), döngüler Faz 5'te zaten yok → üretim ayarı yok; yargıçta cümle tekilleştirme | ✅ 5 Kasım 2026 | [faz-5b/RAPOR.md](faz-5b/RAPOR.md) |
| 5c | Sabit ret cümlesi, soru dilinde ve atıfsız (simülasyonda ret atıfı 0.15→0.00, Türkçe soruya Türkçe ret); başarı tanımı güncellendi | ✅ 5 Kasım 2026 (tam ölçüm yeni baseline'da) | [faz-5c/RAPOR.md](faz-5c/RAPOR.md) |
| B | Tam indeks baseline (doc3 200 sayfa): R@6 0.94, correct 0.97, ret atıfı 0.00; tüm kalite eşikleri geçiyor, gecikme p50/p95 31.4/63.5 sn ❌; e2e 25/25 | ✅ 5 Kasım 2026 | [baseline-full/RAPOR.md](baseline-full/RAPOR.md) |
| 6a | Sayfa görseli 1280→896 px: p50/p95 31.4/63.5 → 22.5/55.7 sn, correct 0.99; faithfulness 0.91 (yargıç etiketi bekleniyor), q36/q37 döngüsü geri geldi | ✅ 5 Kasım 2026 (sadakat için etiket bekleniyor) | [faz-6a/RAPOR.md](faz-6a/RAPOR.md) |
| 6b | Reranker skoru ≥ 0.5 ise arama kararını atla: cevaplar 82/82 aynı, p50 21.6 sn | ✅ 5 Kasım 2026 | [faz-6b/RAPOR.md](faz-6b/RAPOR.md) |
| 6c | sdpa | ⏭ atlandı (hedef 6a+6b ile sağlandı) | — |
| 7 | Streaming: cevaplar 82/82 aynı, p50 toplam 19.9 sn; TTFT p50/p95 17.7/37.5 sn ❌ (prefill 7–10 sn + ilk cümle tamponu) | ✅ 5 Kasım 2026 (TTFT önerisi kullanıcıda) | [faz-7/RAPOR.md](faz-7/RAPOR.md) |
| 8 | Ret tamponu 60 kr + 2 sayfa görseli: correct 0.97, sadakat 0.957 (insan etiketli), TTFT p50 12.9 sn; TTFT hedefi ≤ 15 sn | ✅ 5 Kasım 2026 | [faz-8/RAPOR.md](faz-8/RAPOR.md) |
| Final | Holdout 72 soru: 17 kalite/retrieval ölçütü ✅, yargıç kalibrasyonu 3/3 ✅ (kappa 0.79/1.00/1.00); TTFT p50 15.2 sn (kullanıcı kabulü) | ✅ 5 Kasım 2026 | [final/RAPOR.md](final/RAPOR.md) |
| 9 | (final sonrası) Cevap dili koddan: soru dili / açık istek; dil uyumsuzluğu 1 → 0, doğruluk 0.97 aynı | ✅ 6 Kasım 2026 | [faz-9/RAPOR.md](faz-9/RAPOR.md) |
| 10 | (final sonrası) Türkçe sorgu + İngilizce çeviriyle arama: correct 0.99, Türkçe 12/12; Türkçe TTFT +9 sn (p95 75 ❌, TTFT p50 17.1 ❌). Kullanıcı kararıyla geri alındı, kod Faz 9'da | ↩ 6 Kasım 2026 | [faz-10/RAPOR.md](faz-10/RAPOR.md) |

Faz sırası önerisi [faz-1/RAPOR.md](faz-1/RAPOR.md#faz-planı) sonunda. Basamakların ayrıntısı: [`../IMPROVEMENTS.md`](../IMPROVEMENTS.md).
