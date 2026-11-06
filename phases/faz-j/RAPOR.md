# Faz J — Yargıç düzeltmesi (A–D) + Faz 3c'nin tam ölçümü

Tarih: 4 Kasım 2026. Rapor: `reports/20261104-2303-answers.md` (82 soru, `prompt_sha256` 4af2b18c854a,
`judge_sha256` c2301e4f60d7).

## Değişiklikler

Kullanıcının yargıç eleştirisinden (5 madde) onaylanan A–D, E yok:

- **A.** `CLAIMS_PROMPT` kaldırıldı. Modelin iddia uydurması yerine cevap cümlelere bölünüyor (`answer_sentences`, en çok 8).
- **B.** Her cümle yalnızca **atıf yaptığı** parçalarla kontrol ediliyor (atıfsızsa tüm parçalarla). Altı parçayı birden
  vermekten kaynaklanan "ortada kaybolma" sorunu bu şekilde azalıyor.
- **C.** `SUPPORT_PROMPT`: "cümle ve bağlam farklı dillerde olabilir, anlamı karşılaştır".
- **D.** `CORRECTNESS_PROMPT`: sorunun sormadığı golden detayları eksik olabilir, ek doğru detay sorun değildir.

Aynı koşuda ölçülen diğer değişiklikler:

- Faz 3c prompt'u (sep_rule).
- Bellek için blok blok eager attention (`attention.py`, ZORLUKLAR Z12): bu koşudan önce maske kaydı eksikti ve düzeltildi.

## Sonuçlar

| Metrik | Faz 3 | Faz J | Başarılı eşiği |
|---|---|---|---|
| answer_correctness | 0.91 | **0.94** | ≥ 0.85 |
| faithfulness | 0.94 | 0.93 | ≥ 0.92 |
| cites_expected_page | 0.87 | 0.83 | ≥ 0.85 |
| citation_precision | 0.84 | 0.77 | ≥ 0.80 |
| answers_without_citation | 0.00 | 0.00 | ≤ 0.05 |
| unanswerable_refused | 1.00 | 1.00 | ≥ 0.90 |
| unanswerable_with_citation | 0.38 | **0.00** | 0.00 |
| false_refusals | 0.00 | 0.00 | ≤ 0.05 |
| p50 / p95 gecikme | 43.7 / 84.2 sn | 39.6 / 103.9 sn | ≤ 30 / ≤ 60 sn |

- **unanswerable_with_citation 0.38 → 0.00:** Faz 3c'nin hedefi tam ölçümde de tuttu. Bu metrik yargıca bağlı değil.
- **Doğruluk:** yeni yargıç aynı kalan iki cevabı (d2q08, d3q12) artık doğru sayıyor. Kullanıcı d3q12'yi eleştirisinin
  1. maddesinde "sorunun sormadığı golden detayı" örneği olarak vermişti.
  - Türkçe sorularda doğruluk 0.83'ten 0.75'e indi; tek soru (q33) etkilendi. q33'ün cevabı yeni prompt'la değişti ve
    test seviyelerini saymak yerine genel bir tanım veriyor.
