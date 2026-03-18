import streamlit as st
import google.generativeai as genai
import os

# ── CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="YouTube Faceless Strategy Agent",
    page_icon="🎯",
    layout="centered"
)

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    "gemini-1.5-pro",
    generation_config={"max_output_tokens": 8192, "temperature": 0.7}
)

# ── PROMPTS ──────────────────────────────────────
def prompt_generate_a(nicho, keywords, language):
    return f"""
IDIOMA DE RESPOSTA: Português do Brasil.
Você é um estrategista sênior de canais YouTube Faceless com IA.
REGRA ABSOLUTA: Use dados reais. Não invente nada.

NICHO DO CANAL: {nicho}
KEYWORDS: {keywords}
IDIOMA DO CANAL: {language}

Gere APENAS as Seções 1 a 10. Formato Markdown estruturado. Sem HTML.
Não resuma. Não pule nenhuma seção. Máxima completude.

## SEÇÃO 1 — VALIDAÇÃO DO NICHO
[3 filtros + scoring 7 dimensões com justificativas + checklist 6 itens]

## SEÇÃO 2 — POSIÇÃO NOS RANKINGS
[Top 10 Evergreen + Top 25 Micro-Nichos]

## SEÇÃO 3 — HIERARQUIA DO NICHO
[Nicho Amplo > Micro-Nicho > Pico-Nicho + Lifecycle]

## SEÇÃO 4 — CANAIS DE REFERÊNCIA
[tabela com 5+ canais reais: nome, subs, vídeos, destaque, idioma]

## SEÇÃO 5 — NICHE STACKING
[5 combinações do PDF + 3 específicas + 5 motivos por que funciona]

## SEÇÃO 6 — MICRO-NICHOS RELACIONADOS
[tabela: posição, buscas, competição, RPM, dificuldade, idioma]

## SEÇÃO 7 — PICO-NICHOS ULTRA-ESPECÍFICOS
[lista com 10+ pico-nichos: nome, qtd vídeos, exemplo de série]

## SEÇÃO 8 — ESTRATÉGIA MULTI-IDIOMA
[tabela 5 idiomas: CPM, competição, audiência, recomendação + auto-dubbing 2026]

## SEÇÃO 9 — FRAMEWORK DE DECISÃO POR OBJETIVO
[tabela objetivo > nichos > por quê + melhor encaixe para este nicho]

## SEÇÃO 10 — OS 6 SEGREDOS DO BLUEPRINT
[cada segredo adaptado ao nicho com números concretos]
"""

def prompt_generate_b(nicho, keywords, language):
    return f"""
IDIOMA DE RESPOSTA: Português do Brasil.
Você é um estrategista sênior de canais YouTube Faceless com IA.

NICHO DO CANAL: {nicho}
KEYWORDS: {keywords}
IDIOMA DO CANAL: {language}

Gere APENAS as Seções 11 a 20. Formato Markdown estruturado. Sem HTML.
Não resuma. Não pule nenhuma seção. Máxima completude.

## SEÇÃO 11 — PROJEÇÃO DE CRESCIMENTO
[tabela mês 1/3/6/12: vídeos, subs, views, receita ajustada ao RPM do nicho]

## SEÇÃO 12 — WORKFLOW DE PRODUÇÃO
[6 steps com tempo: script 30min, narração 15min, imagens 45min, edição 60min, thumb 20min, SEO 15min]

## SEÇÃO 13 — BANCO DE 20 IDEIAS DE VÍDEO
[20 títulos em 5 categorias, cada um com hook de 1 linha]

## SEÇÃO 14 — CALENDÁRIO 30 DIAS
[semana a semana, dia a dia, KPIs: CTR 5%+, retenção 50%+]

## SEÇÃO 15 — FERRAMENTAS E CUSTOS
[tabela 10 ferramentas: etapa, ferramenta, custo/mês, alternativa grátis, observação]

## SEÇÃO 16 — ALERTAS E ARMADILHAS
[7 do que fazer + 7 do que NÃO fazer + 3 alertas YouTube 2026]

## SEÇÃO 17 — ARQUÉTIPO DE FORMATO RECOMENDADO
[melhor dos 8 arquétipos + por quê + como produzir + canal referência]

## SEÇÃO 18 — ANÁLISE DE RISCO
[tabela 5 riscos: tipo, nível baixo/médio/alto, como evitar]

## SEÇÃO 19 — ROTEIRO COMPLETO DO PRIMEIRO VÍDEO
[hook 10s + intro 30s + 5 blocos + 5 pattern interrupts + CTA emocional]

## SEÇÃO 20 — PROMPTS MIDJOURNEY v7
[5 prompts de cena + 2 prompts de thumbnail no formato --ar 16:9 --s 750 --v 7]
"""

# ── HTML BUILDER ─────────────────────────────────
def build_html(nicho, keywords, language, part1, part2):
    import datetime
    data = datetime.datetime.now().strftime("%d/%m/%Y")
    
    # Converte markdown em HTML simples
    def md_to_html(text):
        lines = text.split('\n')
        html = []
        for line in lines:
            if line.startswith('#### '):
                html.append(f'<h4>{line[5:]}</h4>')
            elif line.startswith('### '):
                html.append(f'<h3>{line[4:]}</h3>')
            elif line.startswith('## '):
                html.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('# '):
                html.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('- ') or line.startswith('* '):
                html.append(f'<li>{line[2:]}</li>')
            elif line.startswith('|'):
                cols = [c.strip() for c in line.split('|')[1:-1]]
                if all(set(c) <= set('-: ') for c in cols):
                    continue
                tag = 'th' if html and '<th>' in (html[-1] if html else '') else 'td'
                if not html or '<tr>' not in html[-1]:
                    row = '<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cols) + '</tr>'
                    html.append(row)
            elif line.strip() == '':
                html.append('<br>')
            else:
                html.append(f'<p>{line}</p>')
        return '\n'.join(html)

    content1 = md_to_html(part1)
    content2 = md_to_html(part2)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Estratégia YouTube — {nicho}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0f0f0f;color:#e0e0e0;font-family:system-ui,sans-serif;font-size:15px;line-height:1.7;padding:0}}
