# Fact-check: Tevbe (sura 9) claims in the Tebük briefs

Scope: every Tevbe verse number, paraphrase, sabab, sura name and "trap" in
`00-BRIEF.md` and `brief-s1.md` … `brief-s10.md`. Briefs not edited.

## Sources actually consulted (all fetched 2026-10-30)

- **Arabic text**: api.alquran.cloud, edition `quran-simple` (Tanzil text), whole sura.
- **Turkish**: *Diyanet İşleri, Kur'an-ı Kerim Türkçe Meali* (the current
  Diyanet meali), taken verse by verse from acikkuran.com (author id 11).
  kuran.diyanet.gov.tr itself could not be fetched (403 to curl, then a JS-only
  page that timed out in the browser). The older Diyanet translation on
  alquran.cloud (`tr.diyanet`) was also read and differs in wording. Every "Diyanet" quote below is from the acikkuran text.
- **English**: Sahih International (alquran.cloud).
- **Tafsir (Arabic, full text for every verse of sura 9)**: quran.com API v4:
  Taberî (id 15), İbn Kesîr (14), Kurtubî (90), Begavî (94).
- **Names of the sura**: tafsir.app: Zemahşerî *el-Keşşâf*, Râzî *Mefâtîh*
  (quotes Keşşâf), Âlûsî *Rûhu'l-meânî*, İbn Âşûr *et-Tahrîr ve't-tenvîr*
  (sura introduction, placed after 8:75 in that source).
- **Vâhidî, Esbâbü'n-nüzûl**: English translation only (spa5k tafsir_api,
  `en-asbab-al-nuzul-by-al-wahidi`), for 9:42-47, 49, 74, 79, 107. Arabic not seen.
- **Hadith**: fawazahmed0 hadith-api (Arabic + English, with grades for
  Tirmizî): Buhârî 1415, 4418, 4423, 4654, 4668-4679, 4882, 4986, 6933; Tirmizî
  3086; Müslim 2769 (index 7017 in that API). sunnah.com was blocked by Cloudflare.

Legend: **VERIFIED** = I saw it in the text. **CORRECTION** = wrong number,
paraphrase that says more than the source, or a weak or disputed sabab presented as
solid. **NUANCE** = not wrong, but the writer should know. **UNVERIFIED** = I could not see it.

---

## A. Sura names, basmala, ending

### A1. el-Fâdıha (00-BRIEF; s10 opening and fixed first sentence)
- Buhârî 4882 (Kitâbü't-Tefsîr, under **Sûretü'l-Haşr**), Saîd b. Cübeyr:
  «قُلْتُ لاِبْنِ عَبَّاسٍ سُورَةُ التَّوْبَةِ قَالَ التَّوْبَةُ هِيَ الْفَاضِحَةُ، مَا زَالَتْ تَنْزِلُ وَمِنْهُمْ وَمِنْهُمْ، حَتَّى ظَنُّوا أَنَّهَا لَمْ تُبْقِ أَحَدًا مِنْهُمْ إِلاَّ ذُكِرَ فِيهَا». Also Müslim 3031 (not fetched).
  **VERIFIED**: the report exists, it is in Buhârî's tafsir book, and "ve minhum ve minhum" is its content.
- s10 fixed first sentence, "İbn Abbas'a Tevbe sûresini **sorduklarında**, onun
  **asıl adının başka olduğunu** söyledi": **CORRECTION**. (a) One person asked:
  Saîd himself ("قلت"). (b) İbn Abbas does not say its "real name" is something else.
  He answers "et-Tevbe? O, el-Fâdıha'dır" (التوبة هي الفاضحة). Âlûsî gives the Ebû
  Ubeyd/İbnü'l-Münzir wording «التوبة؟ بل هي الفاضحة» ("no, rather it is
  al-Fâdiha"), which comes closer to a renaming. That wording is not Buhârî's.
  Safe version: "Saîd b. Cübeyr İbn Abbas'a Tevbe sûresini sorduğunda İbn Abbas 'Tevbe mi? O el-Fâdıha'dır' dedi."
- 00-BRIEF "İbn Abbas'ın ona **taktığı** adla el-Fâdıha": **NUANCE/CORRECTION (soft)**.
  Taberî (9:64, no. 16909) and İbn Kesîr (9:64) quote Katâde: «كانت تسمى هذه السورة الفاضحة، فاضحة المنافقين». So the name was in general use. İbn Abbas used it; no source shows he coined it. Say "İbn Abbas'ın andığı adla".
- s10 "altmış dördüncü âyet = *el-Fâdıha* adının sûredeki karşılığı": **VERIFIED**,
  and the tafsirs make the same link. Taberî 9:64: «فأظهر الله ذلك عليهم وفضحهم، فكانت هذه السورة تدعى: الفاضحة». İbn Kesîr 9:64 does the same via Katâde. Kurtubî 9:64: «ولهذا سميت الفاضحة والمثيرة والمبعثرة».

### A2. Other names
- Zemahşerî, *Keşşâf* (sura intro): «لها عدة أسماء: براءة، التوبة، المقشقشة، المبعثرة، المشردة، المخزية، الفاضحة، المثيرة، الحافرة، المنكلة، المدمدمة، سورة العذاب». Huzeyfe: «إنكم تسمونها سورة التوبة، وإنما هي سورة العذاب». **VERIFIED**.
- Kurtubî 9:1: also *el-Buhûs* and *el-Mub'asire* (Kuşeyrî). İbn Âşûr counts
  fourteen names: Berâe, Tevbe, Mukaşkışa (İbn Ömer/İbn Abbas), Fâdıha (İbn Abbas), Sûretü'l-azâb (Huzeyfe), Munakkıra (Ubeyd b. Umeyr), Buhûs (Mikdâd, Ebû Eyyûb), Hâfira (Hasan), Mesîre (Katâde), Mub'asire (İbn Abbas), Muhziye, Munekkile, Müşeddide (from *el-İtkân*), Müdemdime (Süfyân). **VERIFIED**.

