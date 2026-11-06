# Faz 7 — Streaming ve TTFT ölçümü

Tarih: 5 Kasım 2026. Rapor: `reports/20261105-1344-answers*`. 6a + 6b üstüne.

## Değişiklik

- `model.generate_stream`: `TextIteratorStreamer` ve ayrı bir thread kullanıyor.
  - Okuyan taraf erken çıkarsa bir `StoppingCriteria` üretimi durduruyor.
  - Hata olursa akış kapatılıyor, böylece okuyan taraf asılı kalmıyor.
- `rag.answer_stream`: cevabı parça parça veriyor, en sonda sonuç sözlüğünü veriyor.
  - Hiçbir şey ilk cümle bitmeden gösterilmiyor (en fazla 300 karakter bekleniyor), çünkü `is_refusal` ilk cümleye
    bakıyor.
  - Ret ise yalnızca sabit cümle gösteriliyor ve üretim durduruluyor.
  - `answer()` aynı akışı sonuna kadar okuyor; tek kod yolu var.
- `app.py`: arama sırasında bekleme göstergesi, sonra `st.write_stream`.
- `evaluate.py`: `ttft_s` ölçülüyor (kullanıcının gördüğü ilk metin parçası), `p50_ttft_s` ve `p95_ttft_s` raporlanıyor.
- Yan etki: retlerde üretim durduğu için `raw_answer` modelin ilk cümlesi oluyor. `raw_unanswerable_with_citation`
  artık ilk cümledeki atıfı ölçüyor.
- Testler: akış, ret değiştirme ve üretimin durması, sonu noktasız kısa cevap. Birim + entegrasyon 79 geçti.

## Sonuç

| Metrik | 6b | 7 |
|---|---|---|
| Cevaplar | — | **82/82 birebir aynı** |
| Kalite | correct 0.99, faith 0.91, prec 0.84, cites 0.90 | aynı |
| p50 / p95 toplam | 21.6 / 56.8 sn | 19.9 / 56.1 sn (retlerde üretim erken durduğu için) |
| **TTFT p50 / p95** | — | **17.7 / 37.5 sn** (hedef ≤ 10) ❌ |

- 82 sorunun 46'sında ilk metin ancak cevap bitince görünüyor. Bunlar tek cümlelik cevaplar; tampon ilk cümlenin
  bitmesini bekliyor.
- Cevapsız sorularda TTFT medyanı 32.7 sn: ek arama turları, ardından sabit cümle.
- Modelin kendi ilk tokeni bile 12–14 sn'de geliyor (7 soruluk ölçüm):
  - arama ve prompt hazırlama 4–5 sn,
  - prefill 7–10 sn.
- Yani ≤ 10 sn hedefi tampon kaldırılsa da tutmaz; prefill'in kısalması gerekiyor.

## Karar

Streaming tutuldu: UI'da cevap daha erken görünüyor, cevaplar değişmedi.

TTFT için kullanıcıya öneri sunuldu (onay bekleniyor):

1. görsel sayısını azaltmak,
2. kısa prompt'larda sdpa (6c),
3. tamponu ilk ~60 karaktere indirmek,
4. hedefi gözden geçirmek.

## UI e2e

Streaming'li arayüzle `tests/e2e` 25/25 geçti (135 sn): Türkçe ret cümlesi, kaynaksız ret ve prompt injection testleri dahil.
