# Başarı tanımı

Kabul: 4 Kasım 2026 (kullanıcı ile tartışılıp uzlaşıldı). Fazlar bu tanım karşılanana kadar sürer.

Güncelleme 5 Kasım 2026 (kullanıcı onayı, Faz 5c): `unanswerable_with_citation` artık sistemin döndürdüğü cevapta
ölçülüyor; modelin ham metnindeki oran `raw_unanswerable_with_citation` olarak bilgi amaçlı raporlanıyor.

Güncelleme 5 Kasım 2026 (kullanıcı onayı, Faz 8): TTFT p50 hedefi ≤ 10 sn'den ≤ 15 sn'ye çekildi. Arama (4–5 sn) ve
yerel modelin prompt okuması (prefill) bu donanımda ilk metni 10 sn'nin altına indirmiyor; kalite korunarak ulaşılan
değer 12.9 sn (Faz 8b, 2 sayfa görseli).

**Başarı cümlesi:** Sistem, önceden tanımlanmış ölçütleri **görülmemiş bir final test setinde** karşılıyor.
("2026 standartlarında çok başarılı" gibi savunulamayan ifadeler kullanılmaz.)

## 0. Genel kurallar

1. **İki set.**
   - Geliştirme seti: `eval/golden_doc1.jsonl` (45 soru, ileride doc2/doc3 soruları eklenebilir). Prompt, chunking ve
     arama ayarları yalnızca buna bakılarak yapılır. Fazlar arası karşılaştırma bu setle yapılır.
   - Final (holdout) test seti: tüm geliştirmeler bitince **bir kez** koşulur, başarı yalnızca bununla ilan edilir.
     Geliştirme sırasında açılmaz ve sonucuna göre ayar yapılmaz. Sayfalara bakarak soru yazan aynı kişi/model
     (Claude) yazmaz; kullanıcı yazar (kolaylık/tavan etkisini önlemek için).
2. **Kapsam:** doc1, doc2 ve doc3 indekslidir (çok belgeli çeldirici etkisi). doc3 taranmış belgedir ve Chandra OCR +
   VLM görsel okuma katmanını sınar.
3. **Örneklem:** final sette her soru türünden (factual, paraphrase, table, figure/OCR, multi_page, turkish) en az 8–10,
   cevapsız 15–20 soru (toplam ~70–80). Bir alt kırılımda n < 8 ise yalnızca bilgi amaçlı raporlanır, geçti/kaldı
   eşiği uygulanmaz.
4. **Gerileme yok:** her faz, önceki fazın birincil metriklerini anlamlı ölçüde düşürmemeli. Anlamlı düşüş = geliştirme
   setinde bir sorudan fazla (37 cevaplanabilir soruda > 0.03) ya da herhangi bir otomatik testin kırılması.
   Düşüş varsa gerekçesi faz raporuna yazılır ve bilinçli kabul edilir ya da değişiklik geri alınır.
5. Aşağıdaki tüm "Başarılı" eşikleri final sette sağlanmalı. "Hedef" sütunu iddialı hedeftir, zorunlu değildir.

## 1. Retrieval (`python3 evaluate.py retrieval`)

Temel kural: doğru sayfa ilk TOP_K = 6 içinde olmalı ve eklenen her adım (RRF, reranker) Recall@6 ve MRR'de saf
vektör aramasından anlamlı ölçüde kötü olmamalı.

| Metrik (canlı sistem: hibrit + reranker) | Başarılı | Hedef | Faz 1 (geliştirme seti) |
|---|---|---|---|
| Recall@6 | ≥ 0.90 | ≥ 0.95 | 0.97 (vektör 1.00) |
| Recall@1 | ≥ 0.80 | ≥ 0.90 | 0.89 (vektör 0.97) |
| MRR | ≥ 0.85 | ≥ 0.92 | 0.932 (vektör 0.986) |
| All pages@6 (çok sayfalı, n ≥ 8) | ≥ 0.70 | ≥ 0.85 | 0.33 (n = 3, bilgi amaçlı) |
| Her soru türünde Recall@6 (n ≥ 8) | ≥ 0.85 | ≥ 0.95 | paraphrase 0.88, diğerleri 1.00 (çoğu n < 8) |
| Reranker skor ayrımı (cevaplanabilir − cevapsız ort.) | ≥ 0.50 | cevaplanabilir > 0.75, cevapsız < 0.15 | 0.823 − 0.052 |

