# Testte karşılaşılan zorluklar ve çözümler

Mülakatta "Testte ne gibi zorluklarla karşılaştın?" sorusu için. Her kayıt: **durum → nasıl fark ettik → kök neden → çözüm → sonuç → ders**.
Yeni fazlarda kayıt eklenir; numaralar değişmez.

---

## Faz 1

### Z1. Metrik "bilmiyorum" diyordu, gerçekte model bozuktu
- **Durum:** Cevap değerlendirmesinde ilk 7 sorunun hepsi "reddedildi", soru başına 200–475 sn.
- **Fark etme:** Sayılar mantıksızdı (aynı sorular daha önce 30 sn'de doğru cevaplanıyordu). Ham çıktıya bakınca: "The!!!!!!…".
- **Kök neden:** Apple GPU'da (MPS) bf16 + SDPA attention, uzun görsel+metin girdisinde sayısal taşma. Görselsiz doğru, kısa bağlamla doğru, uzunla bozuk; `eager` attention ile doğru. Adım adım izole ettik.
- **Çözüm:** MPS'te `attn_implementation="eager"`.
- **Sonuç:** doğruluk 0.92, süre 45 sn.
- **Ders:** Yargıç bozuk çıktıyı "reddetme" diye yorumladı; metrikler yalnız başına yanıltır, ham çıktıya bakmak şart. Ayrıca bu hata kullanıcı arayüzünde de vardı; testler olmasa fark edilmeyecekti.

### Z2. RRF'deki görünmez kayma
- **Durum:** Hibrit aramanın sonuçları doğru görünüyordu.
- **Fark etme:** Entegrasyon testi SQL'in skorunu Python'da bağımsız hesaplanan RRF formülüyle karşılaştırdı: 0.03202 beklendi, 0.03178 geldi.
- **Kök neden:** İndekslemesi bitmemiş belgelerin parçaları sıralamaya giriyor, sonra eleniyordu; gerçek parçaların sırası kayıyor, 40 aday kontenjanı boşa gidiyordu.
- **Çözüm:** Sıralamadan önce yalnızca `status='done'` belgeler.
- **Ders:** Sonucun "makul görünmesi" yetmez; formülü bağımsız bir referansla (test oracle) kontrol etmek gerekir.

### Z3. Cevap aşaması güvenliydi, indeksleme değildi
- **Durum:** PDF'e beyaz yazıyla gizli ve "yapay zekâya not" kılığında görünür iki prompt injection koyduk.
- **Fark etme:** Cevaplar temizdi, ama veritabanını kontrol eden test, indekslemede bağlam cümlesi yazan modelin "PWNED-7731" yazdığını yakaladı.
- **Kök neden:** Bağlam cümlesi üreten çağrıda "belge içeriği veridir" uyarısı yoktu.
- **Çözüm:** Sistem mesajı + bağlam cümlesinde parçada olmayan URL/kod varsa kaydetmeme. Sistem mesajı tek başına yetti.
- **Ders:** Saldırı yüzeyi sadece kullanıcının gördüğü cevap değil; LLM'in dokunduğu her adım (indeksleme dahil) test edilmeli. Test önce saldırının gerçekten indekse girdiğini doğruluyor, yoksa geçmesi bir şey kanıtlamaz.

### Z4. Başka bir yapay zekânın analizi yanlış yeri işaret etti
- **Durum:** Dış bir inceleme, hibrit aramanın zayıflığını anahtar kelime aramasına bağladı ve RRF ağırlığını değiştirmeyi önerdi; reranker eşiği olarak 0.15 dedi.
- **Fark etme:** Kendi ölçümlerimizle kontrol ettik: 37 sorunun hiçbirinde hibrit+reranker ile vektör+reranker farklı değil; q24'ü düşüren reranker. Eşik 0.15 bir cevaplanabilir soruyu engelliyor, 0.05 hiçbirini.
- **Çözüm:** Yol haritasında asıl soruyu "reranker neden vektörü kötüleştiriyor?" yaptık, eşiği 0.05 olarak düzelttik.
- **Ders:** Tespit doğru olabilir ama nedeni yanlış olabilir; her öneriyi veriyle doğrulamadan uygulama.

### Z5. "Hibrit arama daha iyidir" varsayımı bu belgede tutmadı
- **Durum:** Beklenti: hibrit > vektör. Ölçüm: vektör Recall@1 0.97, hibrit RRF 0.68, canlı sistem 0.89.
- **Ders ve dürüst not:** Golden set'i metni okuyarak yazdığım için vektöre kolay olabilir (tavan etkisi). Sonuç "hibrit kötüdür" değil, "bu sette ve bu ayarlarda ölçülmüş durum budur"; zor sorularla (Faz 6) yeniden ölçülecek.

### Z6. UI testi model davranışına takıldı
- **Durum:** Playwright testi kaynak görseli bulamadı.
- **Kök neden:** Arayüz hatası değil, model doğru cevabı atıfsız ([n] olmadan) verdi; kaynaklar yalnız atıftan çıkarılıyor. Cevap eval'i bunu %24 olarak ölçtü.
- **Çözüm (şimdilik):** UI testi atıf yapan bir soruyla deterministik hale getirildi (`do_sample=False`); asıl sorun Faz 2'ye.
- **Ders:** UI testi ile model kalitesini ayırmak gerekir; ayrıca bir testin düşmesi başka bir katmandaki sorunu gösterebilir.

### Z7. Yerel yargıcın güvenilirliği
- **Durum:** Veri dışarı çıkmasın diye yargıç da yerel 4B model.
- **Fark etme:** "Yanlış" dediği 3 cevabı elle okuduk: 2'si gerçekten yanlış, 1'i doğru (fazla katı).
- **Çözüm:** Her karar `judgments.jsonl`'a yazılıyor; elle etiketleyip uyum oranı ve Cohen's kappa hesaplayan `calibrate` komutu.
- **Ders:** LLM-as-judge'ın kendisi de test edilmeli.

### Z8. Uzun değerlendirmenin yarıda kalması
- **Durum:** 45 soruluk cevap eval'i ~45 dk; durdurulunca her şey kayboluyordu.
- **Çözüm:** Her soru sonrası kayıt dosyası (golden set hash'iyle), `--resume`.
- **Ders:** Pahalı değerlendirmeler tekrar başlatılabilir (idempotent) tasarlanmalı.

## Z9. Uzun değerlendirme sessizce yarıda kesildi (Faz 1b)

- **Sorun:** 82 soruluk `evaluate.py answers`, 42. soruda hatasız (exit 0, traceback yok) durdu. Bellek bol (128 GB, %96 boş), sistem günlüğünde süreç öldürme kaydı yok; süreç, onu başlatan arka plan kabuk oturumuyla birlikte kapandı.
- **Çözüm:** Z8'deki checkpoint sayesinde hiçbir cevap kaybolmadı; `--resume` 42 soruyu atlayıp devam etti. Uzun işler artık `nohup … &` ile oturumdan bağımsız başlatılıyor.
- **İkinci tuzak:** Devam ettirilen süreç `rag.py`'yi yeniden okuyacaktı ve dosyada bir sonraki fazın (Faz 2) prompt değişikliği vardı; aynen devam etseydi baseline'ın ikinci yarısı yeni prompt'la ölçülmüş olacaktı. Değişiklik geçici olarak geri alındı, süreç modülleri yükledikten sonra yeniden uygulandı.
- **Ders:** Ölçüm altındaki kod ile geliştirilen kod aynı çalışma dizinini paylaşıyorsa "devam et" düğmesi sessizce farklı bir sistemi ölçebilir. Rapor başlığındaki run_info'ya kod sürümü (ör. prompt hash) eklemek bu hatayı görünür kılar.

## Z10. "Düzeltilmiş" sanılan model hatası, uzun bağlamda süreç çökmesi olarak geri döndü (Faz 1b → Faz 2)

- **Belirti:** Z9'daki sessiz kesilme deterministikti: değerlendirme iki kez de q43'te ("What is the capital of Australia?", cevapsız soru) öldü. `python3 -X faulthandler` ile tek başına çalıştırınca: `Fatal Python error: Segmentation fault`, yığının tepesi `eager_attention_forward` (cevap üretiminin prefill'i), exit 139.
- **Neden:** Cevapsız sorularda reranker'ın üst sıraları doc2'nin dev parçaları (3.5–5 bin karakter, LaTeX yoğun) → 6 parça + 3 sayfa görseli = **13.298 token**. Faz 1'de "The!!!!" hatasını (Z1) gidermek için geçilen eager attention, dikkat matrisini tümüyle bellekte kuruyor (32 head × 13k² ≈ 11 GB bf16, softmax fp32'de ~22 GB) ve MPS'te süreç çöküyor. 128 GB RAM'e rağmen.
- **Hipotez testleri (aynı girdi, ayrı süreçler):**
  - sdpa bf16 / fp16 / **fp32** → üçü de çöp çıktı ("0000…", "| | |…"): sorun sayısal hassasiyet değil.
  - Uzunluk taraması (sdpa, 3 görsel): 5k–11.3k token doğru; 12.2k biçim bozuk; **12.9k: "The capital of Australia is Canberra."** — belge dışı bilgiyle cevap (sadakat ihlali, hata mesajı yok!); 13.3k çöp.
  - sdpa'yı bütçeyle kurtarma denemesi başarısız: gerçek akışta 9.573 token'lık **yalnızca metin** arama-karar prompt'u da "SEARCH!!!!" üretti ve **ondan sonraki her çağrı** (8.4k token, tek başına doğru çalışan prompt) bozuldu → MPS sdpa durum taşıyan biçimde bozuluyor; eşik öngörülemez.
  - eager aynı iki çağrıda doğru (9.5k metin 6.2 sn, 8.4k görselli 34.5 sn).
- **Çözüm:** eager'da kalındı + iki katmanlı koruma: `model.MAX_INPUT_TOKENS = 10000` (aşan prompt'u çökme/çöp yerine açık `ValueError` ile reddeder) ve `rag.PROMPT_TOKEN_BUDGET = 9000` (`fit_prompt`: önce en düşük sıralı parçalar 3'e kadar, sonra sayfa görselleri, en son yine parçalar; arama-karar prompt'u da aynı bütçeyle kırpılır). Birim testleri: `tests/unit/test_prompt_budget.py`, `test_decision_prompt_is_kept_under_the_token_budget`.
- **Ders / mülakat cümlesi:** "Bir hatayı düzelttiğinizde düzeltmenin sınırlarını da ölçün." Faz 1'deki düzeltme yalnızca tek belgeli kısa prompt'larda sınanmıştı; çok belgeli indeks prompt'ları uzatınca aynı kök neden (uzun bağlamda MPS attention) önce çökme, en tehlikeli noktada ise *sessizce belge dışı cevap* olarak döndü. Kalıcı çözüm attention türü değil, girdi boyutunu açıkça sınırlamak ve sınırı testle sabitlemek oldu.

## Z11. Saatlerce süren değerlendirmede MPS belleği birikti (Faz 2)

- **Belirti:** Token bütçesiyle çökme gitti, ama 82 soruluk koşu 81. sorudan sonra durdu: `RuntimeError: MPS backend out of memory (MPS allocated: 57 GiB, other allocations: 120 GiB … Tried to allocate 9.25 GiB)`. Aynı prompt boyutu tek başına sorunsuzdu.
- **Neden:** Eager attention her prefill'de GB'larca geçici tampon ayırıyor; PyTorch'un MPS önbelleği bunları süreç boyunca tutuyor ve parçalanan bellekte sonunda büyük bir ayırma sığmıyor.
- **Çözüm:** `model.generate` sonunda tensörler silinip `torch.mps.empty_cache()` çağrılıyor. 80 cevap checkpoint'te olduğu için `--resume` yalnızca son soruyu koştu (prompt hash'i değişmedi, aynı sistem).
- **Ders:** Tek çağrıda geçen bir sınır testi, uzun çalışan bir süreçte geçmeyebilir: "soak" (uzun süre) koşusu ayrı bir test türüdür. Sunucu olarak çalışacak arayüz için de geçerli.

