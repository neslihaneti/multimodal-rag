# Faz 3b — Reddetme cümlesini atıfsız tutmak (başarısız, geri alındı)

Tarih: 4 Kasım 2026. Faz 3'ün yan etkisi: cevapsız sorularda model reddederken de atıf yazıyordu
(`unanswerable_with_citation` 0.38, hedef 0.00).

## Değişiklik

ANSWER_PROMPT'ta reddetme kuralı atıf kuralının önüne alındı ve istisna olarak yazıldı: "If the documents do not contain
the answer, reply with only one sentence saying so; that sentence has no square brackets and no excerpt numbers.
Otherwise, end every sentence …". Faz 4'ün `db.py` değişikliği de yerindeydi (retrieval ölçümünde canlı sisteme etkisi
nötrdü).

## Sonuç (`reports/20261104-1643-answers.md`, eski yargıç)

| Metrik | Faz 3 | Faz 3b |
|---|---|---|
| unanswerable_with_citation | 0.38 | **0.38** (değişmedi) |
| answer_correctness | 0.91 | 0.88 |
| faithfulness | 0.94 | 0.95 |
| cites_expected_page | 0.87 | 0.86 |
| answers_without_citation | 0.00 | 0.00 |
| unanswerable_refused | 1.00 | 1.00 |
| p50 / p95 | 43.7 / 84.2 | 41.9 / 88.8 |

- Reddederken atıf yazan 5 soru yine aynı biçimde: "The provided documents do not contain information regarding …
  [1][2][3][4][5][6]." Kuralın sırası ve açıkça istisna olarak yazılması 4B modeli etkilemedi.
- Doğruluk farkı 4 sorudan geliyor (q20, q26, q37 doğru → yanlış; q36 yanlış → doğru). Hepsinde altın sayfa iki koşuda da
  bulunmuş ve cevaplar neredeyse aynı cümleler. Yani düşüş büyük olasılıkla yargıcın sınırdaki kararlarından, prompt'tan
  değil. Yine de net 2 soruluk düşüş gerileme eşiğini aştı.

## Karar

Hedef tutmadı ve regresyon şüphesi var. **Prompt Faz 3 haline geri alındı.** Sonraki deneme (Faz 3c) tam 82 soruluk
ölçüm (~80 dk) yerine önce 13 cevapsız + 6 kısa cevaplı soruda, aramayı bir kez yapıp prompt varyantlarını karşılaştıran
hızlı bir taramayla seçilecek (`scratchpad/refusal_sweep.py`, log `phases/logs/faz-3c-sweep.log`).

Ders: tek tek prompt denemesi pahalı. Ucuz bir alt kümeyle önce tarama yapılıp yalnızca kazanan varyantla tam ölçüm
koşulmalı.
