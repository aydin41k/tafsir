# Bedir Kitabı - Durum

Bu dosya işin hâfızasıdır. Her bölüm bittiğinde ve her geri bildirim
alındığında güncellenir. Bir çöküşten sonra iş buradan devam eder.

## Nerede duruyoruz

**v1 tamam ve donduruldu. v2 yazılıyor: söz turu.**

- `v1/` - yedi bölüm, birleştirilmiş `furkan-gunu.md` (10.844 kelime, 34,4 sayfa
  A5) ve üç betik. **Değiştirilmez.** aydin4ik'in "dont just overwrite the files"
  talimatı gereği her tur ayrı dizinde durur.
- `v2/` - üstünde çalışılan tur. Tek mevzuu vardır: dolaylı anlatımla verilen
  konuşmaları söz olarak yazmak. Bağlayıcı brief `v2/BRIEF-V2.md`dir.

Birleştirme yine yapılmayacak; onay gelene kadar `build.py` çalıştırılmaz.

## Nasıl çalışıyoruz

Bir seferde **bir bölüm**. Bölüm yazılır → aydin4ik okur → geri bildirim
buraya yazılır → sonraki bölüm o geri bildirimle yazılır. Onay gelmeden
sonraki bölüme geçilmez.

Sabit dosyalar: `00-BRIEF.md` (bütün kitap için kurallar) ve `brief-s1..s7.md`
(bölüm briefleri). Çıktı: `s1.md` … `s7.md`. Birleştirme en sonda.

**Doğrulama:** `python3 check.py s3` yahut `python3 check.py all`. Kelime sayısı,
sabit ilk/son cümle, uzun çizgi, dipnot/tablo/liste, yasak kelime, ad imlâsı ve
ﷺ sayısını yoklar. Bir bölüm bu kontrolden geçmeden teslim edilmez.

s1 ile s2 sırayla ve onaylanarak yazıldı; üslûp iki bölümde oturduğu ve her
bölümün ilk/son cümlesi briefte harfiyen sabit olduğu için s3-s7 koşut yazıldı.

## Bölümler

v1'in söz sütunu v2'nin niçin gerektiğini gösteriyor: yüz kadar konuşma fiiline
karşılık dokuz tırnaklı söz, üç bölümde ise hiç. v2'de yedisi de `check.py`den
geçti.

| # | Başlık | v1 kelime | v1 söz | v2 kelime | v2 söz |
|---|---|---|---|---|---|
| s1 | Yesrib'in Yemi | 1.338 | 3 | 1.359 | 5 |
| s2 | Üç Yüz On Üç | 1.485 | 2 | 1.549 | 5 |
| s3 | Yelyel Vadisi | 1.689 | 0 | 1.765 | 11 |
| s4 | Yağmur Gecesi | 1.507 | 0 | 1.556 | 9 |
| s5 | Boyunların Üstüne | 1.796 | 2 | 1.854 | 11 |
| s6 | Kuyu ve Esirler | 1.671 | 2 | 1.782 | 16 |
| s7 | Bedir'in Kırdığı | 1.358 | 0 | 1.358 | 0 |

Toplam 10.844 → 11.223 kelime, yani %3,5 uzama; 57 tırnaklı söz. Bantların üst
ucu v2'de %6 kadar genişletilmişti, çünkü söz olarak yazılan bir konuşma dolaylı
şeklinden bir parça uzun sürer; kimse bandın üstüne dayanmadı.

**s7 kasten hiç değiştirilmedi.** Baştan sona anlatıcının muhakemesidir: kervanın
satılması, melenin ne olduğu, otoritenin devredilemezliği, Uhud, humus, bedrî
mertebesi, kaynak tenkidi, tesadüfîlik. Bunlar konuşma değildir ve tırnağa
alınacak sözleri yoktur. Sıfır söz burada kusur değil, bölümün cinsidir.

