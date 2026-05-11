"""Wetterdaten-Auswertung für die Bergbahnen Flumserberg AG.

Liest eine semikolon-getrennte CSV-Datei mit Wetterdaten ein, sortiert sie
mit MergeSort und berechnet Minimum, Maximum und Durchschnitt für die
Felder Temperatur, Windgeschwindigkeit und Schneehöhe.
"""

import csv


def csv_einlesen(dateipfad):
    """Liest eine semikolon-getrennte Wetterdaten-CSV ein.

    Die Kopfzeile wird übersprungen. Erwartete Spaltenreihenfolge:
    datum;temperatur;windgeschwindigkeit;schneehoehe

    Args:
        dateipfad: Pfad zur CSV-Datei (str oder pathlib.Path).

    Returns:
        Liste von Dictionaries mit den Schlüsseln 'datum' (str),
        'temperatur' (float), 'windgeschwindigkeit' (int) und
        'schneehoehe' (int). Leere Liste, wenn nur die Kopfzeile vorhanden ist.

    Raises:
        FileNotFoundError: Wenn die Datei unter ``dateipfad`` nicht existiert.
    """
    datensaetze = []
    with open(dateipfad, 'r', encoding='utf-8', newline='') as datei:
        leser = csv.reader(datei, delimiter=';')
        next(leser, None)  # Kopfzeile überspringen
        for zeile in leser:
            if not zeile:
                continue
            datensaetze.append({
                'datum': zeile[0],
                'temperatur': float(zeile[1]),
                'windgeschwindigkeit': int(zeile[2]),
                'schneehoehe': int(zeile[3]),
            })
    return datensaetze


def merge(links, rechts, schluessel):
    """Fügt zwei aufsteigend sortierte Listen zu einer sortierten Liste zusammen.

    Args:
        links: Aufsteigend sortierte linke Teil-Liste von Dictionaries.
        rechts: Aufsteigend sortierte rechte Teil-Liste von Dictionaries.
        schluessel: Dictionary-Schlüssel, nach dem verglichen wird.

    Returns:
        Eine neue, aufsteigend sortierte Liste, die alle Elemente aus
        ``links`` und ``rechts`` enthält.

    Raises:
        KeyError: Wenn ein Element den angegebenen ``schluessel`` nicht enthält.
    """
    ergebnis = []
    i = 0
    j = 0
    while i < len(links) and j < len(rechts):
        if links[i][schluessel] <= rechts[j][schluessel]:
            ergebnis.append(links[i])
            i += 1
        else:
            ergebnis.append(rechts[j])
            j += 1
    while i < len(links):
        ergebnis.append(links[i])
        i += 1
    while j < len(rechts):
        ergebnis.append(rechts[j])
        j += 1
    return ergebnis


def merge_sort(liste, schluessel):
    """Sortiert eine Liste von Dictionaries aufsteigend mit MergeSort.

    Rekursiver Teile-und-herrsche-Algorithmus. Die übergebene Liste wird
    nicht verändert; es wird eine neue Liste zurückgegeben.

    Args:
        liste: Liste von Dictionaries, die sortiert werden soll.
        schluessel: Dictionary-Schlüssel, nach dem aufsteigend sortiert wird.

    Returns:
        Eine neue, aufsteigend nach ``schluessel`` sortierte Liste.

    Raises:
        KeyError: Wenn ein Element den angegebenen ``schluessel`` nicht enthält.
    """
    if len(liste) <= 1:
        return list(liste)
    mitte = len(liste) // 2
    links = merge_sort(liste[:mitte], schluessel)
    rechts = merge_sort(liste[mitte:], schluessel)
    return merge(links, rechts, schluessel)


def minimum(liste, schluessel):
    """Sucht den Datensatz mit dem kleinsten Wert für ``schluessel``.

    Iteriert manuell durch die Liste, ohne ``min()`` zu verwenden.

    Args:
        liste: Nicht-leere Liste von Dictionaries.
        schluessel: Dictionary-Schlüssel, nach dem verglichen wird.

    Returns:
        Das Dictionary mit dem kleinsten Wert für ``schluessel``. Bei
        Gleichstand das zuerst gefundene Dictionary. ``None``, wenn die
        Liste leer ist.

    Raises:
        KeyError: Wenn ein Element den angegebenen ``schluessel`` nicht enthält.
    """
    if not liste:
        return None
    kleinster = liste[0]
    for eintrag in liste[1:]:
        if eintrag[schluessel] < kleinster[schluessel]:
            kleinster = eintrag
    return kleinster


