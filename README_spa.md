<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | 🇪🇸 <b>Español</b> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### El mapa, la arquitectura y el estado honesto de la EH3D Fabrication Suite: para qué sirve cada repositorio, qué se ha probado y qué aún no se ha ejecutado en una máquina

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Docs-Markdown-blue.svg" alt="Markdown">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Comprobación de honestidad - lo que hay hoy:** documentos y dos pequeñas comprobaciones. La suite está en sus primeros pasos: hay tres repositorios publicados (EH3D-COMMON con el contenedor de proyecto, EH3D-CORE-LIBS con lectores de Gerber, Excellon y G-code, y EH3D-UPDATER) y cada programa de la suite es un plan. Todo lo publicado se ha probado en un ordenador; nada se ha ejecutado en una máquina.

---

> **Estado de seguridad (safety) y de seguridad informática:** este repositorio no ejecuta nada en una máquina y no es un sistema de seguridad. Un documento de aquí nunca sustituye los límites, enclavamientos y la parada de emergencia de la máquina y su controlador.

## 📋 De un vistazo

| | |
|---|---|
| Versión | `0.0.1` |
| Madurez | Andamiaje |
| Pila tecnológica | Markdown / Python 3.10+ (las comprobaciones) |
| En hardware real | No aplica: documentación |

## 🎯 Descripción general

* **El mapa de la suite:** cada repositorio, para qué sirve y si está publicado o solo planificado.
* **La arquitectura:** las dos bibliotecas compartidas, los programas que dependen de ellas y nunca entre sí, y las reglas que sigue todo repositorio.
* **La matriz de capacidades:** qué está probado en un ordenador y qué se ha ejecutado en una máquina (nada todavía), para que nadie tenga que adivinar.
* **Las convenciones:** el manifiesto que lleva cada repositorio, la comprobación del repositorio y los README en ocho idiomas.
* **Dos comprobaciones:** la del repositorio y la de los enlaces entre los documentos, ambas en el CI.

## 📂 Estructura del repositorio

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

## 🛠️ COMPILAR Y EJECUTAR

Necesitas Python 3.10 o más reciente; no hay nada que instalar.

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
```

## 🔗 Proyectos relacionados

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): el contenedor de proyecto y los tipos de máquina
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): los lectores de Gerber, Excellon y G-code
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER): instala y actualiza los repositorios de la suite

## 📚 Documentación y comunidad

* [El mapa de la suite](docs/SUITE_MAP.md), [la arquitectura](docs/ARCHITECTURE.md), [la matriz de capacidades](docs/CAPABILITY_MATRIX.md) y [las convenciones](docs/CONVENTIONS.md) (en inglés).
* [Cómo contribuir](CONTRIBUTING.md), [política de seguridad](SECURITY.md), [soporte](SUPPORT.md) y [código de conducta](CODE_OF_CONDUCT.md).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCIA

Software: GPL-3.0-or-later. Véase [LICENSE](LICENSE).
