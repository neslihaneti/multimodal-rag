# Faz 9: cevap dili (final sonrası, kullanıcı isteği)

Final holdout'tan SONRA yapıldı; yalnızca dev setinde ölçüldü, final tekrar koşulmadı.

**Sorun:** Türkçe soruya İngilizce cevap ("Yapay zeka tabanlı sistemlerde kavram kayması (concept drift) nedir ve nasıl
test edilir?"; dev q37, final f57). Dil yalnız prompt'taki "Answer in the same language as the question" cümlesine
bırakılmıştı; parçalar, talimatlar ve sorudaki İngilizce terimler 4B modeli İngilizceye çekiyordu.

**Değişiklik (`rag.py`):**
- `answer_language()`: soruda açık dil isteği ("İngilizce cevap ver", "Türkçe olarak açıkla", "answer in Turkish",
  "in English") varsa o dil, yoksa `question_language()`. "Türkçe keyword araması" gibi konu olarak geçen dil adı istek sayılmaz.
- `without_language_request()`: istek cümlesi arama sorgusundan çıkarılır (yoksa aramayı bozuyordu).
- `ANSWER_PROMPT`: "Otherwise write the whole answer in {language}, even when the excerpts are in another language."
  Ret cümlesi prompt'ta sabit İngilizce kaldı (Türkçe ret serbest bırakılınca model "terimi bulunamadı" gibi
  `NOT_FOUND`'un tanımadığı ifadeler yazdı); kod `REFUSAL[language]` ile çevirir.
- 9 birim testi; birim + entegrasyon 89 geçti. `prompt_sha256` yeni fonksiyonları kapsıyor.

## Dev ölçümü (82 soru)

| | Faz 8b | Faz 9 |
|---|---|---|
| answer_correctness | 0.97 | 0.97 (yanlışlar aynı: q24, d2q12) |
| faithfulness (yargıç) | 0.90 | 0.92 |
| citation_precision / cites_expected_page | 0.84 / 0.90 | 0.86 / 0.91 |
| without citation / false refusals / refused / with citation | 0.00 / 0.00 / 1.00 / 0.00 | aynı |
| gecikme p50 / p95 | 17.8 / 52.4 | 20.2 / 58.6 |
| TTFT p50 / p95 | 12.9 / 36.4 | 13.4 / 34.1 |
| soru dili ≠ cevap dili | 1 (q37) | **0** |

- p95 artışı tekrar döngüsünün yer değiştirmesi: d2q10 35 → 152 sn (4.466 karakter döngü), q32 124 → 59 sn.
- Kalan bulgu: yalnız Türkçe terimli soru ("Kavram kayması nedir?") İngilizce belgede bulunamıyor (rerank 0.0)
  → Faz 10: arama öncesi İngilizce çeviri (kullanıcı onaylı).
