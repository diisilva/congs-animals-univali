import os
import re
import json
import unicodedata
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
from apify_client import ApifyClient
from dotenv import load_dotenv


# ============================================================
# CONFIGURAÇÕES GERAIS
# ============================================================

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")

if not APIFY_TOKEN:
    raise RuntimeError(
        "APIFY_TOKEN não encontrado. Crie um arquivo .env com APIFY_TOKEN=seu_token"
    )

client = ApifyClient(APIFY_TOKEN)

OUTPUT_DIR = Path("output_apify_ongs")
OUTPUT_DIR.mkdir(exist_ok=True)

PERIODO_INICIO = "2026-02-01"
PERIODO_FIM = "2026-04-30"

RESULTS_LIMIT_INSTAGRAM_POSTS = 100
RESULTS_LIMIT_INSTAGRAM_STORIES = 50
RESULTS_LIMIT_FACEBOOK_POSTS = 100

RODAR_INSTAGRAM_POSTS = True
RODAR_INSTAGRAM_STORIES = True
RODAR_FACEBOOK_POSTS = True


# ============================================================
# BASE DE ONGS
# Fonte: anexo enviado com nomes, cidades e redes sociais.
# ============================================================

ONGS = [
    {
        "nome": "Associação de Proteção Animal Peludinhos BC",
        "cidade": "Balneário Camboriú/SC",
        "instagram": "https://www.instagram.com/peludinhos.bc/",
        "facebook": "https://www.facebook.com/people/Peludinhos-BC/100089120010921/",
    },
    {
        "nome": "ONG Defesa Animal",
        "cidade": "Balneário Camboriú/SC",
        "instagram": "https://www.instagram.com/ongdefesanimal/",
        "facebook": "https://www.facebook.com/ongdefesaanimal/",
    },
    {
        "nome": "Viva Bicho — Associação de Proteção aos Animais",
        "cidade": "Balneário Camboriú/SC",
        "instagram": "https://www.instagram.com/ongvivabichobc/",
        "facebook": "https://www.facebook.com/ongvivabicho/",
    },
    {
        "nome": "ADAB — Defensores de Animais de Blumenau",
        "cidade": "Blumenau/SC",
        "instagram": None,
        "facebook": "https://www.facebook.com/adabbnu/",
    },
    {
        "nome": "APRABLU — Protetora de Animais de Blumenau",
        "cidade": "Blumenau/SC",
        "instagram": "https://www.instagram.com/aprablu/",
        "facebook": "https://www.facebook.com/aprablu/",
    },
    {
        "nome": "Associação Sítio Dona Lúcia",
        "cidade": "Blumenau/SC",
        "instagram": "https://www.instagram.com/sitiodonalucia/",
        "facebook": "https://www.facebook.com/sitiodonalucia/",
    },
    {
        "nome": "Hachi ONG — Proteção Animal",
        "cidade": "Blumenau/SC",
        "instagram": "https://www.instagram.com/hachiong/",
        "facebook": None,
    },
    {
        "nome": "Instituto Bem Animal",
        "cidade": "Blumenau/SC",
        "instagram": "https://www.instagram.com/institutobemanimal/",
        "facebook": "https://m.facebook.com/bemanimalsc/about/",
    },
    {
        "nome": "Instituto Focinho Feliz",
        "cidade": "Blumenau/SC",
        "instagram": "https://www.instagram.com/oinstitutofocinhofelizoficial/",
        "facebook": "https://www.facebook.com/institutofocinhofeliz/",
    },
    {
        "nome": "ONG Guerreiro Caramelo",
        "cidade": "Blumenau/SC",
        "instagram": "https://www.instagram.com/ongguerreirocaramelo/",
        "facebook": None,
    },
    {
        "nome": "Operação Gato de Rua",
        "cidade": "Blumenau/SC",
        "instagram": None,
        "facebook": "https://www.facebook.com/gatoderuablumenau/",
    },
    {
        "nome": "ResGatinhos Blumenau",
        "cidade": "Blumenau/SC",
        "instagram": "https://www.instagram.com/resgatinhosblumenau/",
        "facebook": None,
    },
    {
        "nome": "ACAPRA Brusque",
        "cidade": "Brusque/SC",
        "instagram": "https://www.instagram.com/acaprabrusquesc/",
        "facebook": None,
    },
    {
        "nome": "Protetores Voluntários de Camboriú",
        "cidade": "Camboriú/SC",
        "instagram": "https://www.instagram.com/protetores_camboriu/",
        "facebook": "https://www.facebook.com/camboriuprotetoresvoluntarios/",
    },
    {
        "nome": "AGAPA — Associação Gasparense de Proteção dos Animais",
        "cidade": "Gaspar/SC",
        "instagram": "https://www.instagram.com/agapagaspar/",
        "facebook": "https://www.facebook.com/agapagaspar/",
    },
    {
        "nome": "Abrigo São Francisco de Assis",
        "cidade": "Gaspar/SC",
        "instagram": "https://www.instagram.com/abrigosaofranciscodeassis/",
        "facebook": "https://www.facebook.com/abrigosfassis/",
    },
    {
        "nome": "Causa Animal Ilhota",
        "cidade": "Ilhota/SC",
        "instagram": "https://www.instagram.com/causaanimal.ilhota/",
        "facebook": None,
    },
    {
        "nome": "Associação Protetora Refúgio Animal",
        "cidade": "Indaial/SC",
        "instagram": None,
        "facebook": None,
    },
    {
        "nome": "Entre Cães & Gatos",
        "cidade": "Indaial/SC",
        "instagram": "https://www.instagram.com/ongentrecaesegatos/",
        "facebook": None,
    },
    {
        "nome": "AIPRA — Proteção aos Animais de Itajaí",
        "cidade": "Itajaí/SC",
        "instagram": None,
        "facebook": "https://www.facebook.com/AIPRAPROTECAOANIMAL/",
    },
    {
        "nome": "Associação Amor Animal",
        "cidade": "Itajaí/SC",
        "instagram": "https://www.instagram.com/amoranimalitajai/",
        "facebook": "https://www.facebook.com/amoranimalitajai/",
    },
    {
        "nome": "Instituto Anjos do Mar Brasil",
        "cidade": "Itajaí/SC",
        "instagram": "https://www.instagram.com/anjosdomarbr/",
        "facebook": None,
    },
    {
        "nome": "INIS — Diretoria de Defesa Animal",
        "cidade": "Itajaí/SC",
        "instagram": "https://www.instagram.com/inis.itajai/",
        "facebook": None,
    },
    {
        "nome": "OBRAPA — Organização Brasileira de Proteção Animal",
        "cidade": "Itajaí/SC",
        "instagram": None,
        "facebook": "https://www.facebook.com/ongobrapa/",
    },
    {
        "nome": "SOS Peludinhos",
        "cidade": "Itajaí/SC",
        "instagram": "https://www.instagram.com/sos_peludinhos/",
        "facebook": "https://www.facebook.com/oscipsospeludinhos/",
    },
    {
        "nome": "UAPA — Unidade de Acolhimento Provisório de Animais",
        "cidade": "Itajaí/SC",
        "instagram": "https://www.instagram.com/uapa.itajai/",
        "facebook": None,
    },
    {
        "nome": "Pró-Bichos de Navegantes",
        "cidade": "Navegantes/SC",
        "instagram": "https://www.instagram.com/probichosnavegantes/",
        "facebook": "https://www.facebook.com/VSProBichos/",
    },
    {
        "nome": "Adote Penha",
        "cidade": "Penha/SC",
        "instagram": "https://www.instagram.com/adotepenha/",
        "facebook": None,
    },
]


