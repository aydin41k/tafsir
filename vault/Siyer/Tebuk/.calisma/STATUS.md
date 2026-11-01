# Tebük Kitabı - Durum

Bu dosya işin hâfızasıdır. Her bölüm bittiğinde ve her geri bildirim
alındığında güncellenir. Bir çöküşten sonra iş buradan devam eder.

## Nerede duruyoruz

**Briefler onaylandı ("agree with the brief"). s1 yazıldı (`v1/s1.md`, 1.301
kelime, check.py GEÇTİ) ve aydin4ik'in okumasını bekliyor. Onay gelmeden s2'ye
geçilmez.**

s1'in bandı 1.500-1.800'den 1.250-1.550'ye indirildi: yoklanmış malzeme bu
kadarını taşıyor ve doldurmak yasak. İlk taslakta brief dışı yedi olgu
(Kâbe'nin putları, Hevâzin, Mu'te'nin üç komutan tayini, Ca'fer'in yetimleri,
peşin ödenmiş Rûm askeri, Bedir'de nöbetle binilen develer, Tebük yolunun
kuyusuz günleri) yazılıp çıkarıldı. Ders: brief dışı olgu en çok bağlam
cümlelerinde, "herkesin bildiği" şeylerde kaçıyor.

- `00-BRIEF.md` - bütün kitabın kuralları. Bedir kitabının (`../book/tr-book/`)
  bütün kuralları ve üç turun dersleri baştan içinde.
- `brief-s1.md` … `brief-s10.md` - bölüm briefleri, sabit ilk/son cümleleriyle.
- `v1/` - ilk turun dizini. `check.py`, `overlap.py`, `build.py` hazır;
  `check.py`'nin SPEC'i sabit cümleleri brieflerden almıştır. **Briefte bir
  sabit cümle değişirse `v1/check.py` de elle değişir.**

## aydin4ik'in tarifi (2026-10-30)

"let's write another book like the Bedir book. This will be a Tebuk book. same
scope, same instructions, same style, covering the background, the timeline,
events, narrations etc. Dialogues in the same manner as the Bedir book."

Sorulara cevapları:

1. **Ana fikir:** "two stories told in parallel (and i want your Dostoevsky
   skills in full effect here): the historical timeline + Ka'b b Malik's
   story. in the grand scheme of things we should reflect how big of a test
   this was, who failed and why (there were multiple big names), and what
   happened after."
2. **Tevbe:** bölümlere örülür + kapanış bölümü (Bedir'in Enfâl bölümü gibi).
3. **Uzunluk:** "as long as it needs to be." Plan 10 bölüm, 17-18 bin kelime.
4. **Çalışma düzeni:** Bedir gibi. Briefler önce onaya; sonra s1 ve s2 sırayla
   ve onayla; üslûp oturunca kalanlar koşut.

## Yorum kararı: "Dostoyevski" ile "diyalog uydurma yasağı"

İkisi çatışabilirdi. Karar: Ka'b'ın hadisi birinci şahıstır ve iç sesini
kendisi anlatır; o iç ses cömertçe, uzun tırnakla kullanılır. Başka hiç
kimsenin içi uydurulmaz. Dostoyevski etkisi zaman genişlemesi, tezat, küçük
fiziksel ayrıntı, sükût ve vaazsızlıkla kurulur. Tafsilât `00-BRIEF.md`,
"ANLATI TEKNİĞİ". aydin4ik bunu onaylamadı henüz; briefle birlikte görecek.

## Doğrulama turu (2026-10-30)

aydin4ik: "check all the facts with the source texts, all references should
be 100% solid. also we should close the story with the surah reference about
tawbah, how they could repent and be forgiven etc with the divine mercy."

Dört yoklama ajanı brieflerdeki her olguyu birinci el metinlere (Arapça esas)
karşı yokladı; dökümler `research/fact-*.md`. Toplam ~190 madde doğrulandı,
~50 düzeltme brieflere işlendi. Beşinci bir ajan düzeltilmiş briefleri yeniden yokladı
(`research/fact-audit.md`): 289 madde, 23 ibare kusuru (çoğu sabit cümlelerde
kaynaktan bir parça fazla söyleyen kelime); hepsi işlendi, `v1/check.py`
yeniden üretildi. Açık kalan yalnız ikincil kaynağa dayananlar: yol mesafeleri
(DİA), hicrî-mîlâdî hesap aralıkları.

En ağır düzeltmeler (bir sonraki turda aynı cinsten hata burada aranır):
- Ka'b "tevbemin tamamı" demez, "tevbemdendir" der (*min tevbetî*).
- Yüz on sekizdeki *hullifû* "geride kalan" değildir; Ka'b'ın kendi
  açıklamasıyla **işi ertelenen**. *Muhallefûn* seksen küsur özürcü içindir.
- "Yarın" Ka'b'ın kelimesi değildir; onun sözü "gücüm yeter"dir.
- Mürâre ile Hilâl'in bedrîliği Ka'b'ın sözü olarak verilir (İbn Kayyim: Zührî'nin
  vehmi).
