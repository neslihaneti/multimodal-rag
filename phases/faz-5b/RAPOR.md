# Faz 5b — Cevapta tekrar engeli (tarama) + yargıçta cümle tekilleştirme

Tarih: 5 Kasım 2026. Kullanıcı onayı ve şartları:

- Taramada döngü sorularının yanında sayı, atıf ve ret soruları da olsun.
- `no_repeat_ngram_size` 8–12 de denensin.
- Yargıç değişikliği `judge_sha256`'ya yansısın.
- Faz 5 ile aynı indekste ölçülsün.

Tarama verisi: `faz5b_sweep.json`, `faz5b-sweep.log`.

## Kod

- `rag.ANSWER_OPTIONS`: `model.generate(options=…)` üzerinden yalnızca cevap üretimine gider. Arama kararları ve yargıç
  bundan etkilenmez.
- `no_repeat.AnswerNoRepeatNGram`: yalnızca cevabın kendi n-gram'larını engelliyor. transformers'ın
  `no_repeat_ngram_size`'ı decoder-only modelde prompt'u da sayıyor, yani kaynaktan uzun bir ifadeyi birebir
  kopyalamayı da yasaklıyor. Birim testi: `tests/unit/test_answer_no_repeat.py`.
- Yargıç:
  - `answer_sentences` tekrar eden cümleyi tek iddia sayıyor ve atıflarını birleştiriyor (test eklendi).
  - `judge_sha256` artık `answer_sentences` ve `faithfulness` fonksiyonlarının kaynak kodunu da kapsıyor. Önceden
    yalnızca prompt'ları ve regex'i kapsıyordu; kod değişikliği hash'e yansımazdı.

## Tarama (Faz 5 indeksi, arama bir kez yapılıp önbelleğe alındı, deterministik üretim)

Sorular:

- Döngü soruları: q33, q36, q37, d2q10.
- Sayı ve atıf soruları: q01, d2q03, d2q05, q09, d3q20.
- Ret: q43.
- Ek tur: q42 ve q45. Faz 5'te bu ikisi ret cümlesine `[1]…[6]` ekledi.

| Varyant | Döngü | Sayı/atıf soruları | q42, q45 |
|---|---|---|---|
| base (ayarsız) | yok | 5/5 doğru | `[1][2][3][4][5][6]` |
| repetition_penalty 1.05 | yok | doğru | `[1]` |
| repetition_penalty 1.10 | yok | doğru | `[1]` |
| no_repeat_ngram_size 8 (HF) | yok | **bozuk**: "JTC **2**/SC42 … **2020**", "**0.7** MeV", "CODATA **1973**, 2018, 2022" | atıfsız, soruyu tekrar eden ret |
| no_repeat_ngram_size 12 (HF) | yok | **bozuk**: "SC**41**", "× **0-19** C", "theNewtonian" | `[1]…[6]` |
| cevaba özel 8 | **q36: 3.636 karakter**, 178 sn | doğru | `[1]…[6]` |
| cevaba özel 12 | q36 842 karakter (base 503) | doğru | `[1]…[6]` |

Gözlemler:

1. **Döngüler Faz 5'te kendiliğinden kayboldu.** Kısa parçalarla base'de de hiçbiri döngüye girmiyor.
2. **Kullanıcının uyarısı doğrulandı ve beklenenden ağır çıktı.** HF'nin n-gram engeli kaynaktaki sayıları ve terimleri
   kopyalamayı yasakladığı için model en yakın "izin verilen" token'a kayıyor: 2017 → 2020, 0.5 → 0.7 MeV. Bu sessiz
   bir olgu hatası, metrikte "yanlış" yerine "atıflı ve akıcı" görünür.
3. **Cevaba özel n-gram engeli** döngüyü kırmıyor, biçimini değiştiriyor: q36 aynı içeriği farklı kelimelerle 3.6 bin
   karakter boyunca tekrar etti. Cümle tekrarı sayacı bunu 0 gösteriyor.
4. **Tekrar cezası** bu 12 soruda sayıları bozmadı. Ret cümlesindeki atıfı `[1]`'e indirdi ama sıfırlamadı.

## Karar

- **Üretim: ayar eklenmedi (base).** Döngü artık oluşmuyor, eklenecek her ayar ölçülebilir bir fayda olmadan risk
  getiriyor. `ANSWER_OPTIONS = {}` kaldı; altyapı ileride kullanılabilir.
- **Yargıç: tekilleştirme tutuldu.** Faz 5 cevaplarında tekrar eden cümle olan satır yok, bu yüzden metrikler Faz 5 ile
  aynı. Tam ölçüm (~70 dk) atlandı; üretim deterministik ve değişmedi.
- **Açık sorun: ret cümlesindeki atıf (0.15).** Hiçbir üretim ayarı çözmedi. Öneri kullanıcıya sunuldu: kod tarafında
  ret algılanınca cevabı soru dilinde sabit ret cümlesine çevirmek. Bu, Faz 3c'deki "Türkçe soruya İngilizce ret"
  sınırlamasını da kapatır.
