<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | 🇪🇸 <b>Español</b> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### El mapa, la arquitectura y el estado honesto de la EH3D Fabrication Suite: para qué sirve cada repositorio, qué se ha probado y qué todavía no se ha ejecutado en una máquina

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Markdown%20%2B%20Python-blue.svg" alt="Markdown and Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Comprobación de honestidad - lo que se ejecuta hoy:** documentos y dos pequeñas comprobaciones. La suite está en sus primeros pasos: hay catorce repositorios publicados (EH3D-COMMON, EH3D-CORE-LIBS, EH3D-DRILLPRO, EH3D-ROUTEPRO, EH3D-BUNGARD-GUI, EH3D-MOTIONCNC, EH3D-SERVER, EH3D-STUDIO, EH3D-NODE-BUNGARD, EH3D-NODE-BUNGARD-HMI, EH3D-NODE-BUNGARD-AUX, EH3D-UPDATER, ELECTRO-HOBBY-3D-UPDATER y este) y cualquier otro programa de la suite es un plan. Todo lo publicado se ha probado en un ordenador; de toda la suite solo el protocolo serie de EH3D-DRILLPRO ha movido una máquina real (la referencia y los movimientos de cada eje en una Bungard CCD MTC), y ningún trabajo completo se ha ejecutado todavía en una máquina. 5 pruebas cubren la comprobación del repositorio.

---

> **Estado de seguridad (safety) y de seguridad informática:** este repositorio no ejecuta nada en una máquina y no es un sistema de seguridad (safety). Un documento de aquí nunca sustituye los límites, los enclavamientos y la parada de emergencia de la máquina y de su controlador.

## 📋 De un vistazo

| | |
|---|---|
| Versión | `0.0.1` |
| Madurez | Andamiaje |
| Pruebas | 5 |
| Pila tecnológica | Markdown, con dos comprobaciones en Python 3.10+ |
| En hardware real | No aplica: documentación |

