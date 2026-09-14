from django.db import migrations


MACRO_TYPES = [
    ("MT-NAD", "Nadgrobnik",
     "Individualna ili neposredna grobna oznaka vezana za jedan ili više ukopa.", 10),
    ("MT-GRO", "Grobnica / funerarna arhitektura",
     "Arhitektonska ili prostorna cjelina namijenjena ukopu ili čuvanju posmrtnih ostataka.", 20),
    ("MT-MEM", "Memorijal bez ukopa",
     "Spomen-objekat bez ukopa; vodi se odvojeno od Grave zapisa.", 30),
    ("MT-NEU", "Neutvrđeno",
     "Priroda objekta se ne može pouzdano odrediti.", 90),
]


TRADITIONS = [
    ("ISL", "Islamska", 10),
    ("STE", "Stećci / srednjovjekovna", 20),
    ("PRA", "Pravoslavna", 30),
    ("KAT", "Katolička", 40),
    ("JEV-SEF", "Jevrejska – sefardska", 50),
    ("JEV-ASK", "Jevrejska – aškenaska", 60),
    ("ANT", "Antička / rimska", 70),
    ("MIX", "Različita", 80),
    ("ISL-KON", "Islamski kontekst", 85),
    ("NEU", "Neutvrđena", 90),
    ("DRU", "Druga / neutvrđena", 100),
]