- **Gecikme:** p95'teki artış **tekrar döngüsünden** geliyor (kullanıcı gözlemi, doğrulandı). En yavaş dört soruda
  (q33, q36, q37, d2q10; 175–208 sn, Faz 3'te 41–67 sn) model aynı cümleyi tekrar tekrar yazıyor: cevaplar 3–4.7 bin
  karakter, q37'de 25 cümlenin 21'i tekrar. İlk taslakta bunu bellek baskısına bağlamıştım; bu yanlıştı.
  - Yargıç tarafında `answer_sentences` tekrar eden cümleleri tekilleştirmiyor; q37'nin iddiası 6 kez sayıldı.
  - Düzeltme önerisi kullanıcıya sunuldu: üretimde tekrar cezası ya da n-gram engeli, yargıçta tekilleştirme.
  - Gecikme Faz 6'nın konusu.

## Gerileme: citation_precision 0.84 → 0.77, cites_expected_page 0.87 → 0.83

Düşüşün çoğu doc2'den geliyor: precision 0.31 → 0.14, beklenen sayfa 12 sorunun 2'sinde. Ancak inceleme gösterdi ki
**hata golden sette**. doc2'de aranan bilgilerin çoğu iki sayfada birden geçiyor ve golden yalnızca birini listeliyor.
Model öbür sayfayı gösteriyor (PDF metninden doğrulandı):

| Soru | Golden sayfa | Modelin gösterdiği | Kanıt (o sayfada) |
|---|---|---|---|
| d2q01 | 1 | 2 | "closing date of midnight, December 31, 2022" |
| d2q02 | 1 | 2 | "Committee on Data of the International Science Council … responsibility" |
| d2q04 | 45 | 44 | Tablo: "Vacuum magnetic permeability … 1.6 × 10−10" |
| d2q05 | 45 | 44 | Tablo: "elementary charge e 1.602 176 634 × 10−19 C Exact" |
| d2q06 | 52 | 5 | "133 input data and 79 adjusted constants … ν = 54" |
| d2q09 | 54 | 44 | Tablo: "Inverse fine-structure constant 137.035 999 177(21)" |
| d2q11 | 45 | 44 | Tablo: "Speed of light in vacuum c 299 792 458 m s−1 Exact" |

Bu sayfalar golden'a eklenirse cites_expected_page 0.93 (doc2 9/12), citation_precision 0.87 olur.
**Uygulanmadı:** golden'ı sonuç görüldükten sonra değiştirmek bir karar olduğu için kullanıcı onayına sunuldu.

doc1'de precision 0.96'dan 0.89'a indi. Dört soruda (q23, q24, q26, q31) model doğru sayfanın yanında ikinci bir
sayfaya da atıf yapıyor; q24'te yalnızca yanlış sayfaya atıf yapıyor. Bu, yeni prompt'un yan etkisi olabilir.

## Yargıç güvenilirliği

Eski etiketler (Faz 2 cevapları) bu koşuda kullanılamadı: cevapların neredeyse hepsi değişti ve her türde birebir aynı
kalan yalnızca bir satır var. Yeni tabakalı liste:
`reports/20261104-2303-answers-judgments-to-label.jsonl` (90 satır: claim 17+13, correct 4+26, refusal 13+17).
Kullanıcı 5 Kasım'da etiketledi. `python3 evaluate.py calibrate` sonucu (hedef: uyum ≥ 0.85, kappa ≥ 0.70):

| Tür | n | Uyum | Kappa | Faz 2 yargıcı (kappa) |
|---|---|---|---|---|
| claim_supported | 30 | 0.93 | **0.86** | 0.61 |
| correct | 30 | 0.93 | 0.76 | 0.76 |
| refusal | 30 | 1.00 | 1.00 | 1.00 |

Üç tür de eşiği geçiyor. `claim_supported` 0.61'den 0.86'ya çıktı: A–D'nin hedeflediği sorun buydu.

**Golden düzeltmesi:** kullanıcı onayladı ve 7 sorunun ikinci sayfalarını `eval/golden_dev.jsonl` ile
`eval/golden_dev_doc2.jsonl` dosyalarına kendisi ekledi (Faz 5'ten itibaren geçerli).

## Bellek (ZORLUKLAR Z11, Z12)

- Maske düzeltmesinden sonra blok blok attention tek soruda ~9 GB kullanıyor. Eski eager d2q12'de 50 GB alıyordu.
- Generate çağrıları arasında soru başına ~3 GB birikme sürüyor. Koşu `mem_guard.sh` (70 GB) + `run_resume.sh`
  (`--resume` ile yeniden başlatma) ile tamamlandı; süreç iki kez yeniden başladı. Üretim deterministik olduğu için
  sonuçlar etkilenmiyor.
- Birikmenin kökü açık iş: arayüz sunucusu uzun süre çalışacağı için Faz 6'da incelenecek.
