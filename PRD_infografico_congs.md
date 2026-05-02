# PRD — Infográfico / Landing Page: Projeto Conecta ONGs (C.ONGs)

**Versão:** 1.0  
**Data:** maio de 2026  
**Tipo de entrega:** Single-page application (SPA) — infográfico scrollável + mapa interativo  
**Navegação:** abertura direta no infográfico; botão ao final redireciona para o mapa interativo

---

## 1. Visão Geral do Produto

A landing page do **Projeto Conecta ONGs (C.ONGs)** apresenta, em formato de infográfico digital navegável, dados coletados automaticamente das redes sociais de 28 ONGs de proteção animal do litoral norte e Vale do Itajaí de Santa Catarina, abrangendo o período de fevereiro a abril de 2026. O produto tem dupla função: sensibilizar o cidadão sobre a existência e as ações das organizações próximas a ele e oferecer uma leitura acessível dos dados minerados pelo script `mineracao_ongs_apify.py`.

Ao fim da página, um botão fixo ou CTA leva ao mapa interativo (segunda tela), onde o usuário pode explorar geograficamente as ONGs por município.

---

## 2. Problema que o Produto Resolve

Grande parte da população desconhece a existência de ONGs de proteção animal em sua cidade, mesmo quando essas organizações publicam ativamente em redes sociais. Essa invisibilidade limita o acesso a campanhas de doação, feiras de adoção, mutirões de castração e oportunidades de voluntariado. O infográfico traduz dados reais de atividade digital dessas organizações em informações que motivam o engajamento cívico.

---

## 3. Objetivos

### 3.1 Objetivo Geral
Comunicar ao público os padrões de atuação e as necessidades das ONGs de proteção animal do litoral norte catarinense com base em dados minerados de suas redes sociais, estimulando a aproximação entre cidadãos e organizações locais.

### 3.2 Objetivos Específicos
- Apresentar o escopo do projeto: quantas ONGs monitoradas, em quais cidades, em qual período.
- Mostrar o volume e os tipos de campanhas realizadas no período.
- Comunicar quais tipos de ajuda as ONGs mais precisam (financeira, alimento, castração, lar temporário).
- Exibir a distribuição de campanhas de adoção por cidade.
- Apresentar a frequência mensal de atividade, evidenciando sazonalidade.
- Indicar a importância do acompanhamento das redes sociais dessas organizações.
- Direcionar o usuário ao mapa interativo para exploração geográfica.

---

## 4. Público-Alvo

| Perfil | Motivação de uso |
|---|---|
| Tutores de pets e protetores independentes | Descobrir ONGs próximas e como ajudar |
| Estudantes e pesquisadores | Consumir dados sistematizados sobre o terceiro setor animal |
| Jornalistas e comunicadores | Referência visual sobre atuação das organizações |
| Potenciais adotantes | Conhecer feiras e animais disponíveis por cidade |
| Doadores em potencial | Entender o que as ONGs mais precisam |

---

## 5. Estrutura de Seções da Landing Page

### SEÇÃO 0 — Hero / Abertura

**Conteúdo:**
- Pergunta-gatilho centralizada: **"Você conhece a ONG da causa animal mais próxima a você?"**
- Subtítulo curto: _"Em Santa Catarina, 28 organizações publicaram mais de 1.200 posts em 3 meses pedindo ajuda, buscando lares e salvando vidas."_
- Botão CTA primário: **"Ver os dados"** (scroll suave para seção 1)
- Background: fotografia ou ilustração vetorial com animal + voluntários

---

### SEÇÃO 1 — O que é o Projeto Conecta ONGs (C.ONGs)?

**Conteúdo em formato de parágrafo curto + 3 cards de destaque:**

> O Projeto Conecta ONGs (C.ONGs) mapeou e monitorou 28 organizações de proteção animal em 10 municípios do litoral norte e Vale do Itajaí de Santa Catarina. Por meio de mineração automatizada de dados em redes sociais, foram coletadas e classificadas 1.204 publicações do período de fevereiro a abril de 2026, revelando padrões de atuação, necessidades e campanhas ativas.

