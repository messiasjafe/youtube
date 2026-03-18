import streamlit as st
import google.generativeai as genai
import pathlib

# ── CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="YouTube Faceless Strategy Agent",
    page_icon="🎯",
    layout="centered"
)

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# ── GOOGLE SEARCH GROUNDING ──────────────────────
search_tool = genai.protos.Tool(
    google_search_retrieval=genai.protos.GoogleSearchRetrieval(
        dynamic_retrieval_config=genai.protos.DynamicRetrievalConfig(
            mode=genai.protos.DynamicRetrievalConfig.Mode.MODE_DYNAMIC,
            dynamic_threshold=0.3
        )
    )
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={"max_output_tokens": 8192, "temperature": 0.7},
    tools=[search_tool]
)

# ── CARREGA OS 3 ARQUIVOS ──────────────────────
@st.cache_resource
def load_files():
    md_text       = pathlib.Path("youtube-nichos-2026.md").read_text(encoding="utf-8")
    pdf_nichos    = pathlib.Path("youtube-nichos-2026.pdf").read_bytes()
    pdf_blueprint = pathlib.Path("youtube-blueprint-definitivo.pdf").read_bytes()
    return md_text, pdf_nichos, pdf_blueprint

md_nichos, pdf_nichos, pdf_blueprint = load_files()

