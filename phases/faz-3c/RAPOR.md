# Faz 3c — Reddetme cümlesi: prompt varyant taraması

Tarih: 4 Kasım 2026. Faz 3b'nin prompt değişikliği tam ölçümde (82 soru, ~80 dk) etkisiz çıktı. Bu fazda tam ölçüm yerine
hızlı bir tarama yapıldı: 13 cevapsız soru ve atıfın korunduğunu görmek için 6–11 cevaplı soru. Her soru için arama bir
kez yapılıp önbelleğe alındı (`scratchpad/refusal_sweep.py`), varyantlar yalnızca cevap üretimini tekrarladı. Üretim
deterministik (`do_sample=False`). Loglar: `faz-3c-sweep*.log`.

## Taramanın güvenilirliği

Faz 3 prompt'u taramada, tam ölçümdeki aynı 5 cevapsız soruda (q45, d2u01, d3u01, d3u02, d3u03) atıf yazdı. Yani hızlı
tarama tam ölçümün sonucunu birebir tekrarlıyor.

## Varyantlar ("If the documents do not contain the answer …" cümlesinin yerine)

| Varyant | Metin | Reddederken atıf (13) | Türkçe soruya Türkçe ret (q44, q45, d3u03) | Cevaplı sorularda atıf |
|---|---|---|---|---|
| faz3 | "… reply with one sentence saying so and do not use any square brackets." | 5 | 1/3 | korundu |
| example | + `for example: "The documents do not contain information about this."` | 2 | 1/3 | korundu |
| **sep_rule** | "… the rule about citations does not apply: reply only with "The documents do not contain information about this." in the language of the question, with no excerpt numbers." | **0** | 0/3 | korundu (6/6) |
| sep_rule_tr | "… reply only with one sentence in the language of the question … such as "…" or "Belgelerde bu konuda bilgi yok."" | 2 | 2/3 | korundu (11/11) |
| fixed2 | İki sabit cümle: İngilizce, Türkçe soru için "Belgelerde bu konuda bilgi yok." | 1 | 2/3 | korundu (11/11) |

Gözlem: 4B model, verilen **sabit bir cümleyi** kopyalarken atıfı bırakıyor. "Şöyle bir cümle yaz" denince serbest
cümle kuruyor ve "her cümleyi atıfla bitir" kuralı geri geliyor. Bir sabit cümle ile dil talimatı aynı anda verildiğinde
de sabit cümle dil talimatını eziyor.

## Karar

**sep_rule** seçildi ve `rag.ANSWER_PROMPT`'a alındı. Başarı tanımındaki hedef (`unanswerable_with_citation` 0.00)
yalnızca bunda tutuyor. Reddetme regex'i (`NOT_FOUND`) bu cümleyi tanıyor (doğrulandı).

**Bilinen sınırlama:** Türkçe sorulan cevapsız sorular İngilizce reddediliyor (Faz 3 prompt'unda da 3 sorunun 2'si İngilizce
reddediliyordu; sorun yeni değil, 1/3 → 0/3) ("The documents do not contain information
about this."). Cevaplı Türkçe sorular Türkçe cevaplanmaya devam ediyor. Başarı tanımında dil için bir metrik yok; ileride
kod tarafında çözülebilir (ör. reddetme algılanınca soru diline göre sabit metin).

Tam ölçüm Faz J ile birlikte yapıldı (yeni yargıç). Bu yüzden Faz 3c'nin tam metrikleri Faz J raporunda.
