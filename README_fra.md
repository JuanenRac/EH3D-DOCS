<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | 🇫🇷 <b>Français</b> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### La carte, l'architecture et l'état honnête de l'EH3D Fabrication Suite : à quoi sert chaque dépôt, ce qui a été testé et ce qui n'a pas encore tourné sur une machine

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Docs-Markdown-blue.svg" alt="Markdown">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Vérification d'honnêteté - ce qui existe aujourd'hui :** des documents et deux petites vérifications. La suite en est à ses premiers pas : trois dépôts sont publiés (EH3D-COMMON avec le conteneur de projet, EH3D-CORE-LIBS avec des lecteurs de Gerber, Excellon et G-code, et EH3D-UPDATER) et chaque programme de la suite est un projet. Tout ce qui est publié a été testé sur un ordinateur ; rien n'a tourné sur une machine.

---

> **État de la sûreté et de la sécurité :** ce dépôt ne fait rien tourner sur une machine et n'est pas un système de sûreté. Un document d'ici ne remplace jamais les limites, verrouillages et l'arrêt d'urgence de la machine et de son contrôleur.

## 📋 En un coup d'œil

| | |
|---|---|
| Version | `0.0.1` |
| Maturité | Échafaudage |
| Pile technique | Markdown / Python 3.10+ (les vérifications) |
| Sur matériel réel | Sans objet : documentation |

## 🎯 Vue d'ensemble

* **La carte de la suite :** chaque dépôt, à quoi il sert et s'il est publié ou seulement prévu.
* **L'architecture :** les deux bibliothèques partagées, les programmes qui en dépendent sans jamais dépendre les uns des autres, et les règles que suit tout dépôt.
* **La matrice des capacités :** ce qui est testé sur un ordinateur et ce qui a tourné sur une machine (rien encore), pour que personne n'ait à deviner.
* **Les conventions :** le manifeste de chaque dépôt, la vérification du dépôt et les README en huit langues.
* **Deux vérifications :** celle du dépôt et celle des liens entre les documents, toutes deux dans le CI.

## 📂 Structure du dépôt

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

## 🛠️ COMPILER ET EXÉCUTER

Il faut Python 3.10 ou plus récent ; il n'y a rien à installer.

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
```

## 🔗 Projets liés

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): le conteneur de projet et les types de machine
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): les lecteurs de Gerber, Excellon et G-code
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER): installe et met à jour les dépôts de la suite

## 📚 Documentation et communauté

* [La carte de la suite](docs/SUITE_MAP.md), [l'architecture](docs/ARCHITECTURE.md), [la matrice des capacités](docs/CAPABILITY_MATRIX.md) et [les conventions](docs/CONVENTIONS.md) (en anglais).
* [Contribuer](CONTRIBUTING.md), [politique de sécurité](SECURITY.md), [support](SUPPORT.md) et [code de conduite](CODE_OF_CONDUCT.md).

## 👤 AUTEUR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCE

Logiciel : GPL-3.0-or-later. Voir [LICENSE](LICENSE).