- Hicr'de ordu su çekmiş ve hamur yoğurmuştu; "hiç içmedi" yanlıştı.
- Rüzgâr gecesinin sahih şekli Tebük'tedir, bir adam, kimse ölmez.
- Alaycılar gidiş yolundadır (s6'dan s4'e taşındı).
- Ömer/Ebû Bekir bağışı ile Ebû Akîl hadisleri Tebük'ü anmaz; Ebû Akîl s10'a
  taşındı, Ömer/Ebû Bekir Vâkıdî'ye atfen kaldı.
- Akabe gecesi İbn Hişâm'da yoktur; Müslim yalnız sayıyı verir; sahne Ahmed'den.
- Rûm haberi yalnız Vâkıdî'de Nebatîlerle; Vâkıdî kendisi haberin asılsız
  olduğunu söyler (s9'da bir kere).
- Dırâr âyetlerinin Zû Evân'da indiği söylenmez; orada yalnız haber ulaştı.
- 9:67 "Allah'ı unuttular", "kendilerini" değil; 9:50 "sana", tekil.
- Fâdıha sözünü tek bir adam, Saîd b. Cübeyr sordu; "asıl adı" denmez.

Kapanış değişti: s10'un adı **Fâdıha ve Tevbe**, iki yarısı teşhir ve rahmet;
kitabın son cümlesi yüz on sekizinci âyetin sırasıdır (önce Allah döndü).
Yüz on yedi-yüz on dokuzun mânâsı s8'den s10'a taşındı; *sâatü'l-usre* ile
kitabın adı arasındaki bağ da s10'da kurulur. Sabit cümleleri değişen
bölümler: s1 (ilk), s2 (ilk), s3 (ilk), s4 (ilk), s5 (ilk), s8 (son), s9
(son), s10 (ilk ve son). `v1/check.py` yeniden üretildi.

## Açık sorular (aydin4ik'e)

- **Benî Seleme / Benî Selime:** Arapça ve DİA *Selime*; kitap şimdilik
  *Seleme*.

- Kitabın adı: çalışma adı **Darlık Saati - Tebük Seferi** (Tevbe 117,
  *sâatü'l-usre*).
- Bölüm planı ve sabit cümleler.

## Kararlar

- Kitap sıfırdan Türkçe yazılır; hiçbir EN→TR metin okunmaz.
- Saf anlatı: dipnot, kaynakça, sözlük, ek, tablo, liste yok.
- Her tur ayrı dizinde (`v1/`, `v2/`…); üstüne yazılmaz.
- Onay gelene kadar `build.py` çalıştırılmaz.

## aydin4ik'in geri bildirimleri (biriken - hepsi sonraki bölümlerde geçerli)

1. **s1 beğenildi ("nice"), sıra değişti:** "flip the ka'b and medine parts -
   start with the medine and the general description part, then give the Ka'b
   perspective and then say Bu kitap bundan sonra iki yolu birlikte yürüyecek."
   s1 böyle yeniden dizildi; sabit ilk cümle artık `Sekizinci yılın sonunda
   Arabistan'ın hâli birkaç ay içinde değişmişti.`, sabit son cümle `Ordunun
   yolunu kaynaklar anlatır; öteki yolu ise Ka'b'dan başka anlatan yoktur.`
   Önceki dizilişi `v1/.s1-before-flip.md`. Ders: önce dünya, sonra adam.
2. **Ka'b birinci şahıs anlatıcıdır, yorumsuz:** "let's leave ka'b's narration
   without extra comments on it, unless something is mentioned that needs
   explanation or extra description. he should sound like a first person
   narrator alongside a third person narration of the broader story."
   `00-BRIEF.md`, ANLATI TEKNİĞİ faslına bağlayıcı olarak yazıldı. s2 böyle
   yazıldı. Aynı usul başka birinci şahıs râvilere de uygulandı: Ömer'in
   bağış sahnesi (Tirmizî) tek bir birinci şahıs söz olarak verildi.

## Bantlar indirildi (s2'den sonra)

s1 1.307, s2 1.192 kelimede bütün yoklanmış malzemeyi kullanmış olarak
bitti. Briefteki bantlar tahmindi ve yüzde yirmi beş kadar yüksekti. Bütün
bantlar indirildi; kitap 13.000 kelime kadar olacak. Doldurmak yasak.
s2'de uzunluğu meşru olarak artıran tek şey âyetlerin Diyanet mealiyle
(acikkuran.com'dan indirildi) daha tam verilmesi oldu; seksen birinci âyet
*muhallefûn* terimini getirdi.

## aydin4ik'in geri bildirimleri (devam)

3. **Büyük sahâbe ve Ehl-i beyt çıplak adla yazılmaz:** "when we are talking
   about the big sahaba, we dont write their names like this in turkish. we
   either say Omer ibn Hattab, or say Hz.Omer. this is for the 4 big khalifa
   and the Prophet's family members." `00-BRIEF.md` AD İMLÂSI'na yazıldı;
   `check.py` artık tırnak dışındaki çıplak adları yakalıyor. Kapsamı benim
   yorumum: dört halife, hanımlar, kızlar, torunlar, Hz. Hamza, Hz. Abbas,
   Hz. Ca'fer. *İbn Abbas* râvi adı olarak böyle kaldı.
4. **Nakil dokunulmazdır:** "we never alter a citation or a quote, this is
   only when we are the author of the sentence." `00-BRIEF.md`'ye NAKİL
   DOKUNULMAZDIR faslı eklendi. Bunun üzerine s2'de üç söz Arapçaya göre
   düzeltildi: Ka'b'ın ilân sözü ortasından başlıyordu (sabit ilk cümle
   onun yerine değişti: `Tebük'e çağrı, Medine'nin alışık olmadığı bir
   açıklıkla yapıldı.`); "istediğim zaman yaparım"daki "yaparım" Arapçada
   yoktu; Ulbe'nin "canımda"sı *ceset*, yani "bedenimde" oldu.
5. **Boş dramatik cümle yok:** "the last sentence adds nothing to the story
   imo. everything it says was said before it. dont add these dramatic phrases
   with no value to the story." `00-BRIEF.md`, ÜSLÛP faslına yazıldı. s1 ve
   s2 bu gözle baştan tarandı: s2'den yedi cümle, s1'den bir düzine cümle
   çıktı (s1'de Ka'b'ın sözünü yorumlayan iki paragraf da, 2. madde
   gereğince). s1'in "Haber Medine'ye… ulaştı" cümlesi kendinden önceki İbn
   İshak tarifini tekrar ettiği için mevsim paragrafının başına alındı; s2'nin
   sabit son cümlesi Ka'b'ın sözünü tekrar ettiği için kaldırıldı, bölüm
   Ka'b'ın sözüyle bitiyor. Bantlar artık tavan; s1 696, s2 1.067 kelime.
6. **Ka'b'ın nakli tek parça:** "can we keep ka'b narration separate instead of
   fragmenting it throughout the chapter? either start the chapter with what he
   narrated to give a sneak peek into what is coming, or add to the end as
   commentary." Karar: bölümün sonunda tek blok. s2 böyle yeniden dizildi
   (Buhârî 4418'in kesintisiz ibaresi, s3'e düşen divan cümlesi `(…)` ile
   atlandı; Müslim'in fazlası geçiş cümlesinde). s3-s6 ve s9 brieflerine
   kuruluş notu eklendi.
7. **Ton, kuruluş ve kısalık beğenildi** ("i like the tone, structure and
   brevity as in the first two chapters"). Rivayet farkları geçiş cümlesinde
   değil, Ka'b blokunun içinde, ait olduğu yerde parantezle verilir:
   "maybe try to add this kinda things into the text but in paranthesis.
   otherwise it is detached from the context." s2 düzeltildi; `00-BRIEF.md`'ye
   yazıldı.
8. **s3 ile s4 birleşti** ("Merge s3 into s4"): yeni s3 `Kuzeye Giden Yol`
   (959 kelime). Kitap dokuz bölüm oldu; eski s5-s10 → s4-s9 diye yeniden
   numaralandı (briefler, `00-BRIEF.md` tablosu, `check.py`, `overlap.py`,
   `build.py`). Bu dosyanın yukarısındaki eski numaralar tarihçedir;
   güncel numara briefin başlığındadır. Yeniden numaralamadan önceki hâl
   `.backup-before-renumber/`.
   Birleştirmede kaynaktan fazla söyleyen üç ibare düzeltildi: Hicr sözü
   Arapçadaki gibi olumsuz kuruldu ("ağlayarak olmadıkça girmeyin");
   "Hz. Peygamber o sırada Umâre'nin yanında" ve "Deve orada bulundu"
   çıkarıldı. İbn İshak'ın yağmur rivayeti yerine Hz. Ömer'in sağlam senedli
   nakli kullanıldı; o nakil yeri adlandırmadığı için Hicr'e konmadı.
9. **"finish the rest of the book like this"** (2026-10-31): s4-s9 yazıldı.
   Bütün kitap `check.py all` GEÇTİ; 7.090 kelime, dokuz bölüm, 111 tırnaklı
   söz. Kaynak metinler `research/texts/`e indirildi (Buhârî ve Müslim'in
   Arapça tam metni, kullanılan hadislerin dökümü `hadis-metinleri.md`,
   Diyanet meali `diyanet-tevbe.txt`) ve her söz oradan çevrildi.
   Yazarken düzeltilen ve bir dahaki turda bakılacak cinsten hatalar:
   - Hz. Ömer'in Müslim 27'deki cümlesi yarım kalmıştı; tamamlandı.
   - Kurtubî'de *Ebû Zeyd*; *Ebû Bekir el-Verrâk* halife değildir,
     `check.py` istisnası var.
   - Ka'b'ın *hullifû* açıklamasındaki "onun bizi geri bırakması"
     Resûlullah'ı kasteder, Allah'ı değil (Arapçada önceki cümle
     "Resûlullah işimizi erteledi" der). Brief'teki "O'nun" yanlıştı.
   - s4, s5, s6, s7, s8 Ka'b'ın sözüyle biter; s9 (kitabın sonu) anlatıcının
     sabit son cümlesiyle.
   Bağımsız bir yoklama ajanı bitmiş metni kaynaklara karşı okuyor:
   `research/fact-manuscript-v1.md`.
10. **s6 ile s7 birleşti** ("join s6 to s7"): yeni s6 `Elli Gece` (1.114
    kelime): dönüş ve Sakîf → Tevbe 94-96, 106 → tek parça Ka'b nakli (mescit
    sabahından "tevbemdendir"e kadar). Kitap sekiz bölüm; eski s8 → s7, s9 →
    s8. Briefler, tablo, `check.py`, `overlap.py`, `build.py` güncellendi;
    öncesi `.backup-before-merge67/`.
11. **Ölüm için yalın "düştü" yok:** "dont use düştü for someone dying.
    either say şehit düştü, or öldü depending on the context. Or dünyadan
    göçtü or something if it has to be super poetic." s1 (Mu'te'nin üç
    sancaktarı: şehit oldu / şehit düştü; Abdullah b. Revâha) ve s3 (Mahşî:
    Yemâme'de şehit düştü) düzeltildi; `00-BRIEF.md`'ye ve `check.py`'ye
    yazıldı.
12. **Bitmiş metnin kaynak yoklaması** (`research/fact-manuscript-v1.md`):
    ~110 söz, ~240 anlatıcı iddiası, 52 âyet atfı. 6 ağır, 10 orta, 23 hafif
    kusur ve 6 doğrulanamayan madde; hepsi işlendi:
    - Ortasından başlayan sözlere `(…)` yahut sözün başı eklendi (Ulbe, kaybolan
      deve, Umâre, Dırâr cevabı, 9:42, Müslim 27).
    - İki rivayetin karıştığı yerler ayrıldı (Hz. Ömer'in son cümlesi Tirmizî'ye
      göre; Ammâr'ın dönüşü Ahmed'e göre; s6'da Buhârî bloku içindeki Müslim
      kelimeleri çıktı).
    - Tuzak 8: s8'de 9:118 meali "işi ertelenen üç kişi"; s6'da da.
    - Hilâl'in hanımının sorusu Türkçede ters anlam veriyordu: "hoş görmez misin?"
    - Doğrulanamayanlar çıkarıldı yahut kaynağa bağlandı: Akabe'nin "gizliliği"
      ve "bir avuç adam" çıktı; "Hicaz'da Arap kuvveti kalmamıştı" çıktı;
      Mekke-Huneyn-Tâif sırası DİA (Huneyn) ile doğrulandı, "Tâif geçilmişti"
      "kuşatılıp bırakılmıştı" oldu; "kayaya oyulmuş" yerine Kur'an'ın Hicr
      sûresine atıf; "kabileler birer birer geliyordu" çıktı; 700 km DİA'da.
    - Kurtubî'deki ad Ebû Zeyd'dir (fact-quran'daki "Ebû Yezîd" yanlıştı).
    Kitap 7.144 kelime, sekiz bölüm, hepsi GEÇTİ.
13. Ka'b blokundaki parantezde "Hz. Ümmü Seleme" → "Ümmü Seleme" (aydin4ik: "remove Hz"). Kaide: tırnak içindeki parantezlere de Hz. eklenmez.
14. s1'e Rûm ve Gassânî bağlamı eklendi ("give a bit more context of geopolitics and byzantine"): Sâsânî savaşı, Herakliyus, Rûm 30:2-4, Buhârî 2941, Gassânîler, Mu'te'nin sebebi. Dayanaklar `research/fact-s1-rum.md`. s1 842 kelime.
15. s1'deki "Haberin ne kadar doğru olduğu bu hikâyenin sonlarına doğru tartılacak" çıkarıldı (bölümler arası atıf + boş cümle).
16. Bölümler arası atıf yasağı kaldırıldı ("remove this rule, they can refer to each other where relevant"). Atıf yalnız okura bir şey kazandırıyorsa.
17. Ölçü daima metrik ("always use metric, both in english and turkish"): s3 Cürf "üç mil" → "altı kilometre kadar"; s4 sâ' için parantezle "üç litre kadar" (DİA, Sâ' maddesi: Peygamber sâı 4 müdd, bir ölçüme göre 2,75 L). Brief sözlüğündeki "avuç dolusu ölçek" yanlıştı, düzeltildi.
18. "korur" (preserves kalkı) kaldırıldı ("you use korur too much… in turkish it doesnt fit"): altı yerde nakleder/kaydeder/rivayet eder/yer verir; brieflerde de. Kural 00-BRIEF.md'de. Asıl mânâsındaki iki kullanım (sınırı koruyan; Allah'ın beni korumasını) kaldı.
19. s9 Kaynaklar yazıldı ("as a final chapter, give short intros and bios of the classic sources you used"): Kur'an; Buhârî, Müslim, Tirmizî, Ahmed b. Hanbel; Urve, İbn İshak, İbn Hişâm, Vâkıdî, İbn Sa'd; İbn Abbas ve talebeleri (Mücâhid, İkrime, Katâde); Taberî, Begavî, Zemahşerî, Kurtubî, İbn Kesîr, Âlûsî, İbn Âşûr. Her olgu research/fact-sources.md'den (DİA). Katâde İbn Abbas'ın talebesi değil, talebelerinin talebesi (DİA). 1.270 kelime.
20. s8 (Fâdıha ve Tevbe) kitaptan çıkarıldı (aydin4ik: "remove s8"; teyit edildi). Metni ve briefi removed/'da. Kaynaklar s8 oldu. Not: başka bir Claude oturumu da metin üzerinde çalışıyor (Kaynaklar'ın başına hamd ve salavat ekledi).
