from django.db import migrations


CONDITIONS = [
    (
        "CON-GOOD",
        "Dobro očuvano",
        "Dobro",
        "Spomenik je u cjelini dobro očuvan, bez značajnih vidljivih oštećenja.",
        10,
    ),
    (
        "CON-DAM",
        "Vidljivo oštećeno",
        "Oštećeno",
        "Prisutna su vidljiva oštećenja ili degradacija, ali je spomenik i dalje prepoznatljiv i u značajnoj mjeri očuvan.",
        20,
    ),
    (
        "CON-SEV",
        "Teško oštećeno",
        "Teško oštećeno",
        "Spomenik ima velika oštećenja ili gubitke koji značajno utiču na njegovu cjelovitost ili čitljivost.",
        30,
    ),
    (
        "CON-FRA",
        "Fragmentarno očuvano",
        "Teško oštećeno",
        "Sačuvan je samo dio ili više fragmenata spomenika.",
        40,
    ),
    (
        "CON-NEU",
        "Neutvrđeno",
        "Ne mogu procijeniti",
        "Stanje nije moguće pouzdano procijeniti na osnovu raspoloživih podataka.",
        90,
    ),
]


# code, name, group, admin_label, public_label, description, sort_order
PATTERNS = [
    # --------------------------------------------------------
    # PUKOTINE I DEFORMACIJE
    # --------------------------------------------------------
    (
        "CRK-CRA",
        "Pukotina",
        "crack",
        "Pukotina",
        "Pukotina",
        "Vidljivo razdvajanje materijala u obliku pukotine.",
        100,
    ),
    (
        "CRK-DEF",
        "Deformacija",
        "crack",
        "Deformacija",
        "Drugo",
        "Vidljiva promjena izvornog oblika bez nužnog gubitka materijala.",
        110,
    ),

    # --------------------------------------------------------
    # ODVAJANJE MATERIJALA
    # --------------------------------------------------------
    (
        "DET-BLI",
        "Mjehurasto odvajanje / blistering",
        "detachment",
        "Površinsko odvajanje / ljuštenje",
        "Površina je oštećena / istrošena",
        "Lokalno izdizanje površinskog sloja u obliku mjehura.",
        200,
    ),
    (
        "DET-BUR",
        "Odlomljavanje / bursting",
        "detachment",
        "Površinsko odvajanje / odlomljavanje",
        "Površina je oštećena / istrošena",
        "Lokalno odvajanje i izbacivanje dijela materijala.",
        210,
    ),
    (
        "DET-DEL",
        "Raslojavanje / delamination",
        "detachment",
        "Površinsko odvajanje / raslojavanje",
        "Površina je oštećena / istrošena",
        "Odvajanje materijala u slojevima.",
        220,
    ),
    (
        "DET-EXF",
        "Eksfolijacija",
        "detachment",
        "Površinsko odvajanje / ljuštenje",
        "Površina je oštećena / istrošena",
        "Odvajanje slojeva približno paralelnih površini kamena.",
        230,
    ),
    (
        "DET-FRA",
        "Fragmentacija",
        "detachment",
        "Fragmentacija",
        "Nedostaje dio",
        "Raspadanje ili razdvajanje spomenika na fragmente.",
        240,
    ),
    (
        "DET-PEE",
        "Ljuštenje / peeling",
        "detachment",
        "Površinsko odvajanje / ljuštenje",
        "Površina je oštećena / istrošena",
        "Odvajanje tankog površinskog sloja.",
        250,
    ),
    (
        "DET-SCA",
        "Ljuspanje / scaling",
        "detachment",
        "Površinsko odvajanje / ljuspanje",
        "Površina je oštećena / istrošena",
        "Odvajanje površinskog materijala u obliku ljuski.",
        260,
    ),

    # --------------------------------------------------------
    # GUBITAK MATERIJALA
    # --------------------------------------------------------
    (
        "LOS-ALV",
        "Alveolizacija",
        "loss",
        "Erozija / istrošena površina",
        "Površina je oštećena / istrošena",
        "Formiranje šupljina ili udubljenja na površini kamena.",
        300,
    ),
    (
        "LOS-ERO",
        "Erozija",
        "loss",
        "Erozija / istrošena površina",
        "Površina je oštećena / istrošena",
        "Postepeni gubitak materijala sa površine spomenika.",
        310,
    ),
    (
        "LOS-DER",
        "Diferencijalna erozija",
        "loss",
        "Erozija / istrošena površina",
        "Površina je oštećena / istrošena",
        "Neujednačena erozija različitih dijelova ili zona materijala.",
        320,
    ),
    (
        "LOS-MEC",
        "Mehaničko oštećenje",
        "loss",
        "Mehaničko oštećenje",
        "Drugo",
        "Vidljivo oštećenje povezano sa fizičkim djelovanjem; uzrok se ne pretpostavlja ako nije poznat.",
        330,
    ),
    (
        "LOS-MIS",
        "Nedostajući dio",
        "loss",
        "Nedostajući dio",
        "Nedostaje dio",
        "Vidljiv gubitak dijela spomenika.",
        340,
    ),
    (
        "LOS-ROU",
        "Zaobljavanje / rounding",
        "loss",
        "Erozija / istrošena površina",
        "Površina je oštećena / istrošena",
        "Zaobljavanje rubova ili profilisanih dijelova usljed gubitka materijala.",
        350,
    ),
    (
        "LOS-RGH",
        "Povećana hrapavost / roughening",
        "loss",
        "Erozija / istrošena površina",
        "Površina je oštećena / istrošena",
        "Povećanje hrapavosti površine povezano sa gubitkom materijala.",
        360,
    ),

    # --------------------------------------------------------
    # PROMJENE BOJE I NASLAGE
    # --------------------------------------------------------
    (
        "DIS-CRU",
        "Kora / crust",
        "discoloration",
        "Naslage / promjena površine",
        "Drugo",
        "Kompaktniji površinski sloj ili kora različita od osnovnog materijala.",
        400,
    ),
    (
        "DIS-DEP",
        "Naslaga / deposit",
        "discoloration",
        "Naslage / promjena boje",
        "Drugo",
        "Nakupljeni materijal na površini spomenika.",
        410,
    ),
    (
        "DIS-COL",
        "Promjena boje",
        "discoloration",
        "Promjena boje",
        "Drugo",
        "Vidljiva promjena boje površine.",
        420,
    ),
    (
        "DIS-EFF",
        "Eflorescencija",
        "discoloration",
        "Naslage / eflorescencija",
        "Drugo",
        "Kristalne naslage, najčešće svijetle boje, na površini materijala.",
        430,
    ),
    (
        "DIS-ENC",
        "Inkrustacija / encrustation",
        "discoloration",
        "Naslage / inkrustacija",
        "Drugo",
        "Čvršća naslaga vezana za površinu spomenika.",
        440,
    ),
    (
        "DIS-SOI",
        "Zaprljanje / soiling",
        "discoloration",
        "Zaprljanje / površinska naslaga",
        "Drugo",
        "Površinsko nakupljanje prljavštine koje mijenja izgled spomenika.",
        450,
    ),
    (
        "DIS-GRA",
        "Grafit",
        "discoloration",
        "Grafit / naknadno ispisivanje",
        "Drugo",
        "Naknadno nanesen crtež, natpis ili oznaka na površini spomenika.",
        460,
    ),

    # --------------------------------------------------------
    # BIOLOŠKA KOLONIZACIJA
    # --------------------------------------------------------
    (
        "BIO-ALG",
        "Alge",
        "biological",
        "Biološka obraslost",
        "Obrastao / lišajevi / mahovina",
        "Vidljiva kolonizacija površine algama.",
        500,
    ),
    (
        "BIO-LIC",
        "Lišajevi",
        "biological",
        "Lišajevi / biološka obraslost",
        "Obrastao / lišajevi / mahovina",
        "Vidljiva kolonizacija površine lišajevima.",
        510,
    ),
    (
        "BIO-MOS",
        "Mahovina",
        "biological",
        "Mahovina / biološka obraslost",
        "Obrastao / lišajevi / mahovina",
        "Vidljiva kolonizacija površine mahovinom.",
        520,
    ),
    (
        "BIO-MOU",
        "Plijesan",
        "biological",
        "Plijesan / biološka obraslost",
        "Obrastao / lišajevi / mahovina",
        "Vidljiva kolonizacija površine plijesni.",
        530,
    ),
    (
        "BIO-PLT",
        "Biljke / vegetacija",
        "biological",
        "Vegetacija",
        "Obrastao / lišajevi / mahovina",
        "Prisustvo viših biljaka na spomeniku ili neposredno u njegovoj strukturi.",
        540,
    ),
]


