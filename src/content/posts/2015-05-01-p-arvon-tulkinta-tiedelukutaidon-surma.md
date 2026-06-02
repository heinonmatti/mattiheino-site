---
title: "P-arvon tulkinta, tiedelukutaidon surma"
description: "P-arvon tulkinta, tiedelukutaidon surma"
published: 2015-05-01
lang: fi
vetting_status: pending
migration_source: mattiheino-wp
draft: true
tags: ['ajattelu-ja-päätöksenteko']
wp_guid: "http://blogs.helsinki.fi/hema/?p=941"
---
> Uutiset tiedeuutisten todenperäisyydestä ovat suuresti liioiteltuja (p<0,05).
>
> - Mark Twain

Modernissa maailmassa uutisointi on hankalaa: toimittajaparkojen odotetaan kilpailevan internetin valtavaa sisällöntuottajamassaa vastaan, usein päätyen klikkikalasteluun, käännösuutisiin ja/tai hätäisiin päätelmiin. Varsinkin tiedeuutisten tapauksessa ongelma on yleinen: [esimerkiksi](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0044275 "Why Most Biomedical Findings Echoed by Newspapers Turn Out to be False: The Case of Attention Deficit Hyperactivity Disorder") kymmenestä 1990-luvun suosituimmasta ADHD-tutkimusuutisesta vain kaksi on pitänyt kutinsa jatkotutkimuksessa. Tämä ei ole kuitenkaan (ainoastaan) toimittajien vika. Suurin osa tutkimustuloksista on [alun perinkin](http://blogs.helsinki.fi/mmattsso/ "Menetelmämietteitä: Miksi suurin osa julkaistuista tutkimustuloksista on virheellisiä") virheellisiä, oikeat tulokset yleensä [liioiteltuja](http://journals.lww.com/epidem/Abstract/2008/09000/Why_Most_Discovered_True_Associations_Are_Inflated.2.aspx "Why Most Discovered True Associations Are Inflated") ja medioissa raportoiduissa tutkimuksissa rikkinäinen puhelin saattaa alkaa jo [tutkineen tahon lehdistötiedotteesta](http://www.bmj.com/content/349/bmj.g7015 "The association between exaggeration in health related science news and academic press releases: retrospective observational study") (suosittelen aihepiiristä kiinnostuneita tutustumaan Naturen julkaisemaan [artikkelisarjaan](http://www.nature.com/nature/focus/reproducibility/index.html "Nature Challenges in irreproducible research")).

*[--- Disclaimer: Teksti alla on elämällesi täysin yhdentekevä, mikäli et tapaa tehdä lukea/tehdä päätelmiä tiedeuutisista ---]*

Valitettavasti lähes aina paras tapa suhtautua tiedeuutisen luotettavuuteen on mennä sen alkulähteille ja tehdä itse päätelmät tuloksista. Vieläkin valitettavammin tähän tarvitaan yleensä tilastotieteen tuntemusta. Siinä en voi laajalta kantilta auttaa, mutta voin yrittää murskata ainakin yhden valtavasti väärinkäsityksiä aiheuttavan asian käsittelyssä: p-arvon väärintulkinnassa.

## Mitä p-arvo on?

P-arvo on saadun tai sitä äärimmäisemmän tuloksen todennäköisyys, mikäli oletuksemme (jokin "nollahypoteesi", yleensä konservatiivinen oletus maailman tilasta) pitää paikkansa. Toisin sanoen, p ( T | H0 ) joka luetaan "tulos ehdolla nollahypoteesi".

Ajatellaan asia näin: Tero Tiedemies on vuosien puurtamisen jälkeen päättänyt juhlistaa tutkimuksensa hyväksymistä julkaistavaksi Havannaan suuntautuvalla lomalla. Karibian yössä hänen pöytäänsä istuu Diego de la Vegaksi esittäytyvä sujuvasanainen herrasmies, joka tarjoaa diiliä. Hän heittää kymmenesti yhden dollarin kolikkoa. Jos kolikko laskeutuu kruunapuoli ylöspäin, Tero joutuu maksamaan 10 dollaria ja jos klaavapuoli päätyy ylöspäin, "Diego" maksaa 10 dollaria. Kun kolikkoa on heitetty viidesti, Tero on 50 dollaria tappiolla ja muistaa taikurien toisinaan käyttävän tempuissaan painotettuja kolikoita. Hän siirtyykin baaritiskille tilaamaan mojitoa, saadakseen aikalisän p-arvon laskemiseen. Määritelkäämme "nollahypoteesiksi" (= jokin oletus maailman tilasta) se, että kolikko on reilu (kruunan todennäköisyys 0,5). P-arvo on todennäköisyys saada 5 kruunaa viidellä heitolla silloin, kun kolikko on reilu: 0,5\*0,5\*0,5\*0,5\*0,5 = 0,031 eli 3,1%. Tero Tiedemies muistaa koulutuksensa ja alkaa epäilemään vilunkipeliä.

Tero on suorittanut ns. Fisheriläisen hypoteesitestin, ja saanut havaitulle tulokselle tarkan todennäköisyyden, kun jokin tietty oletus on tosi. Kyseinen testi on tarkoitettu käytettäväksi silloin, kun tiedämme tutkittavasta ilmiöstä hyvin vähän, eikä sitä ole tarkoitettu hypoteesien hylkäykseen tai hyväksymiseen. Myöskään "p<0,05" tyylinen raportointi kuulu siihen mitenkään[lähde](http://educationgroup.mit.edu/HHMIEducationGroup/wp-content/uploads/2011/04/12-Gigerenzer-etal-2004.pdf "Gigerenzer, G., Krauss, S., & Vitouch, O. (2004). The null ritual. The Sage handbook of quantitative methodology for the social sciences, 391."). Testin kehittäjä Sir Ronald Fisher (1890-1962) oli muuten äärimmäisen kärkäs englantilainen tiedemies, joka muun muassa keksi varianssianalyysin, toimi Lontoon yliopiston rodunjalostusopin professorina ja vannoutuneena piippumiehenä [kielsi](http://www.google.fi/url?sa=t&rct=j&q=&esrc=s&source=web&cd=3&ved=0CDEQFjAC&url=http%3A%2F%2Fwww.the-scientist.com%2F%3Farticles.view%2FarticleNo%2F10021%2Ftitle%2FWhy-Arthur-Mourant-Decided-To-Say--No--To-Ronald-Fisher%2F&ei=1eEkVb64IoqbsgGxpYPoDA&usg=AFQjCNFzCDEGaz7knXXsfecC5qmVnLtvOQ&sig2=wlxsaflxFXqcykVxxVbM8A&bvm=bv.90237346,d.bGg "The Scientist: Why Arthur Mourant Decided To Say 'No' To Ronald Fisher") tupakoinnin olevan yhteydessä keuhkosyöpään.

Fisheriläinen hypoteesitestaus sekoitetaan järkyttävän usein (päätelmien kannalta [tuhoisin seurauksin](http://educationgroup.mit.edu/HHMIEducationGroup/wp-content/uploads/2011/04/12-Gigerenzer-etal-2004.pdf "Gigerenzer, G., Krauss, S., & Vitouch, O. (2004). The null ritual. The Sage handbook of quantitative methodology for the social sciences, 391.")) ns. Neyman-Pearson hypoteesitestaukseen, jossa asetetaan vastakkain kaksi toisensa poissulkevaa oletusta maailman tilasta. Fisher ja Neyman tunsivat toisensa 1900-luvun puolivälissä; Neyman julisti Fisherin testit hyödytöntäkin surkeammiksi, Fisherin viitatessa Neymanin testaustapaan kommunistin keksintönä ja paitsi lapsellisena, myös kammottavana uhkana länsimaiselle vapaudelle[lähde](http://educationgroup.mit.edu/HHMIEducationGroup/wp-content/uploads/2011/04/12-Gigerenzer-etal-2004.pdf "Gigerenzer, G., Krauss, S., & Vitouch, O. (2004). The null ritual. The Sage handbook of quantitative methodology for the social sciences, 391.").

Palataan mojitoa tilaavaan Teroon. Hän päättää vielä tehdä Neyman-Pearson-hypoteesitestin. Hän asettaa ensin kaksi kilpailevaa oletusta maailman tilasta: joko kolikko on reilu (kruunan todennäköisyys 50%) tai painotettu (kruunan todennäköisyys 75%). Seuraavaksi täytyy päättää hyväksyttävät erehtymistodennäköisyydet. Tero päättää, että pitkässä juoksussa on ok syyttää rehellisiä pelureita huijareiksi 5%:ssa peleistä (= "merkitsevyystaso"), ja että hän haluaa 80%:ssa peleistä hoksata huijarin kun sellainen on vastassa (= "tilastollinen voima"). Näiden tietojen pohjalta hän voi laskea, montako heittoa per peli tarvitaan päätöksen tekemiseen siitä, kumpi maailman tila (reilu vs, painotettu kolikko) ko. pelissä vallitsee. Tehdessään päätöksen hän

## **Mitä p-arvo EI ole?**

Huomaa, että yllä kuvaillussa esimerkissä p-arvo ei merkitse seuraavaa

### *Harha 1: p-arvo kertoo hypoteesin todennäköisyyden*

- Mitään hypoteesia ei ole ehdottomasti osoitettu oikeaksi tai vääräksi.

Tero tiedemies ei tiedä, onko kyseessä jokseenkin harvinainen sattuma vai vilunkipeli. Jos kolikonheittopeli olisi Havannassa yleinen ja baarissa 50 ihmistä pelaisi kukin illan aikana yhden pelin, noin kolmelle tulisi joko 5 klaavaa tai 5 kruunaa ensimmäisillä viidellä heitolla.

- Myöskään hypoteesien todennäköisyyksiä ei ole määritelty.

Nummenmaa (2009, s. 148 ja s. 153) väittää p-arvon merkitsevän "vaihtoehtoisen hypoteesin vääryyden todennäköisyyttä" tai sitä, "kuinka todennäköisesti asetettu nollahypoteesi on ollut paikkansapitävä". Esimerkissämme nollahypoteesin p(reilu kolikko) todennäköisyyden saamiseen tarvitsemme ensin oletuksen siitä, mikä on ennakkokäsityksemme tarjotun diilin reiluudesta. Sanotaan, että pienessä hiprakassakin Tero antaa vain 10%:n todennäköisyyden sille, että hänen pöytäänsä pyytämättä tuppaantuva yrittäjä on täysin rehellinen. Niin sanottu Bayesin kaava

p(reilu kolikko | 5 kruunaa) \* p(5 kruunaa) = p(5 kruunaa | reilu kolikko) \* p(reilu kolikko)

p(reilu kolikko | 5 kruunaa) = p(5 kruunaa | reilu kolikko) \* p(reilu kolikko) / [ p(5 kruunaa | reilu kolikko) + p(5 kruunaa | epäreilu kolikko) ]

Eli p(reilu kolikko | 5 kruunaa) = 0,031 \* 0,10 / (0,031\*0,1 + 1\*0,9) = 0,0034 = 0,34%. Kymmenen kertaa p-arvoa pienempi todennäköisyys!

### *harha 2: p-arvo on Hylkäämisvirheen todennäköisyys*

- Jos päätät hylätä nollahypoteesin, et tiedä, kuinka todennäköisesti teet väärän päätöksen.

Tilastotieteen oppikirjassaan Holopainen ja Pulkkinen (2013, s. 176) väittävät p-arvon merkitsevän hylkäämisvirheen todennäköisyyttä. Tällä tarkoitetaan ns. 1. tyypin virhettä, nollahypoteesin hylkäämistä silloin kun se on tosi. Mutta edelleenkään emme tiedä mitään hypoteesin todennäköisyydestä tuloksen valossa [merkitään: p(H | T)], ainoastaan tuloksen todennäköisyydestä nollahypoteesin pätiessä [merkitään: p(T | H)]. Jos kuulemme hain purreen Teron pään irti, voimme päätellä hänen kuolleen – p(kuolema | pää irti) on 1.  Toisaalta jos kuulemme hänen kuolleen, on melko todennäköistä, että se on johtunut jostain muusta kuin hain irrottamasta päästä – p(pää irti | kuolema) on hyvin pieni, koska harvat kuolemat johtuvat hain irti puremista päistä.

- Merkitsevyystaso on väärän johtopäätöksen tekeminen vain pitkässä juoksussa.

Todennäköisyys, että teet väärän johtopäätöksen hylätessäsi nollahypoteesin voidaan muotoilla myös näin: "todennäköisyys hylätä nollahypoteesi jos H0 pätee", eli "p(hylkää H0 | H0 pätee)" eli "p(p-arvo on alle merkitsevyystason)" eli yksinkertaisesti "merkitsevyystaso".

Oletetaan, että Tero on pelimiehiä; hän tykkää pelata kolikonheittopeliä mutta tietää myös liikkeellä olevan huijareita. On erittäin epäkohteliasta syytellä rehellisiä pelitovereita huijauksesta, mutta toisaalta Tero ei halua menettää rahaakaan.

Niin sanotun Neyman-Pearson -hypoteesitestauksen hengessä

Lähteitä:

Gigerenzer, G., Krauss, S., & Vitouch, O. (2004). The null ritual. *The Sage handbook of quantitative methodology for the social sciences*, 391.

Gigerenzer, G. (2004). Mindless statistics. *The Journal of Socio-Economics, 33(5)*, 587-606.

Nummenmaa, L. (2009). *Käyttäytymistieteiden tilastolliset menetelmät.* (3. painos, uud.laitos) Tammi. Keuruu.

Holopainen, M., & Pulkkinen, P. (2013). *Tilastolliset menetelmät.* (5.-8. painos) Helsinki: Sanoma Pro.

Ziliak, S. T., & McCloskey, D. N. (2008). The cult of statistical significance. *Ann Arbor: University of Michigan Press*, *27*.

Ziliak, S. T., & McCloskey, D. N. (2008). *The cult of statistical significance: How the standard error costs us jobs, justice, and lives*. University of Michigan Press.
