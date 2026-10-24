<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | 🇩🇪 <b>Deutsch</b> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Die Karte, die Architektur und der ehrliche Stand der EH3D Fabrication Suite: wofür jedes Repository da ist, was getestet wurde und was noch nicht auf einer Maschine lief

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Docs-Markdown-blue.svg" alt="Markdown">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Ehrlichkeitsprüfung - was heute da ist:** Dokumente und zwei kleine Prüfungen. Die Suite steht am Anfang: drei Repositories sind veröffentlicht (EH3D-COMMON mit dem Projektcontainer, EH3D-CORE-LIBS mit Lesern für Gerber, Excellon und G-Code sowie EH3D-UPDATER), und jedes Programm der Suite ist ein Plan. Alles Veröffentlichte wurde auf einem Computer getestet; nichts lief auf einer Maschine.

---

> **Stand von Sicherheit (Safety) und IT-Sicherheit:** dieses Repository führt nichts auf einer Maschine aus und ist kein Sicherheitssystem. Ein Dokument hier ersetzt nie die Grenzen, Verriegelungen und den Not-Halt der Maschine und ihrer Steuerung.

## 📋 Auf einen Blick

| | |
|---|---|
| Version | `0.0.1` |
| Reifegrad | Gerüst |
| Technologie-Stack | Markdown / Python 3.10+ (die Prüfungen) |
| Auf echter Hardware | Nicht zutreffend: Dokumentation |

## 🚦 Projektstatus

Jede Zeile ist ein Teil dieses Repositorys, und die Ampel sagt, wie weit er heute ist. Sie beruht auf dem, was das Repository zeigen kann (Tests, Builds, Läufe), nicht auf dem, was geplant ist.

🟢 Fertig und überprüft · 🟡 Funktioniert, mit bekannten Grenzen · 🟠 Teilweise fertig oder noch nicht überprüft · 🔴 Nicht gemacht oder funktioniert nicht

| Bereich | Stand | Was das hier bedeutet |
|---|---|---|
| Repository-Prüfungen | 🟢 | Die Repository-Prüfung und die Prüfung der Links zwischen den Dokumenten laufen in der CI und bestehen. |
| Tests | 🟠 | Es gibt keine eigene Testsuite: die einzigen automatischen Prüfungen sind diese beiden Skripte. |
| Karte und Fähigkeitsmatrix | 🟠 | Die Karte, die Architekturnotizen und die Fähigkeitsmatrix decken nur die ersten drei veröffentlichten Repositorys ab; EH3D-DRILLPRO, EH3D-ROUTEPRO, EH3D-SERVER und EH3D-NODE-BUNGARD fehlen noch. |
| Echte Hardware | 🟢 | Nicht zutreffend: Dokumentation, nichts hier läuft auf Hardware. |
| Dokumentation | 🟢 | README in acht Sprachen, bei jeder Änderung mit dem Manifest und dem Änderungsprotokoll abgeglichen. |

## 🎯 Überblick

* **Die Karte der Suite:** jedes Repository, wofür es da ist und ob es veröffentlicht oder nur geplant ist.
* **Die Architektur:** die zwei gemeinsamen Bibliotheken, die Programme, die von ihnen abhängen und nie voneinander, und die Regeln jedes Repositorys.
* **Die Fähigkeitsmatrix:** was auf einem Computer getestet ist und was auf einer Maschine lief (noch nichts), damit niemand raten muss.
* **Die Konventionen:** das Manifest jedes Repositorys, die Repository-Prüfung und die README-Dateien in acht Sprachen.
* **Zwei Prüfungen:** die des Repositorys und die der Links zwischen den Dokumenten, beide in der CI.

## 📂 Repository-Struktur

```text
EH3D-DOCS/
├── docs/
│   ├── SUITE_MAP.md          every repository of the suite and whether it exists yet
│   ├── ARCHITECTURE.md       the layers and the rules
│   ├── CAPABILITY_MATRIX.md  what has been tested and what has been run on a machine
│   └── CONVENTIONS.md        the manifest, the check, the README files
├── tools/
│   ├── ci_validate.py        the repository check
│   └── check_links.py        the links between the documents
├── eh3d.project.json         the manifest of the project
└── VERSION
```

## 🛠️ BAUEN & AUSFÜHREN

Sie brauchen Python 3.10 oder neuer; es gibt nichts zu installieren.

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
```

## 🔗 Verwandte Projekte

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): der Projektcontainer und die Maschinentypen
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): die Leser für Gerber, Excellon und G-Code
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER): installiert und aktualisiert die Repositories der Suite

## 📚 Dokumentation & Community

* [Die Karte der Suite](docs/SUITE_MAP.md), [die Architektur](docs/ARCHITECTURE.md), [die Fähigkeitsmatrix](docs/CAPABILITY_MATRIX.md) und [die Konventionen](docs/CONVENTIONS.md) (auf Englisch).
* [Mitwirken](CONTRIBUTING.md), [Sicherheitsrichtlinie](SECURITY.md), [Support](SUPPORT.md) und [Verhaltenskodex](CODE_OF_CONDUCT.md).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LIZENZ

Software: GPL-3.0-or-later. Siehe [LICENSE](LICENSE).
