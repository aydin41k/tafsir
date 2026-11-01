# Fact audit of the manuscript v1 (s1-s8)

Date: 2026-10-31. The manuscript was not edited.

## Chapter numbering

This report uses the current files (8 chapters). Old s6 ("Doğru Söz") and old s7 ("Elli Gece") are now merged as **s6** ("Elli Gece"). Old s8 is now **s7** and old s9 is now **s8**. All findings were re-checked against the current files. The merge and the "düştü" → "şehit oldu / şehit düştü" change in s1 and s3 add no new source problems.

## Method and sources

- Every quotation and every narrator claim in `v1/s1.md` … `v1/s8.md` was checked against the primary Arabic, the Diyanet meal, and the five research reports. Nothing was confirmed from memory.
- **Read directly for this audit:**
  - Hadith: `research/texts/hadis-metinleri.md` (B 4418, M 2769 api 7017 and the Ma'kıl variant 7019, B 4677, 4423, 1481, 2615-2616, 3802, 3743, 4670-4671, 1366, 1269, 4882, 4668, 369, 4655, 4363, 4673, 4676, 4678; M 706, 27, 1392, 2779, 2980-2981, 3031, 2404). From `ara-bukhari.json`: B 4416, 4419, 3378-3380, 2778, 1415, 4415. From jsDelivr (fawazahmed0): Tirmizî 3675 and 3701, Ebû Dâvûd 1678.
  - Qur'an: `diyanet-tevbe.txt`. For verses missing from that file (38, 39, 41, 42, 46, 47, 49, 65, 66, 81, 90, 92) I fetched alquran.cloud (quran-simple, tr.diyanet, tr.vakfi).
  - Sîre: İbn Hişâm, shamela 23833, pages 1253-1268 (= II/515-537); Vâkıdî, shamela 23680, pages 1028-1034 (= III/989-995); İbn Kesîr, *el-Bidâye* (Sîre), shamela 930, pages 1785-1795.
  - Tafsir: Kurtubî 9:117 and İbn Kesîr 9:74 (quran.com API).
- Everything else rests on the Arabic quoted in fact-sira, fact-hadith, fact-quran, fact-kab and fact-audit.
- **Severity:** HIGH = breaks the NAKİL rule (a word added or cut, a quote begun mid-speech, two narrations merged) or a binding trap. MEDIUM = misattribution, a meaning shift, or a claim stated more strongly than the source. LOW = small wording point, scene detail with no source, or a missing hedge.

## Counts

- Quotations checked: **about 110**, including 33 verse quotations or close paraphrases. By chapter: s1 1, s2 18, s3 17, s4 16, s5 13, s6 16, s7 8, s8 20.
- Narrator claims checked (dates, numbers, names, attributions, verse numbers, scene details): **about 240**.
- Verse numbers checked against content: **52 references. All numbers match their content.**
- Problems: **6 HIGH, 10 MEDIUM, 23 LOW**. **6 UNVERIFIED** items.

---

## HIGH

### H1. s5: a detail from Urve's version placed inside Ahmed's
- **Text.** "Ammâr bineklerin yüzlerine vurmaya başladı ve adamlar döndüler." The sentence sits inside the paragraph introduced with "Ahmed'in rivayetinde Ebü't-Tufeyl anlatır".
- **Source.** Ahmed 23792, as quoted in İbn Kesîr's tafsir on 9:74: «وأقبل عمار يضرب وجوه الرواحل، فقال رسول الله لحذيفة: قد، قد. حتى هبط رسول الله … ورجع عمار». In this version it is **Ammâr** who comes back. Ahmed never says the men turned back. "ففزعوا ورجعوا مقبوحين" ("they took fright and turned back") is in **Urve's** mursal report, where it is Huzeyfe who strikes the mounts.
- **Fix.** "Ammâr bineklerin yüzlerine vurmaya başladı; Hz. Peygamber geçitten inince Ammâr geri döndü." Or drop "ve adamlar döndüler" and put the men's flight in the Urve sentence.

### H2. s2: Hz. Ömer's last sentence mixes two collections
- **Text.** "Ben de 'Seni hiçbir şeyde asla geçemeyeceğim' dedim."
- **Source.**
  - Tirmizî 3675: «قُلْتُ وَاللَّهِ لاَ أَسْبِقُهُ إِلَى شَيْءٍ أَبَدًا». Third person, and it has "vallahi".
  - Ebû Dâvûd 1678: «قُلْتُ لاَ أُسَابِقُكَ إِلَى شَىْءٍ أَبَدًا». Second person, with a different verb: "I will never race you again".
  - The book takes the addressee from Ebû Dâvûd and the verb from Tirmizî, and drops Tirmizî's "vallahi".
  - In the same quote, Tirmizî's "يا أبا بكر" before the second "Ailene ne bıraktın?" is left out without "(…)".
  - The chapter never names the collection.
- **Fix.** Follow Tirmizî: "Ben de 'Vallahi onu hiçbir şeyde asla geçemeyeceğim' dedim", and "Resûlullah 'Ey Ebû Bekir, ailene ne bıraktın?' dedi". Or follow Ebû Dâvûd: "'Seninle bir daha hiçbir şeyde yarışmam' dedim". Name the source, e.g. "Tirmizî'nin rivayetinde Hz. Ömer kendisi anlatır".

### H3. s2: Ulbe's quote begins in the middle of his speech
- **Text.** «Sonra şöyle dedi: "Malımda, bedenimde yahut ırzımda bana dokunan her haksızlığı her müslümana sadaka olarak bağışlıyorum."»
- **Source.** *el-Bidâye* (İbn İshak, Yûnus b. Bükeyr's recension), shamela 930/1787: «ثم بكى وقال: اللهم إنك أمرت بالجهاد ورغبت فيه، ثم لم تجعل عندي ما أتقوى به، ولم تجعل في يد رسولك ما يحملني عليه، **وإني** أتصدق على كل مسلم بكل مظلمة…». The quote starts at «وإني». The prayer before it is dropped with no mark.
- **Fix.** Either "Sonra şöyle dedi: "(…) Malımda, bedenimde…"", or give the whole speech: "Allahım, sen cihadı emrettin ve ona teşvik ettin; sonra bana onunla güç bulacağım bir şey vermedin, Resulünün eline de beni bindireceği bir şey koymadın. Ben de…".

### H4. s3: the Prophet's words about the lost camel begin mid-speech
- **Text.** «Hz. Peygamber şöyle dedi: "Vallahi ben ancak Allah'ın bana öğrettiğini bilirim. …"»
- **Source.** İH II/522-523 (shamela 23833/1260): «إن رجلا قال: هذا محمد يخبركم أنه نبي، ويزعم أنه يخبركم بأمر السماء وهو لا يدري أين ناقته، **وإني والله** ما أعلم إلا ما علمني الله…».
  - The speech opens by repeating the hypocrite's words. The quote starts at «وإني».
  - Smaller point: Umâre's words begin «إليّ عباد الله، إن في رحلي لداهية…». The book starts at «إن» without "(…)".
- **Fix.** «"Bir adam: 'Bu Muhammed size peygamber olduğunu haber veriyor, size gökten haber verdiğini iddia ediyor; hâlbuki devesinin nerede olduğunu bilmiyor' dedi. Vallahi ben ancak…"» Or start with "(…) Vallahi ben…". For Umâre: «"(…) Yüklerimin arasında…"».

### H5. s8: verse 118 rendered "geride bırakılan", against Tevbe trap 8
- **Text.** «"Geride bırakılan üç kişiye de tevbe nasip etti. …"»
- **Source and rule.**
  - Trap 8 is binding: "hullifû 'geride kalan' diye çevrilmez … Üçü için: *işi ertelenen üç kişi*".
  - Ka'b himself, in the same chapter (B 4418): «وليس الذي ذكر الله مما خلفنا عن الغزو إنما هو تخليفه إيانا وإرجاؤه أمرنا».
  - "Geride bırakılan" is the Vakfı/Diyanet sense the brief rules out.
- **Fix.** «"İşi ertelenen üç kişiye de tevbe nasip etti. …"» Inside Ka'b's quote, where he cites the verse and explains it himself, the literal "geride bırakılan" may stay.

### H6. s6: Hilâl's wife, a question that reverses its meaning
- **Text.** «"… ona hizmet etmemden hoşlanmaz mısın?" dedi. "Hayır, fakat sana yaklaşmasın" dedi.»
- **Source.** B 4418: «فهل تكره أن أخدمه؟ قال: لا، ولكن لا يقربك».
  - The question is "Do you **dislike** that I serve him?", and "No" grants permission.
  - In Turkish, "hoşlanmaz mısın?" reads as "wouldn't you like it?". Then "Hayır" sounds like a refusal.
- **Fix.** «"… ona hizmet etmemi hoş görmez misin?"». Or «"… ona hizmet etmemden hoşnutsuz olur musun?"».

---

## MEDIUM

### M1. s2: the Prophet's usual practice misdescribed
- **Text.** "Hz. Muhammed ﷺ bir sefere çıkacağı zaman hedefini sükûtla korurdu".
- **Source.**
  - İH II/516: «قلما يخرج في غزوة إلا كنى عنها، وأخبر أنه يريد غير الوجه الذي يصمد له».
  - B 4418: «إلا ورّى بغيرها».
  - He did not keep silent. He alluded to, or named, another destination.
- **Fix.** "…hedefini başka bir yön anarak örterdi".

### M2. s2: verse 42 cut mid-sentence with no "(…)"
- **Text.** The quote ends at "…diye Allah'a yemin edeceklerdir."
- **Source.** «وسيحلفون بالله لو استطعنا لخرجنا معكم **يهلكون أنفسهم والله يعلم إنهم لكاذبون**». The circumstantial clause "kendilerini helâk ederek" belongs to the same sentence. The verse then ends with "Allah onların yalancı olduğunu biliyor".
- **Fix.** End with "…yemin edeceklerdir (…)". Or add "…kendilerini helâk edercesine Allah'a yemin edeceklerdir. Allah ise onların yalancı olduklarını biliyor."

### M3. s6: Müslim's wording inside a quote labelled Buhârî
- **Text.** "namazıma yönelince bana bakar, ona doğru dönünce benden yüz çevirirdi".
- **Source.** B 4418: «فإذا أقبلت على صلاتي **أقبل إليّ**», i.e. "he turned toward me". «نظر إليّ», "he looked at me", is Müslim's wording.
- **Smaller points in the same chapter:**
  - "İnsanlar ona **beni** işaret etmeye başladılar": «إليّ» is Müslim's. B has only «يشيرون له».
  - "'Ka'b b. Mâlik'i **bana** kim gösterir?'": "bana" is not in either text («من يدل على كعب بن مالك»).
  - "yeryüzü **bile** gözümde yabancılaştı": "bile" is an added word.
- **Fix.** "namazıma yönelince bana yönelir…", "İnsanlar onu bana işaret etmeye başladılar" (or "…işaret etmeye başladılar"), "'Ka'b b. Mâlik'i kim gösterir?'", "yeryüzü gözümde yabancılaştı".

### M4. s4: Zülbicâdeyn's death placed "at Tebük"
- **Text.** "Tebük'te bir de ölüm oldu."
- **Source.** İH II/527-528: «وأنا مع رسول الله في **غزوة تبوك**». İbn İshak tells the story right after «ثم انصرف قافلا إلى المدينة» and the Vâdi'l-Müşakkak episode, that is, on the way home. The text gives the campaign, not the place.
- **Fix.** "Tebük seferinde bir de ölüm oldu." Or "Sefer sırasında, bir gece…".

### M5. s6: the three called "geride kalan üç kişi" (term rule and trap 8)
- **Text.** "…bu âyetin geride kalan üç kişi hakkında olduğunu söyler."
- **Fix.** "…bu âyetin işi ertelenen üç kişi hakkında olduğunu söyler."

### M6. s4: Buhârî credited with what only Müslim makes explicit
- **Text.** "Buhârî de … Hz. Peygamber'in ona bir bürde giydirdiğini … kaydeder."
- **Source.**
  - B 1481: «وأهدى ملك أيلة للنبي بغلة بيضاء، وكساه بردا». The subject of «كساه» is grammatically ambiguous.
  - M 1392.02: «فكتب إليه رسول الله وأهدى له بردا». Only Müslim says outright that the Prophet gave the bürde.
- **Fix.** "Buhârî ile Müslim … kaydeder; Müslim'in ibaresinde bürdeyi ona Hz. Peygamber hediye eder." Or attribute the bürde to Müslim.

### M7. s2: Osman's own claim presented as Buhârî's statement
- **Text.** "Buhârî de, senedini vermeden, Hz. Peygamber'in 'Ceyşü'l-usreyi kim donatırsa cennet onundur' dediğini ve Hz. Osman'ın onu donattığını kaydeder."
- **Source.** B 2778 (ta'lîk). Osman says this himself while under siege: «ألستم تعلمون أنه قال: من جهز جيش العسرة فله الجنة. فجهزتهم. قال فصدقوه». Those present confirmed it.
- **Fix.** "Buhârî'nin senedsiz bir kaydında Hz. Osman, kuşatıldığı gün, Hz. Peygamber'in 'Ceyşü'l-usreyi kim donatırsa cennet onundur' dediğini ve kendisinin onu donattığını hatırlatır; oradakiler onu doğrular."

### M8. s5: Müslim's count of the Akabe men flattened
- **Text.** "Akabe ehli on dört yahut on beş kişiydi".
- **Source.** M 2779.03: «كنا نخبر أنهم أربعة عشر فإن كنت منهم فقد كان القوم خمسة عشر». "Fifteen" holds only if the questioner was one of them. It is a barb, not uncertainty. Also, Müslim speaks of "ehlü'l-akabe" without naming Tebük.
- **Fix.** "Huzeyfe, kendisine soran adama, onların on dört kişi olduğunun söylendiğini, eğer o da onlardansa on beş olduklarını söyledi…"

### M9. s3: "tevbe etti" given with no source, beside an İbn İshak attribution
- **Text.** "Alay edenlerden Mahşî b. Humayyir ise tevbe etti. İbn İshak'a göre…"
- **Source.** İH II/525: «وكأن الذي عفي عنه في هذه الآية مخشن بن حمير، فتسمى عبد الرحمن…». İbn İshak gives the pardon, with a hedge ("kâenne"), and the name change. "He repented" is Kurtubî's (per fact-quran). Also, in İH Mahşin objected to the others' talk; he did not join the mockery.
- **Fix.** "İbn İshak'a göre âyetin affettiği kişi Mahşî b. Humayyir olmalıydı; adını Abdurrahman yaptı…" Or attribute "tevbe etti" to Kurtubî.

### M10. s1: the Akabe pledge, details with no source
- **Text.** "…ona İslâm üzere söz veren **bir avuç** Yesribli adamın arasındaydı; bu söz … geceleyin **ve gizlice, çünkü Mekke'de böyle bir sözün işitilmesi o adamların hiçbiri için hayırlı olmazdı**."
- **Source.**
  - Ka'b says only «ليلة العقبة حين تواثقنا على الإسلام». So "geceleyin" is supported.
  - DİA (in fact-kab item 9) puts Ka'b at the **Second** Akabe, in the ensâr delegation of 622, which numbered some seventy men. "Bir avuç" does not fit that.
  - "Gizlice" and the reason given for it appear in none of the texts or reports.
- **Fix.** "…İslâm üzere söz veren Yesribli adamların arasındaydı; bu söz Mekke'de, Akabe denen yerde, geceleyin verilmişti." Or have the secrecy verified first.

---

## LOW

1. **s1.** "Siyer edebiyatında bir sahâbînin kendi kusurunu … başka bir rivayet az bulunur." This is an evaluative claim with no source. Soften it or drop it.
2. **s1.** "Mu'te'de Rûm'un **ve ona bağlı Arap kabilelerinin** karşısına düşmüştü". The allied tribes at Mu'te are not in the reports (fact-sira A4). See UNVERIFIED.
3. **s1.** "Sekizinci yılın sonunda … Mekke fethedilmiş … Huneyn … Tâif" and "Hicaz'da artık … Arap kuvveti kalmamıştı". This chronology and summary are not in the reports. See UNVERIFIED.
4. **s1.** "Haber Medine'ye, meyvenin olgunlaştığı bir mevsimde ulaştı. İbn İshak o zamanı … tarif eder". In İbn İshak the season belongs to the **call to arms** («أمر أصحابه بالتهيؤ … وذلك في زمان…»), not to the arrival of the news. This was already noted as an inference (fact-audit A12). Possible fix: "Çağrı, … bir mevsimde geldi."
5. **s2.** "O andan sonra Medine'de kimse nereye çağrıldığını bilmeden kalmadı." This goes beyond the sources, which say only that he announced the destination. Drop it, or "…herkes nereye çağrıldığını bildi" as narrator inference.
6. **s2.** Verse 90: "…yalan söyleyenler ise **bir mazeret bile söylemeden** oturup kaldılar". "Özür bile beyan etmeksizin" is the older Diyanet's gloss. The Arabic «وقعد الذين كذبوا الله ورسوله» does not say it. Fix: "…yalan söyleyenler ise oturup kaldılar".
7. **s2.** "İbn Kesîr'in naklettiği bir söz …: bundan daha güzel bir sitem işittiniz mi…". The speaker is Avn b. Abdullah, and İbn Kesîr quotes him (fact-quran B). Better: "İbn Kesîr'in Avn b. Abdullah'tan naklettiği söz".
8. **s3.** İbn Übey's quote in Vâkıdî: «"Muhammed Benî Asfar ile savaşmayı oyun mu sanıyor? (…) Yarın onun ashabını…"». In VK III/995 these are two separate sayings: «ثم قال ابن أبي: والله لكأني أنظر…». The "(…)" joins them, and "vallahi" is dropped. Acceptable. Cleaner: "…oyun mu sanıyor?" Sonra şöyle dedi: "Vallahi, yarın…"
9. **s3.** "Medine'ye üç mil kadar mesafedeki Cürf". The three miles come from the editor's footnote in the İH edition, not from İbn İshak. They are acceptable in the narrator's voice, but they sit inside "İbn İshak'ın naklinde".
10. **s3.** The Ali scene. The Cürf scene (İbn İshak) is followed directly by the Buhârî/Müslim exchange. Read together, they suggest Ali's protest was made at Cürf. Buhârî and Müslim give no place (fact-hadith s3/1). Fix: "Buhârî ile Müslim'in, yer belirtmeden, Sa'd b. Ebû Vakkâs'tan naklinde…".
11. **s3.** Hicr: "**yani Sâlih peygamberin devesinin** uğradığı kuyu" is placed within "Buhârî ile Müslim'in … naklettiğine göre". The hadith says only «الناقة». The identification is the narrator's (fact-hadith accepted it). Move it outside the attribution.
12. **s3.** "Semûd kavminin **kayaya oyulmuş** yurdu Hicr". This is not in any text read. See UNVERIFIED.
13. **s3.** Hz. Ömer on the thirst: "**Yanımızdaki kapları doldurduk.**" The Arabic is «فملؤوا ما معهم»: third person, "what they had". "Kaplar" is added. Fix: "Yanlarında ne varsa doldurdular."
14. **s3.** Ebû Zer: "Müslümanlardan biri yolda **bir karaltı** gördü". İH has «نظر ناظر … إن هذا الرجل يمشي على الطريق وحده»; "karaltı" is invented scene detail. Fix: "Müslümanlardan biri baktı ve dedi:".
15. **s3.** The mockers. İbn Ömer's report in Taberî is called "bu alayın dili", which ties it to İbn İshak's scene. Taberî 16912 is a separate report (a majlis during the Tebük campaign). Fix: "Taberî'nin tefsirinde İbn Ömer, aynı seferde söylenmiş bir alayı nakleder:".
16. **s3.** Verse 65: "'Biz sadece lafa dalmıştık ve **aramızda** eğleniyorduk'". "Aramızda" is not in «إنما كنا نخوض ونلعب». Drop it.
17. **s4.** M 27.02: «"…umulur ki Allah onda **(bir bereket)** kılar."» Müslim has «لعل الله أن يجعل في ذلك». The parenthesis adds a word inside the quote, which the brief forbids for verse glosses too. Kurtubî's citation has «البركة», but the quote is labelled Müslim. Drop the parenthesis, or say in the narrator's line that the bereket is meant.
18. **s4.** "Buhârî ile Müslim, Ebû Humeyd'den, Tebük'teki **ilk** geceyi korur". The text has «فلما أتينا تبوك قال: … الليلة» ("when we reached Tebük he said: tonight"). "İlk" is an inference. Fix: "Tebük'e varıldığı geceyi".
19. **s4.** Ükeyder. Enes's report of people touching the kaftan comes right after the kaftan is described on Ükeyder's body, so it reads as if they touched it at the capture. İH: «فاستلبه خالد، فبعث به إلى رسول الله … رأيت قباء أكيدر حين قدم به على رسول الله». Add "Hâlid kaftanı soyup Hz. Peygamber'e gönderdi; Enes'in naklinde…".
20. **s4.** Ebû Hayseme: "Yolda Ümeyr b. Vehb el-Cumahî'ye rastladı ve ona dedi". In İH, Ümeyr overtook him («أدرك أبا خيثمة عمير»). He spoke his sentence «حتى إذا دنوا من تبوك», when they were near Tebük. Fix: "Yolda Ümeyr b. Vehb el-Cumahî ona yetişti; Tebük'e yaklaşınca ona dedi:".
21. **s5.** Zû Evân "Medine'ye **bir saatlik** mesafede". «ساعة من نهار» means "a short part of a day", not an hour. Fix: "Medine'ye gündüzün kısa bir vakti kadar mesafedeki Zû Evân".
22. **s5.** Dırâr reply: «إني على جناح سفر، وحال شغل، **أو كما قال**، ولو قد قدمنا…». İbn İshak's hedge «أو كما قال» ("or as he said") falls inside the quote and is dropped without "(…)". Add "(…)" or say "İbn İshak'ın, 'yahut buna benzer bir söz' kaydıyla verdiğine göre şöyle demişti:".
23. **s5.** The B 3743 "sır sahibi" sentence sits inside the Akabe paragraph. Buhârî does not link the secret to Akabe; İbn Kesîr does (fact-hadith s6/1). Add "Buhârî bunu Akabe'ye bağlamaz" or move the sentence.

Smaller notes, not counted:
- **s3.** "Seniyyetü'l-Vedâ … Şam tarafında" follows İbn Kayyim. The İH editor glosses it toward Mecca. Defensible, but contested (fact-sira C1).
- **s6.** In the B 4677 parenthesis inside Ka'b's quote, "Ümmü Seleme" appears without "Hz.". The parenthesis is narrator paraphrase, not Ka'b's wording, so the "Hz." rule arguably applies. aydin4ik's call.
- **s8.** "İbn İshak'a göre Mahşî b. Humayyir affedilenlerdendi". İH hedges («وكأن»), and Taberî's İbn İshak has «فيما بلغني». A "galiba" would be truer.
- **s8.** In Ka'b's khullifû explanation, "geri bırakılmıştık" follows Müslim's «خلفنا». Buhârî has «تخلفنا» ("geri kalmıştık"). Minor, inside a Buhârî-labelled quote.

---

## UNVERIFIED (no primary text or report seen)

1. **s1.** The secrecy of the Akabe pledge and the reason given for it (M10).
2. **s1.** The Christian Arab tribes fighting beside the Rûm at Mu'te.
3. **s1.** The chronology "Sekizinci yılın sonunda": Mekke, Huneyn, Tâif, and "no Arab force left in Hicaz". None of the reports covers these dates.
4. **s3.** Hicr as "kayaya oyulmuş".
5. **s6.** "Arabistan'ın kabileleri birer birer Medine'ye geliyordu". Only the Sakîf delegation is verified (İH II/537).
6. **s1.** The road distance Medine-Tebük 700 km. It rests on DİA only, which the brief accepts (fact-sira H2).

---

## Items checked and found faithful (summary)

- **Ka'b's quotes.** s1, s2, s3 (Buhârî, with Müslim variants that are really in Müslim: «فأنا إليها أصعر», «إذا أردت», «لا أرى لي أسوة»), s4 (Müslim, incl. Ebû Hayseme and the sâ'), s5, s6 («عقبى الله» really in Müslim; otherwise apart from M3/H6), s7, s8. B 4677 parentheses (funeral prayer, Ümmü Seleme, last third of the night): verified.
- **Other hadith.**
  - Tirmizî 3701 (Osman's dinars, "iki kere").
  - B 4416 (Ali's protest and the Hârûn saying).
  - B 4419 (Hicr, head covered).
  - B 3378-3379 and M 2981 (wells, dough).
  - M 706 (spring; Muâz's reason «أراد أن لا يحرج أمته»).
  - B 1481 and M 1392 (wind; "acele"; Tâbe; Uhud "cübeyl").
  - B 2615 and M 2469 (Sa'd's handkerchiefs; Ükeyder in the ta'lîk).
  - B 4423 with the Companions' question.
  - B 4670 (shirt, garment, "yetmişin üstüne").
  - B 369 (Minâ proclamation; Ali with Berâe).
  - B 4668 (Ebû Akîl, half a sâ').
  - M 3031 («بل هي الفاضحة», «منّا»).
  - M 2779.03 (the three excused).
- **Sîre.**
  - Vâkıdî: the Nabateans, flour and oil, Lahm, Cüzâm, Gassân, Âmile, the vanguards at Belkâ, Hıms, and the verdict quote in s7. Cedd's bedrî son; Cedd's "lâ tenfirû fi'l-harr" to Benî Seleme; 420 riders; Zeyd b. Sâbit's estimate.
  - İbn İshak:
    - Cedd's dialogue, word for word.
    - The seven bekkâûn and their names; Ebû Leylâ and İbn Mugaffel given a mount.
    - Süveylim (İbn Hişâm's unnamed informant), Ali at Cürf and his return, Ebû Hayseme's speech.
    - The lost camel and Zeyd b. Lusayt; Ebû Zer and his death at Rebeze.
    - The mockers on the outward march; Mahşî's martyrdom "with his place unknown".
    - The Eyle treaty text (the "(…)" correctly placed); Ükeyder; Zülbicâdeyn's words; the Dırâr request, Zû Evân "haberi", Ma'n or Âsım.
  - İbn Hişâm: Ca'fer's arms; Ebû Hayseme named Mâlik b. Kays.
  - İbn Kesîr: Ömer's thirst report, «إسناده جيد».
- **Numbers.**
  - Army about 30,000 and 10,000 horses (İbn Sa'd, Vâkıdî); "on binden fazla" (M 2769 Ma'kıl).
  - Stay of twenty nights against "on küsur"; return in Ramazan 9 (Aralık 630); İbn Übey's death in Zilkade (Vâkıdî).
  - Mu'te in Cemâziyelevvel 8 (Eylül 629); Tebük as the last campaign.
- **Verses.** 3, 29, 38, 39, 41, 42 (M2), 43, 44-45, 46, 47, 49, 50, 53-55, 56-57, 61, 64, 65-66, 67 («Allah'ı unuttular»), 74, 79, 80, 81, 83, 84, 86-87, 90, 91, 92, 93, 94, 95, 96, 97, 99, 101, 102, 103, 104, 106, 107, 108, 109, 112, 113, 117, 118 (H5), 119, 120 (incl. "düşmana karşı başarı"), 121, 122, 126, 128.
- **Tafsir.**
  - Mücâhid in Taberî (season); Taberî on 9:106 (Mücâhid, İkrime, Katâde, İbn Abbas); Taberî «عسى من الله واجب»; Taberî on et-Tevvâb.
  - Ebû Lübâbe: İbn Abbas and Taberî for Tebük; İbn el-Müseyyeb, Mücâhid and İbn İshak for Kurayza.
  - Katâde on el-Fâdıha.
  - Zemahşerî, Âlûsî and İbn Âşûr on the name et-Tevbe.
  - Begavî on «غزوة العسرة» and «ليستقيموا على التوبة».
  - Kurtubî: İbn Abbas and ehl-i meânî on 117; Ebû Bekir el-Verrâk; «فبدأ بالتوبة منه»; Ebû **Zeyd**, which is the correct name per fact-audit A4.
  - Câbir in Kurtubî («عسرة الظهر وعسرة الزاد وعسرة الماء»), which backs s2's "binek azdı, azık azdı, su azdı".
- **Traps.**
  - Not used: Sa'lebe, Kayser's envoy, Talea'l-bedru, the cave of verse 40, Huneyn, verses 58-60.
  - Handled correctly: verse 74 "bâzı müfessirlere göre"; Dırâr "dönüşte" with the news at Zû Evân; verse 67; the deputy dispute; the Rûm verdict given once, in s7.
- **Name rule.** No bare names of the four caliphs or of the Prophet's family appear in narrator text. "ﷺ" appears exactly once per chapter.