**Cards de objetivos (visual: ícone + título + descrição de 2 linhas):**

| Card | Objetivo |
|---|---|
| Objetivo Geral | Mapear e comunicar a atuação digital das ONGs de proteção animal do litoral norte de SC com base em dados reais de redes sociais |
| Objetivo Específico 1 | Identificar os tipos de campanhas realizadas e a frequência de publicação por organização e por mês |
| Objetivo Específico 2 | Revelar quais necessidades as ONGs expressam com mais frequência: financeiras, de insumos, de lares temporários ou de adotantes |
| Objetivo Específico 3 | Disponibilizar os dados de forma acessível ao público por meio de um infográfico interativo e um mapa georreferenciado |

---

### SEÇÃO 2 — Números do período

**Formato: painel de KPIs (big numbers) com ícone e label**

| Métrica | Valor | Ícone sugerido |
|---|---|---|
| ONGs monitoradas | 28 | 🏢 |
| Municípios cobertos | 10 | 📍 |
| Postagens coletadas | 1.204 | 📱 |
| Stories capturados | 972 | ⏱️ |
| Plataformas | 2 (Instagram + Facebook) | 🔗 |
| Período | fev–abr 2026 | 📅 |

**Nota de rodapé da seção:** `Fonte: mineração automatizada de informações via Apify — fev a abr/2026`

---

### SEÇÃO 3 — Por que acompanhar as ONGs nas redes sociais?

**Formato: bloco de texto + 4 cards em grid 2×2**

Texto introdutório:
> As redes sociais são o canal primário pelo qual essas organizações comunicam ações urgentes, divulgam eventos e buscam recursos. Sem esse acompanhamento, doadores, adotantes e voluntários perdem oportunidades que existem a poucos quilômetros de distância.

**Cards de "O que você encontra seguindo uma ONG":**

| Card | Conteúdo |
|---|---|
| 📣 Campanhas de doação | Pedidos de ração, medicamentos, recursos financeiros, rifas e vaquinhas |
| 🐾 Feiras de adoção | Datas, locais e animais disponíveis para encontrar uma família |
| ✂️ Mutirões de castração | Eventos com valores sociais para tutores e animais de rua |
| 🚨 Casos urgentes | Resgates, tratamentos clínicos e animais precisando de lar temporário |

---

### SEÇÃO 4 — O que as ONGs mais precisam?

**Gráfico recomendado: Gráfico de barras horizontais com % ou contagem absoluta**

Dados do período (1.204 posts totais, com múltiplos rótulos por post):

| Tipo de necessidade | Posts classificados | % do total |
|---|---|---|
| Campanha de doação (financeiro/insumos) | 399 | 33,1% |
| Campanha de adoção / divulgação de feiras | 325 | 27,0% |
| Resgate ou caso clínico | 210 | 17,4% |
| Animal para adoção (perfil individual) | 141 | 11,7% |
| Castração / mutirão | 134 | 11,1% |
| Educação e conscientização | ~85 | ~7,1% |
| Evento / parceria | ~120 | ~10,0% |
| Prestação de contas | 33 | 2,7% |

**Detalhamento visual secundário — "Dentro de 'Doação', o que foi pedido?"**  
(gráfico de pizza ou treemap baseado em análise das captions)

Categorias identificadas nas captions de campanha_doacao:
- Recursos financeiros (PIX, transferência, rifa, vaquinha) — maior frequência
- Ração e alimentos
- Medicamentos e tratamentos veterinários
- Cobertores, caminhas e acessórios
- Lar temporário (acolhimento provisório)

> **Nota visual:** não atribuir esses dados a ONGs nominalmente; apresentar como dado agregado do ciclo.  
> `Fonte: mineração automatizada de informações via Apify — fev a abr/2026`

---

### SEÇÃO 5 — Campanhas de adoção por cidade