# ── PROMPTS ──────────────────────────────────────
def prompt_generate_a(nicho, keywords, language):
    return f"""
IDIOMA DE RESPOSTA: Português do Brasil. OBRIGATÓRIO em 100% do output.

Você é um estrategista sênior de canais YouTube Faceless com IA.

REGRA DE FONTES (prioridade em ordem):
1. PDFs e arquivo .md anexados — fonte primária obrigatória
2. Google Search — use para complementar dados que NÃO estão nos arquivos
3. Conhecimento interno — apenas como último recurso
NUNCA invente RPM, CPM, nomes de canais ou dados numéricos sem fonte.

NICHO DO CANAL: {nicho}
KEYWORDS: {keywords}
IDIOMA DO CANAL: {language}

CONTEXTO DOS ARQUIVOS DE REFERÊNCIA:
{md_nichos}

Gere APENAS as Seções 1 a 10. Formato Markdown estruturado. Sem HTML.
Não resuma. Não pule nenhuma seção. Máxima completude.

## SEÇÃO 1 — VALIDAÇÃO DO NICHO
### Filtro 1 — INTERESSE
Consegue criar 50-100 vídeos? [APROVADO/REPROVADO] + 5 subtópicos específicos do nicho.

### Filtro 2 — FERRAMENTAS
Viável com Kling AI, Google AI Studio, CapCut, ElevenLabs, Midjourney? [APROVADO/REPROVADO]
Arquétipo recomendado dos 8 tipos (Screen Tutorial / Visual Explainer / Documentary / Product Review / Data Viz / Hands-Only / Ambient / News)

### Filtro 3 — DINHEIRO
RPM exato do arquivo, buscas mensais, competição, tempo estimado até YPP.

### Scoring 7 Dimensões (tabela com score 0-10 e justificativa)
1. Força da Demanda | 2. Pressão de Supply | 3. Densidade de Outliers
4. Potencial de RPM | 5. Viabilidade Faceless | 6. Risco Copyright/Política | 7. Escalabilidade
TOTAL: [soma]/70 — Veredicto: FORTE (50+) / MODERADO (35-49) / FRACO (<35)

### Checklist de Validação (responda ✅ ou ❌)
- Canais com menos de 6 meses já crescendo neste nicho?
- Canais novos têm mais views que subscribers?
- Edição simples para escalar com IA?
- RPM estimado maior que $5?
- É possível produzir 2+ vídeos por semana?
- O nicho é evergreen?

## SEÇÃO 2 — POSIÇÃO NOS RANKINGS
### Top 10 Evergreen (Blueprint)
Posição, nota/10, RPM, dificuldade, risco demonetização, canal referência com earnings estimados.

### Top 25 Micro-Nichos (arquivo de nichos)
Posição, RPM, CPM range, growth score, niche size, audience loyalty.

## SEÇÃO 3 — HIERARQUIA DO NICHO
- NICHO AMPLO: [nome] — milhões de buscas, alta competição
- MICRO-NICHO: [nome] — centenas de milhares de buscas
- PICO-NICHO: [nome] — menos de 10 canais competindo
Lifecycle: [Whitespace/Rising/Breakeven/Saturação/Hidden Market] + justificativa
Insight Chave: estratégia de começar pelo pico-nicho e expandir.

## SEÇÃO 4 — CANAIS DE REFERÊNCIA REAIS
Tabela com 5+ canais do arquivo de referência mais próximos ao nicho.
Se não encontrar no arquivo, pesquise no Google Search canais reais:
Canal | Nicho | Subscribers | Vídeos | Destaque (views/earnings) | Padrão | Idioma

## SEÇÃO 5 — NICHE STACKING
Copie as 5 combinações exatas da tabela do arquivo de nichos (Seção 3).
Depois crie 3 combinações específicas para o nicho do usuário.
Liste os 5 motivos pelos quais funciona em 2026 com detalhes do arquivo.

## SEÇÃO 6 — MICRO-NICHOS RELACIONADOS
Tabela com todos os micro-nichos do arquivo relacionados ao nicho.
Pesquise no Google Search micro-nichos emergentes de 2026 relacionados ao nicho:
# | Micro-Nicho | Buscas/Mês | Competição | RPM | Dificuldade | Idioma | Nota

## SEÇÃO 7 — PICO-NICHOS ULTRA-ESPECÍFICOS
Da Seção 5 do arquivo, copie os da categoria mais próxima.
Para cada: quantos vídeos gera e exemplo de série.
Sugira 5 pico-nichos NOVOS específicos para o nicho do usuário.

## SEÇÃO 8 — ESTRATÉGIA MULTI-IDIOMA
Copie a tabela completa de 5 idiomas do arquivo (Seção 6).
Complemente com dados atuais do Google Search sobre CPM por país em 2026:
Idioma | CPM Médio | Competição | Audiência | Recomendação
Destaque canal principal (maior CPM) e canal espelho (menor competição).
Mencione os dados de auto-dubbing 2026 do arquivo.

## SEÇÃO 9 — FRAMEWORK DE DECISÃO POR OBJETIVO
Copie as 2 tabelas exatas do arquivo (Seção 7).
Indique em qual objetivo este nicho se encaixa melhor.

## SEÇÃO 10 — OS 6 SEGREDOS DO BLUEPRINT
Adapte cada segredo do Blueprint ao nicho com números concretos.
Use Google Search para buscar exemplos reais de canais que aplicam cada segredo:
1. Content Factory | 2. Arbitragem de Idioma | 3. Fórmula 4 Passos
4. Momentum Hack | 5. Niche Bending | 6. Proteção Demonetização 2026
"""

