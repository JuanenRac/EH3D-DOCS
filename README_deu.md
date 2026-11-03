<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | 🇩🇪 <b>Deutsch</b> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Die Karte, die Architektur und der ehrliche Stand der EH3D Fabrication Suite: wofür jedes Repository da ist, was getestet wurde und was noch nicht auf einer Maschine lief

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Markdown%20%2B%20Python-blue.svg" alt="Markdown and Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.8-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-4CAF50.svg" alt="Maturity">
</p>

---

**Ehrlichkeitscheck - was heute tatsächlich läuft:** Dokumente und die Werkzeuge der Suite, die auf einem Rechner laufen und sonst nirgends (die Repository-Prüfung und die Zeichner der Bilder, die jedes Repository mitbringt, der Vertrag zwischen den Repositories, die Skripte, die eine Version erhöhen und eine Veröffentlichung vorbereiten, das Skript, das einen Arbeitsbereich einrichtet, und das, das ein neues Repository anlegt). Die Suite steht am Anfang: siebenundzwanzig Repositories sind veröffentlicht (die Bibliotheken, die Bungard-Programme, der Server und Studio, die Knoten und Touchscreens, die Handy-Apps, die CAM- und Hilfsprogramme, die Updater und dieses), zwei sind mit Code und Tests und ohne veröffentlichte Version begonnen (das Hauptprojekt für elektronisches Design und sein Testlabor) und elf sind nur geplant (das Handbediengerät für kleine Touchscreens und zehn Repositories des Projekts für elektronisches Design und seiner Brücken). Alles Veröffentlichte wurde auf einem Computer getestet, und die Oberflächen sprechen 37 Sprachen; von der ganzen Suite hat nur das serielle Protokoll von EH3D-DRILLPRO eine echte Maschine bewegt (die Referenzfahrt und die Bewegungen jeder Achse an einer Bungard CCD MTC), und noch kein ganzer Auftrag lief auf einer Maschine. 14 Tests decken die Repository-Prüfung ab.

---

> **Stand von Sicherheit und IT-Sicherheit:** dieses Repository führt nichts auf einer Maschine aus und ist kein Sicherheitssystem (Safety). Ein Dokument hier ersetzt nie die Grenzen, Verriegelungen und den Not-Aus der Maschine und ihrer Steuerung.

## 📋 Auf einen Blick

| | |
|---|---|
| Version | `0.0.8` |
| Reifegrad | Funktionsfähig |
| Tests | 151 |
| Technologie-Stack | Markdown, mit Python-3.10+-Werkzeugen |
| Auf echter Hardware | Nicht zutreffend: Dokumentation |