# code, name, level, parent, description, sort_order
MONUMENT_TYPES = [
    # ISLAMSKA TRADICIJA
    ("ISL-NIS-OSN", "Nišan", "physical", None,
     "Osnovni široki tip.", 100),

    ("ISL-STU", "Jednostavna uspravna stela / stup", "physical", None,
     'Bez subjektivne oznake "arhaični"; datacija se vodi zasebno.', 110),

    ("ISL-TUR", "Nišan sa turbanom", "morphological", "ISL-NIS-OSN",
     "Vidljiva forma; ne određuje sama status pokojnika.", 120),

    ("ISL-TUR-MUS", "Mušebek turban", "detailed", "ISL-TUR",
     "Stručni sloj.", 121),

    ("ISL-TUR-AGI", "Aginski turban", "detailed", "ISL-TUR",
     "Stručni sloj; status osobe potvrđivati izvorom.", 122),

    ("ISL-TUR-ULE", "Ulemanski tip turbana", "detailed", "ISL-TUR",
     "Stručni sloj; ne zaključivati zanimanje samo iz forme.", 123),

    ("ISL-TUR-GUZ", 'Turban "u gužve"', "detailed", "ISL-TUR",
     "Stručni morfološki podtip.", 124),

    ("ISL-KAP", "Nišan sa kapom / fesom", "morphological", "ISL-NIS-OSN",
     "Dalje razdvojiti samo kada je forma sigurna.", 130),

    ("ISL-KAP-DER", "Derviška / tekijska kapa", "detailed", "ISL-KAP",
     "Stručni sloj; terminološke varijante mogu se dopunjavati.", 131),

    ("ISL-NIS-PLO", "Plosnati nišan / stela", "morphological", "ISL-NIS-OSN",
     "Bašluk nije morfološki tip; pozicija se vodi zasebno.", 140),

    ("ISL-NIS-SEH", "Savremeni tipski šehidski nišan", "morphological", "ISL-NIS-OSN",
     "Standardizovana savremena forma; tehnički primarni izvor ostaje bibliografski zadatak.", 150),

    # STEĆCI
    ("STE-PLO", "Ploča", "physical", None,
     "Niska horizontalna forma; ne koristiti za visoku uspravnu stelu.", 200),

    ("STE-SAN", "Sanduk", "physical", None,
     "UNESCO osnovni oblik.", 210),

    ("STE-SLJ", "Sljemenjak", "physical", None,
     "UNESCO osnovni oblik.", 220),

    ("STE-STU", "Stub / stup", "physical", None,
     "Stub bez dominantno isklesanog krsta; ako krst dominira koristiti STE-KRS.", 230),

    ("STE-KRS", "Monumentalni križ / krst", "physical", None,
     "UNESCO osnovni oblik.", 240),

    ("STE-STE", "Uspravna stela", "local", None,
     "Stručni/lokalni sloj uz mapiranje na širu tipologiju.", 250),

    # PRAVOSLAVNA
    ("PRA-KRS", "Krstača", "physical", None,
     "Stari kameni nadgrobnik; regionalne varijante zasebno.", 300),

    ("PRA-ANT", "Antropomorfna krstača / stela", "local", "PRA-KRS",
     "Regionalni stručni podtip; ne generalizovati bez izvora.", 310),

    ("PRA-STE", "Stela / uspravna ploča", "physical", None,
     "Pravougaona ili blago zaobljena uspravna ploča; ne uključuje krstaču.", 320),

    # KATOLIČKA
    ("KAT-KRI", "Križ", "physical", None,
     "Osnovni široki tip.", 400),

    ("KAT-STE", "Stela / uspravna ploča", "physical", None,
     "Ne uključuje samostojeći križ.", 410),

    ("KAT-PLO", "Položena ploča", "physical", None,
     "Ne poistovjećivati automatski sa stećkom.", 420),

    ("KAT-STU", "Stup / prizma", "physical", None,
     "Regionalna forma; stručni sloj.", 430),

    ("KAT-TUM", "Tumba / sanduk-sarkofagna forma", "physical", None,
     "Historijski termin; kod konkretnog zapisa makro-tip zavisi od stvarne konstrukcije/funkcije.", 440),

    # JEVREJSKA – SEFARDSKA
    ("JEV-SEF-PLO", "Horizontalna monolitna ploča", "physical", None,
     "Dokumentovana sarajevska forma.", 500),

    ("JEV-SEF-SAN", "Sanduk", "physical", None,
     "Dokumentovana sarajevska forma.", 510),

    ("JEV-SEF-SAR", "Sarkofagna forma", "physical", None,
     "Može imati detaljne varijante.", 520),

    ("JEV-SEF-SLJ", "Sljemenasta sarkofagna forma", "detailed", "JEV-SEF-SAR",
     "Stručni sloj.", 521),

    # JEVREJSKA – AŠKENASKA
    ("JEV-ASK-STE", "Vertikalna stela / ploča", "physical", None,
     "Osnovna aškenaska uspravna forma.", 550),

    ("JEV-ASK-OBE", "Obelisk", "physical", None,
     "Visok četverostrani spomenik koji se sužava prema vrhu.", 560),

    # ANTIČKA / RIMSKA
    ("ANT-STE", "Stela", "physical", None,
     "Stručni sloj.", 600),

    ("ANT-ARA", "Ara ossuaria", "physical", None,
     "Stručni sloj.", 610),

    ("ANT-CIP", "Cipus", "physical", None,
     "Stručni sloj.", 620),

    ("ANT-URN", "Urna", "physical", None,
     "Sepulkralna kategorija; kontekst obavezan.", 630),

    ("ANT-SAR", "Sarkofag", "physical", None,
     "Religijski kontekst se vodi zasebno.", 640),

    ("ANT-MAU", "Mauzolej", "physical", None,
     "Funerarna arhitektura.", 650),

    ("ANT-TIT", "Titulus", "expert", None,
     "Ne tretirati automatski kao nadgrobnik; funkcija mora biti potvrđena kontekstom.", 660),

    # FUNERARNA ARHITEKTURA
    ("FUN-GRO", "Grobnica", "physical", None,
     "Nadzemna ili ukopana zidana grobna komora za jednu ili više osoba.", 700),

    ("FUN-KOL", "Kolektivna / masovna grobnica", "functional", "FUN-GRO",
     "Za osjetljive/forenzičke slučajeve koristiti samo uz pouzdan izvor.", 710),

    ("FUN-KOS", "Kosturnica", "functional", "FUN-GRO",
     "Tehnički prostor za sekundarno čuvanje kostiju.", 720),

    ("FUN-SKO", "Spomen-kosturnica", "functional", "FUN-GRO",
     "Kosturnica sa izraženom memorijalnom/arhitektonskom komponentom.", 730),

    ("FUN-MAU", "Mauzolej", "physical", None,
     "Opći funerarniji arhitektonski tip.", 740),

    ("FUN-TUR", "Turbe", "physical", None,
     "Funerarni/sakralni objekat nad grobom ili grobovima.", 750),

    # MEMORIJAL
    ("MEM-OBI", "Spomen-obilježje / memorijal", "physical", None,
     "Bez ukopa; preporučen poseban model, ne Grave.", 800),

    # REZERVNI
    ("NEU", "Neutvrđeno", "reserve", None,
     "Tačnost ima prednost nad pogađanjem.", 900),

    ("DRU", "Drugo", "reserve", None,
     "Obavezan slobodni opis; omogućava nove lokalne forme.", 910),
]


