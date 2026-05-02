import urllib.error
import urllib.request
import zlib


def _encode_6bit(value):
    if value < 10:
        return chr(48 + value)
    value -= 10
    if value < 26:
        return chr(65 + value)
    value -= 26
    if value < 26:
        return chr(97 + value)
    value -= 26
    if value == 0:
        return "-"
    if value == 1:
        return "_"
    return "?"


def _append_3bytes(b1, b2, b3):
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return (
        _encode_6bit(c1)
        + _encode_6bit(c2)
        + _encode_6bit(c3)
        + _encode_6bit(c4)
    )


def _plantuml_base64(data):
    result = []
    i = 0
    while i < len(data):
        b1 = data[i]
        b2 = data[i + 1] if i + 1 < len(data) else 0
        b3 = data[i + 2] if i + 2 < len(data) else 0
        result.append(_append_3bytes(b1, b2, b3))
        i += 3
    return "".join(result)


def plantuml_encode(plantuml_text):
    compressor = zlib.compressobj(level=9, wbits=-15)
    compressed = compressor.compress(plantuml_text.encode("utf-8")) + compressor.flush()
    return _plantuml_base64(compressed)


def generate_png(file_name, uml_code):
    print(f"Gerando diagrama: {file_name}.png")
    encoded_code = plantuml_encode(uml_code)
    url = f"https://www.plantuml.com/plantuml/png/{encoded_code}"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "image/png,*/*;q=0.8",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            content_type = response.headers.get("Content-Type", "")
            image_bytes = response.read()
    except urllib.error.HTTPError as err:
        body = err.read()
        error_file = f"{file_name}_erro_http.png"
        try:
            with open(error_file, "wb") as out_err:
                out_err.write(body)
        except OSError:
            pass
        raise RuntimeError(
            f"PlantUML HTTP {err.code}. Imagem de erro salva em: {error_file}"
        ) from err

    if not content_type.startswith("image/png"):
        raise RuntimeError("Resposta invalida do servidor PlantUML (nao retornou PNG).")

    with open(f"{file_name}.png", "wb") as out:
        out.write(image_bytes)

    print(f"Arquivo salvo: {file_name}.png")


def main():
    activity_code = """
@startuml
title Fluxo de Mineracao de Posts — ONGs de Protecao Animal\\n(mineracao_ongs_apify.py)

skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam defaultFontName Segoe UI
skinparam defaultFontSize 13
skinparam ArrowColor #1E293B
skinparam ActivityFontColor #0F172A
skinparam activity {
  BackgroundColor #EEF2FF
  BorderColor #1D4ED8
  DiamondBackgroundColor #FEF3C7
  DiamondBorderColor #B45309
  BarColor #334155
  StartColor #0EA5E9
  EndColor #22C55E
}
skinparam note {
  BackgroundColor #F8FAFC
  BorderColor #94A3B8
}
skinparam WrapWidth 240

start

:Carregar variaveis de ambiente (.env);
if (APIFY_TOKEN presente?) then (nao)
    :Lancar RuntimeError;
    stop
else (sim)
endif

note right
  Periodo: 2026-02-01 a 2026-04-30
  28 ONGs cadastradas (SC)
  Limites: 100 posts / 50 stories / 100 fb
end note

group Coleta — Instagram Posts {
    if (RODAR_INSTAGRAM_POSTS?) then (sim)
        if (raw_instagram_posts.json existe no disco?) then (sim)
            :Carregar JSON do disco\\n(sem consumir tokens);
        else (nao)
            :Chamar Actor apify/instagram-scraper\\nresultsType=posts, 23 URLs;
            :Salvar raw_instagram_posts.json;
        endif
    else (nao)
        :Ignorar etapa;
    endif
}

group Coleta — Instagram Stories {
    if (RODAR_INSTAGRAM_STORIES?) then (sim)
        if (raw_instagram_stories.json existe no disco?) then (sim)
            :Carregar JSON do disco;
        else (nao)
            :Chamar Actor apify/instagram-scraper\\nresultsType=stories, 23 URLs;
            :Salvar raw_instagram_stories.json;
        endif
    else (nao)
        :Ignorar etapa;
    endif
}

group Coleta — Facebook Posts {
    if (RODAR_FACEBOOK_POSTS?) then (sim)
        if (raw_facebook_posts.json existe no disco?) then (sim)
            :Carregar JSON do disco;
        else (nao)
            :Chamar Actor apify/facebook-posts-scraper\\n22 paginas, com filtro de periodo;
            :Salvar raw_facebook_posts.json;
        endif
    else (nao)
        :Ignorar etapa;
    endif
}

group Normalizacao (para cada plataforma) {
    :Para cada item coletado:;
    fork
        :Identificar ONG\\n(match por username/slug);
    fork again
        :Extrair caption, URL,\\ntimestamp e engajamento;
    fork again
        :Classificar conteudo\\npor palavras-chave\\n(8 categorias);
    end fork
    :Montar linha do DataFrame;
    if (E um post (nao story)?) then (sim)
        :Filtrar por intervalo de datas\\n(PERIODO_INICIO ate PERIODO_FIM);
    else (nao)
        :Manter todos os stories\\n(sem filtro de data);
    endif
}

:Concatenar Instagram Posts + Facebook Posts\\nem df_posts;
:Manter df_stories separado;

group Exportacao de Arquivos {
    fork
        :posts_classificados.csv;
    fork again
        :posts_classificados.json;
    fork again
        :stories_ativos_classificados.csv;
    fork again
        :stories_ativos_classificados.json;
    end fork
}

group Relatorio TXT {
    :1. Resumo executivo (totais e contagens por categoria);
    :2. Posts por ONG;
    :3. Posts por mes;
    :4. Posts por ONG e mes;
    :5. Campanhas de doacao (caption truncado);
    :6. Campanhas de adocao;
    :7. Animais para adocao;
    :8. Stories ativos;
    :9. Observacoes e limitacoes;
    :Salvar relatorio_mineracao_ongs_fev_mar_abr_2026.txt;
}

:Exibir paths dos 8 arquivos gerados;

stop

@enduml
"""

    try:
        generate_png("fluxo_mineracao_ongs", activity_code)
    except (urllib.error.URLError, OSError, RuntimeError) as exc:
        print(f"Erro ao gerar diagrama: {exc}")
        print("Verifique conexao com internet e tente novamente.")


if __name__ == "__main__":
    main()