# ============================================================
# UTILITÁRIOS
# ============================================================

def normalize_text(value: Any) -> str:
    if value is None:
        return ""

    text = str(value).lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return text


def instagram_username(url: Optional[str]) -> Optional[str]:
    if not url:
        return None

    match = re.search(r"instagram\.com/([^/?#]+)/?", url)
    if not match:
        return None

    return match.group(1).strip().lower()


def facebook_slug(url: Optional[str]) -> Optional[str]:
    if not url:
        return None

    cleaned = url.split("?")[0].rstrip("/")
    parts = cleaned.split("/")

    if "people" in parts:
        idx = parts.index("people")
        if len(parts) > idx + 1:
            return parts[idx + 1].lower()

    return parts[-1].lower() if parts else None


def parse_date(value: Any) -> Optional[pd.Timestamp]:
    if value is None or value == "":
        return None

    try:
        if isinstance(value, (int, float)):
            # Alguns scrapers retornam epoch em segundos ou milissegundos.
            if value > 10_000_000_000:
                return pd.to_datetime(value, unit="ms", utc=True)
            return pd.to_datetime(value, unit="s", utc=True)

        return pd.to_datetime(value, utc=True, errors="coerce")
    except Exception:
        return None


def extract_first_existing(item: Dict[str, Any], keys: List[str]) -> Any:
    for key in keys:
        if key in item and item[key] not in [None, ""]:
            return item[key]
    return None