# code, category, name, description, sort_order
MOTIFS = [
    ("MOT-GEO-CZC", "Geometrijski", "Cik-cak linija / zupčasti friz",
     "Opisni motiv; primjenu vezati za fotografiju/lokalitet.", 10),

    ("MOT-GEO-TVR", "Geometrijski", "Tordirana vrpca / uže",
     "Rubni/prstenasti ornament.", 20),

    ("MOT-GEO-ROZ", "Geometrijski / astralni", "Rozeta",
     "Ne zaključivati značenje bez stručnog izvora.", 30),

    ("MOT-AST-SUN", "Astralni", "Sunce / solarni disk",
     "Opisni motiv; simboličko tumačenje zasebno.", 40),

    ("MOT-AST-POL", "Astralni", "Polumjesec",
     "Sa ili bez zvijezde; evidentirati ono što je vidljivo.", 50),

    ("MOT-HER-STI", "Heraldički / predmetni", "Štit",
     "Ne zaključivati automatski vojni status pokojnika.", 60),

    ("MOT-ORU-MAC", "Oružje / predmetni", "Mač / sablja / handžar",
     "Opisni motiv; interpretacija zasebno.", 70),

    ("MOT-ORU-BUZ", "Oružje / predmetni", "Buzdovan / topuz",
     "Opisni motiv.", 80),

    ("MOT-ORU-LUK", "Oružje / predmetni", "Luk i strijela",
     "Opisni motiv.", 90),

    ("MOT-ORU-SJE", "Oružje / predmetni", "Sjekira",
     "Opisni motiv.", 100),

    ("MOT-PRO-DIV", "Profesionalni / predmetni", "Divit / pernica",
     "Stručna interpretacija zanimanja mora imati izvor.", 110),

    ("MOT-PRO-KNJ", "Profesionalni / predmetni", "Knjiga / levha",
     "Evidentirati fizički motiv; značenje zasebno.", 120),

    ("MOT-ARH-MIH", "Arhitektonski", "Stilizirani mihrab",
     "Opisna arhitektonska forma.", 130),

    ("MOT-BIL-LOZ", "Biljni", "Lozica / vitica",
     "Biljni ornament.", 140),

    ("MOT-BIL-TRO", "Biljni", "Trolist",
     "Biljni ornament.", 150),

    ("MOT-ARH-ARK", "Arhitektonski", "Arkada",
     "Arhitektonski ornament.", 160),

    ("MOT-FIG-LJU", "Figuralni", "Ljudska figura",
     "Bez automatske identifikacije osobe.", 170),

    ("MOT-FIG-KOL", "Figuralni", "Kolo",
     "Scena/figuralni motiv.", 180),

    ("MOT-FIG-LOV", "Figuralni", "Lov",
     "Scena/figuralni motiv.", 190),

    ("MOT-SIM-SST", "Simbolički / arhitektonski", "Slomljeni stup",
     'Značenje "prekinut život" navoditi samo uz izvor.', 200),

    ("MOT-DRU", "Drugo", "Drugi motiv",
     "Obavezan opis.", 210),

    ("MOT-NEU", "Neutvrđeno", "Neutvrđeni motiv",
     "Koristiti kada motiv nije moguće pouzdano prepoznati.", 220),
]


def seed_standard(apps, schema_editor):
    MonumentMacroType = apps.get_model("graves", "MonumentMacroType")
    MonumentTradition = apps.get_model("graves", "MonumentTradition")
    MonumentType = apps.get_model("graves", "MonumentType")
    Motif = apps.get_model("graves", "Motif")

    # Makro-tipovi
    for code, name, description, sort_order in MACRO_TYPES:
        MonumentMacroType.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "description": description,
                "is_active": True,
                "sort_order": sort_order,
            },
        )

    # Tradicije / konteksti
    for code, name, sort_order in TRADITIONS:
        MonumentTradition.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "description": "",
                "is_active": True,
                "sort_order": sort_order,
            },
        )

    # Prvo svi tipovi bez parent veze.
    for code, name, level, parent_code, description, sort_order in MONUMENT_TYPES:
        MonumentType.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "level": level,
                "description": description,
                "identification_notes": "",
                "is_active": True,
                "sort_order": sort_order,
                "parent": None,
            },
        )

    # Zatim hijerarhijske parent veze.
    for code, name, level, parent_code, description, sort_order in MONUMENT_TYPES:
        if parent_code:
            item = MonumentType.objects.get(code=code)
            item.parent = MonumentType.objects.get(code=parent_code)
            item.save(update_fields=["parent"])

    # Ornamentika / simboli
    for code, category, name, description, sort_order in MOTIFS:
        Motif.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "category": category,
                "description": description,
                "is_active": True,
                "sort_order": sort_order,
            },
        )


def reverse_seed(apps, schema_editor):
    """
    Namjerno ne brišemo V1.0 zapise.

    Kada šifrarnik počne koristiti Grave ili drugi korisnički podaci,
    automatsko brisanje prilikom rollbacka moglo bi uništiti ili
    prekinuti postojeće klasifikacije.
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("graves", "0021_alter_monumenttype_level"),
    ]

    operations = [
        migrations.RunPython(
            seed_standard,
            reverse_code=reverse_seed,
        ),
    ]