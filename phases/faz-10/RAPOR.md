# Faz 10: Türkçe sorguyu İngilizce çeviriyle de arama (final sonrası, kullanıcı onaylı)

Final holdout'tan sonra; yalnız dev setinde ölçüldü.

**Sorun:** "Kavram kayması nedir?" gibi yalnız Türkçe terimli soru İngilizce belgede ilgili parçayı bulamıyordu (rerank 0.0 → ret).

**Değişiklik (`rag.py`):** `english_query()` Türkçe sorguyu modelle İngilizceye çevirir (`TRANSLATE_PROMPT`); ilk turda iki sorgu da
aranır, havuz birleşir; `rank()` her parçaya iki sorgudan yüksek rerank skorunu verir. Çeviri arayüzde "Search details"
sorgularında görünür. 3 birim testi; birim + entegrasyon 92 geçti. Elle: "Kavram kayması nedir?" 0.0 → 0.99 ve Türkçe doğru cevap.

## Dev ölçümü (82 soru)

| | Faz 9 | Faz 10 |
|---|---|---|
| answer_correctness | 0.97 | **0.99** (yalnız q24 yanlış; d2q12 düzeldi) |
| Türkçe: doğru / altın sayfa atfı / altın sayfa getirildi | 11 / 11 / 11 (12) | **12 / 12 / 12** |
| faithfulness (yargıç) | 0.92 | 0.92 |
| citation_precision / cites_expected_page | 0.86 / 0.91 | 0.88 / 0.93 |
| ret ölçütleri | 0.00 / 0.00 / 1.00 / 0.00 | aynı |
| gecikme p50 / p95 | 20.2 / 58.6 | 24.2 / **75.3** ❌ |
| TTFT p50 / p95 | 13.4 / 34.1 | **17.1** ❌ / 46.7 |

**Gecikme ayrıştırması:**
- İngilizce 67 soru: cevaplar 82'nin 67'sinde Faz 9 ile **birebir aynı** (kod yolu değişmedi), yine de medyan 19.3 → 22.2 sn,
  d2q09 aynı 93 karakterlik cevapta +47 sn. Bu artış ölçüm ortamından (bellek baskısı/MPS), koddan değil.
- Türkçe 15 soru: TTFT medyanı 14.2 → 23.3 sn (gerçek). Profil (5 soru): çeviri 0.6–1.3 sn, her `retrieve` (40 aday rerank)
  2–3.5 sn; `agentic_search` 7–11 sn (önceden ~4–5).
- **Öneri (kullanıcı onayı bekliyor):** iki sorgunun adaylarını birleştirip tek seferde, yalnız İngilizce çeviriye göre
  rerank etmek (iki ayrı 40'lık rerank + çift skor yerine). Beklenen ek maliyet ~1–2 sn. Ardından dev ölçümü tekrar.

## Karar (kullanıcı, 6 Kasım 2026)

Kod **Faz 9'a döndürüldü** (çeviri kaldırıldı; cevap dili düzeltmesi kaldı). Faz 10 kodu `phases/faz-10/rag_faz10.py` olarak saklandı. Birim + entegrasyon 89 geçti; `prompt_sha256` 2856d18117b9 = Faz 9 raporu.