def extract_caption(item: Dict[str, Any]) -> str:
    value = extract_first_existing(
        item,
        [
            "caption",
            "text",
            "description",
            "message",
            "title",
            "alt",
            "accessibilityCaption",
            "shortCode",
        ],
    )
    return "" if value is None else str(value)


def extract_url(item: Dict[str, Any]) -> str:
    value = extract_first_existing(
        item,
        [
            "url",
            "postUrl",
            "displayUrl",
            "link",
            "permalink",
            "shortCode",
        ],
    )
    return "" if value is None else str(value)


def extract_timestamp(item: Dict[str, Any]) -> Optional[pd.Timestamp]:
    raw = extract_first_existing(
        item,
        [
            "timestamp",
            "takenAtTimestamp",
            "createdAt",
            "date",
            "time",
            "publishedAt",
            "postedAt",
            "creationTime",
        ],
    )
    return parse_date(raw)


def get_engagement(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "likes": extract_first_existing(
            item,
            ["likesCount", "likes", "likeCount", "reactionsCount", "reactionCount"],
        ),
        "comments": extract_first_existing(
            item,
            ["commentsCount", "comments", "commentCount"],
        ),
        "shares": extract_first_existing(
            item,
            ["sharesCount", "shares", "shareCount"],
        ),
        "views": extract_first_existing(
            item,
            ["videoViewCount", "viewsCount", "views", "playCount"],
        ),
    }


def find_ong_for_item(item: Dict[str, Any], platform: str) -> Dict[str, Any]:
    item_text = normalize_text(json.dumps(item, ensure_ascii=False))

    if platform == "instagram":
        owner = normalize_text(
            extract_first_existing(
                item,
                [
                    "ownerUsername",
                    "username",
                    "profileName",
                    "inputUrl",
                    "input",
                ],
            )
        )

        for ong in ONGS:
            username = instagram_username(ong.get("instagram"))
            if username and (
                normalize_text(username) in owner
                or normalize_text(username) in item_text
            ):
                return ong

    if platform == "facebook":
        for ong in ONGS:
            slug = facebook_slug(ong.get("facebook"))
            if slug and normalize_text(slug) in item_text:
                return ong

    return {
        "nome": "ONG não identificada",
        "cidade": "",
        "instagram": None,
        "facebook": None,
    }


# ============================================================
# CLASSIFICAÇÃO DE CONTEÚDO
# ============================================================