Kaynak sözü korumadığı için **kasten dolaylı bırakılanlar**, yani bir sonraki
turda "burası niye çevrilmemiş" diye sorulacak yerler: Zafirân'da Ebû Bekir ile
Ömer'in konuşmaları (kaynak yalnız "güzel konuştu" der), Ukbe'nin buhurdan
sahnesi (s2; incelik sözün söylenmemesindedir, "İthamı buhurdan söyledi, Ukbe'nin
ağzı söylemedi" cümlesi kasten yerinde), Ebû Cehil'in saf ortasındaki kışkırtması,
Sa'd b. Muâz'ın yedek deve teklifi, Nadr b. Hâris ile Süheyl b. Amr'ın
öldürülmesi, Zeyneb'in gerdanlığı, Haysümân'ın Mekke'de ad sayması, Esved b.
Muttalib'in ağlayışı.

## aydin4ik'in geri bildirimleri (biriken - hepsi sonraki bölümlerde geçerli)

1. **s1 kabul edildi.** "good, keep going until all the chapters are done."
   Yedi bölüm tamamlanacak; kaynakça ve ekler sonra ayrı bir iş olarak yapılacak.
2. **Uzun çizgi (—) yasak.** Normal kısa çizgi ( - ) kullanılacak. Brief
   dosyalarındaki bütün uzun çizgiler bu yüzden kısaltıldı. Bkz. `00-BRIEF.md`,
   "NOKTALAMA" faslı.
3. **Ad imlâsı kitap boyunca tek şekil olacak.** Şapka ve kesme işareti dahil.
   Bağlayıcı liste ve sık kaçan yerler: `00-BRIEF.md`, "AD İMLÂSI" faslı.
4. **Kitabın adı `Furkān Günü - Bedir Savaşı` oldu.** Eski ad "Bedir Suyu"
   aydin4ik tarafından reddedildi: "bedir suyu is an ambiguous and uncool title."
   Ad, Kur'an'ın Enfâl sûresinde güne verdiği addır; alt başlık mevzuu açıkça
   söylemek için konmuştur. Değişen yerler: `s1.md` (`#` satırı), `check.py`
   (beklenen başlık), `build.py` (çıktı adı `furkan-gunu.md`). s7'de *furkān
   günü* ilk defa tanıtılıyormuş gibi durmasın diye cümle bir parça çevrildi.
5. **Şimdilik yalnız MD yazılıyor; birleştirme yok.** "we are not assembling
   anything atm, we are only writing the MD, we'll assemble when the text is
   approved." Yani `build.py` **çalıştırılmayacak**, `furkan-gunu.md`
   üretilmeyecek, dizgiye ve PDF'e hiç gidilmeyecek. İş, aydin4ik metni
   onaylayana kadar `s1.md` … `s7.md` dosyalarında kalır. Onay geldikten sonra
   sıra kaynakça ve eklere, ondan sonra birleştirmeye gelir.
6. **Her tur ayrı dizinde durur; üstüne yazılmaz.** "lets do the next version.
   by that i mean version this next pass, dont just overwrite the files." v1
   donduruldu, v2 kendi dizininde açıldı. Bundan sonraki turlar da böyle.
7. **Söz, anlatılmaz; söylenir.** "when you are quoting a story, i want you to
   quote most of them as a story, not as a narration from a third person."
   aydin4ik'in misali s2'deki Mikdâd b. Amr sözüdür: "kalktı ve ... bildirdi"
   yerine "kalktı ve dedi: ..." olacak. v2'nin bütün mevzuu budur. **Sınırı:**
   kaynak sözü korumuşsa tırnağa alınır, korumamışsa dolaylı kalır; çünkü
   00-BRIEF.md diyalog uydurmayı yasaklar ve uydurulmuş bir söz, kazanılan
   canlılıktan kat kat pahalıya gelir. Tafsilât `v2/BRIEF-V2.md`de.

## Bilinen mesele: bölümler arası tekrar

Koşut yazımın bedeli budur ve son turda tek tek yoklanacak. Şimdiye kadar
bulunanlar:

- **bedrî mertebesi** s5 ile s7'de birden anlatıldı. Brief'e göre s7'nin malıdır;
 s5'ten çıkarıldı, s7'de kaldı. ÇÖZÜLDÜ.
- **Ebû Huzeyfe'nin hısımları** s2 ile s5'te aynı kelimelerle sayıldı ("babası
 Utbe b. Rebîa, amcası Şeybe b. Rebîa ve kardeşi Velîd b. Utbe"). Adları s2
 kurar; s5 karşılığını verir, o yüzden s5'te adlar sıfata çevrildi. ÇÖZÜLDÜ.
- Yoklanmış ve temiz çıkanlar: altı zırh / sekiz kılıç (s2 kurar, s4/s5/s7 birer
 cümleyle geri çağırır), mübâreze (yalnız s4), Utbe'nin barış teşebbüsü (s5 ve
 s7'de birer cümle, ikisi de anlatmıyor, anıyor), üç yüz on üç (s5 ve s7 sayıyı
 referans olarak kullanıyor, tekrar anlatmıyor).
- Kalan prose tekrarları ikidir ve ikisi de yerindedir: `İbn İshak'ın kaydına
 göre` bir atıf formülüdür; `Nahle'de öldürülen Amr b. Hadramî` ise s5'te ilk
 müslüman ölüsünü vuran **Âmir** b. Hadramî'nin kardeşi olarak anılır. İki ad
 bir şapkayla ayrıldığı için 1.700 kelime sonra bağı açıkça kurmak okurun
 lehinedir; tekrar değildir.
- s3'te tek mesafe "bir mil" olarak geçmişti, kilometreye çevrildi. Brief'in
 ölçüsü kilometredir.

## Elle bulunan ve düzeltilen maddî hatalar (check.py bunları yakalamaz)

Bunlar kelime sayısıyla yahut desenle bulunamaz; ancak okumakla bulunur. Kayda
geçiyorum, çünkü bir sonraki turda aynı cinsten hata aranacak yer burasıdır.

- **s6 mevsimi yanlış vermişti:** "Ağustos güneşinin altında". Bedir 17 Ramazan 2
 (13 Mart 624) günüdür ve öteki altı bölümün hepsi Mart der. Marta çevrildi.
- **s6 hayatta kalan sayısını yanlış vermişti:** "iki yüz kadar hayatta kalan
 adam". Üç yüz on üç kişiden on dördü ölmüştür, yani sağ kalan üç yüz
 civarındadır. Düzeltildi ve orucun altı çizildi.
- **s6'da ileriye iki atıf vardı** ("bu kitabın başka bir yerinde durulacak",
 "başka bir bölüm konuşacaktır"). Kitapta bölüm numarası yoktur ve s7 ne
 müslüman ölülerin adlarını sayar ne humusu o vaadi karşılayacak şekilde açar;
 ikisi de kaldırıldı. **Kaide: bölümler birbirine atıf yapmaz.**

