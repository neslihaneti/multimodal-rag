# Faz 5c — Sabit ret cümlesi (soru dilinde, atıfsız)

Tarih: 5 Kasım 2026. Kullanıcı onayı: öneri ve başarı tanımı güncellemesi birlikte.

## Sorun

- Faz 5'te q42 ve q45 ret cümlesine `[1]…[6]` ekledi (`unanswerable_with_citation` 0.15).
- Faz 5b'deki hiçbir üretim ayarı bunu sıfırlamadı.
- Faz 3c'den beri açık bir sınırlama daha var: Türkçe soruya İngilizce ret veriliyor (q44, q45, d3u03).

## Değişiklik (`rag.py`)

- `is_refusal(text)`: ret ifadesi (`NOT_FOUND`) cevabın **ilk cümlesinde** geçiyorsa ret sayılıyor.
  - Ret ifadesi kısmi bir cevabın arkasından geliyorsa ("X 5'tir [1]. Y belirtilmemiş.") metin değişmiyor.
  - Böylece doğru kısmi cevap silinmiyor.
- Ret algılanınca `answer` soru dilindeki sabit cümle oluyor:
  - Türkçe: "Belgelerde bu konuda bilgi yok."
  - İngilizce: "The documents do not contain information about this."
- Modelin metni `raw_answer` alanında saklanıyor.
- `question_language`: Türkçe harf veya Türkçe soru/bağlaç kelimesi varsa `tr`.
  - `re.IGNORECASE` kullanılmıyor, çünkü Python'da bu bayrakla `ı` hem `i`'yi hem `I`'yı eşliyor ve her İngilizce soru
    Türkçe görünüyordu.
- `NOT_FOUND` kalıbına "bulunmuyor" ve "yer almıyor" eklendi.

## Ölçüm ve rapor (`evaluate.py`)

- `unanswerable_with_citation` artık sistemin döndürdüğü cevapta ölçülüyor (BASARI_TANIMI.md güncellendi).
- Modelin ham metnindeki oran `raw_unanswerable_with_citation` satırında bilgi amaçlı raporlanıyor.
- Her satıra `raw_answer` ve `raw_cited` eklendi.
- `prompt_sha256` ret cümlelerini, regex'leri ve `is_refusal` kodunu da kapsıyor.

## Testler

Birim testleri (`tests/unit/test_answer_citations.py`):

- İngilizce ve Türkçe ret, sabit cümleye dönüyor ve kaynak göstermiyor. Test edilen durumlar:
  - atıflı ret,
  - Türkçe soruya İngilizce ret,
  - ret + ek açıklama.
- Ret ifadesi kısmi cevaptan sonra geliyorsa metin korunuyor.
- İki sabit cümle de `NOT_FOUND` ve `is_refusal` tarafından tanınıyor.
- `question_language`, geliştirme setinin 82 sorusunun 82'sinde golden'daki `lang` alanıyla aynı.

E2E testleri (gerçek model):

- `tests/e2e/test_refusal_judge.py` — yargıcın `REFUSAL_PROMPT`'u:
  - 13 cevapsız sorunun 13'ünde sabit cümleyi ret saydı (%100).
  - İki gerçek cevabı (TR ve EN) ret saymadı.
  - Sonuç: 15/15 geçti.
- `tests/e2e/test_ui.py::test_turkish_refusal_is_in_turkish_without_sources`: UI'da Türkçe ret gösteriliyor, kaynak
  gösterilmiyor. UI testleri baseline sonrası çalıştırılacak.

## Çevrimdışı etki (Faz 5 cevapları üzerinde simülasyon)

- 13 cevapsız sorunun 13'ü sabit cümleye dönüyor; cevaplanabilir 69 sorudan hiçbiri değişmiyor.
- `unanswerable_with_citation`: 0.15 → 0.00. Ham metinde 0.15 kalıyor.
- Türkçe ret: q44, q45 ve d3u03 artık Türkçe.

Gerçek ölçüm, doc3'ün tamamı indekslendikten sonraki yeni baseline'da yapılacak.
