# v2 - TEK DEĞİŞİKLİK: SÖZ, ANLATILMAZ; SÖYLENİR

v1 yazıldı, okundu ve tek bir mesele üzerine geri geldi. v2'de yapılacak iş
budur ve **yalnız budur**. Anlatıyı yeniden kurma, vak'a ekleme, vak'a çıkarma,
üslûbu değiştirme. Metin aynı metindir; değişecek olan sözün nasıl verildiğidir.

## Mesele

aydin4ik'in kendi sözüyle: "when you are quoting a story, i want you to quote
most of them as a story, not as a narration from a third person."

Verdiği misal, v1'in s2 bölümünden:

> Hz. Peygamber halkı topladı ve görüşlerini istedi. Ebû Bekir kalkıp konuştu ve
> güzel konuştu; Ömer kalkıp konuştu, o da güzel konuştu. Sonra Mikdâd b. Amr
> kalktı ve muhacirler adına, Mûsâ'ya "sen ve Rabbin gidip savaşın" diyen kavmin
> sözünü kendilerinin söylemeyeceğini bildirdi.

Bunun kusuru şudur: adam konuşmuyor, adamın konuştuğu **haber veriliyor**. Söz
üçüncü şahsın ağzında eriyor. Doğrusu, adamın kalkıp söylemesidir:

> Sonra Mikdâd b. Amr kalktı ve dedi: "Yâ Resûlallah! Biz sana İsrâil
> oğullarının Mûsâ'ya dediğini demeyeceğiz. Onlar 'sen ve Rabbin gidip savaşın'
> dediler. Biz diyoruz ki: sen git, biz seninle beraberiz."

Fark üslûp farkı değildir. İlkinde okur sözü hakkında bilgilendirilir, ikincisinde
sözü işitir. Kaynak zaten sözü korumuşsa, onu dolaylı anlatıma çevirmek kaynağın
verdiğini geri almaktır.

## Kaide

**Kaynak sözü korumuşsa, söz olarak yazılır.** Kalıp şudur: `X kalktı ve dedi:`
yahut `X şöyle dedi:` yahut `X sordu:` ve arkasından çift tırnak içinde sözün
kendisi. Söz uzunsa bölünür, kısaltılır, fakat başkasının ağzına aktarılmaz.

**Kaynak sözü korumamışsa, dolaylı kalır.** Bu şarttır ve yasağı taşır:
**diyalog uydurmak yasaktır.** Kaynakta yalnız "şöyle bir teklifte bulundu"
deniyorsa, sen o teklifin cümlelerini kuramazsın. Emin değilsen dolaylı bırak.
Uydurulmuş bir söz, kazanılan canlılıktan kat kat pahalıya gelir; kitabın bütün
îtibârı kaynağa sadâkatinden geliyor.

Ölçü şudur: bu sözü siyer kitaplarında tırnak içinde okudun mu? Okuduysan tırnağa
al. Okumadıysan, hatırladığın şey sözün **muhtevası** ise dolaylı yaz.

## Nasıl yazılır

- `dedi ki:` yerine sade `dedi:` tercih edilir. `şöyle dedi:`, `sordu:`,
  `cevap verdi:`, `haykırdı:` hepsi caizdir; hangisi cümleye oturuyorsa.
- Sözün kime söylendiği belliyse söylenir: `Kureyş'e döndü ve dedi:`
- Söz Arapça bir kalıpsa hem kalıp hem mânası verilir; kitapta zaten böyle
  yapılmıştır: `"Şâhet'l-vücûh", yüzler kara olsun, dedi.`
- Kaynak adı sözün önünde durabilir: `İbn İshak'ın naklinde şöyle der:`
- **Tek paragrafta üç dörtten fazla tırnaklı söz olmasın.** Sayfa bir piyese
  dönmeyecek; nesir, sözü taşıyan zemin olarak kalacak.
- Uzun bir sözü ikiye böl: bir kısmı tırnakta, gerisi dolaylı. Bu en tabiî
  şeklidir ve klasik siyer nesri de böyle yapar.

## Değişmeyecek olanlar

- **SABİT İLK CÜMLE ve SABİT SON CÜMLE harfiyen yerinde kalır.** Dokunulmaz.
- Başlık aynı. Bölümün vak'aları aynı, sırası aynı, hükümleri aynı.
- **Uzun çizgi (—) ve orta çizgi (–) yasağı devam eder; sayısı sıfır olacak.**
- Dipnot, tablo, madde imi, alt başlık yok. Kaynak adı cümle içinde geçer.
- `Hz. Muhammed ﷺ` bölümde bir kez, ilk anışta; sonra `Hz. Peygamber`.
- Ad imlâsı v1'de neyse aynen o. **Ebû Süfyân b. Harb** (kervan reisi) ile
  **Ebû Süfyân b. Hâris** (Hz. Peygamber'in amcaoğlu) ayrı adamlardır.
  **Amr b. Hadramî** (Nahle'de öldürülen) ile **Âmir b. Hadramî** (Bedir'de
  çağrıda bulunan) ayrı adamlardır. `Sa'd`, `Mus'ab`, `Zem'a`, `İbn Sa'd`
  kesmeli; `Vâkıdî`, `Buhârî`, `Taberî`, `Muâz` şapkalı; `İbn İshak` (İshâk
  değil); `Ebû Bekir` (Bekr değil).
- Bölümler birbirine atıf yapmaz ("başka bir bölümde görülecek" denmez).
- Mesafe kilometreyle. Bedir 17 Ramazan 2 (13 Mart 624), yani **Mart**; Ağustos
  değil.

## Kelime bandı

v2'de bant biraz genişletildi, çünkü söz olarak yazılan bir konuşma dolaylı
şeklinden bir parça uzun sürer. Yine de bu bir uzatma işi değildir: hedef,
aynı muhtevayı daha canlı vermektir. Bandın üst ucuna dayanmak zorunda değilsin.

## Kontrol

`python3 check.py sN` çalıştır, GEÇTİ diyene kadar düzelt. Kontrol artık tırnaklı
söz sayısını da bildiriyor (`söz` satırı); bu bir hedef değil, bir aynadır.