CATEGORY_PATTERNS = {
    "campanha_doacao": [
        r"\bdoe\b",
        r"\bdoacao\b",
        r"\bdoacoes\b",
        r"\bdoar\b",
        r"\bajude\b",
        r"\bajuda\b",
        r"\bpix\b",
        r"\bvakinha\b",
        r"\bvaquinha\b",
        r"\brifa\b",
        r"\bracao\b",
        r"\bmedicamento",
        r"\bcobertor",
        r"\bcaminha",
        r"\bareia\b",
        r"\bpatrocin",
        r"\bcontribu",
        r"\bcolabore\b",
        r"\bcesta\b",
        r"\binsumo",
    ],
    "campanha_adocao": [
        r"\bfeira de adocao\b",
        r"\bfeirinha\b",
        r"\bcampanha de adocao\b",
        r"\badocao responsavel\b",
        r"\badote\b",
        r"\badotar\b",
        r"\bprocura.*lar\b",
        r"\bnovo lar\b",
    ],
    "animal_para_adocao": [
        r"\bdisponivel para adocao\b",
        r"\bdisponiveis para adocao\b",
        r"\bpara adocao\b",
        r"\bquer uma familia\b",
        r"\bprocurando uma familia\b",
        r"\bprocurando lar\b",
        r"\blar responsavel\b",
        r"\bfilhote\b",
        r"\bcastrado\b",
        r"\bvacinado\b",
    ],
    "resgate_ou_caso_clinico": [
        r"\bresgate\b",
        r"\bresgatad",
        r"\batropelad",
        r"\bcirurgia\b",
        r"\btratamento\b",
        r"\bveterinari",
        r"\binternad",
        r"\bemergencia\b",
        r"\bfratura\b",
        r"\bdoente\b",
        r"\bferid",
    ],
    "castracao": [
        r"\bcastracao\b",
        r"\bcastrar\b",
        r"\bcastrado\b",
        r"\bmutirao de castracao\b",
        r"\besterilizacao\b",
    ],
    "prestacao_de_contas": [
        r"\bprestacao de contas\b",
        r"\btransparencia\b",
        r"\bcomprovante\b",
        r"\brecibo\b",
        r"\bnota fiscal\b",
        r"\barrecadad",
        r"\bvalor recebido\b",
        r"\bvalor gasto\b",
    ],
    "educacao_conscientizacao": [
        r"\bmaus tratos\b",
        r"\babandono\b",
        r"\bdenuncie\b",
        r"\bdenuncia\b",
        r"\bguarda responsavel\b",
        r"\bconscientizacao\b",
        r"\bcuidados\b",
        r"\bposse responsavel\b",
    ],
    "evento_parceria": [
        r"\bevento\b",
        r"\bparceria\b",
        r"\bbazar\b",
        r"\bbrecho\b",
        r"\bacao\b",
        r"\bencontro\b",
        r"\bmutirao\b",
    ],
}


def classify_text(text: str) -> Dict[str, Any]:
    normalized = normalize_text(text)

    flags = {}
    categories_found = []

    for category, patterns in CATEGORY_PATTERNS.items():
        matched = any(re.search(pattern, normalized) for pattern in patterns)
        flags[category] = matched
        if matched:
            categories_found.append(category)

    if not categories_found:
        categories_found.append("outros")

    flags["categorias"] = "; ".join(categories_found)
    return flags


# ============================================================
# EXECUÇÃO APIFY
# ============================================================

def run_actor(actor_id: str, run_input: Dict[str, Any]) -> List[Dict[str, Any]]:
    print(f"\nRodando Actor: {actor_id}")
    print(json.dumps(run_input, ensure_ascii=False, indent=2))

    run = client.actor(actor_id).call(run_input=run_input)

    dataset_id = run.get("defaultDatasetId")
    status = run.get("status")

    if status != "SUCCEEDED":
        raise RuntimeError(f"Actor {actor_id} terminou com status {status}. Run: {run}")

    if not dataset_id:
        return []

    items = list(client.dataset(dataset_id).iterate_items())
    print(f"Itens coletados em {actor_id}: {len(items)}")
    return items


def scrape_instagram_posts() -> List[Dict[str, Any]]:
    urls = [ong["instagram"] for ong in ONGS if ong.get("instagram")]

    run_input = {
        "resultsType": "posts",
        "directUrls": urls,
        "resultsLimit": RESULTS_LIMIT_INSTAGRAM_POSTS,
        "onlyPostsNewerThan": PERIODO_INICIO,
        "addParentData": True,
    }

    return run_actor("apify/instagram-scraper", run_input)


def scrape_instagram_stories() -> List[Dict[str, Any]]:
    urls = [ong["instagram"] for ong in ONGS if ong.get("instagram")]

    run_input = {
        "resultsType": "stories",
        "directUrls": urls,
        "resultsLimit": RESULTS_LIMIT_INSTAGRAM_STORIES,
        "addParentData": True,
    }

    return run_actor("apify/instagram-scraper", run_input)


def scrape_facebook_posts() -> List[Dict[str, Any]]:
    urls = [{"url": ong["facebook"]} for ong in ONGS if ong.get("facebook")]

    run_input = {
        "startUrls": urls,
        "resultsLimit": RESULTS_LIMIT_FACEBOOK_POSTS,
        "onlyPostsNewerThan": PERIODO_INICIO,
        "onlyPostsOlderThan": PERIODO_FIM,
        "captionText": False,
    }

    return run_actor("apify/facebook-posts-scraper", run_input)