**Gráfico recomendado: Gráfico de barras verticais agrupadas por cidade**

Dados derivados do cruzamento cidade × campanha_adocao (325 posts total):

| Cidade | Posts com campanha de adoção |
|---|---|
| Balneário Camboriú/SC | ~97 |
| Blumenau/SC | ~75 |
| Itajaí/SC | ~55 |
| Brusque/SC | ~37 |
| Penha/SC | ~28 |
| Camboriú/SC | ~35 |
| Gaspar/SC | ~6 |
| Ilhota/SC | ~6 |
| Outros | ~5 |

_Valores aproximados — derivar do CSV consolidado na geração do gráfico final._

**Subtítulo visual:** _"Cidades com mais feiras de adoção divulgadas nas redes"_  
`Fonte: mineração automatizada de informações via Apify — fev a abr/2026`

---

### SEÇÃO 6 — Atividade ao longo dos meses

**Gráfico recomendado: Gráfico de linhas com 3 séries sobrepostas (doação, adoção, resgate)**

Dados mensais disponíveis:

| Mês | Total posts | Doação | Adoção | Resgate/Clínico | Castração |
|---|---|---|---|---|---|
| Fev/2026 | 304 | 80 | 55 | 51 | 27 |
| Mar/2026 | 481 | 151 | 145 | 87 | 48 |
| Abr/2026 | 419 | 168 | 125 | 72 | 59 |

**Insight visual a destacar:**  
- Março foi o mês mais ativo — pico de feiras de adoção coincide com Dia Nacional dos Animais (14/03).
- Campanhas de doação cresceram de fevereiro a abril, com aceleração em abril.
- Castrações aumentaram progressivamente: mutirões tendem a se concentrar no segundo trimestre.

`Fonte: mineração automatizada de informações via Apify — fev a abr/2026`

---

### SEÇÃO 7 — Tipos de conteúdo publicado

**Gráfico recomendado: Gráfico de rosca (donut) — proporção de categorias no total**

| Categoria | Quantidade |
|---|---|
| Campanha de doação | 399 |
| Campanha de adoção | 325 |
| Resgate / caso clínico | 210 |
| Animal para adoção | 141 |
| Castração | 134 |
| Evento / parceria | ~120 |
| Educação / conscientização | ~85 |
| Prestação de contas | 33 |
| Outros (sem categoria) | ~180 |

**Texto âncora da seção:**  
> Mais de um terço das publicações do período envolveu pedidos de apoio financeiro ou de insumos. Campanhas de adoção correspondem a mais de um quarto do conteúdo total, sinalizando que o volume de animais disponíveis supera a capacidade de captação de lares no período.

`Fonte: mineração automatizada de informações via Apify — fev a abr/2026`

---

### SEÇÃO 8 — A castração como ação estrutural

**Formato: card informativo + dado de destaque**

Texto:
> A castração aparece em 134 publicações no período, com pico em abril. Os mutirões com valores sociais são o formato predominante: eventos pontuais que concentram procedimentos para tutores de baixa renda e para animais de rua. A castração preventiva reduz o ciclo de abandono e diminui a demanda por resgates nos meses seguintes.

**Dado de destaque (big number):**  
`134 publicações sobre castração em 3 meses — média de 44 por mês`

`Fonte: mineração automatizada de informações via Apify — fev a abr/2026`

---

### SEÇÃO 9 — Conscientização e denúncia

**Formato: bloco de texto + citação visual de caption real (anonimizada)**

Texto:
> Publicações de educação e conscientização abordaram maus-tratos, abandono, guarda responsável e denúncia. O período coincidiu com repercussão nacional de casos de violência contra animais, o que elevou o volume desse tipo de conteúdo, especialmente em fevereiro e março de 2026.

**Citação ilustrativa (sem nome de ONG):**  
> _"O que aconteceu aqui não é um caso isolado. Até quando vamos tratar isso como exceção?"_  
> — Publicação coletada no período. Fonte: Instagram.

---