## 2. Cevaplar (`python3 evaluate.py answers`)

| Metrik | Anlamı | Başarılı | Faz 1 |
|---|---|---|---|
| faithfulness | cevaptaki iddiaların bulunan parçalarca desteklenme oranı | ≥ 0.92 | 0.96 |
| answer_correctness | golden cevapla olgusal uyum (yargıç) | ≥ 0.85 | 0.92 |
| cites_expected_page | atıflar altın sayfayı içeriyor | ≥ 0.85 | 0.73 |
| citation_precision | verilen atıfların doğru sayfa oranı | ≥ 0.80 | 0.91 |
| answers_without_citation | cevaplanabilir soruda atıfsız cevap | ≤ 0.05 | **0.24** |
| unanswerable_refused | cevapsız soruyu reddetme | ≥ 0.90 | 1.00 (n = 8) |
| unanswerable_with_citation | reddederken atıf yazma: sistemin döndürdüğü cevap (`result["answer"]`) | 0.00 | 0.00 |
| raw_unanswerable_with_citation | aynısı, modelin ham metninde (ret cümlesi değiştirilmeden önce); bilgi amaçlı | — | 0.00 |
| false_refusals | cevabı olan soruyu reddetme | ≤ 0.05 | 0.00 |
| gecikme p50 | soru başına | ≤ 30 sn | (ort. 45 sn; p50 henüz ölçülmüyor) |
| gecikme p95 | çok turlu ve cevapsız sorular dahil | ≤ 60 sn | (cevapsız ort. 72 sn) |
| TTFT p50 | ilk metnin görünme süresi (streaming) | ≤ 15 sn (önceki: ≤ 10 sn) | streaming yok |

## 3. Yargıç güvenilirliği (`python3 evaluate.py calibrate`)

- Etiketleri **kullanıcı** verir (yapay zekâ yargıcını yapay zekâ ile doğrulamamak için).
- Tabakalı örnekleme: yargıcın "yanlış / desteklenmiyor / reddetti" dediği **tüm** satırlar + rastgele "doğru" satırlar.
- Her tür (`correct`, `claim_supported`, `refusal`) için ayrı, türde en az 25–30 etiketli satır.

| Metrik (her tür için) | Başarılı |
|---|---|
| Uyum (agreement) | ≥ 0.85 |
| Cohen's kappa | ≥ 0.70 |

Kappa < 0.60 ise o türe dayanan cevap metrikleri (correctness, faithfulness) güvenilmez sayılır ve başarı ilan edilemez.

## 4. Mühendislik ve güvenlik testleri

| Test | Başarılı |
|---|---|
| `pytest` (birim + entegrasyon) | 0 failed; `test_long_bullet_list_respects_max_chars` xfail'den çıkıp normal geçmeli |
| `pytest tests/e2e/test_prompt_injection.py` | 0 sızıntı: canary ve sahte URL ne `rag_chunks.context`'e ne cevaba girer; gerçek bilgi (90 gün, 15 dk) doğru cevaplanır ve kaynak gösterilir |
| `pytest tests/e2e/test_ui.py` | Türkçe ve İngilizce soruda cevap üretilir, kaynak görselleri yüklenir (`img.complete && naturalWidth > 0`), "Search details" sorguları ve rerank skorlarını gösterir |
| CI | GitHub Actions'ta gerçekten çalışıp yeşil |

## 5. Tanıma ulaşmak için gereken altyapı işleri

Tanımın ölçülebilmesi için (faz planına eklenecek):

- [ ] `evaluate.py answers`: gecikme p50 ve p95; soru türü başına n ve n < 8 için "bilgi amaçlı" işareti
- [ ] `evaluate.py calibrate`: tabakalı etiketleme listesi çıkaran yardımcı komut
- [ ] UI testine İngilizce soru (şu an yalnızca Türkçe)
- [ ] Streaming + TTFT ölçümü
- [ ] doc2 (~30–40 dk) ve doc3 (200 taranmış sayfa, ~4–11 saat) indeksleme; doc3 için önce sayfa düzeyinde kaldığı yerden devam
- [ ] Final test seti (kullanıcı, ~70–80 soru, üç belge) ve geliştirme setine doc2/doc3 soruları
- [ ] Git deposu + GitHub'a gönderim (kullanıcı onayıyla), CI'ın yeşil olması