def prompt_generate_b(nicho, keywords, language):
    return f"""
IDIOMA DE RESPOSTA: Português do Brasil. OBRIGATÓRIO em 100% do output.

Você é um estrategista sênior de canais YouTube Faceless com IA.

REGRA DE FONTES (prioridade em ordem):
1. PDFs e arquivo .md anexados — fonte primária
2. Google Search — para dados atuais não encontrados nos arquivos
3. Conhecimento interno — último recurso
NUNCA invente dados sem fonte.

NICHO DO CANAL: {nicho}
KEYWORDS: {keywords}
IDIOMA DO CANAL: {language}

CONTEXTO DOS ARQUIVOS DE REFERÊNCIA:
{md_nichos}

Gere APENAS as Seções 11 a 20. Formato Markdown estruturado. Sem HTML.
Não resuma. Não pule nenhuma seção. Máxima completude.

## SEÇÃO 11 — PROJEÇÃO DE CRESCIMENTO
Tabela ajustando receita ao RPM real do nicho (do arquivo).
Pesquise no Google Search casos reais de crescimento no nicho para validar projeção:
Mês | Vídeos | Subscribers | Views/Mês | Receita Estimada
Mês 1 / Mês 3 / Mês 6 / Mês 12

## SEÇÃO 12 — WORKFLOW DE PRODUÇÃO POR VÍDEO
6 steps com tempos exatos (total ~2h45min):
Step 7 — Script (30 min): ferramentas + dicas específicas para o nicho
Step 8 — Narração (15 min): ElevenLabs, voz, velocidade 0.9x
Step 9 — Imagens e Vídeo (45 min): Midjourney 15-25 imagens, Kling AI 3-5 animações
Step 10 — Edição (60 min): CapCut, dissolve suave, trilha adequada ao nicho
Step 11 — Thumbnail (20 min): Canva, 2-3 variações, técnicas de contraste
Step 12 — SEO e Upload (15 min): título, descrição 500+ palavras, tags, horário

## SEÇÃO 13 — BANCO DE 20 IDEIAS DE VÍDEO
20 títulos em 5 categorias (4 por categoria) específicas para o nicho.
Para cada: categoria, título completo, hook de 1 linha.

## SEÇÃO 14 — CALENDÁRIO 30 DIAS
Semana 1 (Dias 1-7): Setup e pesquisa
Semana 2 (Dias 8-14): Primeiros 3 vídeos publicados
Semana 3 (Dias 15-21): Análise de métricas e iteração
Semana 4 (Dias 22-30): Ritmo de cruzeiro — 3 vídeos/semana + 1 Short/dia
KPIs: CTR 5%+, Retenção 50%+, Views/48h como KPI principal

## SEÇÃO 15 — FERRAMENTAS E CUSTOS
Tabela completa 10 ferramentas do arquivo com custos atualizados 2026.
Pesquise no Google Search preços atuais das ferramentas:
Etapa | Ferramenta | Custo/Mês | Alternativa Gratuita | Observação
[inclua total pago e total gratuito]

## SEÇÃO 16 — ALERTAS E ARMADILHAS
O QUE FAZER (7 itens) + O QUE NÃO FAZER (7 itens) do Blueprint.
ALERTAS YOUTUBE 2026 — pesquise no Google Search últimas mudanças de política:
[⚠️] AI Slop Cleanup | [⚠️] Disclosure sintético | [⚠️] Reused Content

## SEÇÃO 17 — ARQUÉTIPO DE FORMATO RECOMENDADO
Dos 8 arquétipos (arquivo Seção 4C), recomende O MELHOR para este nicho.
Pesquise no Google Search canais reais de 2025-2026 que usam este formato no nicho:
- Arquétipo escolhido e por quê
- Como produzir: ferramentas e pipeline
- Canal de referência real
- Formato secundário opcional

## SEÇÃO 18 — ANÁLISE DE RISCO
Tabela 5 riscos com nível e mitigação específica ao nicho:
Tipo | Nível | Como Evitar
Demonetização | Copyright | Saturação | AI Slop Flag | Burnout

## SEÇÃO 19 — ROTEIRO COMPLETO DO PRIMEIRO VÍDEO
Escolha o título mais promissor do Banco de Ideias.
TÍTULO: [fórmula CURIOSIDADE + EMOÇÃO + DATA/PERÍODO]

[HOOK — 10 segundos]: dado chocante ou paradoxo
[INTRO — 30 segundos]: contexto + promessa de 3 aprendizados
[BLOCO 1] + [PATTERN INTERRUPT 1]
[BLOCO 2] + [PATTERN INTERRUPT 2]
[BLOCO 3] + [PATTERN INTERRUPT 3]
[BLOCO 4] + [PATTERN INTERRUPT 4]
[BLOCO 5] + [PATTERN INTERRUPT 5]
[CTA EMOCIONAL — 30 segundos]: tom nostálgico + gancho próximo vídeo

DURAÇÃO: 12-20 min | VELOCIDADE: 0.9x | PATTERN INTERRUPT: a cada 45s

## SEÇÃO 20 — PROMPTS MIDJOURNEY v7
5 prompts para cenas do vídeo:
"[Composição], [descrição 20+ palavras], [estilo artístico], [iluminação], [paleta e mood] --ar 16:9 --s 750 --q 2 --v 7"

2 prompts de thumbnail:
"[Elemento focal close-up], [descrição dramática], [estilo], high contrast, clean composition for YouTube thumbnail --ar 16:9 --s 600 --c 10 --q 2 --v 7"
"""

