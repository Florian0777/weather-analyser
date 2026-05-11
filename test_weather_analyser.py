"""Pytest-Tests für ``weather_analyser`` mit 100 % Statement-Coverage.

Aufruf:
    pytest test_weather_analyser.py --cov=weather_analyser --cov-report=term-missing
"""

import runpy
from pathlib import Path

import pytest

import weather_analyser as wa


MODULE_PATH = Path(wa.__file__)

CSV_HEADER = 'datum;temperatur;windgeschwindigkeit;schneehoehe\n'

CSV_INHALT = (
    CSV_HEADER
    + '2024-01-15;-8.2;34;120\n'
    + '2024-01-16;-3.1;18;118\n'
    + '2024-01-17;-12.5;52;125\n'
    + '2024-01-18;-1.8;11;119\n'
    + '2024-01-19;-6.4;29;122\n'
    + '2024-01-20;-15.3;61;130\n'
    + '2024-01-21;-4.7;22;128\n'
)


@pytest.fixture
def test_csv(tmp_path):
    """Schreibt eine kleine ``test_wetterdaten.csv`` in ein Temp-Verzeichnis."""
    pfad = tmp_path / 'test_wetterdaten.csv'
    pfad.write_text(CSV_INHALT, encoding='utf-8')
    return pfad


@pytest.fixture
def test_daten(test_csv):
    """Lädt die Test-CSV einmalig als Liste von Dictionaries."""
    return wa.csv_einlesen(test_csv)


# ---------------------------------------------------------------- csv_einlesen

def test_csv_einlesen_anzahl_datensaetze(test_csv):
    daten = wa.csv_einlesen(test_csv)
    assert len(daten) == 7


def test_csv_einlesen_typen_und_inhalt(test_csv):
    daten = wa.csv_einlesen(test_csv)
    erster = daten[0]
    assert erster == {
        'datum': '2024-01-15',
        'temperatur': -8.2,
        'windgeschwindigkeit': 34,
        'schneehoehe': 120,
    }
    assert isinstance(erster['datum'], str)
    assert isinstance(erster['temperatur'], float)
    assert isinstance(erster['windgeschwindigkeit'], int)
    assert isinstance(erster['schneehoehe'], int)


def test_csv_einlesen_nur_kopfzeile_gibt_leere_liste(tmp_path):
    pfad = tmp_path / 'leer.csv'
    pfad.write_text(CSV_HEADER, encoding='utf-8')
    assert wa.csv_einlesen(pfad) == []


def test_csv_einlesen_ueberspringt_leere_zeilen(tmp_path):
    pfad = tmp_path / 'mit_leerzeilen.csv'
    pfad.write_text(
        CSV_HEADER
        + '2024-01-15;-8.2;34;120\n'
        + '\n'
        + '2024-01-16;-3.1;18;118\n',
        encoding='utf-8',
    )
    daten = wa.csv_einlesen(pfad)
    assert len(daten) == 2
    assert daten[0]['datum'] == '2024-01-15'
    assert daten[1]['datum'] == '2024-01-16'


def test_csv_einlesen_datei_nicht_vorhanden(tmp_path):
    with pytest.raises(FileNotFoundError):
        wa.csv_einlesen(tmp_path / 'gibt_es_nicht.csv')


# ------------------------------------------------------------------ merge_sort

def test_merge_sort_gemischte_liste():
    eingabe = [{'k': 3}, {'k': 1}, {'k': 4}, {'k': 1}, {'k': 5}, {'k': 9}, {'k': 2}]
    sortiert = wa.merge_sort(eingabe, 'k')
    assert [e['k'] for e in sortiert] == [1, 1, 2, 3, 4, 5, 9]


def test_merge_sort_bereits_sortiert():
    eingabe = [{'k': 1}, {'k': 2}, {'k': 3}, {'k': 4}]
    sortiert = wa.merge_sort(eingabe, 'k')
    assert [e['k'] for e in sortiert] == [1, 2, 3, 4]


def test_merge_sort_umgekehrt_sortiert():
    eingabe = [{'k': 5}, {'k': 4}, {'k': 3}, {'k': 2}, {'k': 1}]
    sortiert = wa.merge_sort(eingabe, 'k')
    assert [e['k'] for e in sortiert] == [1, 2, 3, 4, 5]


def test_merge_sort_ein_element():
    eingabe = [{'k': 42}]
    assert wa.merge_sort(eingabe, 'k') == [{'k': 42}]


def test_merge_sort_leere_liste():
    assert wa.merge_sort([], 'k') == []


