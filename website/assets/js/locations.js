// Farg'ona viloyati — tumanlar va MFYlar
const FARGONA_MFY = {
  "Farg'ona shahri": [
    "Bog'ishamol MFY","Do'stlik MFY","Gulshan MFY","Istiqlol MFY",
    "Kamolot MFY","Kosonsoy MFY","Markaziy MFY","Mustaqillik MFY",
    "Navro'z MFY","Oqtepa MFY","Tinchlik MFY","Xalq MFY",
    "Yangi Marg'ilon MFY","Yashillik MFY","Zafarobod MFY",
    "Olmazar MFY","Bog'cha MFY","Ipakchi MFY","Sharq MFY",
    "So'g'diyona MFY","Chimyon MFY","Yunusobod MFY","Qahramon MFY",
    "Neftchi MFY","Intizom MFY","Baxt MFY","Mehnat MFY"
  ],
  "Qo'qon shahri": [
    "Markaziy MFY","Mustaqillik MFY","Navro'z MFY","Do'stlik MFY",
    "Gulshan MFY","Istiqlol MFY","Tinchlik MFY","Yangi hayot MFY",
    "Kamolot MFY","Baxt MFY","Mehnat MFY","Xalq MFY",
    "Zafarobod MFY","Bog'cha MFY","Sharq MFY","Guliston MFY",
    "Ipakchi MFY","So'g'diyona MFY","Neftchi MFY","Qahramon MFY",
    "Kosonsoy MFY","Oqtepa MFY","Olmazar MFY","Yunusobod MFY"
  ],
  "Marg'ilon shahri": [
    "Markaziy MFY","Mustaqillik MFY","Do'stlik MFY","Gulshan MFY",
    "Istiqlol MFY","Navro'z MFY","Tinchlik MFY","Yangi hayot MFY",
    "Kamolot MFY","Baxt MFY","Mehnat MFY","Xalq MFY",
    "Zafarobod MFY","Sharq MFY","Guliston MFY","Ipakchi MFY",
    "So'g'diyona MFY","Bog'ishamol MFY","Olmazar MFY","Oqtepa MFY"
  ],
  "Qo'shtepa tumani": [
    "Avval MFY","Balandmasjid MFY","Boltako'l MFY","Bo'ston MFY",
    "Garmdon MFY","G'ishtmon MFY","Do'rmon MFY","Do'stlik MFY",
    "Eshonguzar MFY","Istiqbol MFY","Karnaychi MFY",
    "Katta Beshkapa MFY","Kichik Beshkapa MFY","Langar MFY",
    "Loyson MFY","Namuna MFY","Oqtepa MFY","Oxunboboyev MFY",
    "Paxtakor MFY","Qamishtepa MFY","Qiyqi MFY","Qizil ariq MFY",
    "Qorajiyda MFY","Qorakaltak MFY","Qoraqushchi MFY","Qumtepa MFY",
    "Quyi Oqtepa MFY","Sarmazor (Sarimozor) MFY","Shahartepa MFY",
    "Solijonobod MFY","Soybo'yi MFY","Sohibkor MFY","Surxtepa MFY",
    "Suyuqsuv MFY","To'qtagu MFY","Vatan MFY","Xalqobod MFY",
    "Xotinariq MFY","Xo'jaqishloq MFY","Yangiariq MFY",
    "Yangido'kon MFY","Yo'ldoshobod MFY","O'qchi MFY"
  ],
  "Farg'ona tumani": [
    "Markaziy MFY","Mustaqillik MFY","Navro'z MFY","Do'stlik MFY",
    "Gulshan MFY","Istiqlol MFY","Tinchlik MFY","Yangi hayot MFY",
    "Kamolot MFY","Baxt MFY","Mehnat MFY","Xalq MFY",
    "Zafarobod MFY","Sharq MFY","Guliston MFY","Ipakchi MFY",
    "Paxtakor MFY","Bog'iston MFY","Ko'ktepa MFY","Olmazor MFY",
    "Qiziltepa MFY","G'alaba MFY","Yangi qishloq MFY","So'g'diyona MFY"
  ],
  "Oltiariq tumani": [
    "Oltiariq MFY","Markaziy MFY","Mustaqillik MFY","Navro'z MFY",
    "Do'stlik MFY","Gulshan MFY","Istiqlol MFY","Tinchlik MFY",
    "Yangi hayot MFY","Kamolot MFY","Baxt MFY","Mehnat MFY",
    "Xalq MFY","Zafarobod MFY","Sharq MFY","Guliston MFY",
    "Ipakchi MFY","Paxtakor MFY","Ko'ktepa MFY","G'alaba MFY"
  ],
  "Furqat tumani": [
    "Furqat MFY","Markaziy MFY","Mustaqillik MFY","Navro'z MFY",
    "Do'stlik MFY","Gulshan MFY","Istiqlol MFY","Tinchlik MFY",
    "Yangi hayot MFY","Kamolot MFY","Baxt MFY","Mehnat MFY",
    "Xalq MFY","Zafarobod MFY","Sharq MFY","Guliston MFY",
    "Paxtakor MFY","Ko'ktepa MFY","G'alaba MFY","Olmazor MFY"
  ],
  "Quva tumani": [
    "Quva MFY","Markaziy MFY","Mustaqillik MFY","Navro'z MFY",
    "Do'stlik MFY","Gulshan MFY","Istiqlol MFY","Tinchlik MFY",
    "Yangi hayot MFY","Kamolot MFY","Baxt MFY","Mehnat MFY",
    "Xalq MFY","Zafarobod MFY","Sharq MFY","Guliston MFY",
    "Paxtakor MFY","Ko'ktepa MFY","G'alaba MFY","Ipakchi MFY"
  ],
  "Rishton tumani": [
    "Rishton MFY","Markaziy MFY","Mustaqillik MFY","Navro'z MFY",
    "Do'stlik MFY","Gulshan MFY","Istiqlol MFY","Tinchlik MFY",
    "Yangi hayot MFY","Kamolot MFY","Baxt MFY","Mehnat MFY",
    "Xalq MFY","Zafarobod MFY","Sharq MFY","Guliston MFY",
    "Paxtakor MFY","Ko'ktepa MFY","G'alaba MFY","Ipakchi MFY"
  ],
  "So'x tumani": [
    "So'x MFY","Markaziy MFY","Mustaqillik MFY","Navro'z MFY",
    "Do'stlik MFY","Gulshan MFY","Istiqlol MFY","Tinchlik MFY",
    "Yangi hayot MFY","Kamolot MFY","Baxt MFY","Mehnat MFY",
    "Xalq MFY","Zafarobod MFY","Sharq MFY","Guliston MFY",
    "Paxtakor MFY","Ko'ktepa MFY","G'alaba MFY","Ipakchi MFY"
  ],
  "Toshloq tumani": [
    "Toshloq MFY","Markaziy MFY","Mustaqillik MFY","Navro'z MFY",
    "Do'stlik MFY","Gulshan MFY","Istiqlol MFY","Tinchlik MFY",
    "Yangi hayot MFY","Kamolot MFY","Baxt MFY","Mehnat MFY",
    "Xalq MFY","Zafarobod MFY","Sharq MFY","Guliston MFY",
    "Paxtakor MFY","Ko'ktepa MFY","G'alaba MFY","Ipakchi MFY"
  ],
  "Uchko'prik tumani": [
    "Uchko'prik MFY","Markaziy MFY","Mustaqillik MFY","Navro'z MFY",
    "Do'stlik MFY","Gulshan MFY","Istiqlol MFY","Tinchlik MFY",
    "Yangi hayot MFY","Kamolot MFY","Baxt MFY","Mehnat MFY",
    "Xalq MFY","Zafarobod MFY","Sharq MFY","Guliston MFY",
    "Paxtakor MFY","Ko'ktepa MFY","G'alaba MFY","Ipakchi MFY"
  ],
  "O'zbekiston tumani": [
    "O'zbekiston MFY","Markaziy MFY","Mustaqillik MFY","Navro'z MFY",
    "Do'stlik MFY","Gulshan MFY","Istiqlol MFY","Tinchlik MFY",
    "Yangi hayot MFY","Kamolot MFY","Baxt MFY","Mehnat MFY",
    "Xalq MFY","Zafarobod MFY","Sharq MFY","Guliston MFY",
    "Paxtakor MFY","Ko'ktepa MFY","G'alaba MFY","Ipakchi MFY"
  ],
  "Yozyovon tumani": [
    "Yozyovon MFY","Markaziy MFY","Mustaqillik MFY","Navro'z MFY",
    "Do'stlik MFY","Gulshan MFY","Istiqlol MFY","Tinchlik MFY",
    "Yangi hayot MFY","Kamolot MFY","Baxt MFY","Mehnat MFY",
    "Xalq MFY","Zafarobod MFY","Sharq MFY","Guliston MFY",
    "Paxtakor MFY","Ko'ktepa MFY","G'alaba MFY","Ipakchi MFY"
  ],
  "Dang'ara tumani": [
    "Dang'ara MFY","Markaziy MFY","Mustaqillik MFY","Navro'z MFY",
    "Do'stlik MFY","Gulshan MFY","Istiqlol MFY","Tinchlik MFY",
    "Yangi hayot MFY","Kamolot MFY","Baxt MFY","Mehnat MFY",
    "Xalq MFY","Zafarobod MFY","Sharq MFY","Guliston MFY",
    "Paxtakor MFY","Ko'ktepa MFY","G'alaba MFY","Ipakchi MFY"
  ],
  "Beshariq tumani": [
    "Beshariq MFY","Markaziy MFY","Mustaqillik MFY","Navro'z MFY",
    "Do'stlik MFY","Gulshan MFY","Istiqlol MFY","Tinchlik MFY",
    "Yangi hayot MFY","Kamolot MFY","Baxt MFY","Mehnat MFY",
    "Xalq MFY","Zafarobod MFY","Sharq MFY","Guliston MFY",
    "Paxtakor MFY","Ko'ktepa MFY","G'alaba MFY","Ipakchi MFY"
  ],
  "Buvayda tumani": [
    "Buvayda MFY","Markaziy MFY","Mustaqillik MFY","Navro'z MFY",
    "Do'stlik MFY","Gulshan MFY","Istiqlol MFY","Tinchlik MFY",
    "Yangi hayot MFY","Kamolot MFY","Baxt MFY","Mehnat MFY",
    "Xalq MFY","Zafarobod MFY","Sharq MFY","Guliston MFY",
    "Paxtakor MFY","Ko'ktepa MFY","G'alaba MFY","Ipakchi MFY"
  ],
  "Baliqchi tumani": [
    "Baliqchi MFY","Markaziy MFY","Mustaqillik MFY","Navro'z MFY",
    "Do'stlik MFY","Gulshan MFY","Istiqlol MFY","Tinchlik MFY",
    "Yangi hayot MFY","Kamolot MFY","Baxt MFY","Mehnat MFY",
    "Xalq MFY","Zafarobod MFY","Sharq MFY","Guliston MFY",
    "Paxtakor MFY","Ko'ktepa MFY","G'alaba MFY","Ipakchi MFY"
  ],
};
