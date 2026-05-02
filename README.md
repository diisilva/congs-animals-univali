# Mineração de Postagens em Redes Sociais de ONGs de Proteção Animal

**Script:** `mineracao_ongs_apify.py`  
**Período analisado:** fevereiro a abril de 2026  
**Plataformas:** Instagram e Facebook  
**Universo:** 28 organizações de proteção animal do litoral norte de Santa Catarina

---

## 1. Contexto e Objetivo

A comunicação digital de organizações do terceiro setor concentra-se progressivamente em plataformas de redes sociais, tornando o monitoramento sistemático de suas publicações uma fonte de dados relevante para pesquisas sobre comportamento organizacional, mobilização social e padrões de engajamento comunitário. O script desenvolvido automatizou a coleta, normalização e classificação temática das postagens públicas de 28 ONGs de proteção animal distribuídas em municípios do Vale do Itajaí e litoral norte catarinense, abrangendo Balneário Camboriú, Blumenau, Itajaí, Gaspar, Navegantes, entre outros.

O objetivo central da ferramenta consistiu em produzir um *dataset* estruturado e um relatório analítico a partir de conteúdo não estruturado extraído de perfis públicos, sem intervenção manual na coleta. Para isso, foram integradas técnicas de raspagem de dados via infraestrutura de *proxies* gerenciados, mineração de texto por correspondência de padrões e filtragem temporal parametrizável.

---

## 2. Arquitetura de Coleta: Web Scraping via Apify

A coleta ocorreu por meio da plataforma **Apify**, que expõe *Actors*, isto é, contêineres de scraping executados em nuvem com rotação automática de sessões e *proxies* residenciais. Dois *Actors* distintos foram acionados via API REST através do cliente oficial `apify-client` para Python.

**`apify/instagram-scraper`** executou duas passagens distintas sobre os 23 perfis com Instagram cadastrado: a primeira com `resultsType=posts`, limitada a 100 publicações por perfil e filtrada pela data mínima `2026-02-01`; a segunda com `resultsType=stories`, capturando até 50 stories ativos no momento da execução. **`apify/facebook-posts-scraper`** processou as 22 páginas com Facebook cadastrado, com limites de data em ambas as extremidades do intervalo.

A comunicação segue o padrão de disparo-e-poll: o método `client.actor().call()` submete o *run* e aguarda a conclusão; ao receber `status=SUCCEEDED`, os itens são paginados via `client.dataset().iterate_items()`. Qualquer status diferente de `SUCCEEDED` interrompe a execução com `RuntimeError`, evitando que dados parciais sejam processados silenciosamente.

O mecanismo de *cache local* implementado na função `load_or_scrape()` verificou a existência do arquivo JSON bruto antes de cada chamada à API. Caso o arquivo já existisse em disco, os dados foram carregados diretamente, preservando o consumo de tokens da conta Apify em caso de reexecução do script. Para forçar uma nova coleta de plataforma específica, basta remover o arquivo raw correspondente em `output_apify_ongs/`.

---

## 3. Normalização de Dados

Os *Actors* do Apify não garantem esquema fixo entre versões ou tipos de conteúdo: um post do Instagram pode expor o campo `likesCount`, enquanto uma publicação do Facebook usa `reactionsCount` para o mesmo conceito. A função `extract_first_existing()` resolveu essa heterogeneidade percorrendo listas de chaves candidatas em ordem de prioridade e retornando o primeiro valor não nulo encontrado, padrão análogo ao operador de coalescência nula comum em bancos de dados relacionais.

Campos críticos foram mapeados por meio de funções especializadas. O texto da publicação foi extraído por `extract_caption()`, que tentou sequencialmente `caption`, `text`, `description`, `message`, `title`, `alt`, `accessibilityCaption` e `shortCode`. Datas foram normalizadas pela função `parse_date()`, que reconheceu timestamps Unix tanto em segundos quanto em milissegundos (distinguidos pelo limiar `> 10.000.000.000`), além de strings ISO 8601, convertendo tudo para `pd.Timestamp` com fuso UTC. As métricas de engajamento (curtidas, comentários, compartilhamentos, visualizações) seguiram o mesmo padrão de múltiplos aliases.

