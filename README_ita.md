<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | 🇮🇹 <b>Italiano</b> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### La mappa, l'architettura e lo stato onesto della EH3D Fabrication Suite: a cosa serve ogni repository, cosa è stato provato e cosa non è ancora stato eseguito su una macchina

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Docs-Markdown-blue.svg" alt="Markdown">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Controllo di onestà - cosa c'è oggi:** documenti e due piccoli controlli. La suite è ai primi passi: sono pubblicati tre repository (EH3D-COMMON con il contenitore di progetto, EH3D-CORE-LIBS con lettori di Gerber, Excellon e G-code, ed EH3D-UPDATER) e ogni programma della suite è un piano. Tutto ciò che è pubblicato è stato provato su un computer; nulla è stato eseguito su una macchina.

---

> **Stato di sicurezza (safety) e di sicurezza informatica:** questo repository non esegue nulla su una macchina e non è un sistema di sicurezza. Un documento di qui non sostituisce mai i limiti, gli interblocchi e l'arresto di emergenza della macchina e del suo controllore.

## 📋 In breve

| | |
|---|---|
| Versione | `0.0.1` |
| Maturità | Impalcatura |
| Stack tecnologico | Markdown / Python 3.10+ (i controlli) |
| Su hardware reale | Non applicabile: documentazione |

## 🎯 Panoramica

* **La mappa della suite:** ogni repository, a cosa serve e se è pubblicato o solo pianificato.
* **L'architettura:** le due librerie condivise, i programmi che ne dipendono e mai l'uno dall'altro, e le regole che ogni repository segue.
* **La matrice delle capacità:** cosa è provato su un computer e cosa è stato eseguito su una macchina (ancora nulla), così nessuno deve indovinare.
* **Le convenzioni:** il manifest di ogni repository, il controllo del repository e i README in otto lingue.
* **Due controlli:** quello del repository e quello dei link tra i documenti, entrambi nel CI.

## 📂 Struttura del repository

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

## 🛠️ COMPILARE ED ESEGUIRE

Serve Python 3.10 o più recente; non c'è nulla da installare.

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
```

## 🔗 Progetti correlati

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): il contenitore di progetto e i tipi di macchina
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): i lettori di Gerber, Excellon e G-code
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER): installa e aggiorna i repository della suite

## 📚 Documentazione e comunità

* [La mappa della suite](docs/SUITE_MAP.md), [l'architettura](docs/ARCHITECTURE.md), [la matrice delle capacità](docs/CAPABILITY_MATRIX.md) e [le convenzioni](docs/CONVENTIONS.md) (in inglese).
* [Contribuire](CONTRIBUTING.md), [politica di sicurezza](SECURITY.md), [supporto](SUPPORT.md) e [codice di condotta](CODE_OF_CONDUCT.md).

## 👤 AUTORE

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENZA

Software: GPL-3.0-or-later. Vedi [LICENSE](LICENSE).
