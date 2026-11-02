<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | 🇫🇷 <b>Français</b> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### La carte, l'architecture et l'état honnête de l'EH3D Fabrication Suite : à quoi sert chaque dépôt, ce qui a été testé et ce qui n'a pas encore tourné sur une machine

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Markdown%20%2B%20Python-blue.svg" alt="Markdown and Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.5-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-4CAF50.svg" alt="Maturity">
</p>

---

**Vérification d'honnêteté - ce qui tourne aujourd'hui :** des documents et les outils de la suite, qui tournent sur un ordinateur et nulle part ailleurs (le contrôle du dépôt et les dessinateurs des images que porte chaque dépôt, le contrat entre les dépôts, les scripts qui montent une version et préparent une publication, le script qui prépare un espace de travail et celui qui crée un nouveau dépôt). La suite en est à ses premiers pas : vingt-sept dépôts sont publiés (les bibliothèques, les programmes Bungard, le serveur et Studio, les nœuds et écrans tactiles, les applications mobiles, les programmes de FAO et utilitaires, les mises à jour et celui-ci) et la télécommande pour petits écrans tactiles est le seul programme qui reste un projet. Tout ce qui est publié a été testé sur un ordinateur et les interfaces parlent 37 langues ; dans toute la suite, seul le protocole série d'EH3D-DRILLPRO a déplacé une vraie machine (la référence et les mouvements de chaque axe sur une Bungard CCD MTC), et aucun travail complet n'a encore tourné sur une machine. 5 tests couvrent le contrôle du dépôt.

---

> **État de la sûreté et de la sécurité :** ce dépôt n'exécute rien sur une machine et n'est pas un système de sûreté. Un document d'ici ne remplace jamais les limites, les verrouillages et l'arrêt d'urgence de la machine et de son contrôleur.

## 📋 En un coup d'œil

| | |
|---|---|
| Version | `0.0.5` |
| Maturité | Fonctionnel |
| Tests | 144 |
| Pile technique | Markdown, avec des outils en Python 3.10+ |
| Sur du matériel réel | Sans objet : documentation |