## Betiklerde bulunan ve düzeltilen bir sayım hatası

v2'nin söz sayacı ilk hâlinde `r'"[^"]*"'` deseniyle yazılmıştı ve **sayıyı iki
katına çıkarıyordu.** Tırnaklar dönüşümlüdür: bu desen kapanan bir tırnakla bir
sonraki açılan tırnağın arasındaki **anlatıyı** da söz sanıyor. `overlap.py` bu
yüzden s4 ile s6 arasında sözde bir söz tekrarı bildirdi; hâlbuki eşleşen şey iki
sözün arasındaki nesirdi. İkisi de tırnaktan bölüp tek sıradaki parçaları alacak
şekilde düzeltildi (`t.split('"')[1::2]`) ve tek kalmış tırnak yoklaması eklendi.
Ders: bir sayı bir hüküm veriyorsa, sayının kendisi de yoklanır.

## Ajan çöküşlerinden çıkan ders

Üç ajan API hatasıyla düştü: s7 bir kere (yazmaya geçeceği anda), s3 ve s6 ise
ilk tool çağrısında, yani daha hiçbir şey okumadan. En uzun iki bölümün, s3 ile
s6'nın ikisinin de düşmesi tesadüf değildir; ikisi de dört dosya okumakla
başlıyordu. Alınan tedbir, sonraki her ajan için geçerlidir:

- Ajan yalnız `00-BRIEF.md` ile kendi `brief-sN.md` dosyasını okur. Bitmiş
 bölümleri okumaz; üslûp briefte tarif edilmiştir, komşuların malı da brief
 mesajında sayılır.
- **Önce dosyayı yaz, sonra say ve düzelt.** Tek Write çağrısıyla metni diske
 indir; bir sonraki API hatası o zaman bir bölüme değil bir revizyona mâl olur.
- Ajan ölürse yeniden doğurmak yerine `SendMessage` ile devam ettirilir.

## Kararlar

- Önceki EN→TR çeviri (`badr-chapter.tr.md`) **reddedildi**. Kullanılmaz,
 okunmaz, ondan alıntı yapılmaz. Kalıpları bulaşıcıdır.
- Kitap sıfırdan Türkçe yazılır. İngilizce bir metinden çevrilmez.
- Saf anlatı: dipnot, kaynakça, sözlük, ek, tablo, liste yok.
