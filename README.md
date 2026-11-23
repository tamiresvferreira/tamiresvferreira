<!-- ===================== BANNER ANIMADO ===================== -->
<!-- Gerado por .github/scripts/gerar_banner_neon.py -->
<p align="center">
  <img src="./assets/banner-neon.svg" alt="Hello world! I am Tamires — AI & Data Science" width="100%"/>
</p>

<p align="center">
  <a href="https://br.linkedin.com/in/tamiresvferreiras"><img src="https://img.shields.io/badge/LinkedIn-0d1117?style=for-the-badge&logo=linkedin&logoColor=ff5fa2" alt="LinkedIn"/></a>
  <a href="mailto:tamiresvferreiras@gmail.com"><img src="https://img.shields.io/badge/E--mail-0d1117?style=for-the-badge&logo=gmail&logoColor=ff5fa2" alt="E-mail"/></a>
  <img src="https://komarev.com/ghpvc/?username=tamiresvferreira&label=visitas&color=ff5fa2&style=for-the-badge" alt="Visitas ao perfil"/>
</p>

<!-- ===================== SOBRE MIM + TECH STACK ===================== -->
<table>
<tr>
<td width="55%" valign="top">

## 👾 Sobre mim

Sou estudante de **Inteligência Artificial na FIAP** e gosto de transformar dados em soluções que as pessoas conseguem usar no dia a dia.

Trabalho o ciclo completo de um projeto de IA. Começo pela **coleta e análise dos dados**, passo pelo **modelo de machine learning** e termino na **interface** que mostra o resultado, às vezes também no **hardware** que captura as informações. Já apliquei isso em problemas reais de **agronegócio**, **segurança viária e cidades inteligentes** e **prevenção de desastres climáticos**, usando dados abertos e públicos e também **dados espaciais**: imagens de satélite de radar (Sentinel-1) e mapas georreferenciados para prever enchentes e deslizamentos. Meu projeto mais completo, a **BetterWay**, junta visão computacional, modelos de risco, simulação de tráfego, IoT e uma plataforma web num semáforo que enxerga a faixa de pedestres.

Também me importo com a parte que fica entre o código e as pessoas: documentação clara, arquitetura bem explicada e interfaces pensadas para quem vai usar.

</td>
<td width="45%" valign="top">

## ⚡ Tech stack

**🧠 Machine Learning & Visão Computacional**<br>
<img src="https://skillicons.dev/icons?i=py,sklearn,pytorch,tensorflow,opencv&theme=dark" alt="Python, Scikit-learn, PyTorch, TensorFlow, OpenCV"/>

**📊 Dados**<br>
<img src="https://skillicons.dev/icons?i=r,mysql,postgres,sqlite&theme=dark" alt="R, SQL, PostgreSQL, SQLite"/>
<img src="./assets/icons/pandas.svg" height="48" alt="Pandas"/>
<img src="./assets/icons/powerbi.svg" height="48" alt="Power BI"/>
<img src="./assets/icons/colab.svg" height="48" alt="Google Colab"/>

**⚙️ Automação**<br>
<img src="./assets/icons/n8n.svg" height="48" alt="n8n"/>
<img src="./assets/icons/botconversa.svg" height="48" alt="BotConversa"/>

**🧩 Prototipagem (interface e hardware)**<br>
<img src="https://skillicons.dev/icons?i=figma,react,js,html,css,arduino,cpp&theme=dark" alt="Figma, React, JavaScript, HTML, CSS, Arduino, C++"/>

**🛠️ Desenvolvimento & Deploy**<br>
<img src="https://skillicons.dev/icons?i=git,github,vscode,aws&theme=dark" alt="Git, GitHub, VS Code, AWS"/>

**🪄 Prompt Engineering**<br>
<img src="./assets/icons/claude.svg" height="48" alt="Claude"/>
<img src="./assets/icons/codex.svg" height="48" alt="Codex"/>
<img src="./assets/icons/gemini.svg" height="48" alt="Gemini"/>
<img src="./assets/icons/grok.svg" height="48" alt="Grok"/>

</td>
</tr>
</table>

## 💻 Hard skills