# ============================================================
# NORMALIZAÇÃO
# ============================================================

def normalize_items(items: List[Dict[str, Any]], platform: str, is_story: bool = False) -> pd.DataFrame:
    rows = []

    for item in items:
        ong = find_ong_for_item(item, platform)
        caption = extract_caption(item)
        post_url = extract_url(item)
        timestamp = extract_timestamp(item)
        engagement = get_engagement(item)
        flags = classify_text(caption)

        row = {
            "plataforma": platform,
            "tipo_conteudo": "story" if is_story else "post",
            "ong": ong.get("nome"),
            "cidade": ong.get("cidade"),
            "data_utc": timestamp.isoformat() if timestamp is not None and not pd.isna(timestamp) else "",
            "mes": timestamp.strftime("%Y-%m") if timestamp is not None and not pd.isna(timestamp) else "",
            "url": post_url,
            "caption": caption,
            "likes": engagement["likes"],
            "comments": engagement["comments"],
            "shares": engagement["shares"],
            "views": engagement["views"],
            "raw_json": json.dumps(item, ensure_ascii=False),
        }

        row.update(flags)
        rows.append(row)

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    if not is_story:
        df["data_parse"] = pd.to_datetime(df["data_utc"], utc=True, errors="coerce")
        inicio = pd.to_datetime(PERIODO_INICIO, utc=True)
        fim = pd.to_datetime(PERIODO_FIM + " 23:59:59", utc=True)

        df = df[(df["data_parse"] >= inicio) & (df["data_parse"] <= fim)]
        df = df.drop(columns=["data_parse"])

    return df


# ============================================================
# RELATÓRIO TXT
# ============================================================

def bool_sum(df: pd.DataFrame, col: str) -> int:
    if df.empty or col not in df.columns:
        return 0
    return int(df[col].fillna(False).astype(bool).sum())


def safe_to_string(df: pd.DataFrame, max_rows: int = 200) -> str:
    if df.empty:
        return "Sem registros encontrados."
    return df.head(max_rows).to_string(index=False)


