# Faz 3 — Atıf oranı: "her cümleyi atıfla bitir"

Tarih: 4 Kasım 2026. Faz 1'den beri en büyük açık atıfsız cevaplardı (Faz 2: 0.30, hedef ≤ 0.05). Model kısa, tek
cümlelik cevaplarda atıfı atlıyordu (ör. d2q06 "…133 input data and 79 adjusted constants.").

## Değişiklik (tek)

`rag.ANSWER_PROMPT`'taki "Cite the excerpts you used with their numbers in square brackets, like [1] or [2][3]." cümlesi
yerine:

> End every sentence of your answer with the numbers of the excerpts it is based on, in square brackets. This applies to
> short answers too: even a one-sentence answer must end with its citation, for example: "The device weighs 4 kg [2]."
> or "Both colours are allowed [1][3]."

Örnek cümleler bilinçli olarak belgelerde geçmeyen nötr cümleler. İlk taslağın örneği ("…set up in 2017") q01'in
cevabını sızdırıyordu, atıldı.

## Sonuç (`reports/20261104-1503-answers.md`, 82 soru)

| Metrik | Hedef | Faz 2 | **Faz 3** |
|---|---|---|---|
| answer_correctness | ≥ 0.85 | 0.91 | **0.91** ✅ |
| faithfulness | ≥ 0.92 | 0.93 | **0.94** ✅ |
| citation_precision | ≥ 0.80 | 0.83 | **0.84** ✅ |
| cites_expected_page | ≥ 0.85 | 0.62 | **0.87** ✅ |
| answers_without_citation | ≤ 0.05 | 0.30 | **0.00** ✅ |
| false_refusals | ≤ 0.05 | 0.00 | **0.00** ✅ |
| unanswerable_refused | ≥ 0.90 | 0.92 | **1.00** ✅ |
| unanswerable_with_citation | 0.00 | 0.08 | **0.38** ❌ (regresyon) |
| gecikme p50 / p95 | ≤ 30 / ≤ 60 sn | 49.9 / 97.8 | **43.7 / 84.2** ❌ |

| Belge (n) | correct | faithfulness | cites expected page | atıfsız | cevapsız reddi |
|---|---|---|---|---|---|
| doc1 (45) | 0.95 | 0.95 | **1.00** | 0.00 | 1.00 |
| doc2 (14) | 0.75 | 0.86 | **0.33** | 0.00 | 1.00 |
| doc3 örneği (23) | 0.95 | 0.98 | 0.95 | 0.00 | 1.00 |

Bulgular:

- **Hedef aşıldı:** atıfsız cevap 0.30 → 0.00, doğru sayfaya atıf 0.62 → 0.87. Doğruluk ve sadakat düşmedi.
- **q44 düzeldi** (Faz 2'de kısmen uydurup reddetmemişti); cevapsız soruların hepsi reddedildi.
- **Yan etki (regresyon):** cevapsız 13 sorunun 5'inde model reddederken de atıf yazıyor:
  "The provided documents do not contain information about the half-life of carbon-14 [1][2][3]." "Her cümleyi atıfla
  bitir" talimatı "reddederken köşeli parantez kullanma" talimatını bastırdı. Kullanıcı arayüzünde kaynak gösterilmiyor
  (`NOT_FOUND` regex'i atıfları siliyor), ama ham metin metriği bunu ölçüyor ve kullanıcı metinde `[1][2][3]` görüyor
  → **Faz 3b**.
- **doc2 hâlâ zayıf:** doğru sayfaya atıf 0.33, doğruluk 0.75. Atıf vardı ama yanlış sayfaya; kök neden retrieval/parçalama
  (Faz 4/5).
- **Yargıç katılığı:** d2q08 "chi-squared 44.2" doğru ama beklenen cevaptaki p-değeri yok diye yanlış sayıldı. Gerçek
  doğruluk muhtemelen bir soru yüksek; kalibrasyon etiketleriyle (kullanıcı) ölçülecek.
- Yanlış sayılanlar: q24, q36, d2q08 (yargıç), d2q10, d2q12, d3q12.
- Gecikme biraz düştü (doğrudan bir hız değişikliği yok; muhtemelen daha kısa cevaplar ve q44'te tek arama turu).

## Sonraki

- **Faz 3b:** reddetme cümlesinin atıfsız kalması için prompt'ta reddetmeyi atıf kuralının istisnası olarak açıkça yazmak.
- **Faz 4:** keyword araması (kod hazır, retrieval ölçülüyor).