### 🧠 Machine Learning & IA
Regressão, classificação e clusterização (K-Means, **DBSCAN espacial**), XGBoost, **gradient boosting com perda Poisson**, validação cruzada e temporal, Grid Search e pipeline **CRISP-DM**. Experiência com scoring de risco: estimei onde e quando um atropelamento é provável em São Paulo, por hora, tipo de dia e chuva.

### 👁️ Visão computacional
Detecção de vocabulário aberto com **YOLO-World**, rastreamento com **ByteTrack**, **ajuste fino de YOLO11** no Google Colab para reconhecer pessoas em cadeira de rodas, medição de travessia e de conflito veículo × pedestre, e anonimização de rostos (por estimativa de pose) e placas.

### 🚦 Simulação
Simulação de tráfego com **SUMO** e TraCI: semáforo de tempo fixo contra semáforo atuado, prioridade para ambulância e cenários comparados com várias sementes.

### 📊 Dados
Análise exploratória com Pandas, **SQL** e modelagem relacional, **dados geoespaciais** (GeoPandas, Folium, OpenStreetMap, GeoSampa), dashboards em **Power BI** e **R Shiny**, e consumo de APIs de dados abertos (INMET, EMBRAPA, ANA, INPE, BACEN).

### ⚙️ Automação
Expertise na criação de **automações avançadas no n8n**, integrando sistemas por APIs e webhooks, com fluxos de várias etapas e lógica condicional. Conhecimento avançado em plataformas de automação de atendimento, como a **BotConversa**.

### ☁️ Cloud
**AWS**: análise de custos entre regiões para hospedar uma API de ML, considerando os requisitos legais de armazenamento de dados. Também trabalho com arquitetura serverless.

### 🎨 Front-end & Design
Do protótipo no **Figma** à interface em **React** ou **Streamlit**: dashboards por perfil de usuário, design system com tokens, tema claro e escuro, responsividade e acessibilidade (leitura em voz). Autenticação com convite, **segundo fator (TOTP)** e senhas em hash scrypt, com privacidade desde o projeto (**LGPD**).

### 🔌 IoT & Hardware
**ESP32 e Arduino** com sensores e Wi-Fi, em protótipos de irrigação inteligente e de cidades inteligentes. Firmware em **C++** com máquina de estados, integração por **MQTT** e simulação no **Wokwi**.

<!-- ===================== PROJETOS ===================== -->
## 📂 Projetos em destaque

<table>
<tr>
<td colspan="2" valign="top">
  <a href="https://github.com/tamiresvferreira/betterway"><img src="./assets/projeto-betterway.png" width="100%" alt="BetterWay"/></a>
  <h3>🚦 BetterWay: o semáforo que enxerga a faixa</h3>
  <b>Visão computacional + modelos de risco + simulação + IoT + plataforma web</b><br>
  Uma câmera entende a faixa de pedestres, uma central junta câmera, chuva e histórico de atropelamentos, e um nó ESP32 ajusta o semáforo na hora: espera quem ainda atravessa e abre caminho para a ambulância. Encontrei 273 pontos críticos de atropelamento em São Paulo com DBSCAN sobre dados abertos, ajustei um YOLO11 para reconhecer cadeira de rodas e, na simulação do piloto, zerei as pessoas na faixa com carros em verde (5,6 → 0 por rodada) e reduzi em 17% o tempo da ambulância. Projeto individual da Global Solution FIAP 2026.2.<br><br>
  <img src="https://img.shields.io/badge/Python-0d1117?style=flat-square&logo=python&logoColor=ff5fa2" alt="Python"/>
  <img src="https://img.shields.io/badge/YOLO-0d1117?style=flat-square&logoColor=ff5fa2" alt="YOLO"/>
  <img src="https://img.shields.io/badge/Scikit--learn-0d1117?style=flat-square&logo=scikitlearn&logoColor=ff5fa2" alt="Scikit-learn"/>
  <img src="https://img.shields.io/badge/SUMO-0d1117?style=flat-square&logoColor=ff5fa2" alt="SUMO"/>
  <img src="https://img.shields.io/badge/ESP32-0d1117?style=flat-square&logo=espressif&logoColor=ff5fa2" alt="ESP32"/>
  <img src="https://img.shields.io/badge/MQTT-0d1117?style=flat-square&logo=mqtt&logoColor=ff5fa2" alt="MQTT"/>
  <img src="https://img.shields.io/badge/Streamlit-0d1117?style=flat-square&logo=streamlit&logoColor=ff5fa2" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/SQLite-0d1117?style=flat-square&logo=sqlite&logoColor=ff5fa2" alt="SQLite"/>
