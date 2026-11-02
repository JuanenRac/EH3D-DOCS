<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | 🇵🇹 <b>Português</b></p>

### O mapa, a arquitetura e o estado honesto da EH3D Fabrication Suite: para que serve cada repositório, o que foi testado e o que ainda não foi executado numa máquina

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Markdown%20%2B%20Python-blue.svg" alt="Markdown and Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.5-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-4CAF50.svg" alt="Maturity">
</p>

---

**Verificação de honestidade - o que funciona hoje:** documentos e as ferramentas da suite, que correm num computador e em mais lado nenhum (a verificação do repositório e os desenhadores das imagens que cada repositório leva, o contrato entre os repositórios, os scripts que sobem uma versão e preparam uma publicação, o script que prepara um espaço de trabalho e o que cria um repositório novo). A suite está nos primeiros passos: estão publicados vinte e sete repositórios (as bibliotecas, os programas Bungard, o servidor e o Studio, os nós e os ecrãs táteis, as aplicações de telemóvel, os programas de CAM e de utilidade, os atualizadores e este) e o comando para ecrãs táteis pequenos é o único programa que continua a ser um plano. Tudo o que está publicado foi testado num computador e as interfaces falam 37 idiomas; de toda a suite só o protocolo série do EH3D-DRILLPRO moveu uma máquina real (a referência e os movimentos de cada eixo numa Bungard CCD MTC), e nenhum trabalho completo correu ainda numa máquina. 5 testes cobrem a verificação do repositório.

---

> **Estado de segurança (safety) e de segurança informática:** este repositório não executa nada numa máquina e não é um sistema de segurança (safety). Um documento daqui nunca substitui os limites, os bloqueios e a paragem de emergência da máquina e do seu controlador.

## 📋 Num relance

| | |
|---|---|
| Versão | `0.0.5` |
| Maturidade | Funcional |
| Testes | 126 |
| Tecnologias | Markdown, com ferramentas em Python 3.10+ |
| Em hardware real | Não se aplica: documentação |