POSITIONS = [
    (
        "POS-UPR",
        "U očekivanom položaju",
        "",
        "Spomenik je u položaju koji na osnovu raspoloživih podataka djeluje očekivano.",
        10,
    ),
    (
        "POS-NAG",
        "Nagnut",
        "Nagnut",
        "Spomenik je vidljivo nagnut.",
        20,
    ),
    (
        "POS-PRE",
        "Prevrnut",
        "Prevrnut",
        "Spomenik leži ili je prevrnut u odnosu na očekivani položaj.",
        30,
    ),
    (
        "POS-UTO",
        "Djelimično utonuo",
        "Djelimično utonuo",
        "Dio spomenika je vidljivo utonuo ili zatrpan.",
        40,
    ),
    (
        "POS-POM",
        "Pomjeren / dislociran",
        "Pomjeren",
        "Postoje pouzdani podaci da spomenik nije na svom ranijem ili izvornom položaju.",
        50,
    ),
    (
        "POS-NEU",
        "Neutvrđeno",
        "Ne mogu procijeniti",
        "Položaj nije moguće pouzdano odrediti.",
        90,
    ),
]


def seed_condition_standard(apps, schema_editor):
    MonumentCondition = apps.get_model("graves", "MonumentCondition")
    DeteriorationPattern = apps.get_model("graves", "DeteriorationPattern")
    MonumentPosition = apps.get_model("graves", "MonumentPosition")

    for code, name, public_label, description, sort_order in CONDITIONS:
        MonumentCondition.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "public_label": public_label,
                "description": description,
                "is_active": True,
                "sort_order": sort_order,
            },
        )

    for (
        code,
        name,
        group,
        admin_label,
        public_label,
        description,
        sort_order,
    ) in PATTERNS:
        DeteriorationPattern.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "group": group,
                "admin_label": admin_label,
                "public_label": public_label,
                "description": description,
                "is_active": True,
                "sort_order": sort_order,
            },
        )

    for code, name, public_label, description, sort_order in POSITIONS:
        MonumentPosition.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "public_label": public_label,
                "description": description,
                "is_active": True,
                "sort_order": sort_order,
            },
        )


def reverse_condition_standard(apps, schema_editor):
    """
    Namjerno ne brišemo šifrarnik pri rollbacku.

    Kada Grave zapisi počnu koristiti ove kodove, automatsko
    brisanje standardnih vrijednosti moglo bi oštetiti veze
    prema postojećim kataloškim podacima.
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        (
            "graves",
            "0024_grave_condition_classification_grave_condition_notes_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(
            seed_condition_standard,
            reverse_code=reverse_condition_standard,
        ),
    ]