</td>
</tr>
<tr>
<td width="50%" valign="top">
  <a href="https://github.com/tamiresvferreira/FarmTechSolutions---FIAP-"><img src="./assets/projeto-farmtech.png" width="100%" alt="FarmTech Solutions"/></a>
  <h3>🌾 FarmTech Solutions</h3>
  <b>Agricultura de precisão</b><br>
  Cálculo de área e insumos por talhão, estatísticas em R e dados meteorológicos em tempo real pela API Open-Meteo.<br><br>
  <img src="https://img.shields.io/badge/Python-0d1117?style=flat-square&logo=python&logoColor=ff5fa2" alt="Python"/>
  <img src="https://img.shields.io/badge/R-0d1117?style=flat-square&logo=r&logoColor=ff5fa2" alt="R"/>
</td>
<td width="50%" valign="top">
  <a href="https://github.com/tamiresvferreira/classificacao-sementes-trigo"><img src="./assets/projeto-sementes.png" width="100%" alt="Classificação de Sementes"/></a>
  <h3>🌱 Classificação de Sementes</h3>
  <b>Machine Learning com CRISP-DM + demo em Streamlit</b><br>
  SVM que identifica três variedades de trigo (Kama, Rosa e Canadian) pelas medidas do grão, com F1 de 0,96 na validação cruzada, análise de erros e app interativo.<br><br>
  <img src="https://img.shields.io/badge/Python-0d1117?style=flat-square&logo=python&logoColor=ff5fa2" alt="Python"/>
  <img src="https://img.shields.io/badge/Scikit--learn-0d1117?style=flat-square&logo=scikitlearn&logoColor=ff5fa2" alt="Scikit-learn"/>
  <img src="https://img.shields.io/badge/Streamlit-0d1117?style=flat-square&logo=streamlit&logoColor=ff5fa2" alt="Streamlit"/>
</td>
</tr>
</table>

## 🤝 Soft skills

- ✍️ **Comunicação escrita:** textos claros e objetivos, de documentação técnica a relatórios para quem não é da área
- 🗣️ **Comunicação técnica:** explico modelos e resultados de forma acessível, em READMEs, diagramas e apresentações
- 📈 **Apresentação de dados para times:** transformo análises em insights que apoiam decisões
- 🧑‍💼 **Vivência em ambiente corporativo:** conduzo reuniões, alinho expectativas com diferentes áreas e lido bem com prazos e prioridades
- 🚀 **Liderança de projetos:** organizo entregas do planejamento à execução e coordeno pessoas em torno de um objetivo
- 🤝 **Trabalho em equipe:** entregas em sprints e projetos colaborativos
- 🧭 **Visão de produto:** começo pelo problema e pelo usuário, não pela ferramenta
- 🔍 **Atenção aos detalhes:** trabalho de forma iterativa, refinando até ficar certo
- 📚 **Aprendizado contínuo:** estou sempre estudando algo novo, hoje com foco em visão computacional e sistemas embarcados
- 🌎 **Inglês avançado**

---

## 📈 Atividade

<!-- Gerado automaticamente pelo workflow .github/workflows/snake.yml -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/tamiresvferreira/tamiresvferreira/output/github-contribution-grid-snake-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/tamiresvferreira/tamiresvferreira/output/github-contribution-grid-snake.svg"/>
  <img alt="Cobrinha comendo o gráfico de contribuições" src="https://raw.githubusercontent.com/tamiresvferreira/tamiresvferreira/output/github-contribution-grid-snake-dark.svg"/>
</picture>

<p align="center">
  <sub>Feito em pixel, um quadradinho de cada vez 🩷</sub>
</p>