**Ir para:** [Visão geral](#-visão-geral) · [Arquitetura](#-arquitetura) · [Início rápido](#-início-rápido) · [Testes](#-testes) · [Estrutura](#-estrutura-do-repositório) · [Relacionados](#-projetos-relacionados)

## 🚦 Estado do projeto

Cada linha é uma parte deste repositório e a luz diz até onde chega hoje. É escrita com o que o repositório consegue demonstrar (testes, compilações, execuções), não com o que está previsto.

🟢 Feito e verificado · 🟡 Funciona, com limites conhecidos · 🟠 Feito a meio ou ainda por verificar · 🔴 Por fazer ou a não funcionar

| Área | Estado | O que significa aqui |
|---|---|---|
| Verificações do repositório | 🟡 | A verificação do repositório, a das ligações entre os documentos e os testes das ferramentas correm na CI e passam. |
| Testes | 🟠 | 126 testes das ferramentas passam num computador, alguns sobre pequenos repositórios de brincar; os documentos e as afirmações que contêm são lidos e verificados à mão e pelos scripts. |
| Contrato da suite | 🟡 | O contrato entre os repositórios lê cada manifesto com o analisador do Updater e avisa dos desvios (portas, idiomas do README, ferramentas partilhadas, formulários de problemas); corre todos os dias na CI como simples aviso, e os repositórios que nomeia são postos em dia um a um. |
| Ferramentas de versão e publicação | 🟠 | Os scripts que sobem uma versão, escrevem as notas e verificam uma publicação, e o fluxo de validação reutilizável, estão testados em repositórios de brincar; nenhum repositório publicou ainda uma versão com eles. |
| Espaço de trabalho e repositórios novos | 🟠 | Os scripts que listam e clonam o que um repositório precisa e que criam um repositório novo estão testados em repositórios de brincar numa pasta temporária; nenhum preparou ainda um espaço de trabalho real nem criou um repositório real. |
| Mapa e matriz de capacidades | 🟡 | O mapa da suite, as notas de arquitetura e a matriz de capacidades cobrem os vinte e sete repositórios publicados, com a versão de cada um, e listam como previsto o único programa que continua a ser um plano; são escritos à mão e podem ficar atrás dos repositórios. |
| Hardware real | 🟡 | Não se aplica: documentação, nada aqui corre em hardware. |
| Documentação | 🟡 | README em oito idiomas, verificado em cada alteração contra o manifesto e o registo de alterações. |

## 🎯 Visão geral

* **O mapa da suite:** cada repositório, para que serve e se está publicado, começado (código com testes e ainda sem versão) ou só previsto.
* **A arquitetura:** as duas bibliotecas partilhadas, os programas que deverão depender delas e nunca uns dos outros, o nó e o servidor que chegam à máquina, e as regras que cada repositório segue.
* **A matriz de capacidades:** o que está testado num computador e o que foi executado numa máquina (só o protocolo do EH3D-DRILLPRO, numa máquina), para que ninguém tenha de adivinhar.
* **As convenções:** o manifesto que cada repositório leva, a verificação do repositório e os ficheiros README em oito idiomas.
* **As verificações e as ferramentas:** a verificação do repositório, a das ligações entre os documentos, os desenhadores das duas imagens do README e as luzes de estado, copiados para cada repositório a partir deste (`tools/sync_shared_tools.py` diz quem está atrasado), e o verificador da convenção dos códigos de saída.
* **O contrato da suite:** `tools/suite_contract.py` verifica as relações que nenhum repositório consegue verificar sozinho: cada manifesto é lido com o analisador do Updater e leva o nome da sua pasta, uma dependência de um irmão por caminho diz que versão precisa, as versões do mapa são as dos manifestos, os ecrãs e o servidor concordam na porta, o validador partilhado é o mesmo em todo o lado, `docs/suite.json` coincide com os sítios que repetem os seus valores e cada repositório tem os formulários de problemas. Só avisa.
* **Versões, publicações e trabalho novo:** `bump_version.py`, `release_notes.py`, `prerelease_check.py`, `readme_staleness.py` e `vendored_tools_report.py` ([docs/RELEASING.md](docs/RELEASING.md)), um fluxo de validação reutilizável ([docs/REUSABLE_VALIDATION.md](docs/REUSABLE_VALIDATION.md)), `bootstrap_workspace.py` para trazer o que um repositório precisa e `new_repo.py` para criar um repositório novo.
* **Como se atualiza:** a CM5 da oficina atualiza-se **por releases** (`deploy/eh3d-update.py` do EH3D-SERVER descarrega a release do GitHub para `/opt`); o EH3D-UPDATER é para os **PC de desenvolvimento, por git** ([docs/UPDATING.md](docs/UPDATING.md)).

## 🧩 Papel no EH3D

O EH3D-DOCS é onde a suite é descrita no seu conjunto. Cada repositório descreve-se no seu próprio README; este diz como encaixam, quais existem e o que foi realmente executado.

## 🏛️ Arquitetura

<p align="center">
  <img src="images/architecture.svg" alt="Arquitetura de EH3D-DOCS: quem o usa, o que contém e de que depende" width="100%">
</p>

Como as partes deste repositório se encaixam: quem o usa, o que contém e de que depende. A imagem é desenhada a partir de `docs/architecture.json` e verificada com o código.

## 🔒 Segurança e proteção

Este repositório não tem nenhum programa que receba entradas de fora; o que defende é a exatidão e a limpeza do que publica.

| Ameaça | Defesa |
|---|---|
| Uma afirmação de que a suite faz mais do que faz | a matriz de capacidades separa «testado num computador» de «executado numa máquina», e um repositório fica como previsto até ter código que qualquer pessoa possa executar |
| Uma referência privada, uma pessoa ou uma ferramenta que não deve ser pública | `tools/ci_validate.py` falha com as palavras que nunca devem aparecer num ficheiro público, em cada ficheiro de texto |
| Uma ligação quebrada entre os documentos | `tools/check_links.py` falha quando uma ligação relativa de um ficheiro Markdown aponta para um ficheiro que não existe |
| Um idioma do README que se desvia dos outros | a verificação compara a estrutura dos títulos, os semáforos do estado do projeto e a versão nos oito ficheiros |
| Ficheiros que não devem ser versionados (compilações, chaves, registos, ficheiros grandes) | a verificação do repositório recusa pastas de compilação, pastas privadas, ficheiros de chaves e de registos e ficheiros com mais de 1,5 MB sob controlo de versões |

## 🔌 Interfaces

| Interface | O que é | Onde |
|---|---|---|
| Os documentos | Markdown: o mapa, a arquitetura, a matriz de capacidades e as convenções | [docs/](docs/SUITE_MAP.md) |
| A verificação do repositório | `python -I tools/ci_validate.py` imprime `CI_VALIDATION=PASS` ou lista o que falha | `tools/ci_validate.py` |
| A verificação das ligações | `python -I tools/check_links.py` imprime `LINKS=PASS` ou lista as ligações quebradas | `tools/check_links.py` |
| Os testes da verificação | `python -I -m unittest discover -s tools -p "test_*.py"` | `tools/test_ci_validate.py` |
| O contrato da suite | `python -I tools/suite_contract.py --workspace ..` imprime `SUITE_CONTRACT=PASS` ou lista os achados; `--write-map` põe as versões dos manifestos no mapa | `tools/suite_contract.py` |
| As ferramentas partilhadas | `python -I tools/sync_shared_tools.py` diz que repositórios têm uma cópia diferente | `tools/sync_shared_tools.py` |
| Versões e publicações | `bump_version.py`, `release_notes.py`, `prerelease_check.py`, `readme_staleness.py`, `vendored_tools_report.py` | [docs/RELEASING.md](docs/RELEASING.md) |
| O fluxo reutilizável | validação com `on: workflow_call`, para os repositórios chamarem | [docs/REUSABLE_VALIDATION.md](docs/REUSABLE_VALIDATION.md) |
| O espaço de trabalho | `bootstrap_workspace.py` lista e clona o que um repositório precisa; `new_repo.py` cria um repositório novo | `tools/bootstrap_workspace.py`, `tools/new_repo.py` |
| Os códigos de saída | `0`, `1`, `2`, `10` e `64`; `exit_conventions.py` confronta as ferramentas com eles | [docs/CONVENTIONS.md](docs/CONVENTIONS.md) |

## ⚙️ Configuração

As ferramentas precisam de Python 3.10 ou posterior e de nenhuma instalação, e leem os ficheiros do repositório onde vivem. As regras que aplicam estão no código de `tools/ci_validate.py`, e os valores da suite que vários repositórios repetem estão em `docs/suite.json`:

| Regra | Limite | Onde |
|---|---|---|
| Tamanho de um ficheiro versionado | no máximo 1 500 000 bytes | `MAX_TRACKED_BYTES` |
| Idiomas do README | oito ficheiros, com a mesma estrutura de títulos e os mesmos semáforos | `LANGUAGES` |
| Campos do manifesto | os 14 campos de `REQUIRED`; a versão do manifesto é igual à de `VERSION` (`native_version`) e à da entrada mais recente do registo de alterações | `REQUIRED` |
| As constantes da suite | a porta do servidor, o esquema do manifesto, os oito idiomas do README, o campo de rpm, a forma de uma versão, os formulários de problemas | `docs/suite.json` |
| Exceções conhecidas do contrato | um `check repositório` por linha, retirado quando a causa é corrigida | `docs/suite_contract_allow.txt` |
| O que um repositório acrescenta à verificação | por exemplo as pastas que a procura de palavras proibidas salta | `tools/ci_config.json` de cada repositório |

## 🚀 Início rápido

Precisa de Python 3.10 ou mais recente; não há nada a instalar.

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
python -I tools/suite_contract.py --workspace ..
python -I tools/bootstrap_workspace.py --workspace .. EH3D-DRILLPRO
python -I -m unittest discover -s tools -p "test_*.py"
```

Para ler os documentos, comece pelo [mapa da suite](docs/SUITE_MAP.md).

## 🧪 Testes

As ferramentas têm 126 testes (`python -I -m unittest discover -s tools -p "test_*.py"`), e passam. A CI executa a verificação do repositório (`tools/ci_validate.py`), a das ligações entre os documentos (`tools/check_links.py`), as verificações das duas imagens e esses testes; um fluxo diário executa o contrato da suite. Os documentos não têm mais testes do que esses: o que afirmam é mantido honesto pela matriz de capacidades e pela leitura.

## 🏗️ Compilação e publicação

A versão vive no ficheiro `VERSION` e em `eh3d.project.json`, e cada versão tem a sua entrada em [CHANGELOG.md](CHANGELOG.md). Não há nada a compilar; as versões são publicadas no GitHub.

## 📂 Estrutura do repositório

<p align="center">
  <img src="images/repository-structure.svg" alt="Estrutura do repositório EH3D-DOCS" width="100%">
</p>

<details>
<summary>Versão em texto da árvore</summary>

```text
EH3D-DOCS/
├── docs/
│   ├── SUITE_MAP.md                             cada repositório e se já existe
│   ├── ARCHITECTURE.md                          as camadas e as regras
│   ├── CAPABILITY_MATRIX.md                     o que foi testado e o que foi executado numa máquina
│   ├── CONVENTIONS.md                           o manifesto, a verificação, os README
│   ├── UPDATING.md                              como se atualizam a CM5 e um PC
│   ├── RELEASING.md                             subir uma versão e publicar com os scripts
│   ├── REUSABLE_VALIDATION.md                   o fluxo de validação que os repositórios podem chamar
│   ├── VENDORED_TOOLS_REPORT.md                 as ferramentas copiadas para os repositórios que ninguém usa
│   ├── suite.json                               as constantes da suite
│   ├── suite_contract_allow.txt                 as exceções conhecidas do contrato
│   ├── templates/                               o modelo de um repositório novo
│   └── architecture.json structure.json         os dados das duas imagens
├── tools/                                       as verificações, o contrato, os scripts de versão e publicação e os seus testes
├── images/                                      banner e as imagens de Arquitetura e Estrutura do repositório
├── .github/                                     fluxos de CI e do painel, modelos de issues e pull requests
├── eh3d.project.json                            manifesto: versão, papel, maturidade e comando de compilação
├── VERSION                                      a versão dos documentos
├── CHANGELOG.md                                 o que mudou em cada versão
├── SECURITY.md SUPPORT.md                       como comunicar uma vulnerabilidade e onde perguntar
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   como contribuir, o código de conduta e a licença
```

</details>

## 🗺️ Roteiro e limites conhecidos

**Limites conhecidos hoje**

* O mapa, as notas de arquitetura e a matriz de capacidades são escritos à mão; nada os verifica contra os manifestos dos repositórios, por isso podem ficar atrás.
* Só os repositórios publicados são descritos em pormenor; os programas começados e os previstos são uma linha do mapa cada um, marcada como tal.
* Os documentos não têm testes próprios além da verificação do repositório e da das ligações.
* Os scripts de publicação, de espaço de trabalho e de repositório novo só foram experimentados em repositórios de brincar; nenhum foi ainda usado numa publicação real nem para criar um repositório real.
* O contrato da suite só avisa, e vários repositórios ainda têm uma cópia mais antiga do validador partilhado.

**A seguir**

* Manter o mapa e a matriz de capacidades ao passo de cada repositório quando é publicado ou muda.
* Verificar o mapa contra os manifestos dos repositórios, para que um repositório novo não possa faltar nele.
* Usar os scripts na próxima publicação real, adotar o fluxo reutilizável nos repositórios e tornar o contrato da suite bloqueante quando os achados conhecidos desaparecerem.

## 🌍 Idiomas

O README e os textos existem em inglês, espanhol, francês, italiano, alemão, chinês, japonês e português europeu.

## 🔗 Projetos relacionados

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): o contentor de projeto, os tipos de máquina e a base de firmware dos nós
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): os leitores de Gerber, Excellon e G-code
* [EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO) e [EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO): os programas de furação e de fresagem
* [EH3D-BUNGARD-GUI](https://github.com/JuanenRac/EH3D-BUNGARD-GUI) e [EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC): a interface moderna das máquinas Bungard e o programa de controlo de máquina
* [EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER) e [EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD): o centro dos programas e o nó que chega à máquina
* [EH3D-STUDIO](https://github.com/JuanenRac/EH3D-STUDIO), [EH3D-NODE-BUNGARD-HMI](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-HMI) e [EH3D-NODE-BUNGARD-AUX](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-AUX): o painel de configuração do servidor (com as suas atualizações a partir do GitHub), o ecrã tátil da máquina e o nó da cabeça de furação (câmara por RTSP e ONVIF, laser que mede a mesa, velocidade e temperatura do fuso)
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) e [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): instalam e atualizam os repositórios

## 📚 Documentação

* [O mapa da suite](docs/SUITE_MAP.md), [a arquitetura](docs/ARCHITECTURE.md), [a matriz de capacidades](docs/CAPABILITY_MATRIX.md) e [as convenções](docs/CONVENTIONS.md).
* [Publicar uma versão](docs/RELEASING.md) e [a validação reutilizável](docs/REUSABLE_VALIDATION.md).
* [Registo de alterações](CHANGELOG.md)

## 🤝 Contribuir e comunidade

* Antes de um pull request, execute `python -I tools/ci_validate.py`, `python -I tools/check_links.py` e os testes das ferramentas: tudo tem de passar. Consulte [CONTRIBUTING.md](CONTRIBUTING.md) e o [código de conduta](CODE_OF_CONDUCT.md).
* O README existe em oito idiomas: uma alteração ao texto faz-se nos oito ficheiros, e as duas imagens são desenhadas a partir de `docs/architecture.json` e `docs/structure.json` com `tools/make_architecture.py` e `tools/make_structure.py`.
* Não descreva como funcionando numa máquina o que só foi experimentado num computador: a matriz de capacidades diz qual é qual.
* Comunique uma vulnerabilidade em privado: [SECURITY.md](SECURITY.md). Perguntas, ideias e relatórios: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENÇA

Software: GPL-3.0-or-later. Ver [LICENSE](LICENSE). Os projetos de hardware da suite usam a CERN OHL-S.