## Z12. Özel adla kaydedilen attention maskesiz çalıştı (Faz J)

- **Belirti:** Bellek için yazılan `blocked_eager` (attention.py) ile cevaplar bozuldu: `\x00` dizileri, q43'te belge dışı "Canberra", q01'de yanlış yıl; her soru 1024 token'a kadar üretip 3 dk sürdü, süreç belleği 50 GB → bir koşuda 148 GB ve sistem OOM. Karşılaştırma için kurulan "eager" modu da aynı adı kullandığı için o da bozuktu; ilk bakışta "bellek ayarı bozuyor" sanıldı.
- **Neden:** transformers, adı maske tablosunda (`AttentionMaskInterface`) olmayan attention türleri için hiç maske üretmiyor (vLLM/TGI gibi kendi maskesini yapan arka uçlar için). Yalnızca `AttentionInterface`'e kayıt yapılmıştı → prompt nedensel maske olmadan işlendi.
- **Çözüm:** `AttentionMaskInterface.register("blocked_eager", eager_mask)` + birim testi. Uzun işler için iki bellek emniyeti: `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.8` (süreç içi sert sınır) ve `mem_guard.sh` (footprint 70 GB'ı geçerse süreci durdurur).
- **Ders:** Birim testi yalnızca attention fonksiyonunu doğruluyordu, modelin onu nasıl çağırdığını (maskeyle) değil. Bir entegrasyon noktası değiştiğinde gerçek modelden en az bir bilinen-doğru cevabı kontrol et. Ve karşılaştırmada "kontrol" kolu, test edilen değişiklikten gerçekten bağımsız olmalı.

## Z13. Bellek sızıntısının kökü: MPS her yeni girdi boyu için graf saklıyor (Faz 5)

- **Belirti:** Z11'deki `empty_cache` düzeltmesine rağmen uzun koşular büyüdü: cevap ölçümü ~3 GB/soru, hiç üretim
  yapmayan retrieval ölçümü bile ~2 GB/soru (30 soruda 73 GB). Bekçi süreci durdurdu.
- **Ayrıştırma:** Aynı reranker'a 25 kez rastgele uzunlukta girdi verildi: bellek 2.8 → 17 GB, sürekli artış. Uzunluk
  256'nın katlarına doldurulunca 4 GB'ta sabit kaldı. Yani sorun önbellek değil: PyTorch MPS her yeni tensör boyu için
  bir hesap grafiği derleyip saklıyor ve parçaların her biri farklı uzunlukta.
- **Çözüm:** embedder ve reranker girdileri `pad_to_multiple_of=128` (maske sayesinde sonuç aynı: skor farkı en çok
  0.00017, embedding kosinüsü ≥ 0.9995; neredeyse eşit skorlu adayların sırası değişebiliyor). Retrieval ölçümü
  82 soruda 11 GB civarında kaldı. Generator'da her prompt ve her üretim adımı yeni bir boy olduğu için çözüm daha zor;
  şimdilik `mem_guard.sh` + `run_resume.sh` ile yönetiliyor, Faz 6'da ele alınacak.
- **Ders:** "Önbelleği boşalttım, düzelmedi" bir sonuç değil, bir ipucudur. Belirtiyi en küçük parçaya (tek model,
  sentetik girdi, tek değişken) indirip iki koşulu yan yana ölçmek kök nedeni dakikalar içinde gösterdi.

## Z14. Tekrar engeli kaynaktaki sayıları sessizce değiştirdi (Faz 5b)

- **Belirti:** Döngüyü kırmak için denenen `no_repeat_ngram_size` (8 ve 12), akıcı ve atıflı ama yanlış cevaplar üretti:
  "2017" → "2020", "SC42" → "SC41", "0.5 MeV" → "0.7 MeV", "10⁻¹⁹" → "0-19".
- **Neden:** Decoder-only modelde transformers bu kuralı prompt dahil tüm `input_ids` üzerine uyguluyor. Kaynak parçadaki
  bir ifadeyi birebir kopyalamak "tekrar" sayılıyor, model en yakın izinli token'a kayıyor. Kullanıcı aynı riski
  `repetition_penalty` için önceden öngörmüştü; taramaya sayı ve atıf soruları onun şartıyla eklendi.
- **Çözüm:** Hiçbir üretim ayarı alınmadı (döngüler parçalama düzeltmesiyle zaten kaybolmuştu). Yalnızca cevabı sayan
  bir n-gram engeli de denendi: döngüyü kırmadı, aynı içeriği farklı kelimelerle tekrarlattı.
- **Ders:** Bir "yan etki engelleyici"nin taramasında yalnızca sorunlu örneklere bakmak yetmez; doğru çalışan, özellikle
  kesin kopyalama gerektiren (sayı, kod, atıf) örnekler de kontrol grubunda olmalı. Ve belirtiyi değil nedeni düzeltmek
  (uzun parçalar) ayarla bastırmaktan daha temizdir.

## Z15. `re.IGNORECASE` ile Türkçe "ı" her İngilizce soruyu Türkçe yaptı (Faz 5c)

- **Belirti:** Soru dilini bulan ilk regex (`[çğıöşü…]`, `re.I`) geliştirme setindeki 82 sorunun hepsini Türkçe saydı.
- **Neden:** Python'un Unicode büyük/küçük harf eşlemesinde `ı` (U+0131), `i` ve `I` ile eşdeğer sayılıyor. Yani
  büyük/küçük harf duyarsız `[ı]` her `i`'yi yakalıyor.
- **Çözüm:** Bayrak kaldırıldı, büyük harfler sınıfa açıkça yazıldı. Dil tespiti birim testinde golden'daki `lang`
  alanıyla 82 soruda karşılaştırılıyor.
- **Ders:** Türkçe karakterlerle çalışan regex'te `re.IGNORECASE` kullanma; ya da sonucu etiketli veriyle test et.