### SEÇÃO 10 — CTA Final / Chamada para o mapa

**Formato: seção de fundo escuro com texto centralizado e botão grande**

Título: **"Encontre a ONG mais próxima de você"**  
Subtítulo: _"Explore o mapa interativo com as 28 organizações monitoradas, seus municípios e perfis nas redes sociais."_  

Botão: **`→ Abrir mapa interativo`**

Nota de rodapé global da página:  
> Dados coletados por mineração automatizada de informações via Apify · Instagram e Facebook · fev–abr 2026 · Projeto Conecta ONGs (C.ONGs)

---

## 6. Segunda Tela — Mapa Interativo

**Tecnologia sugerida:** Leaflet.js ou Mapbox GL JS com marcadores por município

**Funcionalidades mínimas:**
- Marcador por cidade com número de ONGs
- Clique no marcador abre painel lateral com lista de ONGs daquela cidade
- Cada ONG exibe: nome, links para Instagram e Facebook, total de posts no período
- Filtro por categoria (doação / adoção / castração / resgate)
- Botão "Voltar ao infográfico"

**Municípios no dataset:**

| Município | Nº de ONGs |
|---|---|
| Balneário Camboriú | 3 |
| Blumenau | 7 |
| Brusque | 1 |
| Camboriú | 1 |
| Gaspar | 2 |
| Ilhota | 1 |
| Indaial | 2 |
| Itajaí | 7 |
| Navegantes | 1 |
| Penha | 1 |

---

## 7. Restrições de Apresentação dos Dados

- **Nenhum gráfico, ranking ou tabela deve nomear ONGs individualmente** nas seções de dados agregados (seções 4 a 9).
- A identidade das organizações aparece apenas no mapa interativo (seção 10/segunda tela), onde a função é de diretório, não de ranqueamento.
- Todos os dados apresentados devem carregar a nota: `Fonte: mineração automatizada de informações via Apify — fev a abr/2026`.
- Stories foram excluídos dos gráficos de conteúdo (sem filtro temporal aplicável); o total de 972 stories é citado apenas nos KPIs da seção 2.

---

## 8. Stack Técnica Sugerida

| Camada | Tecnologia |
|---|---|
| Marcação | HTML5 semântico |
| Estilo | Tailwind CSS ou CSS custom com variáveis |
| Gráficos | Chart.js (barras, linhas, donut) |
| Mapa | Leaflet.js + OpenStreetMap tiles |
| Dados | JSON estático gerado a partir de `posts_classificados.csv` |
| Deploy | Vercel / GitHub Pages (estático) |

---

## 9. Dados a Extrair do CSV para o Front-end

O script de geração do JSON estático (`gerar_dados_infografico.py` — a criar) deve produzir:

```json
{
  "kpis": { "total_posts": 1204, "total_stories": 972, "ongs": 28, "municipios": 10 },
  "por_categoria": [ { "categoria": "campanha_doacao", "total": 399 }, ... ],
  "por_mes": [ { "mes": "2026-02", "total": 304, "doacao": 80, ... }, ... ],
  "por_cidade_adocao": [ { "cidade": "Balneário Camboriú/SC", "total": 97 }, ... ],
  "mapa_ongs": [ { "nome": "...", "cidade": "...", "lat": -26.99, "lon": -48.63, "instagram": "...", "facebook": "..." }, ... ]
}
```

---

## 10. Critérios de Aceite

- [ ] A página abre diretamente no infográfico sem splash screen ou redirecionamento
- [ ] Todos os gráficos renderizam corretamente em mobile (375px) e desktop (1280px)
- [ ] Nenhum nome de ONG aparece em seções de ranking ou comparação
- [ ] Toda visualização de dados exibe a nota de fonte
- [ ] O botão de mapa navega para a segunda tela sem recarregar a página
- [ ] O mapa exibe todos os 10 municípios com marcadores clicáveis
- [ ] Os dados do JSON estático são consistentes com o CSV gerado pelo script de mineração
