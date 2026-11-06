# Faz 6 hazırlık: gecikme profili (5 Kasım 2026, tam indeks)

Baseline: p50 31.4 sn, p95 63.5 sn. Doğrusal uyum: süre ≈ 10.5 + 0.028 × karakter + 16.5 × arama turu (sn).
82 sorunun 72'si tek turda bitiyor (medyan 30.8 sn).

Adım adım ölçüm (`scratchpad/profile6.py`, 6 soru):

| soru | toplam | embed+db | rerank (toplam) | karar `generate` (token) | cevap `generate` (token, çıktı kr) |
|---|---|---|---|---|---|
| q01 | 26.7 | 0.07 | 3.1 | 2.5 sn (1.790) | **20.9 sn** (5.294, 65) |
| q12 | 21.4 | 0.06 | 2.4 | 1.5 sn (1.161) | **17.3 sn** (4.665, 120) |
| d3q09 | 27.3 | 0.07 | 3.2 | 2.4 sn (1.748) | **21.5 sn** (5.413, 111) |
| q31 | 53.5 | 0.07 | 2.7 | 1.3 sn (994) | **49.4 sn** (4.498, 819) |
| d2q05 | 53.7 | 0.07 | 5.0 | 8.2 sn (4.094) | **40.3 sn** (7.957, 107) |
| q43 | 65.5 | 0.15 | 10.1 | 2 × 10.2 sn (4.252) | **34.8 sn** (8.116, 72) |

- **Darboğaz: cevap prompt'unun ön işlenmesi (prefill).**
  - 65 karakterlik cevap bile 21 sn sürüyor.
  - Aynı parçalarla görselsiz karar prompt'u ~1.800 token; cevap prompt'u ~5.300 token. 3 sayfa görseli ~3.500 token
    ekliyor (görsel başına ~1.170).
  - Eager/blocked attention'da süre token sayısıyla doğrusaldan hızlı artıyor: 1.8k token 2.5 sn, 4.2k token 10 sn.
- **Uzun cevaplar:** q31'de 819 karakter için ~30 sn çözme süresi.
- **Ek arama turları:** her tur bir karar çağrısı (2–10 sn) ve rerank ekliyor.