**Springe zu:** [Überblick](#-überblick) · [Architektur](#-architektur) · [Schnellstart](#-schnellstart) · [Tests](#-tests) · [Struktur](#-struktur-des-repositorys) · [Verwandte](#-verwandte-projekte)

## 🚦 Projektstatus

Jede Zeile ist ein Teil dieses Repositorys, und die Ampel sagt, wie weit er heute ist. Sie beruht auf dem, was das Repository zeigen kann (Tests, Builds, Läufe), nicht auf dem, was geplant ist.

🟢 Fertig und überprüft · 🟡 Funktioniert, mit bekannten Grenzen · 🟠 Teilweise fertig oder noch nicht überprüft · 🔴 Nicht gemacht oder funktioniert nicht

| Bereich | Stand | Was das hier bedeutet |
|---|---|---|
| Repository-Prüfungen | 🟡 | Die Repository-Prüfung, die Prüfung der Links zwischen den Dokumenten und die Tests der Werkzeuge laufen in der CI und bestehen. |
| Tests | 🟠 | 151 Tests der Werkzeuge bestehen auf einem Rechner, einige davon auf kleinen Spielzeug-Repositories; die Dokumente und ihre Aussagen werden von Hand und mit den Skripten gelesen und geprüft. |
| Vertrag der Suite | 🟡 | Der Vertrag zwischen den Repositories liest jedes Manifest mit dem Parser des Updaters und meldet Abweichungen (Ports, README-Sprachen, gemeinsame Werkzeuge, Issue-Formulare); er läuft täglich in der CI als Warnung, und die Repositories, die er nennt, werden eines nach dem anderen nachgezogen. |
| Werkzeuge für Version und Veröffentlichung | 🟠 | Die Skripte, die eine Version erhöhen, die Notizen schreiben und eine Veröffentlichung prüfen, und der wiederverwendbare Validierungs-Workflow sind an Spielzeug-Repositories getestet; noch kein Repository hat damit eine Version veröffentlicht. |
| Arbeitsbereich und neue Repositories | 🟠 | Die Skripte, die auflisten und klonen, was ein Repository braucht, und die ein neues Repository anlegen, sind an Spielzeug-Repositories in einem temporären Ordner getestet; keines hat bisher einen echten Arbeitsbereich eingerichtet oder ein echtes Repository angelegt. |
| Karte und Fähigkeitsmatrix | 🟡 | Die Karte der Suite, die Architekturnotizen und die Fähigkeitsmatrix decken die vierzig Repositories ab: die siebenundzwanzig veröffentlichten mit der Version jedes einzelnen, zwei begonnene (Code mit Tests und ohne veröffentlichte Version) und elf geplante (ein geschriebener Umfang und kein Code); sie werden von Hand geschrieben und können hinter den Repositories zurückbleiben. |
| Echte Hardware | 🟡 | Nicht zutreffend: Dokumentation, nichts hier läuft auf Hardware. |
| Dokumentation | 🟡 | README in acht Sprachen, bei jeder Änderung gegen Manifest und Änderungsprotokoll geprüft. |

## 🎯 Überblick

* **Die Karte der Suite:** jedes Repository, wofür es da ist und ob es veröffentlicht, begonnen (Code mit Tests und noch ohne Release) oder nur geplant ist.
* **Die Architektur:** die zwei gemeinsamen Bibliotheken, die Programme, die davon abhängen sollen und nie voneinander, der Knoten und der Server, die die Maschine erreichen, und die Regeln jedes Repositorys.
* **Die Fähigkeitsmatrix:** was auf einem Computer getestet ist und was auf einer Maschine lief (nur das Protokoll von EH3D-DRILLPRO, an einer Maschine), damit niemand raten muss.
* **Die Konventionen:** das Manifest, das jedes Repository trägt, die Repository-Prüfung und die README-Dateien in acht Sprachen.
* **Die Prüfungen und die Werkzeuge:** die Repository-Prüfung, die Prüfung der Links zwischen den Dokumenten, die Zeichner der beiden README-Bilder und die Statusampeln, von hier in jedes Repository kopiert (`tools/sync_shared_tools.py` sagt, wer zurückliegt), und die Prüfung der Konvention für Exit-Codes; `banner_check.py` prüft, dass der Text jedes Banners sagt, was das Manifest sagt, und `docs/vendored.lock` hält Herkunft und Version jedes gemeinsamen Werkzeugs fest.
* **Der Vertrag der Suite:** `tools/suite_contract.py` prüft die Beziehungen, die kein Repository allein prüfen kann: Jedes Manifest ist mit dem Parser des Updaters lesbar und trägt den Namen seines Ordners, eine Abhängigkeit von einem Nachbarn über einen Pfad nennt die benötigte Version, die Versionen der Karte sind die der Manifeste, Bildschirme und Server sind sich über den Port einig, der gemeinsame Validator ist überall derselbe, `docs/suite.json` stimmt mit den Stellen überein, die seine Werte wiederholen, und jedes Repository hat die Issue-Formulare. Er warnt nur.
* **Versionen, Veröffentlichungen und neue Arbeit:** `bump_version.py`, `release_notes.py`, `prerelease_check.py`, `readme_staleness.py` und `vendored_tools_report.py` ([docs/RELEASING.md](docs/RELEASING.md)), ein wiederverwendbarer Validierungs-Workflow ([docs/REUSABLE_VALIDATION.md](docs/REUSABLE_VALIDATION.md)), `bootstrap_workspace.py`, um zu holen, was ein Repository braucht, und `new_repo.py`, um ein neues Repository anzulegen. `bump_version.py` erhöht außerdem die internen Abhängigkeiten, die eine Mindestversion verlangen, die `Cargo.lock`-Einträge der Pakete eines Workspace und das Manifest des Aktualisierers der ganzen Familie.
* **Wie aktualisiert wird:** Die CM5 der Werkstatt wird **per Releases** aktualisiert (`deploy/eh3d-update.py` von EH3D-SERVER lädt das Release von GitHub nach `/opt`); EH3D-UPDATER ist für **Entwicklungs-PCs, per Git** ([docs/UPDATING.md](docs/UPDATING.md)).

## 🧩 Rolle in EH3D

EH3D-DOCS ist der Ort, an dem die Suite als Ganzes beschrieben wird. Jedes Repository beschreibt sich in seinem eigenen README; dieses sagt, wie sie zusammenpassen, welche es gibt und was wirklich gelaufen ist.

## 🏛️ Architektur

<p align="center">
  <img src="images/architecture.svg" alt="Architektur von EH3D-DOCS: wer es nutzt, was es enthält und wovon es abhängt" width="100%">
</p>

Wie die Teile dieses Repositorys zusammenpassen: wer es nutzt, was es enthält und wovon es abhängt. Das Bild wird aus `docs/architecture.json` gezeichnet und gegen den Code geprüft.

## 🔒 Sicherheit und Schutz

Dieses Repository hat kein Programm, das Eingaben von außen annimmt; es schützt die Richtigkeit und die Sauberkeit dessen, was es veröffentlicht.

| Bedrohung | Abwehr |
|---|---|
| Die Behauptung, die Suite könne mehr, als sie kann | Die Fähigkeitsmatrix trennt „auf einem Computer getestet“ von „auf einer Maschine gelaufen“, und ein Repository gilt als geplant, bis es Code gibt, den jeder ausführen kann |
| Ein privater Verweis, eine Person oder ein Werkzeug, das nicht öffentlich sein darf | `tools/ci_validate.py` schlägt bei den Wörtern fehl, die nie in einer öffentlichen Datei stehen dürfen, in jeder Textdatei |
| Ein kaputter Link zwischen den Dokumenten | `tools/check_links.py` schlägt fehl, wenn ein relativer Link einer Markdown-Datei auf eine nicht vorhandene Datei zeigt |
| Eine README-Sprache driftet von den anderen ab | Die Prüfung vergleicht die Überschriftenstruktur, die Ampeln des Projektstatus und die Version in den acht Dateien |
| Dateien, die nicht versioniert werden dürfen (Builds, Schlüssel, Protokolle, große Dateien) | Die Repository-Prüfung weist versionierte Build-Ordner, private Ordner, Schlüssel- und Protokolldateien und Dateien über 1,5 MB ab |

## 🔌 Schnittstellen

| Schnittstelle | Was es ist | Wo |
|---|---|---|
| Die Dokumente | Markdown: die Karte, die Architektur, die Fähigkeitsmatrix, die Konventionen und die Anleitungen zum Aktualisieren und Veröffentlichen | [docs/](docs/SUITE_MAP.md) |
| Die Repository-Prüfung | `python -I tools/ci_validate.py` gibt `CI_VALIDATION=PASS` aus oder listet, was fehlschlägt | `tools/ci_validate.py` |
| Die Link-Prüfung | `python -I tools/check_links.py` gibt `LINKS=PASS` aus oder listet die kaputten Links | `tools/check_links.py` |
| Die Tests der Prüfung | `python -I -m unittest discover -s tools -p "test_*.py"` | `tools/test_ci_validate.py` |
| Der Vertrag der Suite | `python -I tools/suite_contract.py --workspace ..` gibt `SUITE_CONTRACT=PASS` aus oder listet die Befunde; `--write-map` trägt die Versionen der Manifeste in die Karte ein | `tools/suite_contract.py` |
| Die gemeinsamen Werkzeuge | `python -I tools/sync_shared_tools.py` sagt, welche Repositories eine abweichende Kopie haben | `tools/sync_shared_tools.py` |
| Versionen und Veröffentlichungen | `bump_version.py`, `release_notes.py`, `prerelease_check.py`, `readme_staleness.py`, `vendored_tools_report.py` | [docs/RELEASING.md](docs/RELEASING.md) |
| Der wiederverwendbare Workflow | Validierung mit `on: workflow_call`, zum Aufrufen aus den Repositories | [docs/REUSABLE_VALIDATION.md](docs/REUSABLE_VALIDATION.md) |
| Der Arbeitsbereich | `bootstrap_workspace.py` listet und klont, was ein Repository braucht; `new_repo.py` legt ein neues Repository an | `tools/bootstrap_workspace.py`, `tools/new_repo.py` |
| Die Exit-Codes | `0`, `1`, `2`, `10` und `64`; `exit_conventions.py` prüft die Werkzeuge dagegen | [docs/CONVENTIONS.md](docs/CONVENTIONS.md) |

## ⚙️ Konfiguration

Die Werkzeuge brauchen Python 3.10 oder neuer und keine Installation, und sie lesen die Dateien des Repositorys, in dem sie liegen. Die Regeln, die sie durchsetzen, stehen im Code von `tools/ci_validate.py`, und die Werte der Suite, die mehrere Repositories wiederholen, stehen in `docs/suite.json`:

| Regel | Grenze | Wo |
|---|---|---|
| Größe einer versionierten Datei | höchstens 1.500.000 Bytes | `MAX_TRACKED_BYTES` |
| Sprachen des README | acht Dateien, mit derselben Überschriftenstruktur und denselben Ampeln | `LANGUAGES` |
| Manifestfelder | die 14 Felder von `REQUIRED`; die Version des Manifests entspricht der in `VERSION` (`native_version`) und im neuesten Eintrag des Änderungsprotokolls | `REQUIRED` |
| Die Konstanten der Suite | der Port des Servers, das Manifest-Schema, die acht README-Sprachen, das Drehzahlfeld, die Form einer Version, die Issue-Formulare | `docs/suite.json` |
| Bekannte Ausnahmen des Vertrags | ein `check Repository` pro Zeile, entfernt, wenn die Ursache behoben ist | `docs/suite_contract_allow.txt` |
| Was ein Repository zur Prüfung hinzufügt | zum Beispiel die Ordner, die die Suche nach verbotenen Wörtern überspringt | `tools/ci_config.json` jedes Repositorys |

## 🚀 Schnellstart

Du brauchst Python 3.10 oder neuer; es gibt nichts zu installieren.

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
python -I tools/suite_contract.py --workspace ..
python -I tools/bootstrap_workspace.py --workspace .. EH3D-DRILLPRO
python -I -m unittest discover -s tools -p "test_*.py"
```

Zum Lesen der Dokumente beginne mit [der Karte der Suite](docs/SUITE_MAP.md).

## 🧪 Tests

Die Werkzeuge haben 151 Tests (`python -I -m unittest discover -s tools -p "test_*.py"`), und sie bestehen. Die CI führt die Repository-Prüfung (`tools/ci_validate.py`), die Prüfung der Links zwischen den Dokumenten (`tools/check_links.py`), die Prüfungen der beiden Bilder und diese Tests aus; ein täglicher Workflow führt den Vertrag der Suite aus. Die Dokumente selbst haben keinen weiteren Test: Was sie behaupten, wird durch die Fähigkeitsmatrix und durch Lesen ehrlich gehalten.

## 🏗️ Build und Veröffentlichung

Die Version steht in der Datei `VERSION` und in `eh3d.project.json`, und jede Version hat ihren Eintrag in [CHANGELOG.md](CHANGELOG.md). Es gibt nichts zu bauen; Releases werden auf GitHub veröffentlicht.

## 📂 Struktur des Repositorys

<p align="center">
  <img src="images/repository-structure.svg" alt="Struktur des Repositorys EH3D-DOCS" width="100%">
</p>

<details>
<summary>Textversion des Baums</summary>

```text
EH3D-DOCS/
├── docs/
│   ├── SUITE_MAP.md                             jedes Repository und ob es schon existiert
│   ├── ARCHITECTURE.md                          die Schichten und die Regeln
│   ├── CAPABILITY_MATRIX.md                     was getestet wurde und was auf einer Maschine lief
│   ├── CONVENTIONS.md                           das Manifest, die Prüfung, die README-Dateien
│   ├── UPDATING.md                              wie CM5 und PC aktualisiert werden
│   ├── RELEASING.md                             eine Version erhöhen und mit den Skripten veröffentlichen
│   ├── REUSABLE_VALIDATION.md                   der Validierungs-Workflow, den die Repositories aufrufen können
│   ├── VENDORED_TOOLS_REPORT.md                 die in die Repositories kopierten Werkzeuge, die niemand benutzt
│   ├── suite.json                               die Konstanten der Suite
│   ├── suite_contract_allow.txt                 die bekannten Ausnahmen des Vertrags
│   ├── templates/                               die Vorlage eines neuen Repositorys
│   └── architecture.json structure.json         die Daten der beiden Bilder
├── tools/                                       die Prüfungen, der Vertrag, die Skripte für Version und Veröffentlichung und ihre Tests
├── registry/                                    die Register der Container- und Identitätscodes und ihre Tests
├── images/                                      Banner und die Bilder von Architektur und Repository-Struktur
├── .github/                                     CI- und Dashboard-Workflows, Vorlagen für Issues und Pull Requests
├── eh3d.project.json                            Manifest: Version, Rolle, Reifegrad und Build-Befehl
├── VERSION                                      die Version der Dokumente
├── CHANGELOG.md                                 was sich in jeder Version geändert hat
├── SECURITY.md SUPPORT.md                       Schwachstellen melden und Fragen stellen
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   Mitwirken, Verhaltenskodex und Lizenz
```

</details>

## 🗺️ Roadmap und bekannte Grenzen

**Bekannte Grenzen heute**

* Die Karte, die Architekturnotizen und die Fähigkeitsmatrix werden von Hand geschrieben; nichts prüft sie gegen die Manifeste der Repositories, sie können also zurückbleiben.
* Nur die veröffentlichten Repositories sind ausführlich beschrieben; die begonnenen und die geplanten Programme sind je eine entsprechend markierte Zeile der Karte.
* Die Dokumente haben keinen eigenen Test außer der Repository-Prüfung und der Link-Prüfung.
* Die Skripte für Veröffentlichung, Arbeitsbereich und neue Repositories wurden nur an Spielzeug-Repositories ausprobiert; keines wurde bisher für eine echte Veröffentlichung oder zum Anlegen eines echten Repositorys benutzt.
* Der Vertrag der Suite warnt nur, und mehrere Repositories haben noch eine ältere Kopie des gemeinsamen Validators.

**Als Nächstes**

* Die Karte und die Fähigkeitsmatrix mit jedem Repository im Gleichschritt halten, wenn es veröffentlicht wird oder sich ändert.
* Die Karte gegen die Manifeste der Repositories prüfen, damit ein neues Repository darin nicht fehlen kann.
* Die Skripte für die nächste echte Veröffentlichung verwenden, den wiederverwendbaren Workflow in den Repositories einführen und den Vertrag der Suite blockierend machen, sobald seine bekannten Befunde verschwunden sind.

## 🌍 Sprachen

README und Texte gibt es auf Englisch, Spanisch, Französisch, Italienisch, Deutsch, Chinesisch, Japanisch und europäischem Portugiesisch.

## 🔗 Verwandte Projekte

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): der Projektcontainer, die Maschinentypen und die Firmware-Basis der Knoten
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): die Leser für Gerber, Excellon und G-Code
* [EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO) und [EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO): die Bohr- und Fräsprogramme
* [EH3D-BUNGARD-GUI](https://github.com/JuanenRac/EH3D-BUNGARD-GUI) und [EH3D-PHOENIX-CNC](https://github.com/JuanenRac/EH3D-PHOENIX-CNC): die moderne Oberfläche der Bungard-Maschinen und das Maschinensteuerprogramm
* [EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER) und [EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD): das Zentrum der Programme und der Knoten, der die Maschine erreicht
* [EH3D-STUDIO](https://github.com/JuanenRac/EH3D-STUDIO), [EH3D-NODE-BUNGARD-HMI](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-HMI) und [EH3D-NODE-BUNGARD-AUX](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-AUX): das Konfigurationspanel des Servers (mit seinen Aktualisierungen von GitHub), der Touchscreen der Maschine und der Knoten am Bohrkopf (Kamera über RTSP und ONVIF, Laser, der den Tisch misst, Drehzahl und Temperatur der Spindel)
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) und [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): installieren und aktualisieren die Repositories
* [EH3D-PHOENIX-PCB](https://github.com/JuanenRac/EH3D-PHOENIX-PCB) und die elf weiteren Repositories des Projekts für elektronisches Design und seiner Brücken (das Labor, der Verifizierer, das Thermiklabor, der Adapter zu HYDRA-UMC): begonnen oder geplant, ohne veröffentlichte Version

## 📚 Dokumentation

* [Die Karte der Suite](docs/SUITE_MAP.md), [die Architektur](docs/ARCHITECTURE.md), [die Fähigkeitsmatrix](docs/CAPABILITY_MATRIX.md) und [die Konventionen](docs/CONVENTIONS.md).
* [Eine Version veröffentlichen](docs/RELEASING.md), [wie die Maschinen aktuell gehalten werden](docs/UPDATING.md) und [die wiederverwendbare Validierung](docs/REUSABLE_VALIDATION.md).
* [Änderungsprotokoll](CHANGELOG.md)

## 🤝 Mitwirken und Community

* Führe vor einem Pull Request `python -I tools/ci_validate.py`, `python -I tools/check_links.py` und die Tests der Werkzeuge aus: alles muss bestehen. Siehe [CONTRIBUTING.md](CONTRIBUTING.md) und den [Verhaltenskodex](CODE_OF_CONDUCT.md).
* Das README gibt es in acht Sprachen: Eine Textänderung wird in allen acht Dateien gemacht, und die beiden Bilder werden aus `docs/architecture.json` und `docs/structure.json` mit `tools/make_architecture.py` und `tools/make_structure.py` gezeichnet.
* Beschreibe nicht als auf einer Maschine funktionierend, was nur auf einem Computer erprobt wurde: Die Fähigkeitsmatrix sagt, was was ist.
* Melde eine Schwachstelle privat: [SECURITY.md](SECURITY.md). Fragen, Ideen und Meldungen: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LIZENZ

Software: GPL-3.0-or-later. Siehe [LICENSE](LICENSE). Die Hardware-Entwürfe der Suite verwenden die CERN OHL-S.