# ── HTML BUILDER ─────────────────────────────────
def build_html(nicho, keywords, language, part1, part2):
    import datetime, re
    data = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")

    def md_to_html(text):
        lines = text.split('\n')
        html = []
        in_table = False
        in_ul = False
        in_ol = False
        for line in lines:
            if line.startswith('#### '):
                if in_ul: html.append('</ul>'); in_ul=False
                if in_ol: html.append('</ol>'); in_ol=False
                html.append(f'<h4>{line[5:]}</h4>')
            elif line.startswith('### '):
                if in_ul: html.append('</ul>'); in_ul=False
                if in_ol: html.append('</ol>'); in_ol=False
                html.append(f'<h3>{line[4:]}</h3>')
            elif line.startswith('## '):
                if in_ul: html.append('</ul>'); in_ul=False
                if in_ol: html.append('</ol>'); in_ol=False
                if in_table: html.append('</table></div>'); in_table=False
                html.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('# '):
                html.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('- ') or line.startswith('* '):
                if in_ol: html.append('</ol>'); in_ol=False
                if not in_ul: html.append('<ul>'); in_ul=True
                c = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line[2:])
                html.append(f'<li>{c}</li>')
            elif re.match(r'^\d+\. ', line):
                if in_ul: html.append('</ul>'); in_ul=False
                if not in_ol: html.append('<ol>'); in_ol=True
                c = re.sub(r'^\d+\. ', '', line)
                c = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', c)
                html.append(f'<li>{c}</li>')
            elif line.startswith('|') and '|' in line[1:]:
                if in_ul: html.append('</ul>'); in_ul=False
                if in_ol: html.append('</ol>'); in_ol=False
                cols = [c.strip() for c in line.split('|')[1:-1]]
                if all(set(c) <= set('-: ') for c in cols):
                    continue
                if not in_table:
                    html.append('<div class="tw"><table><thead>')
                    in_table = True
                    html.append('<tr>'+''.join(f'<th>{c}</th>' for c in cols)+'</tr>')
                    html.append('</thead><tbody>')
                else:
                    html.append('<tr>'+''.join(f'<td>{c}</td>' for c in cols)+'</tr>')
            else:
                if in_table: html.append('</tbody></table></div>'); in_table=False
                if in_ul: html.append('</ul>'); in_ul=False
                if in_ol: html.append('</ol>'); in_ol=False
                if line.strip() == '':
                    html.append('<br>')
                else:
                    l = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
                    l = re.sub(r'\*(.*?)\*', r'<em>\1</em>', l)
                    l = re.sub(r'`(.*?)`', r'<code>\1</code>', l)
                    html.append(f'<p>{l}</p>')
        if in_table: html.append('</tbody></table></div>')
        if in_ul: html.append('</ul>')
        if in_ol: html.append('</ol>')
        return '\n'.join(html)

    c1 = md_to_html(part1)
    c2 = md_to_html(part2)

    sections = [
        ("📊","Validação"),("🏆","Rankings"),("🔺","Hierarquia"),("📺","Canais"),
        ("🔀","Stacking"),("🎯","Micro-Nichos"),("🔍","Pico-Nichos"),("🌍","Multi-Idioma"),
        ("📋","Framework"),("🔐","Segredos"),("📈","Projeção"),("⚙️","Workflow"),
        ("💡","20 Ideias"),("📅","Calendário"),("🛠️","Ferramentas"),("⚠️","Alertas"),
        ("🎬","Formato"),("🛡️","Riscos"),("📝","Roteiro"),("🖼️","Prompts MJ")
    ]

    tabs_html = ''.join(
        f'<button class="tab{"  active" if i==0 else ""}" onclick="show({i})">{e} {n}</button>'
        for i,(e,n) in enumerate(sections)
    )

    panels_html = ''.join(
        f'<div id="p{i}" class="panel {"active" if i==0 else ""}">{ c1 if i < 10 else c2 }</div>'
        for i in range(20)
    )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Estratégia YouTube — {nicho}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0f0f0f;color:#e0e0e0;font-family:system-ui,sans-serif;font-size:15px;line-height:1.7}}