def generate_report(df_posts: pd.DataFrame, df_stories: pd.DataFrame) -> str:
    lines = []

    lines.append("MINERAÇÃO DE POSTAGENS — ONGS DE PROTEÇÃO ANIMAL")
    lines.append(f"Período analisado: {PERIODO_INICIO} até {PERIODO_FIM}")
    lines.append(f"Data/hora de geração: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("=" * 80)
    lines.append("1. RESUMO EXECUTIVO")
    lines.append("=" * 80)
    lines.append("")

    total_posts = len(df_posts)
    total_stories = len(df_stories)

    lines.append(f"Total de postagens coletadas no período: {total_posts}")
    lines.append(f"Total de stories ativos coletados no momento da execução: {total_stories}")
    lines.append(f"Postagens com campanha de doação: {bool_sum(df_posts, 'campanha_doacao')}")
    lines.append(f"Postagens com campanha de adoção: {bool_sum(df_posts, 'campanha_adocao')}")
    lines.append(f"Postagens de animais para adoção: {bool_sum(df_posts, 'animal_para_adocao')}")
    lines.append(f"Postagens de resgate ou caso clínico: {bool_sum(df_posts, 'resgate_ou_caso_clinico')}")
    lines.append(f"Postagens sobre castração: {bool_sum(df_posts, 'castracao')}")
    lines.append(f"Postagens com prestação de contas: {bool_sum(df_posts, 'prestacao_de_contas')}")
    lines.append("")

    lines.append("=" * 80)
    lines.append("2. QUANTIDADE DE POSTAGENS POR ONG")
    lines.append("=" * 80)
    lines.append("")

    if not df_posts.empty:
        resumo_ong = (
            df_posts.groupby(["ong", "cidade"], dropna=False)
            .agg(
                total_posts=("url", "count"),
                campanhas_doacao=("campanha_doacao", "sum"),
                campanhas_adocao=("campanha_adocao", "sum"),
                animais_para_adocao=("animal_para_adocao", "sum"),
                resgates_casos_clinicos=("resgate_ou_caso_clinico", "sum"),
                castracao=("castracao", "sum"),
                prestacao_de_contas=("prestacao_de_contas", "sum"),
            )
            .reset_index()
            .sort_values(["total_posts", "campanhas_doacao", "campanhas_adocao"], ascending=False)
        )
        lines.append(safe_to_string(resumo_ong))
    else:
        lines.append("Sem postagens encontradas no período.")
    lines.append("")

    lines.append("=" * 80)
    lines.append("3. QUANTIDADE POR MÊS")
    lines.append("=" * 80)
    lines.append("")

    if not df_posts.empty:
        resumo_mes = (
            df_posts.groupby(["mes"], dropna=False)
            .agg(
                total_posts=("url", "count"),
                campanhas_doacao=("campanha_doacao", "sum"),
                campanhas_adocao=("campanha_adocao", "sum"),
                animais_para_adocao=("animal_para_adocao", "sum"),
                resgates_casos_clinicos=("resgate_ou_caso_clinico", "sum"),
                castracao=("castracao", "sum"),
                prestacao_de_contas=("prestacao_de_contas", "sum"),
            )
            .reset_index()
            .sort_values("mes")
        )
        lines.append(safe_to_string(resumo_mes))
    else:
        lines.append("Sem postagens encontradas no período.")
    lines.append("")

    lines.append("=" * 80)
    lines.append("4. QUANTIDADE POR ONG E MÊS")
    lines.append("=" * 80)
    lines.append("")

    if not df_posts.empty:
        resumo_ong_mes = (
            df_posts.groupby(["ong", "mes"], dropna=False)
            .agg(
                total_posts=("url", "count"),
                campanhas_doacao=("campanha_doacao", "sum"),
                campanhas_adocao=("campanha_adocao", "sum"),
                animais_para_adocao=("animal_para_adocao", "sum"),
                resgates_casos_clinicos=("resgate_ou_caso_clinico", "sum"),
            )
            .reset_index()
            .sort_values(["ong", "mes"])
        )
        lines.append(safe_to_string(resumo_ong_mes, max_rows=500))
    else:
        lines.append("Sem postagens encontradas no período.")
    lines.append("")

    lines.append("=" * 80)
    lines.append("5. POSTAGENS CLASSIFICADAS COMO CAMPANHA DE DOAÇÃO")
    lines.append("=" * 80)
    lines.append("")

    if not df_posts.empty:
        doacoes = df_posts[df_posts["campanha_doacao"] == True][
            ["ong", "mes", "plataforma", "url", "caption"]
        ].copy()
        doacoes["caption"] = doacoes["caption"].str.slice(0, 300)
        lines.append(safe_to_string(doacoes, max_rows=200))
    else:
        lines.append("Sem registros.")
    lines.append("")

    lines.append("=" * 80)
    lines.append("6. POSTAGENS CLASSIFICADAS COMO CAMPANHA DE ADOÇÃO")
    lines.append("=" * 80)
    lines.append("")

    if not df_posts.empty:
        adocoes = df_posts[df_posts["campanha_adocao"] == True][
            ["ong", "mes", "plataforma", "url", "caption"]
        ].copy()
        adocoes["caption"] = adocoes["caption"].str.slice(0, 300)
        lines.append(safe_to_string(adocoes, max_rows=200))
    else:
        lines.append("Sem registros.")
    lines.append("")

    lines.append("=" * 80)
    lines.append("7. POSTAGENS DE ANIMAIS PARA ADOÇÃO")
    lines.append("=" * 80)
    lines.append("")

    if not df_posts.empty:
        animais = df_posts[df_posts["animal_para_adocao"] == True][
            ["ong", "mes", "plataforma", "url", "caption"]
        ].copy()
        animais["caption"] = animais["caption"].str.slice(0, 300)
        lines.append(safe_to_string(animais, max_rows=300))
    else:
        lines.append("Sem registros.")
    lines.append("")

    lines.append("=" * 80)
    lines.append("8. STORIES ATIVOS NO MOMENTO DA COLETA")
    lines.append("=" * 80)
    lines.append("")

    if not df_stories.empty:
        stories_cols = ["ong", "cidade", "plataforma", "url", "caption", "categorias"]
        available_cols = [col for col in stories_cols if col in df_stories.columns]
        stories_view = df_stories[available_cols].copy()
        if "caption" in stories_view.columns:
            stories_view["caption"] = stories_view["caption"].str.slice(0, 300)
        lines.append(safe_to_string(stories_view, max_rows=300))
    else:
        lines.append("Nenhum story ativo retornado pelo scraper no momento da execução.")
    lines.append("")

    lines.append("=" * 80)
    lines.append("9. OBSERVAÇÕES E LIMITAÇÕES")
    lines.append("=" * 80)
    lines.append("")
    lines.append("- A coleta depende da disponibilidade pública dos perfis e páginas.")
    lines.append("- Stories são temporários; o relatório registra apenas stories ativos no momento da execução.")
    lines.append("- Instagram usa filtro de data mínima; por isso o script também filtra localmente até a data final.")
    lines.append("- A classificação é heurística por palavras-chave, podendo exigir revisão manual.")
    lines.append("- Postagens com múltiplos objetivos podem aparecer em mais de uma categoria.")
    lines.append("- Resultados de Facebook podem variar conforme bloqueios, restrições públicas e formato da página.")
    lines.append("")

    return "\n".join(lines)


# ============================================================
# MAIN
# ============================================================

def load_or_scrape(raw_path: Path, scrape_fn, label: str) -> List[Dict[str, Any]]:
    if raw_path.exists():
        print(f"\nArquivo '{raw_path}' já existe — carregando do disco (sem gastar tokens).")
        with open(raw_path, "r", encoding="utf-8") as f:
            return json.load(f)
    data = scrape_fn()
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Salvo: {raw_path}")
    return data


def main() -> None:
    instagram_posts_raw = []
    instagram_stories_raw = []
    facebook_posts_raw = []

    if RODAR_INSTAGRAM_POSTS:
        instagram_posts_raw = load_or_scrape(
            OUTPUT_DIR / "raw_instagram_posts.json",
            scrape_instagram_posts,
            "Instagram Posts",
        )

    if RODAR_INSTAGRAM_STORIES:
        instagram_stories_raw = load_or_scrape(
            OUTPUT_DIR / "raw_instagram_stories.json",
            scrape_instagram_stories,
            "Instagram Stories",
        )

    if RODAR_FACEBOOK_POSTS:
        facebook_posts_raw = load_or_scrape(
            OUTPUT_DIR / "raw_facebook_posts.json",
            scrape_facebook_posts,
            "Facebook Posts",
        )

    df_instagram_posts = normalize_items(instagram_posts_raw, platform="instagram", is_story=False)
    df_instagram_stories = normalize_items(instagram_stories_raw, platform="instagram", is_story=True)
    df_facebook_posts = normalize_items(facebook_posts_raw, platform="facebook", is_story=False)

    df_posts = pd.concat(
        [df_instagram_posts, df_facebook_posts],
        ignore_index=True,
    )

    df_stories = df_instagram_stories.copy()

    df_posts.to_csv(OUTPUT_DIR / "posts_classificados.csv", index=False, encoding="utf-8-sig")
    df_stories.to_csv(OUTPUT_DIR / "stories_ativos_classificados.csv", index=False, encoding="utf-8-sig")

    df_posts.to_json(
        OUTPUT_DIR / "posts_classificados.json",
        orient="records",
        force_ascii=False,
        indent=2,
    )

    df_stories.to_json(
        OUTPUT_DIR / "stories_ativos_classificados.json",
        orient="records",
        force_ascii=False,
        indent=2,
    )

    report = generate_report(df_posts, df_stories)

    report_path = OUTPUT_DIR / "relatorio_mineracao_ongs_fev_mar_abr_2026.txt"
    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report)

    print("\nArquivos gerados:")
    print(f"- {OUTPUT_DIR / 'raw_instagram_posts.json'}")
    print(f"- {OUTPUT_DIR / 'raw_instagram_stories.json'}")
    print(f"- {OUTPUT_DIR / 'raw_facebook_posts.json'}")
    print(f"- {OUTPUT_DIR / 'posts_classificados.csv'}")
    print(f"- {OUTPUT_DIR / 'stories_ativos_classificados.csv'}")
    print(f"- {OUTPUT_DIR / 'posts_classificados.json'}")
    print(f"- {OUTPUT_DIR / 'stories_ativos_classificados.json'}")
    print(f"- {report_path}")


if __name__ == "__main__":
    main()