A associação de cada item coletado à sua ONG correspondente ocorreu na função `find_ong_for_item()`. Para o Instagram, extraiu-se o nome de usuário do campo `ownerUsername` ou equivalente e comparou-se com os slugs derivados das URLs cadastradas via expressão regular `instagram\.com/([^/?#]+)`. Para o Facebook, o slug foi extraído da URL da página por decomposição de path, com tratamento especial para URLs no formato `/people/<nome>/<id>`. Em ambos os casos, a comparação foi realizada sobre texto normalizado por `normalize_text()`, que converteu para minúsculas, removeu acentos via `unicodedata.normalize("NFD")` e descartou caracteres da categoria Unicode `Mn` (marcas de combinação). Itens sem correspondência foram rotulados como "ONG não identificada".

---

## 4. Mineração de Texto: Classificação por Categorias Temáticas

A classificação das publicações fundamentou-se em mineração de texto por correspondência de expressões regulares (*pattern matching*), técnica pertencente ao escopo da mineração de dados textuais (*text mining*) baseada em regras. Esse método não emprega modelos probabilísticos ou vetorização semântica; ao contrário, opera com dicionários de padrões construídos manualmente a partir do vocabulário característico de cada tema, o que garante interpretabilidade total e controle preciso sobre os critérios de classificação.

Oito categorias foram definidas no dicionário `CATEGORY_PATTERNS`:

| Categoria | Exemplos de padrões |
|---|---|
| `campanha_doacao` | `\bdoe\b`, `\bpix\b`, `\bvaquinha\b`, `\brifa\b`, `\bracao\b` |
| `campanha_adocao` | `\bfeira de adocao\b`, `\badote\b`, `\bnovo lar\b` |
| `animal_para_adocao` | `\bpara adocao\b`, `\bfilhote\b`, `\bcastrado\b`, `\bvacinado\b` |
| `resgate_ou_caso_clinico` | `\bresgate\b`, `\batropelad`, `\bcirurgia\b`, `\bveterinari` |
| `castracao` | `\bcastracao\b`, `\bmutirao de castracao\b`, `\besterilizacao\b` |
| `prestacao_de_contas` | `\btransparencia\b`, `\bcomprovante\b`, `\barrecadad` |
| `educacao_conscientizacao` | `\bmaus tratos\b`, `\bdenuncie\b`, `\bposse responsavel\b` |
| `evento_parceria` | `\bevento\b`, `\bbazar\b`, `\bbrecho\b`, `\bmutirao\b` |

Antes da classificação, cada texto passou pela mesma normalização descrita na seção anterior, com remoção de acentos e conversão para minúsculas, o que permitiu que padrões sem acento correspondessem ao texto original acentuado sem necessidade de duplicar as entradas. A função `classify_text()` retornou um dicionário booleano por categoria mais a chave `categorias`, que concatenou os nomes de todas as categorias ativadas separados por ponto e vírgula. Publicações sem correspondência em nenhuma categoria receberam o rótulo `outros`. O modelo admite múltiplos rótulos simultaneamente, pois uma publicação pode abordar resgate e campanha de doação no mesmo texto.

---

## 5. Filtragem Temporal

O filtro de data aplicou-se exclusivamente às postagens (posts), não aos stories. Stories têm validade de 24 horas nas plataformas, portanto o dataset de stories registra apenas o estado ativo no momento da execução, sendo semanticamente incoerente aplicar filtro retroativo a esse tipo de conteúdo.