def maximum(liste, schluessel):
    """Sucht den Datensatz mit dem grössten Wert für ``schluessel``.

    Iteriert manuell durch die Liste, ohne ``max()`` zu verwenden.

    Args:
        liste: Nicht-leere Liste von Dictionaries.
        schluessel: Dictionary-Schlüssel, nach dem verglichen wird.

    Returns:
        Das Dictionary mit dem grössten Wert für ``schluessel``. Bei
        Gleichstand das zuerst gefundene Dictionary. ``None``, wenn die
        Liste leer ist.

    Raises:
        KeyError: Wenn ein Element den angegebenen ``schluessel`` nicht enthält.
    """
    if not liste:
        return None
    groesster = liste[0]
    for eintrag in liste[1:]:
        if eintrag[schluessel] > groesster[schluessel]:
            groesster = eintrag
    return groesster


def durchschnitt(liste, schluessel):
    """Berechnet den arithmetischen Mittelwert für ``schluessel``.

    Args:
        liste: Liste von Dictionaries.
        schluessel: Dictionary-Schlüssel, dessen Werte gemittelt werden.

    Returns:
        Der auf zwei Dezimalstellen gerundete Mittelwert als ``float``.
        ``None``, wenn die Liste leer ist (kein ``ZeroDivisionError``).

    Raises:
        KeyError: Wenn ein Element den angegebenen ``schluessel`` nicht enthält.
    """
    if not liste:
        return None
    summe = 0
    for eintrag in liste:
        summe += eintrag[schluessel]
    return round(summe / len(liste), 2)


def auswertung(dateipfad):
    """Liest die CSV ein und gibt einen formatierten Statistik-Bericht aus.

    Sortiert die Daten zur Demonstration mit MergeSort nach Datum und
    berechnet danach Min, Max und Durchschnitt für Temperatur,
    Windgeschwindigkeit und Schneehöhe.

    Args:
        dateipfad: Pfad zur Wetterdaten-CSV.

    Returns:
        ``None``. Die Ausgabe erfolgt direkt auf ``stdout``.

    Raises:
        FileNotFoundError: Wenn die Datei unter ``dateipfad`` nicht existiert.
    """
    daten = csv_einlesen(dateipfad)
    if not daten:
        print('Keine Wetterdaten vorhanden.')
        return

    sortiert = merge_sort(daten, 'datum')

    t_min = minimum(sortiert, 'temperatur')
    t_max = maximum(sortiert, 'temperatur')
    t_avg = durchschnitt(sortiert, 'temperatur')

    w_min = minimum(sortiert, 'windgeschwindigkeit')
    w_max = maximum(sortiert, 'windgeschwindigkeit')
    w_avg = durchschnitt(sortiert, 'windgeschwindigkeit')

    s_min = minimum(sortiert, 'schneehoehe')
    s_max = maximum(sortiert, 'schneehoehe')
    s_avg = durchschnitt(sortiert, 'schneehoehe')

    print(
        f"Temperatur:          "
        f"Min {t_min['temperatur']}°C ({t_min['datum']}) | "
        f"Max {t_max['temperatur']}°C ({t_max['datum']}) | "
        f"Ø {t_avg}°C"
    )
    print(
        f"Windgeschwindigkeit: "
        f"Min {w_min['windgeschwindigkeit']} km/h ({w_min['datum']}) | "
        f"Max {w_max['windgeschwindigkeit']} km/h ({w_max['datum']}) | "
        f"Ø {w_avg} km/h"
    )
    print(
        f"Schneehöhe:          "
        f"Min {s_min['schneehoehe']} cm ({s_min['datum']})  | "
        f"Max {s_max['schneehoehe']} cm ({s_max['datum']})  | "
        f"Ø {s_avg} cm"
    )


if __name__ == '__main__':
    auswertung('wetterdaten.csv')
