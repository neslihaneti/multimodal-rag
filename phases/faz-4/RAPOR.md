# Faz 4 — Keyword araması: dolgu kelimeleri + uzunluk normalizasyonu

Tarih: 4 Kasım 2026. Faz 1b'de keyword araması neredeyse işe yaramıyordu (R@6 0.29) ve RRF, vektör sırasını bozuyordu
(hibrit R@1 0.41 < vektör 0.81). İki neden vardı. Sorgu "what/the/does…" gibi dolgu kelimeleri dahil bütün kelimeleri
OR'luyordu. `ts_rank_cd` de çok terimli OR sorgularında uzun parçaları kayırıyordu.

## Değişiklik (`db.py`)

- `STOPWORDS`: İngilizce ve Türkçe soru/dolgu kelimeleri (`what, the, does, …, nedir, hangi, için, …`) sorgudan atılır.
- `ts_rank_cd(tsv, q)` → `ts_rank(tsv, q, 1)`. Normalizasyon 1, skoru `1 + log(parça uzunluğu)`'na böler. Hem
  `keyword_search` hem `hybrid_search`'ün sparse CTE'si aynı sıralamayı kullanır.
- Testler: `test_keyword_query_drops_question_words`. Türkçe test "nedir"in atıldığını doğrular. Entegrasyon testi
  (D "zebra zebra zebra" > C) normalizasyonla da geçiyor. Birim + entegrasyon 53 test geçti.

## Sonuç (`reports/20261104-1515-retrieval.md`, 69 cevaplanabilir soru)

| Yöntem | Faz 1b R@1 / R@6 / MRR | **Faz 4 R@1 / R@6 / MRR** |
|---|---|---|
| vector | 0.81 / 0.94 / 0.867 | 0.81 / 0.94 / 0.867 (aynı) |
| keyword | 0.07 / 0.29 / 0.169 | **0.51 / 0.86 / 0.655** |
| hybrid (RRF) | 0.41 / 0.83 / 0.548 | **0.71 / 0.90 / 0.792** |
| vector + reranker | 0.81 / 0.96 / 0.879 | 0.81 / 0.96 / 0.879 (aynı) |
| **hybrid + reranker (canlı)** | 0.81 / 0.96 / 0.880 | **0.81 / 0.96 / 0.879** |

| Belge (n), canlı R@6 / MRR | Faz 1b | Faz 4 |
|---|---|---|
| doc1 (37) | 1.00 / 0.94 | 0.97 / 0.93 |
| doc2 (12) | 0.75 / 0.55 | **0.83 / 0.56** |
| doc3 örneği (20) | 1.00 / 0.97 | 1.00 / 0.97 |

Canlı sistemde sırası değişen 5 soru:

| Soru | Faz 1b sıra | Faz 4 sıra | |
|---|---|---|---|
| d2q03 (G sabiti, tablo) | 29 | **6** | ilk 6'ya girdi |
| q24 (back-to-back, paraphrase) | 6 | 7 | ilk 6'dan çıktı |
| q17 | 2 | 3 | |
| d2q10 | 14 | 15 | |
| d2q12 | 7 | 8 | |

Bulgular:

- **Keyword araması artık çalışıyor** (R@6 0.29 → 0.86), RRF de vektör sırasını bozmuyor (hibrit R@1 0.41 → 0.71).
  Scratchpad deneyinin öngördüğü 0.86 tuttu.
- **Canlı sisteme net etki nötr.** Reranker 40 adayın sırasını baştan belirliyor; adaylar zaten çoğunlukla aynı. Bir soru
  kazanıldı (d2q03), bir soru kaybedildi (q24). Gerileme kuralı (birden fazla soruda düşüş) ihlal edilmedi.
- Değişiklik yine de tutuldu. Reranker'dan önceki aday kümesi artık tam terimler ve kodlar için daha sağlam. RRF'nin kendi
  sıralaması da anlamlı oldu: reranker ileride kısaltılırsa veya atlanırsa (Faz 6 gecikme) bu önemli olacak.
- Türkçe keyword hâlâ zayıf (R@6 0.50): `simple` sözlüğü kök bulmuyor ("zehirlenmesi" ≠ "zehirlenme"). Vektör arama
  Türkçeyi zaten taşıyor (1.00), şimdilik ayrı faz açılmadı.
- doc2'nin kalan zayıflığı (d2q10 15., d2q11, d2q12) uzun LaTeX/tablo parçalarından → Faz 5.

## Sonraki

Faz 3b (reddetme cümlesi atıfsız) cevap ölçümü bu kodla koşuluyor; Faz 5 parçalama.
