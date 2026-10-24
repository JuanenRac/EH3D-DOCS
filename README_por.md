<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | 🇵🇹 <b>Português</b></p>

### O mapa, a arquitetura e o estado honesto da EH3D Fabrication Suite: para que serve cada repositório, o que foi testado e o que ainda não correu numa máquina

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Docs-Markdown-blue.svg" alt="Markdown">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Verificação de honestidade - o que existe hoje:** documentos e duas pequenas verificações. A suite está nos primeiros passos: há três repositórios publicados (EH3D-COMMON com o contentor de projeto, EH3D-CORE-LIBS com leitores de Gerber, Excellon e G-code, e EH3D-UPDATER) e cada programa da suite é um plano. Tudo o que está publicado foi testado num computador; nada correu numa máquina.

---

> **Estado de segurança (safety) e de segurança informática:** este repositório não executa nada numa máquina e não é um sistema de segurança. Um documento daqui nunca substitui os limites, os bloqueios e a paragem de emergência da máquina e do seu controlador.

## 📋 Num relance

| | |
|---|---|
| Versão | `0.0.1` |
| Maturidade | Andaime |
| Pilha tecnológica | Markdown / Python 3.10+ (as verificações) |
| Em hardware real | Não aplicável: documentação |

## 🚦 Estado do projeto

Cada linha é uma parte deste repositório e a luz diz até onde chega hoje. É escrita com o que o repositório consegue demonstrar (testes, compilações, execuções), não com o que está previsto.

🟢 Feito e verificado · 🟡 Funciona, com limites conhecidos · 🟠 Feito a meio ou ainda por verificar · 🔴 Por fazer ou a não funcionar

| Área | Estado | O que significa aqui |
|---|---|---|
| Verificações do repositório | 🟢 | A verificação do repositório e a das ligações entre documentos correm no CI e passam. |
| Testes | 🟠 | Não tem um conjunto de testes próprio: as únicas verificações automáticas são esses dois scripts. |
| Mapa e matriz de capacidades | 🟠 | O mapa, as notas de arquitetura e a matriz de capacidades só cobrem os três primeiros repositórios publicados; EH3D-DRILLPRO, EH3D-ROUTEPRO, EH3D-SERVER e EH3D-NODE-BUNGARD ainda não constam. |
| Hardware real | 🟢 | Não se aplica: é documentação, nada aqui corre em hardware. |
| Documentação | 🟢 | README em oito idiomas, verificado contra o manifesto e o registo de alterações a cada alteração. |

## 🎯 Visão geral

* **O mapa da suite:** cada repositório, para que serve e se está publicado ou apenas planeado.
* **A arquitetura:** as duas bibliotecas partilhadas, os programas que dependem delas e nunca uns dos outros, e as regras que todo o repositório segue.
* **A matriz de capacidades:** o que está testado num computador e o que correu numa máquina (ainda nada), para que ninguém tenha de adivinhar.
* **As convenções:** o manifesto que cada repositório leva, a verificação do repositório e os README em oito idiomas.
* **Duas verificações:** a do repositório e a das ligações entre os documentos, ambas no CI.

## 📂 Estrutura do repositório

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

## 🛠️ COMPILAR E EXECUTAR

Precisa de Python 3.10 ou mais recente; não há nada para instalar.

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
```

## 🔗 Projetos relacionados

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): o contentor de projeto e os tipos de máquina
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): os leitores de Gerber, Excellon e G-code
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER): instala e atualiza os repositórios da suite

## 📚 Documentação e comunidade

* [O mapa da suite](docs/SUITE_MAP.md), [a arquitetura](docs/ARCHITECTURE.md), [a matriz de capacidades](docs/CAPABILITY_MATRIX.md) e [as convenções](docs/CONVENTIONS.md) (em inglês).
* [Como contribuir](CONTRIBUTING.md), [política de segurança](SECURITY.md), [suporte](SUPPORT.md) e [código de conduta](CODE_OF_CONDUCT.md).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENÇA

Software: GPL-3.0-or-later. Consulte [LICENSE](LICENSE).