**Aller à  :** [Présentation](#-présentation) · [Architecture](#-architecture) · [Démarrage rapide](#-démarrage-rapide) · [Tests](#-tests) · [Structure](#-structure-du-dépôt) · [Liés](#-projets-liés)

## 🚦 État du projet

Chaque ligne est une partie de ce dépôt et le feu dit où elle en est aujourd'hui. Elle est écrite d'après ce que le dépôt peut montrer (tests, compilations, exécutions), pas d'après ce qui est prévu.

🟢 Fait et vérifié · 🟡 Fonctionne, avec des limites connues · 🟠 À moitié fait ou pas encore vérifié · 🔴 Pas fait ou ne fonctionne pas

| Domaine | État | Ce que cela veut dire ici |
|---|---|---|
| Contrôles du dépôt | 🟡 | Le contrôle du dépôt, celui des liens entre les documents et les tests des outils tournent dans la CI et réussissent. |
| Tests | 🟠 | 144 tests des outils réussissent sur un ordinateur, certains sur de petits dépôts jouets ; les documents et les affirmations qu'ils contiennent sont lus et vérifiés à la main et par les scripts. |
| Contrat de la suite | 🟡 | Le contrat entre les dépôts lit chaque manifeste avec l'analyseur de l'Updater et signale les dérives (ports, langues du README, outils partagés, formulaires de tickets) ; il tourne chaque jour dans la CI comme simple avertissement, et les dépôts qu'il nomme sont remis à jour un par un. |
| Outils de version et de publication | 🟠 | Les scripts qui montent une version, écrivent les notes et vérifient une publication, ainsi que le workflow de validation réutilisable, sont testés sur des dépôts jouets ; aucun dépôt n'a encore publié de version avec eux. |
| Espace de travail et nouveaux dépôts | 🟠 | Les scripts qui listent et clonent ce dont un dépôt a besoin et qui créent un nouveau dépôt sont testés sur des dépôts jouets dans un dossier temporaire ; aucun n'a encore préparé un vrai espace de travail ni créé un vrai dépôt. |
| Carte et matrice des capacités | 🟡 | La carte de la suite, les notes d'architecture et la matrice des capacités couvrent les vingt-sept dépôts publiés, avec la version de chacun, et listent comme prévu le seul programme qui reste un projet ; elles sont écrites à la main et peuvent prendre du retard sur les dépôts. |
| Matériel réel | 🟡 | Sans objet : documentation, rien ici ne tourne sur du matériel. |
| Documentation | 🟡 | README en huit langues, vérifié à chaque changement contre le manifeste et le journal des modifications. |

## 🎯 Présentation

* **La carte de la suite :** chaque dépôt, à quoi il sert, et s'il est publié, commencé (du code avec des tests et pas encore de version) ou seulement prévu.
* **L'architecture :** les deux bibliothèques partagées, les programmes qui sont censés en dépendre et jamais les uns des autres, le nœud et le serveur qui atteignent la machine, et les règles que suit chaque dépôt.
* **La matrice des capacités :** ce qui est testé sur un ordinateur et ce qui a tourné sur une machine (seulement le protocole d'EH3D-DRILLPRO, sur une machine), pour que personne n'ait à deviner.
* **Les conventions :** le manifeste que porte chaque dépôt, le contrôle du dépôt et les fichiers README en huit langues.
* **Les contrôles et les outils :** le contrôle du dépôt, celui des liens entre les documents, les dessinateurs des deux images du README et les feux d'état, copiés dans chaque dépôt depuis celui-ci (`tools/sync_shared_tools.py` dit qui est en retard), et le vérificateur de la convention des codes de sortie; `banner_check.py` vérifie que le texte de chaque bannière dit ce que dit le manifeste, et `docs/vendored.lock` consigne l'origine et la version de chaque outil partagé.
* **Le contrat de la suite :** `tools/suite_contract.py` vérifie les relations qu'aucun dépôt ne peut vérifier seul : chaque manifeste est lisible avec l'analyseur de l'Updater et porte le nom de son dossier, une dépendance d'un voisin par chemin dit quelle version il lui faut, les versions de la carte sont celles des manifestes, les écrans et le serveur s'accordent sur le port, le validateur partagé est le même partout, `docs/suite.json` correspond aux endroits qui répètent ses valeurs et chaque dépôt a les formulaires de tickets. Il ne fait qu'avertir.
* **Versions, publications et nouveau travail :** `bump_version.py`, `release_notes.py`, `prerelease_check.py`, `readme_staleness.py` et `vendored_tools_report.py` ([docs/RELEASING.md](docs/RELEASING.md)), un workflow de validation réutilisable ([docs/REUSABLE_VALIDATION.md](docs/REUSABLE_VALIDATION.md)), `bootstrap_workspace.py` pour récupérer ce dont un dépôt a besoin et `new_repo.py` pour créer un nouveau dépôt. `bump_version.py` monte aussi les dépendances internes qui demandent une version minimale, les entrées `Cargo.lock` des paquets d'un espace de travail et le manifeste de l'actualisateur de toute la famille.
* **Comment on met à jour :** la CM5 de l'atelier est mise à jour **par releases** (`deploy/eh3d-update.py` d'EH3D-SERVER télécharge la release de GitHub dans `/opt`) ; EH3D-UPDATER est pour les **PC de développement, par git** ([docs/UPDATING.md](docs/UPDATING.md)).

## 🧩 Rôle dans EH3D

EH3D-DOCS est l'endroit où la suite est décrite dans son ensemble. Chaque dépôt se décrit dans son propre README ; celui-ci dit comment ils s'emboîtent, lesquels existent et ce qui a vraiment tourné.

## 🏛️ Architecture

<p align="center">
  <img src="images/architecture.svg" alt="Architecture de EH3D-DOCS : qui l'utilise, ce qu'il contient et de quoi il dépend" width="100%">
</p>

Comment les parties de ce dépôt s'articulent : qui l'utilise, ce qu'il contient et de quoi il dépend. L'image est dessinée à partir de `docs/architecture.json` et vérifiée par rapport au code.

## 🔒 Sécurité et protection

Ce dépôt n'a aucun programme qui reçoive des entrées de l'extérieur ; ce qu'il défend, c'est l'exactitude et la propreté de ce qu'il publie.

| Menace | Défense |
|---|---|
| Une affirmation selon laquelle la suite fait plus qu'elle ne fait | la matrice des capacités sépare « testé sur un ordinateur » de « exécuté sur une machine », et un dépôt est listé comme prévu tant qu'il n'a pas de code que quiconque peut exécuter |
| Une référence privée, une personne ou un outil qui ne doit pas être public | `tools/ci_validate.py` échoue sur les mots qui ne doivent jamais figurer dans un fichier public, dans chaque fichier texte |
| Un lien cassé entre les documents | `tools/check_links.py` échoue quand un lien relatif d'un fichier Markdown pointe vers un fichier inexistant |
| Une langue du README qui dérive des autres | le contrôle compare la structure des titres, les feux de l'état du projet et la version dans les huit fichiers |
| Des fichiers qui ne doivent pas être versionnés (compilations, clés, journaux, gros fichiers) | le contrôle du dépôt refuse les dossiers de compilation, les dossiers privés, les fichiers de clés et de journaux et les fichiers de plus de 1,5 Mo suivis par git |

## 🔌 Interfaces

| Interface | Ce que c'est | Où |
|---|---|---|
| Les documents | Markdown : la carte, l'architecture, la matrice des capacités et les conventions | [docs/](docs/SUITE_MAP.md) |
| Le contrôle du dépôt | `python -I tools/ci_validate.py` affiche `CI_VALIDATION=PASS` ou liste ce qui échoue | `tools/ci_validate.py` |
| Le contrôle des liens | `python -I tools/check_links.py` affiche `LINKS=PASS` ou liste les liens cassés | `tools/check_links.py` |
| Les tests du contrôle | `python -I -m unittest discover -s tools -p "test_*.py"` | `tools/test_ci_validate.py` |
| Le contrat de la suite | `python -I tools/suite_contract.py --workspace ..` affiche `SUITE_CONTRACT=PASS` ou liste les constats ; `--write-map` met les versions des manifestes dans la carte | `tools/suite_contract.py` |
| Les outils partagés | `python -I tools/sync_shared_tools.py` dit quels dépôts ont une copie différente | `tools/sync_shared_tools.py` |
| Versions et publications | `bump_version.py`, `release_notes.py`, `prerelease_check.py`, `readme_staleness.py`, `vendored_tools_report.py` | [docs/RELEASING.md](docs/RELEASING.md) |
| Le workflow réutilisable | validation avec `on: workflow_call`, à appeler depuis les dépôts | [docs/REUSABLE_VALIDATION.md](docs/REUSABLE_VALIDATION.md) |
| L'espace de travail | `bootstrap_workspace.py` liste et clone ce dont un dépôt a besoin ; `new_repo.py` crée un nouveau dépôt | `tools/bootstrap_workspace.py`, `tools/new_repo.py` |
| Les codes de sortie | `0`, `1`, `2`, `10` et `64` ; `exit_conventions.py` y confronte les outils | [docs/CONVENTIONS.md](docs/CONVENTIONS.md) |

## ⚙️ Configuration

Les outils demandent Python 3.10 ou plus récent et aucune installation, et lisent les fichiers du dépôt où ils se trouvent. Les règles qu'ils appliquent sont dans le code de `tools/ci_validate.py`, et les valeurs de la suite que plusieurs dépôts répètent sont dans `docs/suite.json` :

| Règle | Limite | Où |
|---|---|---|
| Taille d'un fichier versionné | au plus 1 500 000 octets | `MAX_TRACKED_BYTES` |
| Langues du README | huit fichiers, avec la même structure de titres et les mêmes feux | `LANGUAGES` |
| Champs du manifeste | les 14 champs de `REQUIRED` ; la version du manifeste égale celle de `VERSION` (`native_version`) et de l'entrée la plus récente du journal des modifications | `REQUIRED` |
| Les constantes de la suite | le port du serveur, le schéma du manifeste, les huit langues du README, le champ de rpm, la forme d'une version, les formulaires de tickets | `docs/suite.json` |
| Exceptions connues du contrat | un `check dépôt` par ligne, retiré quand la cause est corrigée | `docs/suite_contract_allow.txt` |
| Ce qu'un dépôt ajoute au contrôle | par exemple les dossiers que la recherche de mots interdits ignore | `tools/ci_config.json` de chaque dépôt |

## 🚀 Démarrage rapide

Il faut Python 3.10 ou plus récent ; il n'y a rien à installer.

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
python -I tools/suite_contract.py --workspace ..
python -I tools/bootstrap_workspace.py --workspace .. EH3D-DRILLPRO
python -I -m unittest discover -s tools -p "test_*.py"
```

Pour lire les documents, commence par [la carte de la suite](docs/SUITE_MAP.md).

## 🧪 Tests

Les outils ont 144 tests (`python -I -m unittest discover -s tools -p "test_*.py"`), et ils réussissent. La CI exécute le contrôle du dépôt (`tools/ci_validate.py`), celui des liens entre les documents (`tools/check_links.py`), les contrôles des deux images et ces tests ; un workflow quotidien exécute le contrat de la suite. Les documents n'ont pas d'autre test : ce qu'ils affirment est tenu honnête par la matrice des capacités et par leur relecture.

## 🏗️ Compilation et publication

La version se trouve dans le fichier `VERSION` et dans `eh3d.project.json`, et chaque version a son entrée dans [CHANGELOG.md](CHANGELOG.md). Il n'y a rien à compiler ; les versions sont publiées sur GitHub.

## 📂 Structure du dépôt

<p align="center">
  <img src="images/repository-structure.svg" alt="Structure du dépôt EH3D-DOCS" width="100%">
</p>

<details>
<summary>Version texte de l'arborescence</summary>

```text
EH3D-DOCS/
├── docs/
│   ├── SUITE_MAP.md                             chaque dépôt et s'il existe déjà
│   ├── ARCHITECTURE.md                          les couches et les règles
│   ├── CAPABILITY_MATRIX.md                     ce qui a été testé et ce qui a tourné sur une machine
│   ├── CONVENTIONS.md                           le manifeste, le contrôle, les README
│   ├── UPDATING.md                              mise à jour de la CM5 et d'un PC
│   ├── RELEASING.md                             monter une version et publier avec les scripts
│   ├── REUSABLE_VALIDATION.md                   le workflow de validation que les dépôts peuvent appeler
│   ├── VENDORED_TOOLS_REPORT.md                 les outils copiés dans les dépôts que rien n'utilise
│   ├── suite.json                               les constantes de la suite
│   ├── suite_contract_allow.txt                 les exceptions connues du contrat
│   ├── templates/                               le modèle d'un nouveau dépôt
│   └── architecture.json structure.json         les données des deux images
├── tools/                                       les contrôles, le contrat, les scripts de version et de publication et leurs tests
├── images/                                      bannière et images d'Architecture et de Structure du dépôt
├── .github/                                     workflows de CI et du tableau de bord, modèles d'issues et de pull requests
├── eh3d.project.json                            manifeste : version, rôle, maturité et commande de compilation
├── VERSION                                      la version des documents
├── CHANGELOG.md                                 ce qui a changé dans chaque version
├── SECURITY.md SUPPORT.md                       signaler une vulnérabilité et poser des questions
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   contribuer, code de conduite et licence
```

</details>

## 🗺️ Feuille de route et limites connues

**Limites connues aujourd'hui**

* La carte, les notes d'architecture et la matrice des capacités sont écrites à la main ; rien ne les compare aux manifestes des dépôts, elles peuvent donc prendre du retard.
* Seuls les dépôts publiés sont décrits en détail ; les programmes commencés et les programmes prévus sont chacun une ligne de la carte, marquée comme telle.
* Les documents n'ont pas de test propre au-delà du contrôle du dépôt et du contrôle des liens.
* Les scripts de publication, d'espace de travail et de nouveau dépôt n'ont été essayés que sur des dépôts jouets ; aucun n'a encore servi pour une vraie publication ni pour créer un vrai dépôt.
* Le contrat de la suite ne fait qu'avertir, et plusieurs dépôts gardent encore une copie plus ancienne du validateur partagé.

**Ensuite**

* Garder la carte et la matrice des capacités au rythme de chaque dépôt quand il est publié ou change.
* Comparer la carte aux manifestes des dépôts, pour qu'un nouveau dépôt ne puisse pas y manquer.
* Utiliser les scripts pour la prochaine vraie publication, adopter le workflow réutilisable dans les dépôts et rendre le contrat de la suite bloquant une fois ses constats connus disparus.

## 🌍 Langues

Le README et les textes existent en anglais, espagnol, français, italien, allemand, chinois, japonais et portugais européen.

## 🔗 Projets liés

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON) : le conteneur de projet, les types de machine et la base de firmware des nœuds
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS) : les lecteurs de Gerber, Excellon et G-code
* [EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO) et [EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO) : les programmes de perçage et de défonçage
* [EH3D-BUNGARD-GUI](https://github.com/JuanenRac/EH3D-BUNGARD-GUI) et [EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC) : l'interface moderne des machines Bungard et le programme de commande de machine
* [EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER) et [EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD) : le centre des programmes et le nœud qui atteint la machine
* [EH3D-STUDIO](https://github.com/JuanenRac/EH3D-STUDIO), [EH3D-NODE-BUNGARD-HMI](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-HMI) et [EH3D-NODE-BUNGARD-AUX](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-AUX) : le panneau de configuration du serveur (avec ses mises à jour depuis GitHub), l'écran tactile de la machine et le nœud de la tête de perçage (caméra en RTSP et ONVIF, laser qui mesure la table, vitesse et température de la broche)
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) et [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) : installent et mettent à jour les dépôts

## 📚 Documentation

* [La carte de la suite](docs/SUITE_MAP.md), [l'architecture](docs/ARCHITECTURE.md), [la matrice des capacités](docs/CAPABILITY_MATRIX.md) et [les conventions](docs/CONVENTIONS.md).
* [Publier une version](docs/RELEASING.md) et [la validation réutilisable](docs/REUSABLE_VALIDATION.md).
* [Journal des modifications](CHANGELOG.md)

## 🤝 Contribuer et communauté

* Avant une pull request, exécutez `python -I tools/ci_validate.py`, `python -I tools/check_links.py` et les tests des outils : tout doit réussir. Voir [CONTRIBUTING.md](CONTRIBUTING.md) et le [code de conduite](CODE_OF_CONDUCT.md).
* Le README existe en huit langues : une modification du texte se fait dans les huit fichiers, et les deux images sont dessinées à partir de `docs/architecture.json` et `docs/structure.json` par `tools/make_architecture.py` et `tools/make_structure.py`.
* Ne décris pas comme fonctionnant sur une machine ce qui n'a été essayé que sur un ordinateur : la matrice des capacités dit lequel est lequel.
* Signalez une vulnérabilité en privé : [SECURITY.md](SECURITY.md). Questions, idées et rapports : electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTEUR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCE

Logiciel : GPL-3.0-or-later. Voir [LICENSE](LICENSE). Les conceptions matérielles de la suite utilisent la CERN OHL-S.