**Ir a:** [Resumen](#-resumen) · [Arquitectura](#-arquitectura) · [Inicio rápido](#-inicio-rápido) · [Pruebas](#-pruebas) · [Estructura](#-estructura-del-repositorio) · [Relacionados](#-proyectos-relacionados)

## 🚦 Estado del proyecto

Cada línea es una parte de este repositorio y la luz dice hasta dónde llega hoy. Se escribe con lo que el repositorio puede demostrar (pruebas, compilaciones, ejecuciones), no con lo previsto.

🟢 Hecho y verificado · 🟡 Funciona, con límites conocidos · 🟠 Hecho a medias o sin verificar · 🔴 Sin hacer o sin funcionar

| Área | Estado | Qué significa aquí |
|---|---|---|
| Comprobaciones del repositorio | 🟡 | La comprobación del repositorio, la de los enlaces entre los documentos y las 5 pruebas de la comprobación del repositorio se ejecutan en el CI y pasan. |
| Pruebas | 🟠 | Solo la comprobación del repositorio tiene pruebas (5); los documentos y las afirmaciones que contienen se leen y comprueban a mano y con los dos scripts. |
| Mapa y matriz de capacidades | 🟡 | El mapa de la suite, las notas de arquitectura y la matriz de capacidades cubren los once repositorios publicados y listan cualquier otro programa como previsto; se escriben a mano y pueden quedar por detrás de los repositorios. |
| Hardware real | 🟡 | No aplica: documentación, nada aquí se ejecuta en hardware. |
| Documentación | 🟡 | README en ocho idiomas, comprobado contra el manifiesto y el registro de cambios en cada cambio. |

## 🎯 Resumen

* **El mapa de la suite:** cada repositorio, para qué sirve y si está publicado o solo previsto.
* **La arquitectura:** las dos bibliotecas compartidas, los programas que deben depender de ellas y nunca entre sí, el nodo y el servidor que llegan a la máquina, y las reglas que sigue cada repositorio.
* **La matriz de capacidades:** qué se ha probado en un ordenador y qué se ha ejecutado en una máquina (solo el protocolo de EH3D-DRILLPRO, en una máquina), para que nadie tenga que adivinar.
* **Las convenciones:** el manifiesto que lleva cada repositorio, la comprobación del repositorio y los ficheros README en ocho idiomas.
* **Dos comprobaciones:** la comprobación del repositorio y una de los enlaces entre los documentos, ambas en el CI.

## 🧩 Papel en EH3D

EH3D-DOCS es donde se describe la suite en su conjunto. Cada repositorio se describe a sí mismo en su README; este dice cómo encajan, cuáles existen y qué se ha ejecutado de verdad.

## 🏛️ Arquitectura

<p align="center">
  <img src="images/architecture.svg" alt="Arquitectura de EH3D-DOCS: quién lo usa, qué contiene y de qué depende" width="100%">
</p>

Cómo encajan las partes de este repositorio: quién lo usa, qué contiene y de qué depende. La imagen se dibuja desde `docs/architecture.json` y se comprueba contra el código.

## 🔒 Seguridad y protección

Este repositorio no tiene ningún programa que reciba entradas de fuera; lo que defiende es la exactitud y la limpieza de lo que publica.

| Amenaza | Defensa |
|---|---|
| Una afirmación de que la suite hace más de lo que hace | la matriz de capacidades separa «probado en un ordenador» de «ejecutado en una máquina», y un repositorio figura como previsto hasta que tenga código que cualquiera pueda ejecutar |
| Una referencia privada, una persona o una herramienta que no debe ser pública | `tools/ci_validate.py` falla con las palabras que nunca deben aparecer en un fichero público, en cada fichero de texto |
| Un enlace roto entre los documentos | `tools/check_links.py` falla cuando un enlace relativo de un fichero Markdown apunta a un fichero que no existe |
| Un idioma del README que se desvía de los demás | la comprobación compara la estructura de los encabezados, los semáforos del estado del proyecto y la versión en los ocho ficheros |
| Ficheros que no deben versionarse (compilaciones, claves, registros, ficheros grandes) | la comprobación del repositorio rechaza carpetas de compilación, carpetas privadas, ficheros de claves y de registros y ficheros de más de 1,5 MB bajo control de versiones |

## 🔌 Interfaces

| Interfaz | Qué es | Dónde |
|---|---|---|
| Los documentos | Markdown: el mapa, la arquitectura, la matriz de capacidades y las convenciones | [docs/](docs/SUITE_MAP.md) |
| La comprobación del repositorio | `python -I tools/ci_validate.py` imprime `CI_VALIDATION=PASS` o lista lo que falla | `tools/ci_validate.py` |
| La comprobación de enlaces | `python -I tools/check_links.py` imprime `LINKS=PASS` o lista los enlaces rotos | `tools/check_links.py` |
| Las pruebas de la comprobación | `python -I -m unittest discover -s tools -p "test_*.py"` | `tools/test_ci_validate.py` |

## ⚙️ Configuración

No hay nada que configurar: las dos comprobaciones necesitan Python 3.10 o posterior y ninguna instalación, y leen los ficheros del repositorio en el que viven. Las reglas que aplican están en el código de `tools/ci_validate.py`:

| Regla | Límite | Dónde |
|---|---|---|
| Tamaño de un fichero versionado | como máximo 1 500 000 bytes | `MAX_TRACKED_BYTES` |
| Idiomas del README | ocho ficheros, con la misma estructura de encabezados y los mismos semáforos | `LANGUAGES` |
| Campos del manifiesto | los 14 campos de `REQUIRED`; la versión del manifiesto es la de `VERSION` (`native_version`) y la de la entrada más reciente del registro de cambios | `REQUIRED` |

## 🚀 Inicio rápido

Necesitas Python 3.10 o posterior; no hay nada que instalar.

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
python -I -m unittest discover -s tools -p "test_*.py"
```

Para leer los documentos, empieza por [el mapa de la suite](docs/SUITE_MAP.md).

## 🧪 Pruebas

La comprobación del repositorio tiene 5 pruebas (`python -I -m unittest discover -s tools -p "test_*.py"`), y pasan. El CI ejecuta la comprobación del repositorio (`tools/ci_validate.py`), la de los enlaces entre los documentos (`tools/check_links.py`) y esas pruebas. Los documentos en sí no tienen más pruebas: lo que afirman se mantiene honesto leyendo los repositorios que describen.

## 🏗️ Compilación y publicación

La versión vive en el fichero `VERSION` y en `eh3d.project.json`, y cada versión tiene su entrada en [CHANGELOG.md](CHANGELOG.md). No hay nada que compilar; las versiones se publican en GitHub.

## 📂 Estructura del repositorio

<p align="center">
  <img src="images/repository-structure.svg" alt="Estructura del repositorio EH3D-DOCS" width="100%">
</p>

<details>
<summary>Versión en texto del árbol</summary>

```text
EH3D-DOCS/
├── docs/
│   ├── SUITE_MAP.md                             cada repositorio y si existe ya
│   ├── ARCHITECTURE.md                          las capas y las reglas
│   ├── CAPABILITY_MATRIX.md                     qué se ha probado y qué se ha ejecutado en una máquina
│   ├── CONVENTIONS.md                           el manifiesto, la comprobación, los README
│   └── architecture.json structure.json         los datos de las dos imágenes
├── tools/                                       la comprobación del repositorio, la de enlaces, sus pruebas y las herramientas de imágenes
├── images/                                      banner y las imágenes de Arquitectura y Estructura del repositorio
├── .github/                                     flujos de CI y de publicación, plantillas de issues y pull requests
├── eh3d.project.json                            manifiesto: versión, rol, madurez y comando de compilación
├── VERSION                                      la versión de los documentos
├── CHANGELOG.md                                 qué cambió en cada versión
├── SECURITY.md SUPPORT.md                       cómo informar de una vulnerabilidad y dónde preguntar
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   cómo contribuir, el código de conducta y la licencia
```

</details>

## 🗺️ Hoja de ruta y límites conocidos

**Límites conocidos hoy**

* El mapa, las notas de arquitectura y la matriz de capacidades se escriben a mano; nada los comprueba contra los manifiestos de los repositorios, así que pueden quedar por detrás.
* Solo los repositorios publicados se describen con detalle; cualquier otro programa es una línea del mapa marcada como prevista.
* Los documentos no tienen más pruebas propias que la comprobación del repositorio y la de los enlaces.

**Siguiente**

* Mantener el mapa y la matriz de capacidades al ritmo de cada repositorio cuando se publica o cambia.
* Comprobar el mapa contra los manifiestos de los repositorios, para que un repositorio nuevo no pueda faltar en él.

## 🌍 Idiomas

El README y los textos existen en inglés, español, francés, italiano, alemán, chino, japonés y portugués de Portugal.

## 🔗 Proyectos relacionados

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): el contenedor de proyecto, los tipos de máquina y la base de firmware de los nodos
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): los lectores de Gerber, Excellon y G-code
* [EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO) y [EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO): los programas de taladrado y de fresado
* [EH3D-BUNGARD-GUI](https://github.com/JuanenRac/EH3D-BUNGARD-GUI) y [EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC): la interfaz moderna de las máquinas Bungard y el programa de control de máquina
* [EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER) y [EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD): el centro de los programas y el nodo que llega a la máquina
* [EH3D-STUDIO](https://github.com/JuanenRac/EH3D-STUDIO), [EH3D-NODE-BUNGARD-HMI](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-HMI) y [EH3D-NODE-BUNGARD-AUX](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-AUX): el panel de configuración del servidor (con sus actualizaciones desde GitHub), la pantalla táctil de la máquina y el nodo del cabezal de taladro (cámara por RTSP y ONVIF, láser que mide la mesa, velocidad y temperatura del husillo)
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) y [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): instalan y actualizan los repositorios

## 📚 Documentación

* [El mapa de la suite](docs/SUITE_MAP.md), [la arquitectura](docs/ARCHITECTURE.md), [la matriz de capacidades](docs/CAPABILITY_MATRIX.md) y [las convenciones](docs/CONVENTIONS.md).
* [Registro de cambios](CHANGELOG.md)

## 🤝 Contribuir y comunidad

* Antes de una pull request ejecuta `python -I tools/ci_validate.py`, `python -I tools/check_links.py` y las pruebas de la comprobación: todo debe pasar. Consulta [CONTRIBUTING.md](CONTRIBUTING.md) y el [código de conducta](CODE_OF_CONDUCT.md).
* El README existe en ocho idiomas: un cambio en el texto se hace en los ocho archivos, y las dos imágenes se dibujan a partir de `docs/architecture.json` y `docs/structure.json` con `tools/make_architecture.py` y `tools/make_structure.py`.
* No describas como funcionando en una máquina lo que solo se ha probado en un ordenador: la matriz de capacidades dice cuál es cuál.
* Informa de una vulnerabilidad en privado: [SECURITY.md](SECURITY.md). Preguntas, ideas e informes: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCIA

Software: GPL-3.0-or-later. Véase [LICENSE](LICENSE). Los diseños de hardware de la suite usan CERN OHL-S.