def test_merge_sort_veraendert_original_nicht():
    eingabe = [{'k': 3}, {'k': 1}, {'k': 2}]
    kopie = [dict(e) for e in eingabe]
    wa.merge_sort(eingabe, 'k')
    assert eingabe == kopie


def test_merge_sort_nach_temperatur(test_daten):
    sortiert = wa.merge_sort(test_daten, 'temperatur')
    temperaturen = [e['temperatur'] for e in sortiert]
    assert temperaturen == sorted(temperaturen)
    assert sortiert[0]['datum'] == '2024-01-20'   # -15.3 °C
    assert sortiert[-1]['datum'] == '2024-01-18'  # -1.8 °C


# --------------------------------------------------------------------- minimum

def test_minimum_temperatur(test_daten):
    ergebnis = wa.minimum(test_daten, 'temperatur')
    assert ergebnis['datum'] == '2024-01-20'
    assert ergebnis['temperatur'] == -15.3


def test_minimum_windgeschwindigkeit(test_daten):
    ergebnis = wa.minimum(test_daten, 'windgeschwindigkeit')
    assert ergebnis['datum'] == '2024-01-18'
    assert ergebnis['windgeschwindigkeit'] == 11


def test_minimum_leere_liste_gibt_none():
    assert wa.minimum([], 'temperatur') is None


# --------------------------------------------------------------------- maximum

def test_maximum_temperatur(test_daten):
    ergebnis = wa.maximum(test_daten, 'temperatur')
    assert ergebnis['datum'] == '2024-01-18'
    assert ergebnis['temperatur'] == -1.8


def test_maximum_schneehoehe(test_daten):
    ergebnis = wa.maximum(test_daten, 'schneehoehe')
    assert ergebnis['datum'] == '2024-01-20'
    assert ergebnis['schneehoehe'] == 130


def test_maximum_leere_liste_gibt_none():
    assert wa.maximum([], 'schneehoehe') is None


# ----------------------------------------------------------------- durchschnitt

def test_durchschnitt_temperatur(test_daten):
    # (-8.2 + -3.1 + -12.5 + -1.8 + -6.4 + -15.3 + -4.7) / 7 = -7.4285... → -7.43
    assert wa.durchschnitt(test_daten, 'temperatur') == -7.43


def test_durchschnitt_windgeschwindigkeit(test_daten):
    # (34 + 18 + 52 + 11 + 29 + 61 + 22) / 7 = 32.4285... → 32.43
    assert wa.durchschnitt(test_daten, 'windgeschwindigkeit') == 32.43


def test_durchschnitt_schneehoehe(test_daten):
    # (120 + 118 + 125 + 119 + 122 + 130 + 128) / 7 = 123.1428... → 123.14
    assert wa.durchschnitt(test_daten, 'schneehoehe') == 123.14


def test_durchschnitt_rundet_auf_zwei_dezimalstellen():
    liste = [{'k': 1}, {'k': 2}, {'k': 2}]  # 5 / 3 = 1.6666...
    assert wa.durchschnitt(liste, 'k') == 1.67


def test_durchschnitt_leere_liste_gibt_none():
    assert wa.durchschnitt([], 'k') is None


# ------------------------------------------------------------------ auswertung

def test_auswertung_gibt_bericht_aus(test_csv, capsys):
    wa.auswertung(test_csv)
    ausgabe = capsys.readouterr().out
    assert 'Temperatur:' in ausgabe
    assert 'Windgeschwindigkeit:' in ausgabe
    assert 'Schneehöhe:' in ausgabe
    assert '-15.3' in ausgabe and '2024-01-20' in ausgabe
    assert '-1.8' in ausgabe and '2024-01-18' in ausgabe
    assert '-7.43' in ausgabe
    assert '32.43' in ausgabe
    assert '123.14' in ausgabe


def test_auswertung_bei_leeren_daten(tmp_path, capsys):
    pfad = tmp_path / 'leer.csv'
    pfad.write_text(CSV_HEADER, encoding='utf-8')
    wa.auswertung(pfad)
    assert 'Keine Wetterdaten vorhanden.' in capsys.readouterr().out


# ------------------------------------- ``if __name__ == '__main__'`` Hauptblock

def test_main_block_wird_ausgefuehrt(tmp_path, monkeypatch, capsys):
    pfad = tmp_path / 'wetterdaten.csv'
    pfad.write_text(CSV_INHALT, encoding='utf-8')
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(MODULE_PATH), run_name='__main__')
    ausgabe = capsys.readouterr().out
    assert 'Temperatur:' in ausgabe