Para os posts, o Actor do Instagram aceita o parâmetro `onlyPostsNewerThan`, que limita a busca pela data de início do período. Por não existir parâmetro análogo para a data final na API do scraper de Instagram, aplicou-se um filtro local após a coleta: o DataFrame foi restrito ao intervalo `[PERIODO_INICIO, PERIODO_FIM 23:59:59]` com todos os timestamps em UTC, prevenindo falsos positivos por diferença de fuso horário. O scraper do Facebook aceitou ambos os parâmetros de data diretamente no `run_input`.

---

## 6. Saídas Geradas

A execução produziu oito arquivos no diretório `output_apify_ongs/`:

- **`raw_instagram_posts.json`**, **`raw_instagram_stories.json`**, **`raw_facebook_posts.json`**: dados brutos preservados para reprocessamento sem custo adicional de API.
- **`posts_classificados.csv`** e **`posts_classificados.json`**: dataset consolidado de Instagram e Facebook com todos os campos normalizados e flags de classificação.
- **`stories_ativos_classificados.csv`** e **`stories_ativos_classificados.json`**: dataset de stories com o mesmo schema.
- **`relatorio_mineracao_ongs_fev_mar_abr_2026.txt`**: relatório analítico em texto plano com nove seções, resumo executivo com totais por categoria, distribuição por ONG, distribuição mensal, cruzamento ONG × mês, listagens de publicações por categoria temática e observações metodológicas.

---

## 7. Limitações e Condicionantes Técnicos

A raspagem de perfis públicos no Instagram enfrenta bloqueios ativos da Meta, que detecta padrões de requisição automatizada e retorna erros 429 ou respostas HTML em endpoints JSON. Os logs de execução registraram múltiplas tentativas recusadas com mensagens `Request blocked, retrying with different session`, tratadas automaticamente pela infraestrutura de rotação de sessões do Apify. Perfis com visibilidade restrita ou sem publicações no período resultaram em zero itens sem interromper o processo.

A classificação por palavras-chave apresenta limitações inerentes ao método baseado em regras: termos ambíguos podem ativar categorias incorretas (por exemplo, `\bcastrado\b` classifica tanto o animal como candidato à adoção quanto a campanha de castração), e publicações com linguagem figurada ou abreviações fora do dicionário escapam à categorização. A revisão manual de amostras representativas constitui etapa complementar necessária para validação dos resultados.

A cobertura da base de ONGs limitou-se às 28 organizações identificadas previamente para o escopo geográfico definido. Organizações sem presença pública nas plataformas suportadas ou com perfis privados ficaram fora do alcance da coleta.

Por fim, os dados do Facebook apresentaram maior variabilidade de cobertura que os do Instagram, dado que o formato e a visibilidade de páginas no Facebook dependem de configurações individuais de privacidade e das políticas de acesso da plataforma, que se tornaram progressivamente mais restritivas desde 2018.

---

## 8. Conceitos de Mineração de Dados Aplicados

| Conceito | Aplicação no script |
|---|---|
| **Web scraping** | Extração automatizada de postagens via Apify Actors com rotação de proxies |
| **Extração de características (*feature extraction*)** | Derivação de campos normalizados (data UTC, mês, engajamento) a partir de JSON heterogêneo |
| **Classificação por regras (*rule-based classification*)** | Atribuição de categorias temáticas por dicionário de expressões regulares |
| **Normalização textual** | Remoção de acentos e padronização de caixa para comparação invariante a diacríticos |
| **Filtragem temporal** | Restrição do corpus ao intervalo de análise por parse e comparação de timestamps UTC |
| **Resolução de entidades (*entity resolution*)** | Associação de itens coletados às ONGs cadastradas por correspondência de slugs e usernames |
| **Persistência incremental (*checkpointing*)** | Cache em disco de dados brutos para reprocessamento sem nova chamada à API |
| **Classificação multi-rótulo (*multi-label classification*)** | Atribuição simultânea de múltiplas categorias temáticas a uma mesma publicação |