.header{{background:linear-gradient(180deg,#0a0a1a,#0f0f0f);padding:2.5rem 1.5rem 2rem;text-align:center;border-bottom:2px solid #FFD700}}
.header h1{{font-size:1.9rem;color:#FFD700;margin-bottom:0.4rem}}
.header p{{color:#9e9e9e;font-size:0.85rem}}
.pills{{display:flex;gap:0.5rem;justify-content:center;flex-wrap:wrap;margin-top:0.75rem}}
.pill{{display:inline-block;padding:0.2rem 0.8rem;border-radius:50px;font-size:0.8rem;font-weight:600}}
.pg{{background:#FFD700;color:#000}}.pt{{background:#66B2B2;color:#000}}.po{{border:1px solid #FFD700;color:#FFD700}}
.tabs{{position:sticky;top:0;z-index:100;background:#111122;border-bottom:2px solid #2a2a2a;display:flex;overflow-x:auto;scrollbar-width:none}}
.tabs::-webkit-scrollbar{{display:none}}
.tab{{flex-shrink:0;padding:0.85rem 1.1rem;background:transparent;border:none;border-bottom:3px solid transparent;color:#9e9e9e;font-size:0.8rem;font-weight:600;cursor:pointer;white-space:nowrap;transition:all 0.2s}}
.tab:hover{{color:#fff;background:rgba(255,215,0,0.05)}}
.tab.active{{color:#FFD700;border-bottom-color:#FFD700;background:rgba(255,215,0,0.07)}}
.panel{{display:none;max-width:1100px;margin:0 auto;padding:2rem 1.5rem;animation:fi 0.3s ease}}
.panel.active{{display:block}}
@keyframes fi{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:translateY(0)}}}}
h1{{font-size:1.6rem;color:#FFD700;margin:1.5rem 0 0.75rem}}
h2{{font-size:1.3rem;color:#FFD700;margin:2rem 0 1rem;padding-bottom:0.4rem;border-bottom:2px solid #2a2a2a}}
h3{{font-size:1.05rem;color:#fff;margin:1.2rem 0 0.5rem}}
h4{{color:#66B2B2;margin:0.75rem 0 0.25rem}}
p{{margin-bottom:0.75rem;max-width:860px}}
strong{{color:#FFD700}}
em{{color:#66B2B2;font-style:normal}}
code{{background:#1a1a2e;color:#66B2B2;padding:0.1rem 0.4rem;border-radius:4px;font-size:0.85rem}}
ul,ol{{padding-left:1.4rem;margin-bottom:1rem}}
li{{margin-bottom:0.35rem;line-height:1.7}}
.tw{{overflow-x:auto;margin:1rem 0;border-radius:8px;border:1px solid #2a2a2a}}
table{{width:100%;border-collapse:collapse;font-size:0.88rem}}
th{{background:#1a1a2e;color:#FFD700;padding:0.65rem 0.9rem;text-align:left;border-bottom:2px solid #FFD700;white-space:nowrap;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.3px}}
td{{padding:0.65rem 0.9rem;border-bottom:1px solid #1a1a2e;vertical-align:top}}
tr:hover td{{background:#1a1a1a}}
br{{display:block;content:"";margin-top:0.3rem}}
@media(max-width:600px){{.header h1{{font-size:1.3rem}}.panel{{padding:1rem}}.tab{{padding:0.7rem 0.75rem;font-size:0.72rem}}}}
@media print{{.tabs{{display:none}}.panel{{display:block!important}}body{{background:#fff;color:#000}}}}
</style>
</head>
<body>
<div class="header">
  <h1>🎯 Estratégia YouTube Faceless</h1>
  <p>Relatório gerado em {data} · 20 seções completas · Dados em tempo real</p>
  <div class="pills">
    <span class="pill pg">{nicho}</span>
    <span class="pill pt">{keywords}</span>
    <span class="pill po">{language}</span>
  </div>
</div>
<div class="tabs">{tabs_html}</div>
{panels_html}
<script>
function show(i){{
  document.querySelectorAll('.panel').forEach((p,j)=>p.classList.toggle('active',j===i));
  document.querySelectorAll('.tab').forEach((t,j)=>t.classList.toggle('active',j===i));
  window.scrollTo({{top:0,behavior:'smooth'}});
}}
</script>
</body>
</html>"""

# ── INTERFACE ──────────────────────────────────────
st.title("🎯 YouTube Faceless Strategy Agent")
st.markdown("Preencha os campos e receba um relatório completo com **20 seções** · PDFs + Google Search em tempo real.")

with st.form("agent_form"):
    nicho    = st.text_input("🎬 Nicho do Canal", placeholder="Ex: Nostalgia industrial brasileira anos 1950")
    keywords = st.text_input("🔑 Keywords", placeholder="Ex: FNM, JK, ABC paulista, metalúrgicos")
    language = st.selectbox("🌍 Idioma Principal", [
        "Português (PT-BR)", "Inglês (EN)", "Espanhol (ES)", "Indonésio (ID)", "Turco (TR)"
    ])
    submitted = st.form_submit_button("🚀 Gerar Estratégia Completa")

if submitted:
    if not nicho or not keywords:
        st.error("⚠️ Preencha o nicho e as keywords!")
    else:
        progress = st.progress(0, text="🔍 Iniciando análise com PDFs + Google Search...")

        with st.spinner("⏳ Gerando Seções 1-10 — Validação, Rankings, Nichos, Segredos..."):
            resp_a = model.generate_content([
                {"mime_type": "application/pdf", "data": pdf_blueprint},
                {"mime_type": "application/pdf", "data": pdf_nichos},
                prompt_generate_a(nicho, keywords, language)
            ])
            part1 = resp_a.text
            progress.progress(45, text="✅ Seções 1-10 prontas — Gerando Seções 11-20...")

        with st.spinner("⏳ Gerando Seções 11-20 — Projeção, Workflow, Roteiro, Prompts..."):
            resp_b = model.generate_content([
                {"mime_type": "application/pdf", "data": pdf_blueprint},
                {"mime_type": "application/pdf", "data": pdf_nichos},
                prompt_generate_b(nicho, keywords, language)
            ])
            part2 = resp_b.text
            progress.progress(85, text="✅ Seções 11-20 prontas — Montando HTML...")

        with st.spinner("🔨 Montando relatório HTML com 20 abas navegáveis..."):
            html_final = build_html(nicho, keywords, language, part1, part2)
            progress.progress(100, text="🎉 Relatório completo!")

        st.success("🎉 Estratégia gerada com sucesso! PDFs + Google Search utilizados.")

        st.download_button(
            label="⬇️ Baixar Relatório HTML Completo (20 seções)",
            data=html_final.encode("utf-8"),
            file_name=f"estrategia-{nicho[:40].replace(' ','-').lower()}.html",
            mime="text/html",
            use_container_width=True
        )

        with st.expander("👁️ Ver conteúdo bruto gerado"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Seções 1-10**")
                st.text_area("", part1, height=400, label_visibility="collapsed")
            with col2:
                st.markdown("**Seções 11-20**")
                st.text_area("", part2, height=400, label_visibility="collapsed")