.header{{background:linear-gradient(180deg,#0a0a1a,#0f0f0f);padding:2rem 1.5rem;text-align:center;border-bottom:1px solid #2a2a2a}}
h1{{font-size:1.8rem;color:#FFD700;margin-bottom:0.5rem}}
h2{{font-size:1.3rem;color:#FFD700;margin:2rem 0 1rem;padding-bottom:0.5rem;border-bottom:2px solid #2a2a2a}}
h3{{font-size:1.1rem;color:#fff;margin:1rem 0 0.5rem}}
h4{{color:#66B2B2;margin:0.75rem 0 0.25rem}}
p{{margin-bottom:0.75rem;max-width:800px}}
li{{margin-bottom:0.4rem;margin-left:1.2rem}}
.content{{max-width:1100px;margin:0 auto;padding:1.5rem}}
.part{{background:#1a1a2e;border-radius:10px;padding:1.5rem;margin-bottom:2rem;border:1px solid #2a2a2a}}
.pill{{display:inline-block;padding:0.2rem 0.75rem;border-radius:50px;font-size:0.8rem;font-weight:600;margin:0.2rem}}
.gold{{background:#FFD700;color:#000}}
.teal{{background:#66B2B2;color:#000}}
.outline{{border:1px solid #FFD700;color:#FFD700}}
table{{width:100%;border-collapse:collapse;margin:1rem 0;font-size:0.9rem}}
th{{background:#252540;color:#FFD700;padding:0.6rem 0.8rem;text-align:left;border-bottom:2px solid #FFD700}}
td{{padding:0.6rem 0.8rem;border-bottom:1px solid #2a2a2a}}
tr:hover td{{background:#252540}}
.badge{{display:inline-block;background:linear-gradient(135deg,#FFD700,#FFA500);color:#000;padding:0.15rem 0.6rem;border-radius:50px;font-size:0.7rem;font-weight:700;margin-left:0.5rem}}
@media(max-width:600px){{h1{{font-size:1.4rem}}h2{{font-size:1.1rem}}}}
</style>
</head>
<body>
<div class="header">
  <h1>🎯 Estratégia YouTube Faceless <span class="badge">v2.0</span></h1>
  <p style="color:#9e9e9e;margin-top:0.5rem">Gerado em {data} · 20 Seções Completas</p>
  <div style="margin-top:0.75rem">
    <span class="pill gold">{nicho}</span>
    <span class="pill teal">{keywords}</span>
    <span class="pill outline">{language}</span>
  </div>
</div>
<div class="content">
  <div class="part">
    <h2>📊 Parte 1 — Estratégia (Seções 1 a 10)</h2>
    {content1}
  </div>
  <div class="part">
    <h2>⚙️ Parte 2 — Execução (Seções 11 a 20)</h2>
    {content2}
  </div>
</div>
</body>
</html>"""

# ── INTERFACE ─────────────────────────────────────
st.title("🎯 YouTube Faceless Strategy Agent")
st.markdown("Preencha os campos abaixo e receba um relatório completo com **20 seções** de estratégia.")

with st.form("agent_form"):
    nicho    = st.text_input("🎬 Nicho do Canal", placeholder="Ex: Nostalgia industrial brasileira anos 1950")
    keywords = st.text_input("🔑 Keywords", placeholder="Ex: FNM, JK, ABC paulista, metalúrgicos")
    language = st.selectbox("🌍 Idioma Principal", ["Português (PT-BR)", "Inglês (EN)", "Espanhol (ES)", "Indonésio (ID)", "Turco (TR)"])
    submitted = st.form_submit_button("🚀 Gerar Estratégia Completa")

if submitted:
    if not nicho or not keywords:
        st.error("Preencha o nicho e as keywords!")
    else:
        with st.spinner("⏳ Gerando Parte 1 — Estratégia (Seções 1-10)..."):
            resp_a = model.generate_content(prompt_generate_a(nicho, keywords, language))
            part1  = resp_a.text

        with st.spinner("⏳ Gerando Parte 2 — Execução (Seções 11-20)..."):
            resp_b = model.generate_content(prompt_generate_b(nicho, keywords, language))
            part2  = resp_b.text

        with st.spinner("🔨 Montando HTML final..."):
            html_final = build_html(nicho, keywords, language, part1, part2)

        st.success("✅ Relatório gerado com sucesso!")

        st.download_button(
            label="⬇️ Baixar Relatório HTML",
            data=html_final.encode("utf-8"),
            file_name=f"estrategia-youtube-{nicho[:30].replace(' ','-')}.html",
            mime="text/html"
        )

        with st.expander("👁 Pré-visualizar conteúdo bruto"):
            st.text_area("Parte 1", part1, height=300)
            st.text_area("Parte 2", part2, height=300)
