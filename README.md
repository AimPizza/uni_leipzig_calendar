# Uni Leipzig Kalender

Dieses Projekt ermöglicht es, den Stundenplan an der Universität Leipzig über [.ics](https://wikipedia.org/wiki/ICalendar) abzurufen und so stets eine aktuelle Version zu synchronisieren.

> Die Grundlage bildet das Projekt [MrMxffin/uni_leipzig_scheduler](https://github.com/MrMxffin/uni_leipzig_scheduler), welches wöchentliche Benachrichtigung per Telegram Bot ermöglicht.

## Inhaltsverzeichnis

1. [Einleitung](#einleitung)
2. [Funktionsweise](#funktionsweise)
3. [Konfiguration](#konfiguration)
4. [Installation](#installation)
5. [Beitragen](#beitragen)
6. [Lizenz](#lizenz)

## Einleitung

Niemand mag manuelles Eintragen und Bearbeiten von Kalendererignissen. Deshalb sollen die Dinge, so weit es geht, automatisiert werden.

## Funktionsweise

Das Skript bietet eine API an, über die unter dem Endpunkt `/calendar/<zahl>` die iCalendar-Daten abgerufen werden können. Die Almaweb Login-Daten liegen dabei (noch?) in einer `.env`-Datei in der Wurzel des Projekts. Der Parameter `<zahl>` bestimmt die Menge an **Wochen**, die der Kalender ausgehend von heute aus beinhaltet.

Um das Scraping zu minimieren (und mögliches rate-limiting zu vermeiden) ist es empfehlenswert, den Parameter `<zahl>` gering zu halten, denn pro Woche wird eine Anfrage an das Portal gesendet. Auf Seiten des Skripts ist ein Cache implementiert, welcher die Antwort für 3 Tage zwischenspeichert.

## Konfiguration

Die Konfiguration erfolgt über Umgebungsvariablen, die in einer .env-Datei bereitgestellt werden. Folgende Variablen müssen konfiguriert werden:

- `ALMAWEB_USERNAME`: Benutzername für den Zugriff auf die AlmaWeb-Plattform.
- `ALMAWEB_PASSWORD`: Passwort für den Zugriff auf die AlmaWeb-Plattform.

## Installation

Um das Projekt lokal auszuführen, müssen Sie die folgenden Schritte ausführen:

1. Klone das Repository: `git clone git@github.com:AimPizza/uni_leipzig_calendar.git`
2. Wechsle in das Verzeichnis: `cd uni_leipzig_calendar`
3. Installiere die Abhängigkeiten: `pixi install`
4. Erstelle eine .env-Datei und konfiguriere die erforderlichen Umgebungsvariablen.
5. Führe das Hauptskript aus: `pixi run start`

> **Hinweis**: Hier wurde [Pixi](https://pixi.prefix.dev/latest/python/tutorial/) aus Gewohnheit genutzt. Alternativ funktioniert auch der klassische Weg über `venv` und `pip`:
>
> - `python -m venv .venv`
> - `source .venv/bin/activate`
> - `pip install .`

## Beitragen

Beiträge sind immer willkommen! Bugfixes, Feature-Ideen oder anderweitige Kritik helfen, das Projekt in einen besseren Zustand zu bringen.

Als Einstieg ist unter [Perspektivisch](#perspektivisch) Verbesserungspotential aufgelistet.

## Perspektivisch

offene TODOs:

- nach anderen Endpunkten suchen, die ggf. sofort gewünschte Anzahl oder gar gesamten Kalender bereitstellt
- Docker Pipeline und Containerisierung (wichtig)

## Lizenz

Dieses Projekt ist unter der [Unlicense](https://unlicense.org/) lizenziert. Das bedeutet, dass es sich um freie und gemeinfreie Software handelt, die in die Public Domain entlassen wurde. Du bist frei, die Software zu kopieren, zu modifizieren, zu veröffentlichen, zu verwenden, zu kompilieren, zu verkaufen oder zu verteilen, sowohl in Quellcode-Form als auch als kompilierte Binärdatei, für jeden Zweck, kommerziell oder nicht kommerziell, und auf jede erdenkliche Weise.

Weitere Informationen findest du in der [Lizenzdatei](./LICENSE).
