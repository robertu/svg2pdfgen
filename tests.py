import os
import shutil

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from svg2pdf.models import context_to_pdf, faktura_context_calc  # noqa

FOLDER_NA_FAKTURY_TESTOWE = "faktury_testowe"


class Jednostka:
    def __init__(self, nazwa, dziesietna):
        self.nazwa = nazwa
        self.dziesietna = dziesietna


class Pozycja:
    def __init__(self, nazwa, cenaN, ilosc=1, podatek=23, jednostka=Jednostka("SZT", False)):
        self.nazwa = nazwa
        self.jednostka = jednostka
        self.cena_Netto = cenaN
        self.ilosc = ilosc
        self.podatek = podatek


def basic_con():
    context = {
        "FVATNAME": "test",
        "NAB": "test",
        "NABA": "test",
        "NABK": "test",
        "NABNIP": "123 456 78 90",
        "VATNAME": "test",
        "DATASP": "01-01-0001",
        "DATAWYS": "01-01-0001",
        "TERPLAT": "01-01-0001",
        "POZYCJE": [Pozycja("Poz 1", 10, 10)],
        "ZAPLACONO": 2,
        "DAYS": "2",
        "STRGL": True,
        "STRKON": False,
    }
    return context


try:
    shutil.rmtree(FOLDER_NA_FAKTURY_TESTOWE)
except Exception:
    pass


# tests
def test_podstawowy():
    context = basic_con()
    context, pozycje_c, tabelarys = faktura_context_calc(context)
    context_to_pdf(context, pozycje_c, tabelarys, "test_podstawowy", FOLDER_NA_FAKTURY_TESTOWE)
    assert os.path.exists(f"{FOLDER_NA_FAKTURY_TESTOWE}/fak-test_podstawowy.pdf")


def test_pozycje():
    context = basic_con()
    TEMP = []
    for x in range(100):
        TEMP += [Pozycja(f"poz {x}", x)]
    context.update({"POZYCJE": TEMP})
    context, pozycje_c, tabelarys = faktura_context_calc(context)
    context_to_pdf(context, pozycje_c, tabelarys, "test_pozycje", FOLDER_NA_FAKTURY_TESTOWE)
    assert os.path.exists(f"{FOLDER_NA_FAKTURY_TESTOWE}/fak-test_pozycje.pdf")


def test_nazwa_wrap():
    context = basic_con()
    TEMP = []
    TEMPN = ""
    for x in range(100):
        TEMPN = "poz" + str(x) + " a" * 4 * x
        TEMP += [Pozycja(TEMPN, x)]
    context.update({"POZYCJE": TEMP})
    context, pozycje_c, tabelarys = faktura_context_calc(context)
    context_to_pdf(context, pozycje_c, tabelarys, "test_nazwa_wrap", FOLDER_NA_FAKTURY_TESTOWE)
    assert os.path.exists(f"{FOLDER_NA_FAKTURY_TESTOWE}/fak-test_nazwa_wrap.pdf")


def test_podatki_pozycje():
    context = basic_con()
    TEMP = []
    for x in range(100):
        TEMP += [Pozycja(f"poz {x}", x, 1, 23)]
        TEMP += [Pozycja(f"poz {x}", x, 2, 8)]
        TEMP += [Pozycja(f"poz {x}", x, 3, 0)]
    context.update({"POZYCJE": TEMP})
    context, pozycje_c, tabelarys = faktura_context_calc(context)
    context_to_pdf(context, pozycje_c, tabelarys, "test_podatki_pozycje", FOLDER_NA_FAKTURY_TESTOWE)
    assert os.path.exists(f"{FOLDER_NA_FAKTURY_TESTOWE}/fak-test_podatki_pozycje.pdf")


def test_vat():
    context = basic_con()
    TEMP = []
    for x in range(10):
        TEMP += [Pozycja(f"poz {x}", x, 1, x)]
    context.update({"POZYCJE": TEMP})
    context, pozycje_c, tabelarys = faktura_context_calc(context)
    context_to_pdf(context, pozycje_c, tabelarys, "test_vat", FOLDER_NA_FAKTURY_TESTOWE)
    assert os.path.exists(f"{FOLDER_NA_FAKTURY_TESTOWE}/fak-test_vat.pdf")


def test_jednostki():
    context = basic_con()
    TEMP = []
    jednostki = [Jednostka("SZT", False), Jednostka("KG", True)]
    for x in range(10):
        TEMP += [Pozycja(f"poz {x}", x, float(f"{x}.{x}"), 23, jednostki[0])]
        TEMP += [Pozycja(f"poz {x}", x, float(f"{x}.{x}"), 23, jednostki[1])]
    context.update({"POZYCJE": TEMP})
    context, pozycje_c, tabelarys = faktura_context_calc(context)
    context_to_pdf(context, pozycje_c, tabelarys, "test_jednostki", FOLDER_NA_FAKTURY_TESTOWE)
    assert os.path.exists(f"{FOLDER_NA_FAKTURY_TESTOWE}/fak-test_jednostki.pdf")