### A3. WHY it is called *et-Tevbe* (exact quotes)
- **Zemahşerî, Keşşâf**: «…لأن فيها التوبة على المؤمنين» ("because in it is the
  turning [of Allah] upon the believers"). **VERIFIED.** Râzî copies the whole passage from Keşşâf, attributed by name.
- **Âlûsî, Rûhu'l-meânî**: «ولها عدة أسماء؛ التوبة لقوله تعالى فيها: ﴿لقد تاب الله على النبي والمهاجرين والأنصار﴾ إلى قوله سبحانه: ﴿وعلى الثلاثة الذين خلفوا﴾». **VERIFIED.**
- **İbn Âşûr, et-Tahrîr ve't-tenvîr** (intro): «ووجه التسمية: أنها وردت فيها توبة الله تعالى عن الثلاثة الذين تخلفوا عن غزوة تبوك وهو حدث عظيم». **VERIFIED.** He also notes Tirmizî titles it "et-Tevbe" and that both names appear together in Zeyd b. Sâbit's hadith in Buhârî.
- Kurtubî: does not explain the name in the passage read. Râzî: no reason of his own beyond the Keşşâf quote. "Many mentions of repentance" as the reason: **UNVERIFIED**. None of the four sources says it. They say "Allah's tawba on the believers / on the Prophet, muhâjirûn, ansâr / on the three".

### A4. No basmala
- Tirmizî 3086 (İbn Abbas asks Osman): Osman says Enfâl was among the first Medinan
  revelations and Berâe among the last, «وكانت قصتها شبيهة بقصتها فظننت أنها منها، فقبض رسول الله ﷺ ولم يبين لنا أنها منها». Tirmizî: «هذا حديث حسن لا نعرفه إلا من حديث عوف عن يزيد الفارسي». **Grades shown by the API: Ahmed Şâkir: da'îf; Elbânî: da'îf; Beşşâr Avvâd: hasen; Zübeyr Ali Zaî: isnâdı hasen.** The weak point is Yezîd el-Fârisî. İbn Kesîr (9:1) quotes it and reports that Hâkim called it "sahîhu'l-isnâd".
  **VERIFIED, but the hadith is disputed**: say "Tirmizî'nin rivayetine göre", never "sahih".
- Ali's view (Kurtubî 9:1, İbn Abbas asking Ali): «لأن بسم الله الرحمن الرحيم أمان، وبراءة نزلت بالسيف ليس فيها أمان». Süfyân b. Uyeyne and Müberred say the same. **VERIFIED** as quoted by Kurtubî (chain not given).
- Other views in Kurtubî: the Arab custom of no basmala when breaking a treaty;
  Mâlik's view that the opening part was lost; the Companions disagreed whether
  Enfâl and Berâe are one sura. Kurtubî's own preference, after Kuşeyrî: «والصحيح أن التسمية لم تكتب لأن جبريل عليه السلام ما نزل بها في هذه السورة». **VERIFIED.**
- Brief (s10) only asks for one sentence on the missing basmala. Any of the views is usable if attributed.

### A5. Ending: 9:128-129; "last revealed"; Huzeyme / Ebû Huzeyme
- 9:128-129 are the last two verses (sura has 129). **VERIFIED.**
- Buhârî 4679: Zeyd b. Sâbit found two verses of et-Tevbe with **Huzeyme
  el-Ensârî**: «لَقَدْ جَاءَكُمْ رَسُولٌ…» to their end. Buhârî's own notes in the same place give "Ebû Huzeyme" in some chains and "Huzeyme or Ebû Huzeyme" in others. Buhârî 4986: «حَتَّى وَجَدْتُ آخِرَ سُورَةِ التَّوْبَةِ مَعَ أَبِي خُزَيْمَةَ الأَنْصَارِيِّ… حَتَّى خَاتِمَةِ بَرَاءَةَ». **VERIFIED.**
- Last revealed: Buhârî 4654 (Berâ'): «وَآخِرُ سُورَةٍ نَزَلَتْ بَرَاءَةٌ». **VERIFIED.**
  Übey b. Ka'b, "the last verse revealed was 'Lekad câekum…'" (Taberî 17514; İbn Kesîr 9:129; Kurtubî): chain through Ali b. Zeyd b. Cüd'ân, a known weak narrator. Kurtubî reconciles it with Saîd b. Cübeyr's report that 2:281 was last. So "the last sura revealed" is sahih. "The last verse revealed" is weak and disputed.
- s10 fixed last sentence, "Sûre … ümmetinin sıkıntıya düşmesi kendisine ağır gelen bir peygamberle **kapanır**": **NUANCE**. That is 9:128. The actual last verse is 9:129 («حسبي الله لا إله إلا هو عليه توكلت وهو رب العرش العظيم»). Acceptable if read as "the closing pair"; strictly the sura ends on 129.

---

## B. Verse-by-verse (in brief order)

Format: verse, Arabic key phrase, Diyanet wording (abridged), verdict.

**s2**
- **9:38-39** «اثَّاقَلْتُمْ إِلَى الْأَرْضِ» / «وَيَسْتَبْدِلْ قَوْمًا غَيْرَكُمْ». Diyanet: "yere çakılıp kaldınız … yerinize sizden başka bir toplum getirir". Brief paraphrase **VERIFIED**. Tabuk link: Taberî 9:38 «وذلك غزوة رسول الله ﷺ تبوك»; Mücâhid: «أمروا بالنفير في الصيف حين خرفت النخل وطابت الثمار واشتهوا الظلال» (no. 16719). This also supports the brief's season and shade motif.
- **9:40** «إِذْ هُمَا فِي الْغَارِ». Diyanet: "(Mekke'den) çıkardıkları zaman… mağarada". Trap 2 (cave = hicret, a reminder inside the call) **VERIFIED**.
- **9:41** «انْفِرُوا خِفَافًا وَثِقَالًا». Brief "hafif ve ağır çıkın" is literal, **VERIFIED**. Diyanet interprets it as "gerek yaya, gerek binek üzerinde".
- **9:42** «لَوْ كَانَ عَرَضًا قَرِيبًا وَسَفَرًا قَاصِدًا… بَعُدَتْ عَلَيْهِمُ الشُّقَّةُ». **VERIFIED**. Katâde: «هي غزوة تبوك» (Taberî 16761).
- **9:43** «عَفَا اللَّهُ عَنْكَ لِمَ أَذِنْتَ لَهُمْ». **VERIFIED** number and content.
  Tone "azar değil, sitem ve af": **VERIFIED** as the tafsirs' reading. Taberî calls it «عتاب». İbn Kesîr quotes Avn: «هل سمعتم بمعاتبة أحسن من هذا؟ بدأ بالعفو قبل المعاتبة». Kurtubî: «عتاب تلطف».
  **NUANCE**: the brief says "Allah seni affetti"; Diyanet says "Allah, seni affetsin!". Kurtubî gives both readings: a prayer-style opening, or a statement of pardon. Either is defensible; a quoted meal should follow its source.
- **9:49** «ائْذَنْ لِي وَلَا تَفْتِنِّي ۚ أَلَا فِي الْفِتْنَةِ سَقَطُوا». Diyanet: "fitnenin ta içine düştüler". **VERIFIED**. Sabab Cedd b. Kays: Taberî 16788 (İbn İshak): «هل لك يا جد العام في جلاد بني الأصفر؟ … لقد عرف قومي ما رجل أشد عجبا بالنساء مني، وإني أخشى إن رأيت نساء بني الأصفر أن لا أصبر عنهن». The Prophet answered «قد أذنت لك». İbn İshak calls him «أخي بني سلمة», which confirms he was from Ka'b's clan. Vâhidî (English) gives the same story. **VERIFIED.**
- **9:79** «يَلْمِزُونَ الْمُطَّوِّعِينَ… وَالَّذِينَ لَا يَجِدُونَ إِلَّا جُهْدَهُمْ». **VERIFIED** number and content. The two-sided mockery (the big giver is "showing off", the small giver "Allah has no need of his sâ'") is in Buhârî 1415 and 4668. **VERIFIED.**
  **CORRECTION (attribution and details)**:
  - Buhârî 4668 (Ebû Mes'ûd) names **Ebû Akîl** but says he brought **half a sâ'**: «فَجَاءَ أَبُو عَقِيلٍ بِنِصْفِ صَاعٍ».
  - Buhârî 1415 (Ebû Mes'ûd) has «بِصَاعٍ», with the giver unnamed.
  - The detail "worked the night drawing water (أجر الجرير) for two sâ', kept one for his family, brought one" is **not in Buhârî**. It is in Taberî 17008 (Katâde, mursal, «حبحاب أبو عقيل») and Taberî 17014 (from Ebû Akîl's son, via Mûsâ b. Ubeyde, a weak narrator).
  - So "Buhârî'de Ebû Mes'ûd el-Ensârî nakli" covers the mockery but not "iki sâ'ın biri".
  - Also: Müslim (Ka'b hadith) identifies the sâ'-giver as **Ebû Hayseme**: «وهو الذي تصدق بصاع التمر حين لمزه المنافقون». The brief already flags this conflict.
  **UNVERIFIED**: the Tebük setting. Buhârî's wording is «لما أمرنا بالصدقة» / «لما نزلت آية الصدقة». Taberî, İbn Kesîr and Kurtubî on 9:79 do not mention Tebük. Link it to the donations for the army only as "rivayet olunur" or by placement.
- **9:81** «وَقَالُوا لَا تَنْفِرُوا فِي الْحَرِّ ۗ قُلْ نَارُ جَهَنَّمَ أَشَدُّ حَرًّا». Diyanet: "Bu sıcakta sefere çıkmayın… Cehennemin ateşi daha sıcaktır". **VERIFIED**. Taberî: «وهي غزوة تبوك، في حر شديد، فقال المنافقون بعضهم لبعض: لا تنفروا في الحر». This confirms "münafıkların birbirine sözü".
- **9:90** «وَجَاءَ الْمُعَذِّرُونَ مِنَ الْأَعْرَابِ». **VERIFIED**. Taberî 17075 and 17077: a group of Benî Gıfâr, including Hufâf b. Îmâ' (İbn İshak).
- **9:91-92** «وَأَعْيُنُهُمْ تَفِيضُ مِنَ الدَّمْعِ حَزَنًا»; the Prophet's words «لَا أَجِدُ مَا أَحْمِلُكُمْ عَلَيْهِ» are inside the verse. Diyanet: "gözleri yaş döke döke". **VERIFIED**. Names (Taberî, İbn Kesîr, Kurtubî) vary: Sâlim b. Umeyr, Ulbe b. Zeyd, Abdullah b. Mugaffel, Irbâz b. Sâriye, Benû Mukarrin and others. **VERIFIED** ("liste rivayetten rivayete değişir" is accurate).
  **CORRECTION (attribution)**: "Ulbe b. Zeyd's sadaqa of his honour (İbn Kesîr)". In İbn Kesîr's tafsir of 9:92, in Muhammed b. Ka'b's list, the one «الذي تصدق بعرضه فقبله الله منه» is **"Abdurrahman b. Yezîd Ebû Able"** of Benî Hârise. Taberî has the same. Ulbe b. Zeyd "of Benî Hârise" appears in İbn İshak's separate list on the same page without the sadaqa story. They may be the same man; the text does not say so. The "gece kalkıp" (night) detail: **UNVERIFIED**, not in these tafsirs.

**s3**
- **9:46-47** «لَوْ أَرَادُوا الْخُرُوجَ لَأَعَدُّوا لَهُ عُدَّةً… وَقِيلَ اقْعُدُوا مَعَ الْقَاعِدِينَ» / «لَوْ خَرَجُوا فِيكُمْ مَا زَادُوكُمْ إِلَّا خَبَالًا». Paraphrase **VERIFIED**.
  Link to Abdullah b. Übey's turning back: **VERIFIED**. Vâhidî (9:42-47) explicitly ties it to Ibn Übey camping below Seniyyetü'l-Vedâ and turning back. Taberî 16770 and 16781 (İbn İshak) name Ibn Übey and Cedd among those who sought leave.

**s4**
- **9:120** «لَا يُصِيبُهُمْ ظَمَأٌ وَلَا نَصَبٌ وَلَا مَخْمَصَةٌ… إِلَّا كُتِبَ لَهُمْ بِهِ عَمَلٌ صَالِحٌ». **VERIFIED.** Addressed to «أَهْلِ الْمَدِينَةِ وَمَنْ حَوْلَهُمْ مِنَ الْأَعْرَابِ».

**s5**
- **9:29** cizye. **VERIFIED**. Taberî 16616 (Mücâhid): «حين أمر محمد وأصحابه بغزوة تبوك». İbn Kesîr: the first order to fight the People of the Book, year 9, «ولهذا تجهز رسول الله ﷺ لقتال الروم».

**s6**
- **9:65-66** «إِنَّمَا كُنَّا نَخُوضُ وَنَلْعَبُ» / «لَا تَعْتَذِرُوا… إِنْ نَعْفُ عَنْ طَائِفَةٍ مِنْكُمْ نُعَذِّبْ طَائِفَةً». **VERIFIED**.
  - The İbn Ömer quote in Taberî 16912: «ما رأينا مثل قرائنا هؤلاء أرغب بطونا ولا أكذب ألسنا ولا أجبن عند اللقاء», set «في غزوة تبوك». **VERIFIED**.
  - The man clinging to the camel's girth with stones striking his feet: Taberî «متعلقا بحقب ناقة رسول الله ﷺ تنكبه الحجارة» and «وإن رجليه لتنسفان الحجارة وما يلتفت إليه». **VERIFIED.**
  - Mahşî b. Humayyir as the pardoned "tâife": Taberî 16919 (İbn İshak, «فيما بلغني»): «كان الذي عفي عنه… مخشي بن حمير الأشجعي حليف بني سلمة، وذلك أنه أنكر منهم بعض ما سمع». Kurtubî adds that he repented, was renamed Abdurrahman, prayed to be killed as a martyr with no trace left, and fell at Yemâme. Name variants: Mahşen, Muhâşin. **VERIFIED**, but it rests on İbn İshak's chainless "fîmâ belağanî".
- **9:74** «وَهَمُّوا بِمَا لَمْ يَنَالُوا… فَإِنْ يَتُوبُوا يَكُ خَيْرًا لَهُمْ». Diyanet: "başaramadıkları şeye (peygamberi öldürmeye) de yeltendiler… Eğer tövbe ederlerse, kendileri için hayırlı olur". **VERIFIED**.
  **CORRECTION (sabab strength)**: the Akabe link is one opinion among several.
  - **Taberî** gives these occasions: Cülâs b. Süveyd («لئن كان ما جاء به محمد حقا لنحن أشر من الحمر», 16967, 16969); a blue-eyed man and his companions (İbn Abbas); Abdullah b. Übey (Katâde, Müreysî' setting).
  - For "hammû" Taberî gives: killing the believer who reported Cülâs (Mücâhid); a Qurayshi named "el-Esved" who planned to kill the Prophet; Ibn Übey's «لئن رجعنا…».
  - **Taberî does not mention Akabe at all.**
  - **Kurtubî**: «وهموا بما لم ينالوا يعني المنافقين من قتل النبي ﷺ ليلة العقبة في غزوة تبوك، وكانوا اثني عشر رجلا».
  - **İbn Kesîr** ties it to Akabe via Beyhakî's *Delâil* (İbn İshak, A'meş, Huzeyfe: «فإذا أنا باثني عشر راكبا قد اعترضوه فيها») and Ahmed (Ebû't-Tufeyl). He supports the story with Müslim's «كم كان أصحاب العقبة» (14 or 15 men) and notes Huzeyfe's title «صاحب السر».
  - "If they repent it is better": Taberî 16984-85: Cülâs said «قد استثنى الله لي التوبة، فأنا أتوب», and the Prophet accepted it.
  - The brief's "atfen ve ihtiyatla" is right. The writer should say "bâzı müfessirler bu âyeti Akabe gecesine bağlar", not present 74 as simply "the Akabe verse".
- **9:107-110** Mescid-i Dırâr. Number and content **VERIFIED** («مَسْجِدًا ضِرَارًا وَكُفْرًا وَتَفْرِيقًا بَيْنَ الْمُؤْمِنِينَ وَإِرْصَادًا لِمَنْ حَارَبَ اللَّهَ وَرَسُولَهُ مِنْ قَبْلُ»). Ebû Âmir er-Râhib as «لمن حارب»: Taberî 17189-90. **VERIFIED.**
  - The request and answer: «إني على جناح سفر وحال شغل… ولو قد قدمنا أتيناكم». "Sâatün min nehâr" from Medina. Mâlik b. Duhşum lighting palm fronds («فأخذ سعفا من النخل فأشعل فيه نارا»). All **VERIFIED**: Taberî 17186 = İbn İshak; İbn Kesîr identical.
  - **CORRECTION (s6 and 00-BRIEF trap 5, "Zû Evân'da âyetlerin inmesi")**. İbn İshak says «فلما نزل بذي أوان، **أتاه خبر المسجد**» ("the news of the mosque reached him"). After the burning: «ونزل فيهم من القرآن ما نزل». He does not place the revelation at Zû Evân. Kurtubî's version: after his return, when he called for his shirt to go there, «فنزل عليه القرآن بخبر مسجد الضرار».
  - Safe wording: "dönüşte, Zû Evân'da mescidin haberi ona geldi". The trap's core (return journey, not outbound) is **VERIFIED**.
  - Variant: «معن بن عدي = أو أخاه: عاصم بن عدي».
  - Side note: İbn İshak's list of the twelve builders includes «ثعلبة بن حاطب». This is another reason to keep the Sa'lebe material out.

**s7**
- **9:94-96** «يَعْتَذِرُونَ إِلَيْكُمْ إِذَا رَجَعْتُمْ» / «سَيَحْلِفُونَ بِاللَّهِ لَكُمْ إِذَا انْقَلَبْتُمْ إِلَيْهِمْ لِتُعْرِضُوا عَنْهُمْ ۖ فَأَعْرِضُوا عَنْهُمْ» / «يَحْلِفُونَ لَكُمْ لِتَرْضَوْا عَنْهُمْ». **VERIFIED**. Ka'b himself cites 9:95-96 for the liars (Buhârî 4418, 4673) and 9:94 (Buhârî 4677). "Yalanı âyet söyler" is well grounded.
- **9:106** «وَآخَرُونَ مُرْجَوْنَ لِأَمْرِ اللَّهِ إِمَّا يُعَذِّبُهُمْ وَإِمَّا يَتُوبُ عَلَيْهِمْ». Diyanet: "Allah'ın emrine bırakılmışlardır. Bunlara ya azap eder ya da tövbelerini kabul eder". The number and the paraphrase ("adlarını vermez") are **VERIFIED**.
  **CORRECTION**: "Ka'b'ın kendisi bu âyetin onlar hakkında olduğunu söyler".
  - In Buhârî 4418, 4673, 4676, 4677 and 4678, Ka'b cites 9:117-119, 9:94 and 9:95-96. **He never cites 9:106.**
  - What he says is about the word «خُلِّفُوا» in **9:118**: «وَأَرْجَأَ رَسُولُ اللَّهِ ﷺ أَمْرَنَا حَتَّى قَضَى اللَّهُ فِيهِ، فَبِذَلِكَ قَالَ اللَّهُ ﴿وَعَلَى الثَّلاَثَةِ الَّذِينَ خُلِّفُوا﴾». He uses the irjâ' idea without citing 106.
  - The identification of 106 with the three comes from the tafsir scholars: İkrime (Taberî 17176), Mücâhid (17177-78, naming Hilâl, Mürâre, Ka'b), Katâde («كنا نحدث أنهم الثلاثة الذين خلفوا», 17183), and İbn Abbas via Avfî (17137).
  - Taberî himself on 9:118: «هم الآخرون الذين قال… وآخرون مرجون لأمر الله».
  - Rewrite: "müfessirler (Mücâhid, İkrime, Katâde) bu âyetin o üç kişi hakkında olduğunu söyler; Ka'b da işinin ertelendiğini anlatır."

**s8**
- **9:117** «لَقَدْ تَابَ اللَّهُ عَلَى النَّبِيِّ وَالْمُهَاجِرِينَ وَالْأَنْصَارِ الَّذِينَ اتَّبَعُوهُ فِي سَاعَةِ الْعُسْرَةِ مِنْ بَعْدِ مَا كَادَ يَزِيغُ قُلُوبُ فَرِيقٍ مِنْهُمْ ثُمَّ تَابَ عَلَيْهِمْ». **VERIFIED**. Begavî: «وكانت غزوة تبوك تسمى غزوة العسرة، والجيش يسمى جيش العسرة». The working title's derivation is VERIFIED.
- **9:118** «وَعَلَى الثَّلَاثَةِ الَّذِينَ خُلِّفُوا حَتَّىٰ إِذَا ضَاقَتْ عَلَيْهِمُ الْأَرْضُ بِمَا رَحُبَتْ وَضَاقَتْ عَلَيْهِمْ أَنْفُسُهُمْ وَظَنُّوا أَنْ لَا مَلْجَأَ مِنَ اللَّهِ إِلَّا إِلَيْهِ». The brief's paraphrase is **VERIFIED**. "Ka'b bu âyeti kendi hâlini anlatırken anar" is **VERIFIED** (Buhârî 4418): «فَبَيْنَا أَنَا جَالِسٌ عَلَى الْحَالِ الَّتِي ذَكَرَ اللَّهُ، قَدْ ضَاقَتْ عَلَىَّ نَفْسِي، وَضَاقَتْ عَلَىَّ الأَرْضُ بِمَا رَحُبَتْ».
  **NUANCE (important for the book)**: the brief says "geride bırakılan üç kişi", and Diyanet says "savaştan geri kalan üç kişi". Ka'b explicitly rejects that reading: «وَلَيْسَ الَّذِي ذَكَرَ اللَّهُ مِمَّا خُلِّفْنَا عَنِ الْغَزْوِ، إِنَّمَا هُوَ تَخْلِيفُهُ إِيَّانَا وَإِرْجَاؤُهُ أَمْرَنَا» (Buhârî 4418). Taberî: «خلفهم الله عن التوبة فأرجأهم» (İkrime, Katâde: «خلفوا عن التوبة»). Kurtubî lists both (Katâde in another report: «عن غزوة تبوك»). This is Ka'b's own words, so it is usable as speech. It fits the book's thesis better than "geride kalan".
- **9:119** «اتَّقُوا اللَّهَ وَكُونُوا مَعَ الصَّادِقِينَ». **VERIFIED**.
- Brief claim (00 and s8) that **Ka'b says 117-119 were revealed about them**: **VERIFIED**. Buhârî 4418 and 4678: «وَأَنْزَلَ اللَّهُ عَلَى رَسُولِهِ ﴿لَقَدْ تَابَ اللَّهُ عَلَى النَّبِيِّ وَالْمُهَاجِرِينَ﴾ إِلَى قَوْلِهِ ﴿وَكُونُوا مَعَ الصَّادِقِينَ﴾». Kurtubî, citing Tirmizî's version of Ka'b, adds: «وفينا أنزلت أيضا: اتقوا الله وكونوا مع الصادقين». I saw that in Kurtubî's quotation, not in Tirmizî directly. The tafsirs agree: Taberî 17433-43 (Câbir, Mücâhid, Dahhâk, Katâde name the three); İbn Kesîr; Kurtubî. **VERIFIED.**
  - Side note: Katâde's report in Taberî 17443 says Ka'b tied himself to a pillar. That contradicts Buhârî. Do not use it.
- Ka'b's last word and keeping part of his wealth: Buhârî 4676 «إِنَّ مِنْ تَوْبَتِي أَنْ أَنْخَلِعَ مِنْ مَالِي صَدَقَةً… أَمْسِكْ بَعْضَ مَالِكَ فَهْوَ خَيْرٌ لَكَ». **VERIFIED** (outside Tevbe scope).

**s9**
- **9:84** «وَلَا تُصَلِّ عَلَىٰ أَحَدٍ مِنْهُمْ مَاتَ أَبَدًا وَلَا تَقُمْ عَلَىٰ قَبْرِهِ». Diyanet: "Onlardan ölen hiçbirine asla namaz kılma ve kabrinin başında durma". **VERIFIED**. The scene (shirt, Ömer pulling his garment, the choice, «لَوْ أَعْلَمُ أَنِّي إِنْ زِدْتُ عَلَى السَّبْعِينَ يُغْفَرْ لَهُ لَزِدْتُ عَلَيْهَا», the Prophet prays, then the verse descends) is **VERIFIED** in Buhârî 4670, 4671 and 4672. Usable as speech: «إِنِّي خُيِّرْتُ فَاخْتَرْتُ» and Ömer's «فَعَجِبْتُ بَعْدُ مِنْ جُرْأَتِي».
  **UNVERIFIED** (not in these texts): the date "Zilkade 9" and "Tebük'ten iki ay kadar sonra".
- **9:80** «إِنْ تَسْتَغْفِرْ لَهُمْ سَبْعِينَ مَرَّةً فَلَنْ يَغْفِرَ اللَّهُ لَهُمْ». **VERIFIED**.
- **9:1-3** Berâe at the hajj of year 9. İbn Kesîr 9:1: «وأول هذه السورة الكريمة نزل… لما رجع من غزوة تبوك وهم بالحج… فبعث أبا بكر الصديق أميرا على الحج… فلما قفل أتبعه بعلي بن أبي طالب ليكون مبلغا». Taberî 16356 (İbn İshak) is the same. **VERIFIED.**

**s10** (items not already covered above)
- **9:44-45** «لَا يَسْتَأْذِنُكَ الَّذِينَ يُؤْمِنُونَ بِاللَّهِ…» / «إِنَّمَا يَسْتَأْذِنُكَ الَّذِينَ لَا يُؤْمِنُونَ…». **VERIFIED.**
- **9:50-52, 56-57**. Content **VERIFIED**: 50 good news grieves them; 56 «وَيَحْلِفُونَ بِاللَّهِ إِنَّهُمْ لَمِنْكُمْ»; 57 «لَوْ يَجِدُونَ مَلْجَأً أَوْ مَغَارَاتٍ أَوْ مُدَّخَلًا لَوَلَّوْا إِلَيْهِ».
  **CORRECTION (minor)**: the brief says "**Size** bir iyilik dokunsa". Verse 50 is singular, addressed to the Prophet: «إِنْ تُصِبْكَ حَسَنَةٌ تَسُؤْهُمْ», Diyanet "**Sana** bir iyilik gelirse". 52 is "Say" plus plural "us", with the "two best things" (Diyanet: şehitlik veya zafer).
- **9:53-55** spending not accepted; «فَلَا تُعْجِبْكَ أَمْوَالُهُمْ وَلَا أَوْلَادُهُمْ». **VERIFIED**. The link to the size of Ibn Übey's camp is the brief's own inference.
- **9:61-64** «وَيَقُولُونَ هُوَ أُذُنٌ» (61). 64: «يَحْذَرُ الْمُنَافِقُونَ أَنْ تُنَزَّلَ عَلَيْهِمْ سُورَةٌ تُنَبِّئُهُمْ بِمَا فِي قُلُوبِهِمْ». **VERIFIED.**
- **9:67-68, 73** **CORRECTION**: the brief says "birbirindendir; **kendilerini unutmuşlardır**". The verse says «نَسُوا اللَّهَ فَنَسِيَهُمْ», Diyanet "**Onlar Allah'ı unuttular; Allah da onları unuttu.**" "They forgot themselves" is Haşr 59:19, not Tevbe. "Birbirlerindendir" is VERIFIED. 73 «جَاهِدِ الْكُفَّارَ وَالْمُنَافِقِينَ وَاغْلُظْ عَلَيْهِمْ» is VERIFIED.
- **9:75-78** Sa'lebe. Verses: «وَمِنْهُمْ مَنْ عَاهَدَ اللَّهَ لَئِنْ آتَانَا مِنْ فَضْلِهِ…» → «فَأَعْقَبَهُمْ نِفَاقًا». The brief's general reading ("ahde vefasızlık") is **VERIFIED**.
  Trap 1 (story weak; Sa'lebe a bedrî) is **VERIFIED**:
  - İbn Kesîr gives the chain through Muân b. Rifâa, Ali b. Yezîd, el-Kâsım, Ebû Ümâme.
  - Kurtubî: «وثعلبة بدري أنصاري وممن شهد الله له ورسوله بالإيمان… فما روي عنه غير صحيح».
  - İbn Abdülber, quoted by Kurtubî: «ولعل قول من قال في ثعلبة أنه مانع الزكاة الذي نزلت فيه الآية غير صحيح».
  - Kurtubî prefers Dahhâk's view that the verses concern named hypocrites (Nebtel b. el-Hâris, Cedd b. Kays, Muattib b. Kuşeyr).
  - İbn Kesîr himself only relays the story here and does not weaken it in this passage. The weakening comes from Kurtubî and İbn Abdülber.
  - Ibn Hacer's judgement ("isnâdı çok zayıf"): **UNVERIFIED**, not seen.
- **9:83** «لَنْ تَخْرُجُوا مَعِيَ أَبَدًا». **VERIFIED.**
- **9:86-89** «رَضُوا بِأَنْ يَكُونُوا مَعَ الْخَوَالِفِ»; Diyanet: "geride kalan (kadın ve çocuk)larla". 88: «لَٰكِنِ الرَّسُولُ وَالَّذِينَ آمَنُوا مَعَهُ جَاهَدُوا». **VERIFIED.**
- **9:93** «إِنَّمَا السَّبِيلُ عَلَى الَّذِينَ يَسْتَأْذِنُونَكَ وَهُمْ أَغْنِيَاءُ». **VERIFIED.**
- **9:97-99** «الْأَعْرَابُ أَشَدُّ كُفْرًا وَنِفَاقًا» / 99: «وَيَتَّخِذُ مَا يُنْفِقُ قُرُبَاتٍ عِنْدَ اللَّهِ… سَيُدْخِلُهُمُ اللَّهُ فِي رَحْمَتِهِ». **VERIFIED.**
- **9:100** «وَالسَّابِقُونَ الْأَوَّلُونَ مِنَ الْمُهَاجِرِينَ وَالْأَنْصَارِ». **VERIFIED**. "Akabe ehline, Bedir ehline verdiği yer" is the brief's inference. Classical glosses on who the sâbikûn are differ (people who prayed toward both qiblas, people of Hudeybiye, etc.; not checked in detail). Keep it as an "ibare", not a claim.
- **9:101** «لَا تَعْلَمُهُمْ ۖ نَحْنُ نَعْلَمُهُمْ». Diyanet: "sen onları bilmezsin. Biz onları biliriz". **VERIFIED**. The Huzeyfe link: İbn Kesîr 9:101 says the Prophet told Huzeyfe the identities of 14 or 15 hypocrites, «وهذا تخصيص». **VERIFIED.**
- **9:102-103** «وَآخَرُونَ اعْتَرَفُوا بِذُنُوبِهِمْ خَلَطُوا عَمَلًا صَالِحًا وَآخَرَ سَيِّئًا عَسَى اللَّهُ أَنْ يَتُوبَ عَلَيْهِمْ» / «خُذْ مِنْ أَمْوَالِهِمْ صَدَقَةً». **VERIFIED**.
  Ebû Lübâbe and the pillars:
  - **Tebük reports**: Taberî 17136 (Ali b. Ebî Talha from İbn Abbas): «كانوا عشرة رهط تخلفوا… في غزوة تبوك… أوثق سبعة منهم أنفسهم بسواري المسجد». Taberî 17137 (Avfî from İbn Abbas): six stayed behind; Ebû Lübâbe and two others tied themselves; three did not, and those three are the 106 group.
  - **Kurayza report**: Mücâhid (17144-45) says it was about Ebû Lübâbe alone and his gesture to Kurayza.
  - **Taberî's own preference is the Tebük reading**: «وأن الذين نزل ذلك فيهم جماعة، أحدهم أبو لبابة». His reason is that the verse speaks of a group, while at Kurayza only Ebû Lübâbe tied himself.
  - 00-BRIEF's "bir rivayet Tebük'e, başkası Kurayza'ya" is **VERIFIED**. "Bir rivayete göre" is right, and the writer may add that Taberî preferred the Tebük reading.
  - The "fifth kind of one who stayed behind" framing is the brief's own and is supported by these reports.
- **9:111** «إِنَّ اللَّهَ اشْتَرَىٰ مِنَ الْمُؤْمِنِينَ أَنْفُسَهُمْ وَأَمْوَالَهُمْ بِأَنَّ لَهُمُ الْجَنَّةَ». **VERIFIED.**
- **9:120-122** 120 as above; 121 «وَلَا يُنْفِقُونَ نَفَقَةً صَغِيرَةً وَلَا كَبِيرَةً وَلَا يَقْطَعُونَ وَادِيًا إِلَّا كُتِبَ لَهُمْ»; 122 «وَمَا كَانَ الْمُؤْمِنُونَ لِيَنْفِرُوا كَافَّةً». **VERIFIED**. The brief's list "kâfiri öfkelendiren her adım" (يَطَئُونَ مَوْطِئًا يَغِيظُ الْكُفَّارَ) is VERIFIED. 120 also includes «وَلَا يَنَالُونَ مِنْ عَدُوٍّ نَيْلًا» (every gain against an enemy). The brief may omit it, but a meal of 120 should not imply that enduring hardship is the only thing recorded.
- **9:124-127** 124 «أَيُّكُمْ زَادَتْهُ هَٰذِهِ إِيمَانًا»; 127 «نَظَرَ بَعْضُهُمْ إِلَىٰ بَعْضٍ هَلْ يَرَاكُمْ مِنْ أَحَدٍ ثُمَّ انْصَرَفُوا». Diyanet: "göz ederler, sonra da sıvışıp giderler". **VERIFIED.**
- **9:128-129** see A5. **VERIFIED.**

**00-BRIEF traps**
- Trap 1 (Sa'lebe): **VERIFIED** (see 75-78).
- Trap 2 (40, cave): **VERIFIED.**
- Trap 3 (1-28 is the post-Tebük Berâe; 25-27 Huneyn not Tebük): the core is **VERIFIED** (İbn Kesîr 9:1).
  **NUANCE**: Taberî 16759, Mücâhid: «إن أول ما نزل من براءة: لقد نصركم الله في مواطن كثيرة… يعرفهم نصره، ويوطنهم لغزوة تبوك». The Huneyn verses narrate Huneyn, but in Mücâhid's view they were revealed to prepare the Muslims for Tebük. Not a reason to change the rule, but "Tebük'le ilgisi yoktur" would be too strong.
- Trap 4 (58-60, Zülhuveysıra, not Tebük): **VERIFIED**. Buhârî 6933 (Ebû Saîd): during the Prophet's distribution «عبد الله بن ذي الخويصرة التميمي فقال اعدل… فنزلت فيه ﴿ومنهم من يلمزك في الصدقات﴾».
- Trap 5 (107-110 on the return, Zû Evân): the return journey is **VERIFIED**. "Revealed at Zû Evân" needs a **CORRECTION** to "the news came at Zû Evân" (see s6).

**Other 00-BRIEF items touching Tevbe**
- "Buhârî'nin koruduğu, Medine'de kalıp her vadide orduyla beraber olan adamlar sözü" (s6): Buhârî 4423 (Enes): «إِنَّ بِالْمَدِينَةِ أَقْوَامًا مَا سِرْتُمْ مَسِيرًا وَلاَ قَطَعْتُمْ وَادِيًا إِلاَّ كَانُوا مَعَكُمْ… وَهُمْ بِالْمَدِينَةِ، حَبَسَهُمُ الْعُذْرُ». **VERIFIED**. It verbally echoes 9:121 («وَلَا يَقْطَعُونَ وَادِيًا»), a link the s10 writer can use.

---

## C. Mercy / tawba verses in sura 9 (for the new closing)

All Arabic is from the Tanzil text and all Turkish from the current Diyanet meali (acikkuran). The addressee comes from the verse context plus Taberî.

| Verse | Arabic (key) | Diyanet meali (key words) | Addressed to / about |
|---|---|---|---|
| 9:3 | فَإِنْ تُبْتُمْ فَهُوَ خَيْرٌ لَكُمْ | "Eğer tövbe ederseniz, bu sizin için hayırlıdır." | Müşrikler (bildiri, hacc-ı ekber günü bütün insanlara) |
| 9:5 | فَإِنْ تَابُوا وَأَقَامُوا الصَّلَاةَ وَآتَوُا الزَّكَاةَ فَخَلُّوا سَبِيلَهُمْ ۚ إِنَّ اللَّهَ غَفُورٌ رَحِيمٌ | "Eğer tövbe ederler… kendilerini serbest bırakın. Şüphesiz Allah çok bağışlayıcıdır, çok merhamet edicidir." | Müşrikler |
| 9:6 | فَأَجِرْهُ حَتَّىٰ يَسْمَعَ كَلَامَ اللَّهِ | "Allah'ın kelamını işitebilmesi için ona sığınma hakkı tanı." | Sığınma isteyen müşrik (the door kept open; not a tawba verse proper) |
| 9:11 | فَإِنْ تَابُوا… فَإِخْوَانُكُمْ فِي الدِّينِ | "Fakat tövbe edip… artık onlar sizin din kardeşlerinizdir." | Ahdini bozan müşrikler |
| 9:15 | وَيَتُوبُ اللَّهُ عَلَىٰ مَنْ يَشَاءُ | "Allah, dilediğinin tövbesini kabul eder." | Savaşılan müşrikler. Taberî: a new sentence, «ويمن الله على من يشاء من عباده الكافرين فيقبل به إلى التوبة» |
| 9:27 | ثُمَّ يَتُوبُ اللَّهُ مِنْ بَعْدِ ذَٰلِكَ عَلَىٰ مَنْ يَشَاءُ ۗ وَاللَّهُ غَفُورٌ رَحِيمٌ | "Sonra Allah, bunun ardından yine dilediği kimsenin tövbesini kabul eder." | Huneyn'de yenilen kâfirler (Taberî: «من الأحياء» after the defeat) |
| 9:43 | عَفَا اللَّهُ عَنْكَ | "Allah, seni affetsin!" | Hz. Peygamber |
| 9:61 | وَرَحْمَةٌ لِلَّذِينَ آمَنُوا مِنْكُمْ | "İçinizden inanan kimseler için bir rahmettir." | Peygamber, about believers (said in reply to the hypocrites) |
| 9:66 | إِنْ نَعْفُ عَنْ طَائِفَةٍ مِنْكُمْ | "İçinizden (tövbe eden) bir zümreyi affetsek bile…" | Alaycı münafıklar; the pardoned one is Mahşî b. Humayyir per İbn İshak |
| 9:71 | أُولَٰئِكَ سَيَرْحَمُهُمُ اللَّهُ | "İşte bunlara Allah merhamet edecektir." | Mümin erkek ve kadınlar |
| 9:74 | فَإِنْ يَتُوبُوا يَكُ خَيْرًا لَهُمْ | "Eğer tövbe ederlerse, kendileri için hayırlı olur." | Küfür sözü söyleyip yeltenen münafıklar; Cülâs repented (Taberî 16984-85) |
| 9:91 | مَا عَلَى الْمُحْسِنِينَ مِنْ سَبِيلٍ ۚ وَاللَّهُ غَفُورٌ رَحِيمٌ | "İyilikte bulunan kimselerin (kınanması) için de bir sebep yoktur. Allah, çok bağışlayandır, çok merhamet edendir." | Gerçek özürle kalanlar |
| 9:99 | سَيُدْخِلُهُمُ اللَّهُ فِي رَحْمَتِهِ ۗ إِنَّ اللَّهَ غَفُورٌ رَحِيمٌ | "Allah, onları rahmetine sokacaktır." | İnanan bedevîler |
| 9:102 | عَسَى اللَّهُ أَنْ يَتُوبَ عَلَيْهِمْ ۚ إِنَّ اللَّهَ غَفُورٌ رَحِيمٌ | "Umulur ki Allah tövbelerini kabul eder." | Günahını itiraf eden geride kalanlar (Ebû Lübâbe and companions). Taberî, İbn Abbas: «وعسى من الله واجب» |
| 9:103 | وَصَلِّ عَلَيْهِمْ ۖ إِنَّ صَلَاتَكَ سَكَنٌ لَهُمْ | "Onlara dua et. Çünkü senin duan onlar için sükunettir." | Same group |
| 9:104 | أَلَمْ يَعْلَمُوا أَنَّ اللَّهَ هُوَ يَقْبَلُ التَّوْبَةَ عَنْ عِبَادِهِ… وَأَنَّ اللَّهَ هُوَ التَّوَّابُ الرَّحِيمُ | "Kullarının tövbesini kabul edenin… tövbeyi çok kabul edenin, çok merhametli olanın Allah olduğunu bilmediler mi?" | General, following 102-103 |
| 9:106 | وَإِمَّا يَتُوبُ عَلَيْهِمْ | "Bunlara ya azap eder ya da tövbelerini kabul eder." | İşi ertelenenler, the three per the tafsirs |
| 9:112 | التَّائِبُونَ الْعَابِدُونَ… | "Bunlar, tövbe edenler, ibadet edenler…" | The believers of 9:111. **The first quality listed is repentance.** |
| 9:117 | لَقَدْ تَابَ اللَّهُ عَلَى النَّبِيِّ وَالْمُهَاجِرِينَ وَالْأَنْصَارِ… ثُمَّ تَابَ عَلَيْهِمْ ۚ إِنَّهُ بِهِمْ رَءُوفٌ رَحِيمٌ | "Andolsun Allah; Peygamber ile… sıkıntılı bir zamanda ona uyan muhacirlerle ensarın tövbelerini kabul etmiştir. Evet, onların tövbelerini kabul etmiştir. Şüphesiz O, onlara çok şefkatli ve çok merhametlidir." | **The ones who went**: the Prophet, muhâjirûn, ansâr |
| 9:118 | ثُمَّ تَابَ عَلَيْهِمْ لِيَتُوبُوا ۚ إِنَّ اللَّهَ هُوَ التَّوَّابُ الرَّحِيمُ | "Sonra (eski hallerine) dönsünler diye, onların tövbelerini de kabul etti. Şüphesiz Allah, tövbeyi çok kabul eden ve çok merhamet edendir." | The three |
| 9:126 | ثُمَّ لَا يَتُوبُونَ وَلَا هُمْ يَذَّكَّرُونَ | "Sonra ne tövbe ederler, ne de ibret alırlar." | Kalbinde hastalık olanlar (münafıklar). A rebuke that presumes the door is open |
| 9:128 | بِالْمُؤْمِنِينَ رَءُوفٌ رَحِيمٌ | "Mü'minlere karşı da çok şefkatli ve merhametlidir." | The Prophet's mercy (the same two attributes Allah takes in 117) |

Counter-weights the closing must not hide: 9:80 (seventy istiğfârs will not bring forgiveness), 9:84, 9:113. All VERIFIED in the text.

Textual observation (VERIFIED from the Arabic, not a tafsir claim): **9:117 ends with رَءُوفٌ رَحِيمٌ for Allah, and 9:128 gives the same pair, رَءُوفٌ رَحِيمٌ, to the Prophet.** **9:104 and 9:118 both end with التَّوَّابُ الرَّحِيمُ.**

### C1. Tafsir on 9:118 «ثُمَّ تَابَ عَلَيْهِمْ لِيَتُوبُوا»: Allah's turning comes first
- **Taberî**: «ثم رزقهم الإنابة إلى طاعته، والرجوع إلى ما يرضيه عنهم، لينيبوا إليه ويرجعوا إلى طاعته» ("then He granted them the turning back to obedience, so that they would turn back"). On التواب: «إن الله هو الوهاب لعباده الإنابة إلى طاعته، الموفق من أحب توفيقه منهم لما يرضيه عنه». **VERIFIED.**
- **Kurtubî**: «ثم تاب عليهم ليتوبوا… **فبدأ بالتوبة منه**». He then quotes Ebû Yezîd: «غلطت في أربعة أشياء… وظننت أني أتوب فإذا هو قد تاب علي؛ قال الله تعالى: ثم تاب عليهم ليتوبوا». Alternatives he records: «ليثبتوا على التوبة», and others. **VERIFIED.**
- **Begavî**: «ليتوبوا: أي ليستقيموا على التوبة، **فإن توبتهم قد سبقت**». **VERIFIED.**
- Kurtubî on 118 also cites Ebû Bekr el-Verrâk: «التوبة النصوح أن تضيق على التائب الأرض بما رحبت، وتضيق عليه نفسه؛ كتوبة كعب وصاحبيه». **VERIFIED.** This quote fits the closing well.
- Diyanet's rendering ("eski hallerine dönsünler diye") follows the "so that they return" reading.

### C2. Tafsir on 9:117: tawba for those who went
- **Taberî**: «لقد رزق الله الإنابة إلى أمره وطاعته، نبيه محمدا ﷺ، والمهاجرين… والأنصار… الذين اتبعوا رسول الله في ساعة العسرة… من بعد ما كاد يميل قلوب بعضهم عن الحق… بالذي ناله من المشقة والشدة». **VERIFIED.**
- **Kurtubî**: «واختلف العلماء في هذه التوبة… فقال ابن عباس: كانت التوبة على النبي لأجل إذنه للمنافقين في القعود، دليله قوله: عفا الله عنك لم أذنت لهم، وعلى المؤمنين من ميل قلوب بعضهم إلى التخلف عنه». Other views: rescue from the hardship; deliverance from the enemy. «وقال أهل المعاني: إنما ذكر النبي ﷺ في التوبة لأنه لما كان سبب توبتهم ذكر معهم». **VERIFIED.** This links 117 back to 43, a ready-made bridge for the closing.
- **Begavî**: «ومعنى توبته على النبي ﷺ بإذنه للمنافقين بالتخلف عنه. وقيل: افتتح الكلام به لأنه كان سبب توبتهم». **VERIFIED.**
- İbn Kesîr 9:117 gives the hardship that explains "sâatü'l-usre": Katâde (two men splitting one date), Ömer (camels slaughtered and their stomach contents squeezed for water, then the rain prayer). This supports s4's "işkembe suyu" with its source (Taberî/İbn Kesîr via İbn Abbas from Ömer). **VERIFIED.**

---

## D. Counts

- **VERIFIED**: 78 items (verse numbers plus content, sabab reports, names, basmala reports, ending, traps, Ka'b citations, tafsir quotes, and the 22 mercy verses).
- **CORRECTION**: 10 (listed below).
- **NUANCE**: 5 (43 affetti/affetsin; 118 "khullifû"; trap 3 Mücâhid; 128 vs 129 as last verse; 46-47 is fine but Ibn Übey is also listed among those who asked leave).
- **UNVERIFIED**: 7 (listed below).

### CORRECTIONS
1. s10 fixed first sentence: plural "sorduklarında" and "asıl adının başka olduğunu" are not in Buhârî 4882. Saîd b. Cübeyr asked; İbn Abbas said "et-Tevbe? O el-Fâdıha'dır".
2. 00-BRIEF: "İbn Abbas'ın ona taktığı adla": Katâde says it was commonly called that. Write "andığı".
3. s7: "Ka'b'ın kendisi (106'nın) onlar hakkında olduğunu söyler": Ka'b never cites 106. He cites 117-119 and 94-96 and explains "khullifû" of 118. The 106 identification is Mücâhid, İkrime, Katâde and İbn Abbas (Taberî).
4. s2: 9:79, Ebû Akîl's "iki sâ'ın biri" attributed to Buhârî/Ebû Mes'ûd. Buhârî 4668 has Ebû Akîl with half a sâ'; 1415 has an unnamed man with a sâ'. The two-sâ'/night-work story is from Taberî (Katâde, mursal; another chain weak).
5. s2: Ulbe b. Zeyd's sadaqa of his honour "(İbn Kesîr)". İbn Kesîr names Abdurrahman b. Yezîd Ebû Able (Benî Hârise). "Gece" is not found.
6. s10: 9:67 "kendilerini unutmuşlardır" is wrong. Correct: "Allah'ı unuttular, Allah da onları unuttu" (59:19 is "kendilerini unutturdu").
7. s10: 9:50 "Size bir iyilik dokunsa" should be "Sana" (singular, the Prophet).
8. s6 and 00 trap 5: "Zû Evân'da âyetlerin inmesi". İbn İshak says "the news of the mosque came to him" at Zû Evân; the place of revelation is not stated (Kurtubî: after arrival).
9. s6: 9:74 as the Akabe verse. This is one opinion (Kurtubî; İbn Kesîr via Beyhakî and Ahmed). Taberî gives Cülâs, Ibn Übey and others and does not mention Akabe. Present it as "bâzı müfessirlere göre".
10. s8 (soft): 9:118 "geride bırakılan üç kişi". Ka'b himself (Buhârî 4418) says "khullifû" means their case was deferred, not that they stayed behind. Taberî: «خلفوا عن التوبة».

### UNVERIFIED
1. Tebük setting of 9:79 / Ebû Akîl. Not stated in Buhârî or in Taberî, İbn Kesîr or Kurtubî on 9:79.
2. Ulbe b. Zeyd's "gece kalkıp" sadaqa of his honour (s2).
3. "Many mentions of repentance" as the reason for the name et-Tevbe. Not in Zemahşerî, Âlûsî or İbn Âşûr (they give 117-118 and the three).
4. Ibn Hacer's grading of the Sa'lebe hadith (not seen; Kurtubî and İbn Abdülber were seen).
5. Date of Ibn Übey's death (Zilkade 9 / "iki ay kadar sonra").
6. kuran.diyanet.gov.tr directly (blocked). The Diyanet text was taken from acikkuran's "Diyanet İşleri" edition.
7. Vâhidî's Arabic original (only the English translation was read). Also Ka'b's Tirmizî wording «وفينا أنزلت أيضا…», seen only as quoted by Kurtubî.
