# -*- coding: utf-8 -*-
"""Genera todas las páginas HTML del prototipo UTMA.
Uso:  python herramientas/generar.py      (desde la carpeta del sitio)
Después: npm run build  (compila css/styles.css con Tailwind)
"""
import json, os, html, sys
from datetime import date
sys.path.insert(0, os.path.dirname(__file__))
from datos import *

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
E = lambda s: html.escape(str(s), quote=True)
PBY = {p["id"]: p for p in PROGRAMAS}

# ------------------------------------------------------------------ íconos
ICON = {
 "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "x": '<path d="M6 6l12 12M18 6 6 18"/>',
 "down": '<path d="m6 9 6 6 6-6"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "ext": '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
 "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
 "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 "cal": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/>',
 "doc": '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
 "check": '<path d="m5 12 5 5 9-10"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
 "leaf": '<path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15M5 19l7-7"/>',
 "chat2": '<path d="M4 5h16v11H8l-4 4z"/>',
}
def ic(n, cls="h-5 w-5"):
    return f'<svg aria-hidden="true" class="{cls} shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[n]}</svg>'

def demo(label, txt, cls="link"):
    """Enlace a un sistema externo que en producción apunta al servicio real."""
    return f'<a href="#" data-demo="{E(txt)}" class="{cls}">{label}</a>'

# ------------------------------------------------------------------ layout
NAV = [("Oferta educativa", "oferta-educativa.html", "oferta"), ("Admisiones", "admisiones.html", "admisiones"),
       ("Vida universitaria", "vida-universitaria.html", "vida"), ("Internacional", "internacional.html", "internacional"),
       ("Empresas", "empresas.html", "empresas"), ("Conoce la UTMA", "conoce-la-utma.html", "conoce")]

def mega(r):
    esc_ = [p for p in PROGRAMAS if "esc" in p["mods"]]
    mix = [p for p in PROGRAMAS if "mix" in p["mods"]]
    def li(p, suf=""):
        a = AREAS[p["area"]]
        return f'<li><a class="flex items-center gap-2 rounded-lg px-2 py-1.5 hover:bg-paper" href="{r}carreras/{p["id"]}.html"><span class="dot" style="background:{a["color"]}"></span>{E(p["nombre"].replace(" (mixta)",""))}{suf}</a></li>'
    return f'''<div id="mm-oferta" data-open="false" class="pop absolute inset-x-0 top-full mx-auto mt-2 w-[min(960px,calc(100vw-32px))] whitespace-normal rounded-2xl border border-ink/10 bg-white p-6 shadow-2xl">
  <div class="grid grid-cols-[1.4fr_1fr_.9fr] gap-8 text-[14.5px] font-normal">
    <div><p class="eyebrow mb-2">Escolarizada · TSU + Ingeniería o Licenciatura</p><ul class="grid grid-cols-2 gap-x-4">{"".join(li(p) for p in esc_)}</ul></div>
    <div>
      <p class="eyebrow mb-2">Mixta · para quien trabaja</p><ul>{"".join(li(p) for p in mix)}</ul>
      <p class="eyebrow mb-2 mt-5">Posgrado</p><ul>{li(PBY["maestria-en-gestion-gubernamental"])}</ul>
      <p class="eyebrow mb-2 mt-5">Próximamente</p><ul>{li(PBY["psicologia"])}</ul>
    </div>
    <div class="rounded-xl bg-ut-soft p-5">
      <p class="font-display text-xl font-bold leading-tight">¿Aún no sabes qué estudiar?</p>
      <p class="mt-2 text-ink/80">Responde 4 preguntas y te sugerimos un área.</p>
      <a href="{r}oferta-educativa.html#test" class="btn-primary btn-sm mt-4">Hacer el test</a>
      <a href="{r}oferta-educativa.html" class="link mt-4 block">Ver las 16 opciones →</a>
    </div>
  </div>
</div>'''

def header(r, active):
    items = []
    for name, href, key in NAV:
        cur = ' aria-current="page"' if key == active else ""
        curcls = " text-navy" if key == active else ""
        if key == "oferta":
            items.append(f'''<li><button class="nav-btn flex items-center gap-1 rounded-lg px-2.5 py-2 hover:bg-navy-soft{curcls}" aria-expanded="false" aria-controls="mm-oferta"{cur}>{name}{ic("down","h-4 w-4")}</button>{mega(r)}</li>''')
        else:
            items.append(f'<li><a class="block rounded-lg px-2.5 py-2 hover:bg-navy-soft{curcls}" href="{r}{href}"{cur}>{name}</a></li>')
    drawer_links = "".join(f'<a class="block rounded-lg px-3 py-3 hover:bg-paper{" text-navy" if k==active else ""}" href="{r}{h}">{n}</a>' for n, h, k in NAV)
    return f'''<a href="#contenido" class="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[70] focus:rounded-lg focus:bg-white focus:px-4 focus:py-2 focus:font-bold focus:shadow-lg">Saltar al contenido</a>
<div class="hidden bg-navy-deep text-white lg:block">
  <div class="wrap flex items-center justify-between py-1.5 text-[13px]">
    <nav aria-label="Accesos para la comunidad" class="flex items-center gap-5">
      <a class="hover:underline" href="{r}alumnos.html">Alumnos</a><a class="hover:underline" href="{r}docentes.html">Docentes</a><a class="hover:underline" href="{r}egresados.html">Egresados</a>
      <a class="hover:underline" href="#" data-demo="En el sitio real este enlace abre SAEKO, el sistema escolar.">SAEKO</a>
      <a class="hover:underline" href="#" data-demo="En el sitio real este enlace abre la Biblioteca Digital.">Biblioteca digital</a>
      <span aria-hidden="true" class="h-3 w-px bg-white/30"></span>
      <a class="hover:underline" href="{r}transparencia.html">Transparencia</a><a class="hover:underline" href="{r}contacto.html#directorio">Directorio</a><a class="hover:underline" href="{r}calendario.html">Calendario</a>
    </nav>
    <div class="flex items-center gap-4"><span>Tel. <span class="tabular-nums">449 786 0951</span></span><a class="rounded border border-white/40 px-2 py-0.5 font-bold hover:bg-white/10" href="{r}en.html" lang="en" hreflang="en">English</a></div>
  </div>
</div>
<header class="sticky top-0 z-40 border-b border-ink/10 bg-white/95 backdrop-blur no-print" style="padding-top:env(safe-area-inset-top,0px)">
  <div class="wrap flex items-center gap-3 py-3">
    <a href="{r}index.html" class="shrink-0" aria-label="UTMA, ir al inicio"><img src="{r}img/logo-utma.png" alt="Universidad Tecnológica Metropolitana de Aguascalientes" class="h-10 w-auto sm:h-12" width="392" height="132"></a>
    <nav aria-label="Principal" class="ml-auto hidden xl:block"><ul class="flex items-center gap-0.5 whitespace-nowrap text-[15px] font-bold" id="mainnav">{"".join(items)}</ul></nav>
    <div class="ml-auto flex items-center gap-2 xl:ml-2">
      <button id="openSearch" class="flex h-11 items-center gap-2 rounded-lg border border-ink/15 px-3 text-sm hover:border-navy" aria-haspopup="dialog">{ic("search")}<span class="hidden sm:inline">Buscar</span><kbd class="hidden whitespace-nowrap rounded bg-paper px-1.5 text-xs text-ink/60 2xl:inline">Ctrl K</kbd></button>
      <a href="{r}admisiones.html#solicitud" class="btn-primary hidden h-11 rounded-lg px-4 text-sm sm:inline-flex">Solicita tu examen</a>
      <button id="openMenu" class="flex h-11 w-11 items-center justify-center rounded-lg border border-ink/15 xl:hidden" aria-expanded="false" aria-controls="drawer" aria-label="Abrir menú">{ic("menu","h-6 w-6")}</button>
    </div>
  </div>
</header>
<div id="scrim" class="pointer-events-none fixed inset-0 z-50 bg-ink/40 opacity-0 transition-opacity duration-200"></div>
<aside id="drawer" data-open="false" role="dialog" aria-modal="true" aria-label="Menú" class="drawer fixed inset-y-0 right-0 z-50 flex w-[88%] max-w-sm flex-col bg-white shadow-2xl" style="padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)">
  <div class="flex items-center justify-between border-b border-ink/10 px-5 py-4"><p class="font-display text-lg font-bold">Menú</p><button id="closeMenu" class="flex h-11 w-11 items-center justify-center rounded-lg hover:bg-paper" aria-label="Cerrar menú">{ic("x","h-6 w-6")}</button></div>
  <nav aria-label="Principal móvil" class="flex-1 overflow-y-auto px-3 py-3 text-base font-bold">
    <a class="block rounded-lg px-3 py-3 hover:bg-paper" href="{r}index.html">Inicio</a>
    {drawer_links}
    <p class="eyebrow mt-4 px-3">Comunidad</p>
    <div class="grid grid-cols-2 gap-2 px-3 py-2 text-sm font-normal">
      <a class="rounded-lg bg-paper px-3 py-2.5" href="{r}alumnos.html">Alumnos</a><a class="rounded-lg bg-paper px-3 py-2.5" href="{r}docentes.html">Docentes</a>
      <a class="rounded-lg bg-paper px-3 py-2.5" href="{r}egresados.html">Egresados</a><a class="rounded-lg bg-paper px-3 py-2.5" href="{r}estudia-y-trabaja.html">Modalidad mixta</a>
      <a class="rounded-lg bg-paper px-3 py-2.5" href="{r}calendario.html">Calendario</a><a class="rounded-lg bg-paper px-3 py-2.5" href="{r}transparencia.html">Transparencia</a>
      <a class="rounded-lg bg-paper px-3 py-2.5" href="{r}contacto.html">Contacto</a><a class="rounded-lg bg-paper px-3 py-2.5" href="{r}en.html" lang="en">English</a>
    </div>
  </nav>
  <div class="border-t border-ink/10 p-4"><a href="{r}admisiones.html#solicitud" class="btn-primary w-full">Solicita tu examen</a></div>
</aside>
<div id="searchDlg" data-open="false" role="dialog" aria-modal="true" aria-label="Buscar en el sitio" class="pop fixed inset-0 z-[60] flex items-start justify-center bg-ink/40 px-4 pt-[10vh]">
  <div class="w-full max-w-xl overflow-hidden rounded-2xl bg-white shadow-2xl">
    <form class="flex items-center gap-3 border-b border-ink/10 px-4" action="{r}buscar.html" role="search">
      {ic("search","h-5 w-5 text-ink/60")}
      <label for="gq" class="sr-only">Buscar carreras, trámites y páginas</label>
      <input id="gq" name="q" class="h-14 w-full bg-transparent text-base outline-none" placeholder="Carreras, trámites, documentos…" role="combobox" aria-expanded="false" aria-controls="gq-list" aria-autocomplete="list" autocomplete="off" data-combobox="todo">
      <kbd class="rounded bg-paper px-1.5 text-xs text-ink/60">Esc</kbd>
    </form>
    <ul id="gq-list" role="listbox" class="max-h-[55vh] overflow-y-auto p-2 text-sm"></ul>
  </div>
</div>'''

def footer(r):
    return f'''<footer class="mt-0 bg-navy-deep text-[#DDE7ED] no-print">
  <div class="wrap grid gap-10 py-14 sm:grid-cols-2 lg:grid-cols-[1.3fr_1fr_1fr_1fr]">
    <div class="space-y-4">
      <div class="inline-block rounded-xl bg-white p-3"><img src="{r}img/logo-utma.png" alt="UTMA" class="h-12 w-auto" width="392" height="132"></div>
      <p class="flex gap-2 text-sm">{ic("pin","h-5 w-5 mt-0.5")}<span>Av. Gerónimo de la Cueva S/N, Fracc. Villas del Río, C.P. 20126, Aguascalientes, Ags.</span></p>
      <p class="flex gap-2 text-sm">{ic("phone","h-5 w-5")}<span class="tabular-nums">449 786 0951 · 449 786 0952</span></p>
      <a class="inline-flex items-center gap-2 text-sm font-bold text-white hover:underline" href="{r}conoce-la-utma.html#como-llegar">Cómo llegar {ic("arrow","h-4 w-4")}</a>
    </div>
    <nav aria-label="Estudia"><p class="mb-3 font-display font-bold text-white">Estudia</p><ul class="space-y-2 text-sm">
      <li><a class="hover:underline" href="{r}oferta-educativa.html">Oferta educativa</a></li><li><a class="hover:underline" href="{r}admisiones.html">Admisiones</a></li>
      <li><a class="hover:underline" href="{r}estudia-y-trabaja.html">Modalidad mixta</a></li><li><a class="hover:underline" href="{r}carreras/maestria-en-gestion-gubernamental.html">Posgrado</a></li>
      <li><a class="hover:underline" href="{r}internacional.html#becas">Becas</a></li><li><a class="hover:underline" href="{r}calendario.html">Calendario</a></li></ul></nav>
    <nav aria-label="Institucional"><p class="mb-3 font-display font-bold text-white">Institucional</p><ul class="space-y-2 text-sm">
      <li><a class="hover:underline" href="{r}transparencia.html">Transparencia</a></li><li><a class="hover:underline" href="{r}transparencia.html#normativa">Normativa</a></li>
      <li><a class="hover:underline" href="{r}transparencia.html#scii">SCII y Contraloría Social</a></li><li><a class="hover:underline" href="{r}conoce-la-utma.html#trabaja">Trabaja con nosotros</a></li>
      <li><a class="hover:underline" href="{r}noticias.html">Noticias</a></li><li><a class="hover:underline" href="{r}mapa-del-sitio.html">Mapa del sitio</a></li></ul></nav>
    <nav aria-label="Atención"><p class="mb-3 font-display font-bold text-white">Atención</p><ul class="space-y-2 text-sm">
      <li><a class="hover:underline" href="{r}contacto.html">Contacto</a></li><li><a class="hover:underline" href="{r}contacto.html#directorio">Directorio</a></li>
      <li><a class="hover:underline" href="{r}contacto.html#buzon">Buzón de sugerencias</a></li><li><a class="hover:underline" href="{r}aviso-de-privacidad.html">Avisos de privacidad</a></li></ul>
      <p class="mb-3 mt-6 font-display font-bold text-white">Síguenos</p>
      <ul class="flex flex-wrap gap-2 text-sm">
        <li><a class="inline-flex min-h-[36px] items-center rounded-lg border border-white/25 px-3 hover:bg-white/10" href="https://www.facebook.com/UTMABiS" rel="noopener" target="_blank">Facebook</a></li>
        <li><a class="inline-flex min-h-[36px] items-center rounded-lg border border-white/25 px-3 hover:bg-white/10" href="https://www.instagram.com/ut.metropolitana" rel="noopener" target="_blank">Instagram</a></li>
        <li><a class="inline-flex min-h-[36px] items-center rounded-lg border border-white/25 px-3 hover:bg-white/10" href="https://x.com/UTMetropolitana" rel="noopener" target="_blank">X</a></li>
        <li><a class="inline-flex min-h-[36px] items-center rounded-lg border border-white/25 px-3 hover:bg-white/10" href="https://www.youtube.com/@utmetropolitana" rel="noopener" target="_blank">YouTube</a></li>
        <li><a class="inline-flex min-h-[36px] items-center rounded-lg border border-white/25 px-3 hover:bg-white/10" href="https://www.tiktok.com/@utmetropolitana" rel="noopener" target="_blank">TikTok</a></li>
      </ul></nav>
  </div>
  <div class="border-t border-white/10"><div class="wrap flex flex-wrap items-center justify-between gap-3 py-5 text-xs text-white/70">
    <p>© 2026 Universidad Tecnológica Metropolitana de Aguascalientes · Subsistema de Universidades Tecnológicas y Politécnicas</p>
    <p>Prototipo de rediseño · Área de TI</p></div></div>
</footer>
<a href="#" data-asesor aria-label="Hablar con un asesor por WhatsApp" class="fixed bottom-4 right-4 z-30 inline-flex h-12 items-center justify-center gap-2 rounded-full bg-ut px-5 font-bold lg:w-12 lg:px-0 text-white shadow-lg hover:bg-[#006650] no-print" style="margin-bottom:env(safe-area-inset-bottom,0px)">{ic("chat")}<span class="lg:sr-only">Asesor</span></a>
<div id="toast" data-open="false" role="status" aria-live="polite" class="toast fixed bottom-20 left-1/2 z-[80] w-[min(92vw,460px)] -translate-x-1/2 rounded-xl bg-ink px-4 py-3 text-sm text-white shadow-2xl"></div>'''

def layout(path, title, desc, main, active="", page="", lang="es-MX"):
    depth = path.count("/")
    r = "../" * depth
    full_title = f"{title} · UTMA Aguascalientes" if title != "Inicio" else "UTMA · Universidad Tecnológica Metropolitana de Aguascalientes"
    doc = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(full_title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(full_title)}">
<meta property="og:description" content="{E(desc)}">
<meta name="theme-color" content="#173F57">
<link rel="icon" href="{r}img/logo-utma.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&display=swap">
<link rel="stylesheet" href="{r}css/styles.css">
<script src="{r}js/datos.js" defer></script>
<script src="{r}js/app.js" defer></script>
</head>
<body data-root="{r}" data-page="{page}">
{header(r, active)}
<main id="contenido">
{main(r)}
</main>
{footer(r)}
</body>
</html>
'''
    out = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)

# ------------------------------------------------------------------ piezas
def crumbs(r, *items):
    parts = [f'<a href="{r}index.html">Inicio</a>']
    for name, href in items:
        parts.append('<span aria-hidden="true">/</span>')
        parts.append(f'<a href="{r}{href}">{E(name)}</a>' if href else f'<span aria-current="page" class="text-ink/80">{E(name)}</span>')
    return f'<nav aria-label="Ruta" class="crumbs">{"".join(parts)}</nav>'

def page_head(r, eyebrow, title, lead, crumbs_html, color="#235F83", soft="#E6F0F5", extra=""):
    return f'''<section class="border-b border-ink/10 bg-white">
  <div class="wrap grid gap-8 py-10 sm:py-14 lg:grid-cols-[1.4fr_1fr] lg:items-end">
    <div class="min-w-0">{crumbs_html}
      <p class="eyebrow mt-6" style="color:{color if color not in ('#FDC24E','#F57E26','#35BAA4') else '#1D191A'}">{E(eyebrow)}</p>
      <h1 class="page-title mt-2">{title}</h1>
      <p class="sec-lead">{lead}</p>{extra}
    </div>
    <div class="media hidden aspect-[16/10] max-h-[300px] w-full rounded-3xl lg:block" style="--c:{color};--s:{soft}" role="img" aria-label="Espacio para fotografía institucional"></div>
  </div>
</section>'''

def note(txt):
    return f'<p class="flex gap-2 rounded-xl border border-sol bg-[#FFF6DF] px-4 py-3 text-sm text-[#5C4100]"><span aria-hidden="true" class="font-bold">i</span><span>{txt}</span></p>'

def prog_card(r, p):
    a = AREAS[p["area"]]
    mods = "".join(f'<span class="badge border border-ink/10 bg-paper text-ink/80">{MODALIDADES[m]}</span>' for m in p["mods"])
    return f'''<a href="{r}carreras/{p["id"]}.html" class="card-hover group relative flex flex-col gap-2 overflow-hidden p-5">
  <span class="absolute inset-x-0 top-0 h-1.5" style="background:{a["color"]}"></span>
  <span class="eyebrow">{E(a["nombre"])}</span>
  <span class="font-display text-lg font-bold leading-snug">{E(p["nombre"])}</span>
  <span class="text-sm text-ink/70">{E(p["resumen"])}</span>
  <span class="mt-auto flex flex-wrap gap-1.5 pt-2">{mods}</span>
</a>'''

def news_card(r, n, big=False):
    if big:
        return f'''<a href="{r}noticias/{n["id"]}.html" class="card-hover group grid overflow-hidden lg:grid-cols-[1.1fr_1fr]">
  <div class="media aspect-[16/10] lg:aspect-auto" style="--c:#235F83;--s:#E6F0F5" role="img" aria-label="Espacio para fotografía de la nota"></div>
  <div class="flex flex-col gap-3 p-6 sm:p-8"><span class="badge self-start bg-naranja-soft text-naranja-text">Historia destacada · {E(n["cat"])}</span>
  <h3 class="text-2xl font-bold leading-tight sm:text-3xl">{E(n["titulo"])}</h3><p class="text-ink/75">{E(n["resumen"])}</p>
  <span class="link mt-auto inline-flex items-center gap-1">Leer la historia {ic("arrow","h-4 w-4")}</span></div></a>'''
    return f'''<a href="{r}noticias/{n["id"]}.html" class="card-hover flex flex-col overflow-hidden" data-cat="{E(n["cat"])}">
  <div class="media aspect-[16/9]" style="--c:{ {'Internacional':'#35BAA4','Deportes':'#F57E26','Posgrado':'#235F83','Convenios':'#00A884','Logros':'#B61F3E'}.get(n['cat'],'#81B4B8') };--s:#F1F5F6" role="img" aria-label="Espacio para fotografía"></div>
  <div class="flex flex-1 flex-col gap-2 p-5"><span class="eyebrow">{E(n["cat"])} · {E(n["fecha"])}</span><h3 class="text-lg font-bold leading-snug">{E(n["titulo"])}</h3>
  <span class="link mt-auto pt-2 text-sm">Leer nota</span></div></a>'''

def steps_block(r):
    lis = []
    for i, s in enumerate(CONVOCATORIA, 1):
        lis.append(f'''<li class="card relative flex flex-col gap-2 p-5" data-desde="{s["desde"]}" data-hasta="{s["hasta"]}">
  <div class="flex items-center justify-between"><span class="flex h-9 w-9 items-center justify-center rounded-full bg-navy-soft font-display font-bold text-navy" data-num>{i}</span><span class="badge" data-state></span></div>
  <h3 class="text-lg font-bold">{E(s["paso"])}</h3><p class="text-sm text-ink/75">{E(s["txt"])}</p>
  <p class="mt-auto pt-2 text-sm font-bold tabular-nums" data-range></p></li>''')
    return f'<ol class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4" data-steps>{"".join(lis)}</ol>'

def profiles(r):
    P = [("Aspirantes", "Carreras, examen, becas", "admisiones.html"), ("Alumnos", "SAEKO, calendario, trámites", "alumnos.html"),
         ("Estudias y trabajas", "Modalidad mixta", "estudia-y-trabaja.html"), ("Empresas", "Convenios, estadías, talento", "empresas.html"),
         ("Egresados", "Bolsa de trabajo, titulación", "egresados.html")]
    cells = "".join(f'<a href="{r}{h}" class="group flex items-center justify-between gap-3 bg-white px-5 py-5 hover:bg-paper{" col-span-2 sm:col-span-1" if i==4 else ""}"><span><span class="block font-display text-lg font-bold">{t}</span><span class="block text-sm text-ink/70">{s}</span></span>{ic("arrow","h-5 w-5 text-ink/40 transition-transform group-hover:translate-x-0.5 group-hover:text-navy")}</a>' for i, (t, s, h) in enumerate(P))
    return f'<div class="border-y border-ink/10 bg-white"><nav aria-label="Accesos por perfil" class="mx-auto grid max-w-7xl grid-cols-2 gap-px bg-ink/10 sm:grid-cols-3 lg:grid-cols-5">{cells}</nav></div>'

def asesor_cta(r, title="¿Tienes dudas? Habla con un asesor", txt="Te ayudamos a elegir carrera, resolver dudas de la convocatoria o de la modalidad mixta."):
    return f'''<section class="sec"><div class="wrap"><div class="grid items-center gap-6 rounded-3xl bg-navy-deep p-8 text-white sm:p-12 lg:grid-cols-[1.5fr_1fr]">
  <div><h2 class="font-display text-3xl font-extrabold leading-tight sm:text-4xl">{title}</h2><p class="mt-3 max-w-xl text-lg text-white/80">{txt}</p></div>
  <div class="flex flex-col gap-3 sm:flex-row lg:justify-end"><a href="#" data-asesor class="btn bg-ut-brand text-ink hover:bg-[#00C298]">{ic("chat")} WhatsApp</a><a href="{r}contacto.html" class="btn border-2 border-white/30 text-white hover:bg-white/10">Otros contactos</a></div>
</div></div></section>'''

# ================================================================== PÁGINAS
def p_inicio(r):
    feat = NOTICIAS[8]
    rest = [NOTICIAS[6], NOTICIAS[0], NOTICIAS[3]]
    chips = "".join(f'<a href="{r}oferta-educativa.html?area={k}" class="chip"><span class="dot" style="background:{a["color"]}"></span>{a["nombre"].split(" ")[0]}</a>' for k, a in AREAS.items())
    avisos = [("Convocatoria de admisión 2027", "Solicitudes a partir del 16 de enero (fecha de ejemplo).", "admisiones.html", "Admisiones"),
              ("Certificación Oxford Test of English", "Regístrate para la próxima aplicación en la UTMA.", "internacional.html#bilingue", "Bilingüe"),
              ("Rutas de transporte actualizadas", "Consulta las rutas vigentes para llegar a la UTMA.", "conoce-la-utma.html#como-llegar", "Comunidad"),
              ("Trabaja con nosotros", "Conoce las vacantes para personal docente y administrativo.", "conoce-la-utma.html#trabaja", "Capital Humano")]
    av = "".join(f'<a href="{r}{u}" class="card-hover flex flex-col gap-1.5 p-5"><span class="eyebrow">{c}</span><span class="font-bold leading-snug">{t}</span><span class="text-sm text-ink/70">{d}</span></a>' for t, d, u, c in avisos)
    return f'''
<section class="relative overflow-hidden">
  <div class="wrap grid items-center gap-10 pb-12 pt-8 lg:grid-cols-[1.1fr_.9fr] lg:pb-16 lg:pt-14">
    <div class="min-w-0">
      <p class="inline-flex items-center gap-2 rounded-full bg-naranja-soft px-3 py-1 text-sm font-bold text-naranja-text"><span class="dot bg-naranja"></span>Admisiones 2027 · consulta la convocatoria</p>
      <h1 class="mt-4 font-display text-[2.5rem] font-extrabold leading-[1.02] tracking-tight sm:text-6xl lg:text-[4.2rem]">Dos títulos, una carrera que te lleva más lejos.</h1>
      <p class="mt-5 max-w-xl text-lg leading-relaxed text-ink/80">Estudia TSU y continúa a Ingeniería o Licenciatura en la UTMA, en modalidad escolarizada o mixta, con el Modelo BIS: bilingüe, internacional y sostenible.</p>
      <div class="relative mt-7 max-w-xl">
        <label for="hq" class="label">¿Qué te gustaría estudiar?</label>
        <div class="flex items-center gap-2 rounded-2xl border-2 border-ink/15 bg-white p-1.5 focus-within:border-navy">
          {ic("search","ml-2 h-5 w-5 text-ink/60")}
          <input id="hq" class="h-11 min-w-0 flex-1 bg-transparent text-base outline-none" placeholder="Ej. robótica, software, enfermería" role="combobox" aria-expanded="false" aria-controls="hq-list" aria-autocomplete="list" autocomplete="off" data-combobox="programas" data-popup>
          <a href="{r}oferta-educativa.html" class="btn-navy hidden h-11 rounded-xl px-4 text-sm sm:inline-flex">Ver carreras</a>
        </div>
        <ul id="hq-list" role="listbox" data-open="false" class="pop absolute left-0 right-0 top-full z-30 mt-2 max-h-80 overflow-y-auto rounded-2xl border border-ink/10 bg-white p-2 text-sm shadow-xl"></ul>
      </div>
      <div class="mt-4 flex flex-wrap gap-2" aria-label="Áreas">{chips}</div>
      <div class="mt-8 flex flex-col gap-3 sm:flex-row"><a href="{r}admisiones.html#solicitud" class="btn-primary h-12">Solicita tu examen de admisión</a><a href="#" data-asesor class="btn-ghost h-12"><span class="dot bg-ut-brand"></span>Habla con un asesor</a></div>
    </div>
    <div class="relative hidden min-w-0 sm:block">
      <div class="relative mx-auto aspect-square w-full max-w-[520px]">
        <svg viewBox="0 0 400 400" class="absolute inset-0 h-full w-full overflow-visible" aria-hidden="true"><g data-rays transform="translate(200 200)"></g><circle cx="200" cy="200" r="34" fill="#fff"/></svg>
        <div class="absolute left-0 top-[8%] w-[62%] rounded-2xl bg-white p-4 shadow-xl ring-1 ring-ink/5">
          <p class="eyebrow">Admisión en 4 pasos</p>
          <ol class="mt-3 space-y-2 text-sm">{"".join(f'<li class="flex items-center gap-2"><span class="flex h-6 w-6 items-center justify-center rounded-full {"bg-ut text-white" if i==1 else "bg-navy-soft text-navy"} text-xs font-bold">{i}</span>{E(s["paso"])}</li>' for i, s in enumerate(CONVOCATORIA, 1))}</ol>
        </div>
        <div class="absolute bottom-[6%] right-0 w-[58%] rounded-2xl bg-white p-4 shadow-xl ring-1 ring-ink/5">
          <p class="eyebrow">Modelo BIS</p>
          <div class="mt-2 flex flex-wrap gap-1.5 text-sm font-bold"><span class="badge bg-navy-soft text-sm text-navy">Bilingüe</span><span class="badge bg-naranja-soft text-sm text-naranja-text">Internacional</span><span class="badge bg-ut-soft text-sm text-ut">Sostenible</span></div>
          <p class="mt-3 font-display text-3xl font-extrabold tabular-nums">+1,500</p><p class="text-sm text-ink/70">estudiantes en la UTMA</p>
        </div>
      </div>
    </div>
  </div>
  {profiles(r)}
</section>

<section class="sec pb-0" aria-labelledby="avisos-t"><div class="wrap">
  <div class="flex flex-wrap items-end justify-between gap-4"><h2 id="avisos-t" class="sec-title">Avisos y convocatorias</h2><a class="link" href="{r}noticias.html">Ver noticias</a></div>
  <div class="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">{av}</div>
</div></section>

<section class="sec" aria-labelledby="oferta-t"><div class="wrap">
  <div class="flex flex-wrap items-end justify-between gap-4"><div><h2 id="oferta-t" class="sec-title">Encuentra tu carrera</h2><p class="sec-lead">16 opciones en 5 áreas. Filtra por área y modalidad.</p></div><a class="btn-ghost" href="{r}oferta-educativa.html">Explorador completo</a></div>
  <div class="mt-8" data-explorer="compact"></div>
</div></section>

<section class="sec bg-white" aria-labelledby="adm-t"><div class="wrap">
  <div class="flex flex-wrap items-end justify-between gap-4"><div><p class="eyebrow">Convocatoria 2027 · fechas de ejemplo</p><h2 id="adm-t" class="sec-title mt-2">Así entras a la UTMA</h2></div><a class="btn-primary" href="{r}admisiones.html#solicitud">Solicita tu examen</a></div>
  <div class="mt-8">{steps_block(r)}</div>
  <p class="mt-4 text-sm text-ink/70">¿Requisitos y costos? <a class="link" href="{r}admisiones.html#requisitos">Consulta la guía completa</a>.</p>
</div></section>

<section class="sec" aria-labelledby="bis-t"><div class="wrap">
  <p class="eyebrow">Modelo educativo</p><h2 id="bis-t" class="sec-title mt-2 max-w-3xl">Modelo BIS: bilingüe, internacional y sostenible</h2>
  <div class="mt-8 grid gap-4 md:grid-cols-3">
    <article class="card p-6"><span class="flex h-11 w-11 items-center justify-center rounded-xl bg-navy-soft text-navy">{ic("chat2")}</span><h3 class="mt-4 text-xl font-bold">Bilingüe</h3><p class="mt-2 text-ink/75">Inglés en todos los cuatrimestres y certificación Oxford Test of English en la propia universidad.</p></article>
    <article class="card p-6"><span class="flex h-11 w-11 items-center justify-center rounded-xl bg-naranja-soft text-naranja-text">{ic("globe")}</span><h3 class="mt-4 text-xl font-bold">Internacional</h3><p class="mt-2 text-ink/75">Movilidad con Quarks Abroad, becas internacionales y convenios con universidades de otros países.</p></article>
    <article class="card p-6"><span class="flex h-11 w-11 items-center justify-center rounded-xl bg-ut-soft text-ut">{ic("leaf")}</span><h3 class="mt-4 text-xl font-bold">Sostenible</h3><p class="mt-2 text-ink/75">Proyectos con impacto social y ambiental en carreras como Electromovilidad, Nanotecnología y Arquitectura.</p></article>
  </div>
  <div class="mt-4 card grid gap-6 p-6 sm:p-8 lg:grid-cols-[1fr_2fr] lg:items-center">
    <div><h3 class="text-2xl font-bold">Dos títulos, dos cédulas</h3><p class="mt-2 text-ink/75">Primero obtienes tu título de Técnico Superior Universitario y puedes trabajar. Después continúas a Ingeniería o Licenciatura.</p></div>
    <div class="grid grid-cols-[6fr_5fr] gap-2 text-sm font-bold">
      <div class="rounded-xl bg-navy p-4 text-white">TSU<span class="mt-1 block font-normal text-white/80">Cuatrimestres 1–6 · incluye estadía en empresa</span></div>
      <div class="rounded-xl bg-ink p-4 text-white">Ingeniería o Licenciatura<span class="mt-1 block font-normal text-white/80">Cuatrimestres 7–11 · segunda estadía</span></div>
    </div>
  </div>
</div></section>

<section class="border-y border-ink/10 bg-white" aria-label="Cifras"><div class="wrap grid grid-cols-2 gap-px bg-ink/10 lg:grid-cols-4">
  {"".join(f'<div class="bg-white px-4 py-8 sm:px-6"><p class="font-display text-4xl font-extrabold tabular-nums sm:text-5xl">{n}</p><p class="mt-1 text-sm text-ink/70">{t}</p></div>' for n, t in [("+1,500","estudiantes (antes 120)"),("16","programas educativos"),("2","títulos en un solo trayecto"),("3","modalidades: escolarizada, mixta y posgrado")])}
</div></section>

<section class="sec" aria-labelledby="hist-t"><div class="wrap">
  <div class="flex flex-wrap items-end justify-between gap-4"><h2 id="hist-t" class="sec-title">Historias UTMA</h2><a class="link" href="{r}noticias.html">Todas las noticias</a></div>
  <div class="mt-8">{news_card(r, feat, True)}</div>
  <div class="mt-4 grid gap-4 md:grid-cols-3">{"".join(news_card(r, n) for n in rest)}</div>
</div></section>

<section class="sec bg-white" aria-labelledby="ev-t"><div class="wrap grid gap-10 lg:grid-cols-[1fr_1.2fr]">
  <div><p class="eyebrow">Vida universitaria</p><h2 id="ev-t" class="sec-title mt-2">Próximos eventos</h2><p class="sec-lead">Deportes con los Quarks, E-Sports, cultura y fechas escolares en un solo calendario.</p>
  <div class="mt-6 flex flex-wrap gap-3"><a class="btn-navy" href="{r}calendario.html">Ver calendario</a><a class="btn-ghost" href="{r}vida-universitaria.html">Vida universitaria</a></div></div>
  <div data-events="4"></div>
</div></section>

<section class="sec" aria-labelledby="emp-t"><div class="wrap grid gap-4 lg:grid-cols-2">
  <div class="card flex flex-col gap-3 p-8"><p class="eyebrow">Empresas</p><h2 id="emp-t" class="text-3xl font-extrabold">Contrata talento UTMA</h2><p class="text-ink/75">Recibe estudiantes en estadía, firma un convenio o capacita a tu personal con educación continua.</p><a class="btn-navy mt-auto self-start" href="{r}empresas.html">Vinculación con empresas</a></div>
  <div class="card flex flex-col gap-3 p-8" id="llegar"><p class="eyebrow">Visítanos</p><h2 class="text-3xl font-extrabold">Cómo llegar</h2><p class="text-ink/75">Av. Gerónimo de la Cueva S/N, Fracc. Villas del Río, 20126, Aguascalientes.</p>
    <div class="mt-auto flex flex-wrap gap-3"><a class="btn-ghost" target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query=Universidad+Tecnol%C3%B3gica+Metropolitana+de+Aguascalientes">{ic("pin")} Abrir en Google Maps</a><a class="btn-ghost" href="{r}conoce-la-utma.html#como-llegar">Rutas de transporte</a></div></div>
</div></section>
'''

def p_oferta(r):
    qs = [("¿Qué disfrutas más?", [("Crear apps o resolver problemas con lógica", "ti"), ("Armar, reparar o automatizar máquinas", "ing"), ("Dibujar y diseñar espacios", "con"), ("Organizar, negociar o manejar dinero", "neg"), ("Ayudar y cuidar a otras personas", "sal")]),
          ("¿Qué materia se te da mejor?", [("Matemáticas y computación", "ti"), ("Física y química", "ing"), ("Dibujo y geometría", "con"), ("Economía y administración", "neg"), ("Biología", "sal")]),
          ("¿Dónde te imaginas trabajando?", [("En una empresa de software o desde casa", "ti"), ("En una planta industrial", "ing"), ("En una obra o un despacho", "con"), ("En una oficina o aduana", "neg"), ("En un hospital o clínica", "sal")]),
          ("¿Qué te gustaría lograr?", [("Lanzar una app o un producto digital", "ti"), ("Diseñar un robot o un auto eléctrico", "ing"), ("Construir algo que dure años", "con"), ("Tener mi propio negocio", "neg"), ("Mejorar la salud de mi comunidad", "sal")])]
    test = "".join(f'''<fieldset class="step-panel" data-q="{i}" {"hidden" if i else ""}><legend class="text-xl font-bold">{i+1}. {q}</legend><div class="mt-4 grid gap-2">{"".join(f'<button type="button" class="chip justify-start rounded-xl px-4 py-3 text-left" data-a="{a}">{E(t)}</button>' for t, a in opts)}</div></fieldset>''' for i, (q, opts) in enumerate(qs))
    return page_head(r, "Oferta educativa", "Encuentra tu carrera", "Licenciaturas e ingenierías con título de TSU incluido, en modalidad escolarizada o mixta, y posgrado. Filtra por área, modalidad o palabra clave, y compara hasta 3 opciones.", crumbs(r, ("Oferta educativa", None))) + f'''
<section class="sec pt-10"><div class="wrap"><div data-explorer="full"></div></div></section>
<section id="test" class="sec bg-white" aria-labelledby="test-t"><div class="wrap grid gap-10 lg:grid-cols-[1fr_1.2fr]">
  <div><p class="eyebrow">Test rápido</p><h2 id="test-t" class="sec-title mt-2">¿Aún no sabes qué estudiar?</h2><p class="sec-lead">Responde 4 preguntas y te sugerimos un área. No sustituye la orientación vocacional; si quieres, un asesor te acompaña.</p></div>
  <div class="card p-6 sm:p-8" data-quiz>{test}
    <div data-quiz-result hidden class="step-panel"></div>
    <div class="mt-6 flex items-center justify-between"><p class="text-sm text-ink/60" data-quiz-progress>Pregunta 1 de 4</p><button type="button" class="link text-sm" data-quiz-reset>Reiniciar</button></div>
  </div>
</div></section>
<section class="sec" aria-labelledby="mod-t"><div class="wrap">
  <h2 id="mod-t" class="sec-title">Modalidades</h2>
  <div class="mt-8 grid gap-4 md:grid-cols-3">
    <a href="{r}admisiones.html" class="card-hover p-6"><h3 class="text-xl font-bold">Escolarizada</h3><p class="mt-2 text-ink/75">Clases presenciales de lunes a viernes. 13 carreras con TSU + Ingeniería o Licenciatura.</p></a>
    <a href="{r}estudia-y-trabaja.html" class="card-hover p-6"><h3 class="text-xl font-bold">Mixta</h3><p class="mt-2 text-ink/75">Para quien trabaja: sesiones presenciales reducidas y plataforma en línea. 3 carreras.</p></a>
    <a href="{r}carreras/maestria-en-gestion-gubernamental.html" class="card-hover p-6"><h3 class="text-xl font-bold">Posgrado</h3><p class="mt-2 text-ink/75">Maestría en Gestión Gubernamental con especialidad en Finanzas Públicas.</p></a>
  </div>
</div></section>
''' + asesor_cta(r)

def p_carrera(p):
    def m(r):
        a = AREAS[p["area"]]
        txtc = "#1D191A" if p["area"] in ("con", "ing", "neg") else "#fff"
        mods = " · ".join(MODALIDADES[x] for x in p["mods"])
        is_ug = p["mods"][0] in ("esc", "mix")
        mat = MATERIAS[p["area"]]
        cq = []
        for n in range(1, 12):
            if n in (6, 11):
                cq.append(f'<div class="flex min-w-[130px] flex-col gap-1.5 rounded-xl border border-[#F6C9A4] bg-naranja-soft p-3 text-sm"><b class="text-xs text-ink/60">C{n}</b><span class="rounded-md bg-white px-2 py-1">Estadía en empresa</span><span class="rounded-md bg-white px-2 py-1 font-bold">{"Título TSU" if n==6 else "Título " + p["nivel"]}</span></div>')
            else:
                sub = mat[n-1] if n < 6 else mat[n-2]
                cq.append(f'<div class="flex min-w-[130px] flex-col gap-1.5 rounded-xl border border-ink/10 bg-white p-3 text-sm"><b class="text-xs text-ink/60">C{n}</b><span class="rounded-md bg-paper px-2 py-1">{E(sub)}</span><span class="rounded-md bg-paper px-2 py-1">Inglés {n if n<6 else n-1}</span></div>')
        plan = f'''<div class="grid grid-cols-[6fr_5fr] gap-2 text-sm font-bold"><div class="rounded-lg px-3 py-2" style="background:{a["color"]};color:{txtc}">TSU · cuatrimestres 1–6</div><div class="rounded-lg bg-ink px-3 py-2 text-white">{p["nivel"]} · cuatrimestres 7–11</div></div>
<div class="mt-3 grid grid-flow-col gap-2 overflow-x-auto pb-2" style="grid-auto-columns:minmax(130px,1fr)" tabindex="0" aria-label="Mapa curricular, desplázate horizontalmente">{"".join(cq)}</div>
<p class="mt-2 text-sm text-ink/60">Mapa ilustrativo del modelo de Universidades Tecnológicas. Se reemplaza con el plan oficial.</p>''' if is_ug else '<p class="text-ink/75">El plan de estudios se publicará con la información oficial del programa.</p>'
        rel = [x for x in PROGRAMAS if x["area"] == p["area"] and x["id"] != p["id"]][:3]
        req = ["Certificado de bachillerato o constancia de estudios", "CURP", "Acta de nacimiento", "Identificación oficial", "Comprobante de pago de ficha"] if p["mods"][0] != "pos" else ["Título y cédula de licenciatura", "CURP e identificación oficial", "Carta de exposición de motivos", "Entrevista con la coordinación"]
        tabs = [("plan", "Plan de estudios", plan),
                ("perfil", "Perfil de egreso", "<ul class='grid gap-2 sm:grid-cols-2'>" + "".join(f"<li class='flex gap-2 rounded-xl bg-paper p-4'>{ic('check','h-5 w-5 text-ut mt-0.5')}<span>{E(x)}</span></li>" for x in p["perfil"]) + "</ul>"),
                ("campo", "Campo laboral", "<ul class='grid gap-2 sm:grid-cols-2'>" + "".join(f"<li class='flex gap-2 rounded-xl bg-paper p-4'>{ic('arrow','h-5 w-5 text-navy mt-0.5')}<span>{E(x)}</span></li>" for x in p["campo"]) + "</ul>"),
                ("requisitos", "Requisitos", "<ul class='grid gap-2'>" + "".join(f"<li class='flex gap-2'>{ic('doc','h-5 w-5 text-ink/50 mt-0.5')}<span>{E(x)}</span></li>" for x in req) + f"</ul><p class='mt-4 text-sm text-ink/60'>Lista de referencia: la convocatoria vigente es la fuente oficial. <a class='link' href='{r}admisiones.html#requisitos'>Ver requisitos completos</a></p>")]
        tablist = "".join(f'<button role="tab" id="tab-{k}" aria-controls="pn-{k}" aria-selected="{"true" if i==0 else "false"}" class="chip" tabindex="{0 if i==0 else -1}">{t}</button>' for i, (k, t, _) in enumerate(tabs))
        panels = "".join(f'<div role="tabpanel" id="pn-{k}" aria-labelledby="tab-{k}" class="step-panel" {"hidden" if i else ""}>{c}</div>' for i, (k, _, c) in enumerate(tabs))
        cta = "Avísame cuando abra" if "nva" in p["mods"] else "Solicita tu examen"
        cta_href = f'{r}contacto.html#buzon' if "nva" in p["mods"] else f'{r}admisiones.html?carrera={p["id"]}#solicitud'
        dur = "Hasta 11 cuatrimestres (TSU en 6)" if is_ug else ("Por confirmar" if "nva" in p["mods"] else "Consultar coordinación")
        return f'''<section class="border-b border-ink/10 bg-white"><div class="wrap py-10 sm:py-14">
  {crumbs(r, ("Oferta educativa", "oferta-educativa.html"), (p["nombre"], None))}
  <div class="mt-6 grid gap-8 lg:grid-cols-[1.5fr_1fr] lg:items-end">
    <div><span class="badge" style="background:{a["suave"]};color:{a["color"] if p["area"] in ("ti","sal") else "#1D191A"}"><span class="dot mr-1.5" style="background:{a["color"]}"></span>{a["nombre"]}</span>
      <h1 class="page-title mt-3">{E(p["nombre"])}</h1><p class="sec-lead">{E(p["resumen"])}</p></div>
    <div class="media aspect-[16/10] max-h-[300px] w-full rounded-3xl" style="--c:{a["color"]};--s:{a["suave"]}" role="img" aria-label="Espacio para fotografía de la carrera"></div>
  </div>
  <dl class="mt-8 grid grid-cols-2 gap-px overflow-hidden rounded-2xl border border-ink/10 bg-ink/10 lg:grid-cols-4">
    <div class="bg-white p-4"><dt class="eyebrow">Modalidad</dt><dd class="mt-1 font-bold">{mods}</dd></div>
    <div class="bg-white p-4"><dt class="eyebrow">Título</dt><dd class="mt-1 font-bold">{"TSU + " + p["nivel"] if is_ug else p["nivel"]}</dd></div>
    <div class="bg-white p-4"><dt class="eyebrow">Duración</dt><dd class="mt-1 font-bold">{dur}</dd></div>
    <div class="bg-white p-4"><dt class="eyebrow">Inglés</dt><dd class="mt-1 font-bold">Todos los cuatrimestres</dd></div>
  </dl>
</div></section>
<section class="sec pt-10"><div class="wrap grid gap-8 lg:grid-cols-[1fr_340px]">
  <div class="min-w-0 space-y-6">
    {note("Contenido de muestra para el prototipo. Validar perfil, campo laboral y plan de estudios con la Dirección de Carrera.")}
    <div data-tabs><div role="tablist" aria-label="Información de la carrera" class="flex flex-wrap gap-2">{tablist}</div><div class="card mt-4 p-5 sm:p-7">{panels}</div></div>
  </div>
  <aside class="space-y-4 lg:sticky lg:top-24 lg:self-start">
    <div class="card p-6"><p class="font-display text-xl font-bold">¿Te interesa {E(p["nombre"].replace(" (mixta)",""))}?</p><p class="mt-2 text-sm text-ink/70">{"Te avisamos en cuanto abra la convocatoria." if "nva" in p["mods"] else "La carrera ya queda seleccionada en tu solicitud."}</p>
      <a href="{cta_href}" class="btn-primary mt-4 w-full">{cta}</a>
      <a href="#" data-asesor class="btn-ghost mt-2 w-full">{ic("chat")} Hablar con un asesor</a>
      <a href="#" data-demo="En el sitio real se descarga el PDF oficial del plan de estudios." class="link mt-4 inline-flex items-center gap-2 text-sm">{ic("doc","h-4 w-4")} Descargar plan en PDF</a></div>
    {f'<a href="{r}estudia-y-trabaja.html" class="card-hover block p-5"><p class="font-bold">También en modalidad mixta</p><p class="text-sm text-ink/70">Para quien trabaja. Conoce cómo funciona.</p></a>' if "mix" in p["mods"] else ""}
  </aside>
</div></section>
{f'<section class="sec bg-white"><div class="wrap"><h2 class="sec-title">Otras carreras del área</h2><div class="mt-8 grid gap-4 md:grid-cols-3">{"".join(prog_card(r, x) for x in rel)}</div></div></section>' if rel else ""}
'''
    return m

def p_admisiones(r):
    opts = "".join(f'<option value="{p["id"]}">{E(p["nombre"])}</option>' for p in PROGRAMAS if "nva" not in p["mods"])
    faq = [("¿Cuánto cuesta la ficha?", "El costo se publica en la convocatoria vigente. En este prototipo aparece como «por confirmar con Finanzas»."),
           ("¿Puedo estudiar si trabajo?", "Sí. La modalidad mixta tiene sesiones presenciales reducidas y plataforma en línea. Revisa «Estudias y trabajas»."),
           ("¿Qué pasa si no termino el bachillerato a tiempo?", "Puedes registrarte con constancia de estudios y entregar el certificado al inscribirte, según lo indique la convocatoria."),
           ("¿El examen es en línea o presencial?", "Lo indica la convocatoria. Tu pase al examen trae la sede, el horario y lo que debes llevar."),
           ("¿Hay becas?", "Sí, hay becas institucionales y apoyos para movilidad internacional. Consulta Internacional › Becas."),
           ("¿Puedo cambiar de carrera después?", "Consulta con Servicios Escolares; depende del cupo y del avance en tu plan de estudios.")]
    return page_head(r, "Admisiones 2027", "Entra a la UTMA en 4 pasos", "Todo el proceso en un solo lugar: fechas, requisitos, costos, solicitud de examen y resultados. Sin PDFs ni botones-imagen.", crumbs(r, ("Admisiones", None)), "#00785F", "#E3F5EF",
      f'<div class="mt-6 flex flex-wrap gap-3"><a class="btn-primary" href="#solicitud">Solicita tu examen</a><a class="btn-ghost" href="#resultados">Consultar resultados</a></div>') + f'''
<section class="sec pt-10" aria-labelledby="cal-t"><div class="wrap">
  <div class="flex flex-wrap items-end justify-between gap-3"><h2 id="cal-t" class="sec-title">Calendario de la convocatoria</h2><span class="badge bg-[#FFF6DF] text-[#5C4100]">Fechas de ejemplo</span></div>
  <div class="mt-8">{steps_block(r)}</div>
</div></section>
<section id="requisitos" class="sec bg-white scroll-mt-24" aria-labelledby="req-t"><div class="wrap grid gap-10 lg:grid-cols-2">
  <div><h2 id="req-t" class="sec-title">Requisitos</h2><ul class="mt-6 space-y-3">{"".join(f'<li class="flex gap-3">{ic("check","h-6 w-6 text-ut")}<span class="text-lg">{x}</span></li>' for x in ["Certificado de bachillerato o constancia de estudios con promedio", "CURP actualizada", "Acta de nacimiento", "Identificación oficial con fotografía", "Fotografía digital reciente", "Comprobante de pago de ficha"])}</ul>
  <p class="mt-4 text-sm text-ink/60">Validar lista con Servicios Escolares antes de publicar.</p></div>
  <div><h2 class="sec-title">Costos</h2><div class="mt-6 overflow-x-auto rounded-2xl border border-ink/10"><table class="tbl"><thead><tr><th>Concepto</th><th>Monto</th></tr></thead><tbody>
    <tr><td>Ficha de examen de admisión</td><td class="text-ink/60">Por confirmar con Finanzas</td></tr><tr><td>Inscripción</td><td class="text-ink/60">Por confirmar con Finanzas</td></tr>
    <tr><td>Cuota cuatrimestral</td><td class="text-ink/60">Por confirmar con Finanzas</td></tr><tr><td>Curso propedéutico (si aplica)</td><td class="text-ink/60">Por confirmar</td></tr></tbody></table></div>
    <p class="mt-4 text-sm text-ink/70">¿Necesitas apoyo económico? <a class="link" href="{r}internacional.html#becas">Conoce las becas</a>.</p></div>
</div></section>

<section id="solicitud" class="sec scroll-mt-24" aria-labelledby="sol-t"><div class="wrap grid gap-10 lg:grid-cols-[1fr_1.4fr]">
  <div><p class="eyebrow">Paso 1</p><h2 id="sol-t" class="sec-title mt-2">Solicita tu examen</h2><p class="sec-lead">Toma unos 5 minutos. Al terminar recibes un folio para dar seguimiento.</p>
  <div class="mt-6">{note("Prototipo: la solicitud se guarda sólo en este navegador. En producción se envía al sistema de admisiones.")}</div></div>
  <form class="card p-6 sm:p-8" data-wizard novalidate>
    <ol class="mb-6 grid grid-cols-3 gap-2 text-xs font-bold" aria-label="Progreso">{"".join(f'<li class="rounded-lg bg-paper px-2 py-2 text-center text-ink/60" data-dot="{i}">{i+1}. {t}</li>' for i, t in enumerate(["Tus datos", "Escuela", "Carrera"]))}</ol>
    <fieldset data-step="0" class="step-panel space-y-4"><legend class="sr-only">Tus datos</legend>
      <div class="grid gap-4 sm:grid-cols-2"><div><label class="label" for="s-nombre">Nombre(s)</label><input class="input" id="s-nombre" name="nombre" required autocomplete="given-name"></div>
      <div><label class="label" for="s-apellidos">Apellidos</label><input class="input" id="s-apellidos" name="apellidos" required autocomplete="family-name"></div></div>
      <div><label class="label" for="s-curp">CURP</label><input class="input uppercase" id="s-curp" name="curp" required maxlength="18" data-rule="curp" placeholder="18 caracteres" autocomplete="off"><p class="hint">La encuentras en tu acta o en gob.mx/curp.</p></div>
      <div class="grid gap-4 sm:grid-cols-2"><div><label class="label" for="s-email">Correo electrónico</label><input class="input" id="s-email" name="email" type="email" required autocomplete="email"></div>
      <div><label class="label" for="s-tel">Celular (10 dígitos)</label><input class="input" id="s-tel" name="tel" type="tel" inputmode="numeric" required data-rule="tel" autocomplete="tel-national"></div></div>
    </fieldset>
    <fieldset data-step="1" class="step-panel space-y-4" hidden><legend class="sr-only">Escuela</legend>
      <div><label class="label" for="s-bach">Bachillerato de procedencia</label><input class="input" id="s-bach" name="bachillerato" required></div>
      <div class="grid gap-4 sm:grid-cols-2"><div><label class="label" for="s-prom">Promedio</label><input class="input" id="s-prom" name="promedio" inputmode="decimal" required data-rule="promedio" placeholder="Ej. 8.5"></div>
      <div><label class="label" for="s-egreso">Año de egreso</label><select class="input" id="s-egreso" name="egreso" required><option value="">Elige</option><option>2027 (en curso)</option><option>2026</option><option>2025</option><option>2024 o antes</option></select></div></div>
    </fieldset>
    <fieldset data-step="2" class="step-panel space-y-4" hidden><legend class="sr-only">Carrera</legend>
      <div><label class="label" for="s-carrera">Carrera de interés</label><select class="input" id="s-carrera" name="carrera" required><option value="">Elige una carrera</option>{opts}</select></div>
      <div><label class="label" for="s-carrera2">Segunda opción (opcional)</label><select class="input" id="s-carrera2" name="carrera2"><option value="">Ninguna</option>{opts}</select></div>
      <label class="flex items-start gap-3 text-sm"><input type="checkbox" name="aviso" required class="mt-1 h-5 w-5 accent-[#00785F]"><span>Leí el <a class="link" href="{r}aviso-de-privacidad.html" target="_blank">aviso de privacidad</a> y acepto el uso de mis datos para el proceso de admisión.</span></label>
    </fieldset>
    <div data-done hidden class="step-panel"></div>
    <div class="mt-6 flex items-center justify-between gap-3" data-nav><button type="button" class="btn-ghost" data-prev hidden>Atrás</button><span></span><button type="button" class="btn-primary" data-next>Continuar</button></div>
  </form>
</div></section>

<section id="resultados" class="sec bg-white scroll-mt-24" aria-labelledby="res-t"><div class="wrap grid gap-10 lg:grid-cols-[1fr_1.4fr]">
  <div><p class="eyebrow">Paso 4</p><h2 id="res-t" class="sec-title mt-2">Consulta tus resultados</h2><p class="sec-lead">Escribe el folio que recibiste al solicitar tu examen. Para probar: <b class="tabular-nums">UTMA-27-0001</b>.</p></div>
  <form class="card p-6 sm:p-8" data-results novalidate><label class="label" for="r-folio">Folio</label><div class="flex flex-col gap-2 sm:flex-row"><input class="input uppercase" id="r-folio" required placeholder="UTMA-27-0000" autocomplete="off"><button class="btn-navy">Consultar</button></div><div data-out class="mt-5" aria-live="polite"></div></form>
</div></section>

<section id="visita" class="sec scroll-mt-24"><div class="wrap grid gap-10 lg:grid-cols-[1fr_1.4fr]">
  <div><p class="eyebrow">Vive la UTMA</p><h2 class="sec-title mt-2">Agenda una visita al campus</h2><p class="sec-lead">Conoce laboratorios, talleres y platica con estudiantes. Visitas guiadas los sábados (ejemplo).</p></div>
  <form class="card grid gap-4 p-6 sm:grid-cols-2 sm:p-8" data-form="visita" novalidate>
    <div><label class="label" for="v-nombre">Nombre</label><input class="input" id="v-nombre" required></div>
    <div><label class="label" for="v-tel">Celular</label><input class="input" id="v-tel" type="tel" inputmode="numeric" data-rule="tel" required></div>
    <div><label class="label" for="v-fecha">Fecha</label><select class="input" id="v-fecha" required><option value="">Elige</option><option>Sábado 5 de diciembre (ejemplo)</option><option>Sábado 6 de febrero (ejemplo)</option></select></div>
    <div><label class="label" for="v-personas">Personas</label><select class="input" id="v-personas"><option>1</option><option>2</option><option>3</option><option>4 o más</option></select></div>
    <div class="sm:col-span-2"><button class="btn-primary">Reservar visita</button></div>
    <div data-ok hidden class="sm:col-span-2"></div>
  </form>
</div></section>

<section id="faq" class="sec bg-white scroll-mt-24" aria-labelledby="faq-t"><div class="wrap grid gap-10 lg:grid-cols-[1fr_1.6fr]">
  <h2 id="faq-t" class="sec-title">Preguntas frecuentes</h2>
  <div class="space-y-3">{"".join(f'<details class="details-u"><summary>{q}</summary><div>{a}</div></details>' for q, a in faq)}</div>
</div></section>
''' + asesor_cta(r)

def p_vida(r):
    blocks = [("deportes", "Deportes · Quarks", "#F57E26", "#FFF0E4", "Los Quarks representan a la UTMA en fútbol americano y llegaron a la final de la Liga FAM. Además hay selecciones y talleres deportivos abiertos a toda la comunidad.", [("Fútbol americano", "Quarks"), ("Selecciones", "Por confirmar"), ("Acondicionamiento", "Gimnasio")]),
              ("esports", "E-Sports", "#235F83", "#E6F0F5", "Equipos competitivos y torneos internos. Antes estaba suelto en el menú principal; ahora vive con el resto de la vida universitaria.", [("Torneos internos", "Cada cuatrimestre"), ("Equipo representativo", "Selección"), ("Comunidad", "Discord por confirmar")]),
              ("cultura", "Cultura", "#B61F3E", "#FDECF0", "Talleres artísticos, eventos culturales y actividades para la comunidad. Contenido a completar con el área de Cultura.", [("Talleres", "Por confirmar"), ("Eventos", "Calendario"), ("Grupos", "Por confirmar")])]
    secs = "".join(f'''<section id="{k}" class="sec scroll-mt-24 {"bg-white" if i%2==0 else ""}"><div class="wrap grid items-center gap-10 lg:grid-cols-2">
  <div class="media aspect-[4/3] rounded-3xl {"lg:order-2" if i%2 else ""}" style="--c:{c};--s:{s}" role="img" aria-label="Espacio para fotografía de {t}"></div>
  <div><h2 class="sec-title">{t}</h2><p class="sec-lead">{d}</p><dl class="mt-6 grid gap-3 sm:grid-cols-3">{"".join(f'<div class="rounded-xl bg-paper p-3"><dt class="text-sm font-bold">{a}</dt><dd class="text-sm text-ink/60">{b}</dd></div>' for a, b in items)}</dl></div>
</div></section>''' for i, (k, t, c, s, d, items) in enumerate(blocks))
    return page_head(r, "Vida universitaria", "Más que clases", "Deporte, E-Sports, cultura y bienestar. Todo lo que pasa en la UTMA fuera del salón.", crumbs(r, ("Vida universitaria", None)), "#F57E26", "#FFF0E4",
       '<div class="mt-6 flex flex-wrap gap-2"><a class="chip" href="#deportes">Deportes</a><a class="chip" href="#esports">E-Sports</a><a class="chip" href="#cultura">Cultura</a><a class="chip" href="#bienestar">Bienestar</a><a class="chip" href="#eventos">Eventos</a></div>') + secs + f'''
<section id="bienestar" class="sec scroll-mt-24"><div class="wrap">
  <h2 class="sec-title">Bienestar y seguridad</h2><p class="sec-lead">Protocolos que antes estaban en «Normativa» y ahora son fáciles de encontrar.</p>
  <div class="mt-8 grid gap-4 md:grid-cols-3">
    <a href="{r}transparencia.html?q=acoso" class="card-hover p-6"><h3 class="text-lg font-bold">Protocolo contra el acoso y hostigamiento sexual</h3><p class="mt-2 text-sm text-ink/70">Cómo denunciar y a quién acudir.</p></a>
    <a href="{r}transparencia.html?q=sustancias" class="card-hover p-6"><h3 class="text-lg font-bold">Protocolo ante sustancias adictivas</h3><p class="mt-2 text-sm text-ink/70">Prevención y atención.</p></a>
    <a href="{r}contacto.html#buzon" class="card-hover p-6"><h3 class="text-lg font-bold">Buzón de sugerencias</h3><p class="mt-2 text-sm text-ink/70">Envía una queja o sugerencia con seguimiento por folio.</p></a>
  </div>
</div></section>
<section id="eventos" class="sec bg-white scroll-mt-24"><div class="wrap grid gap-10 lg:grid-cols-[1fr_1.3fr]">
  <div><h2 class="sec-title">Próximos eventos</h2><p class="sec-lead">Deportes, E-Sports y cultura.</p><a class="btn-navy mt-6" href="{r}calendario.html">Calendario completo</a></div>
  <div data-events="5" data-types="Deportes,Vida universitaria,Internacional,Vinculación"></div>
</div></section>
<section id="publicaciones" class="sec scroll-mt-24"><div class="wrap"><h2 class="sec-title">Publicaciones BIG BANG</h2><p class="sec-lead">Archivo mensual que antes estaba en el menú principal. Confirmar con Comunicación el tipo de publicación.</p>
<div class="mt-6 flex flex-wrap gap-2">{"".join(f'<a href="#" class="chip" data-demo="En el sitio real se abre la edición de {mes} de BIG BANG.">{mes}</a>' for mes in ["Julio", "Agosto", "Septiembre", "Octubre"])}</div></div></section>
'''

def p_internacional(r):
    intl = [n for n in NOTICIAS if n["cat"] == "Internacional"][:3]
    return page_head(r, "Internacional", "Modelo BIS: el mundo empieza en la UTMA", "Bilingüe, internacional y sostenible. Certifica tu inglés, estudia una temporada fuera y participa en proyectos con impacto.", crumbs(r, ("Internacional", None)), "#35BAA4", "#E3F5EF",
      '<div class="mt-6 flex flex-wrap gap-2"><a class="chip" href="#bilingue">Bilingüe</a><a class="chip" href="#becas">Becas y movilidad</a><a class="chip" href="#kickoff">Pasaportes KickOff</a><a class="chip" href="en.html" lang="en">English version</a></div>') + f'''
<section id="bilingue" class="sec scroll-mt-24"><div class="wrap grid gap-10 lg:grid-cols-2">
  <div><p class="eyebrow">Bilingüe</p><h2 class="sec-title mt-2">Oxford Test of English en la UTMA</h2><p class="sec-lead">Inglés en todos los cuatrimestres y la posibilidad de certificarte sin salir del campus.</p>
  <ul class="mt-6 space-y-3">{"".join(f'<li class="flex gap-3">{ic("check","h-6 w-6 text-ut")}<span>{x}</span></li>' for x in ["Certificación reconocida internacionalmente", "Aplicación en la universidad (fechas en el calendario)", "Válida para movilidad y para tu CV"])}</ul>
  <a class="btn-navy mt-6" href="{r}calendario.html">Ver fechas de aplicación</a></div>
  <form class="card grid gap-4 p-6 sm:p-8" data-form="oxford" novalidate><h3 class="text-xl font-bold">Pre-registro Oxford Test</h3>
    <div><label class="label" for="o-nombre">Nombre completo</label><input class="input" id="o-nombre" required></div>
    <div><label class="label" for="o-mat">Matrícula (si eres alumno)</label><input class="input" id="o-mat"></div>
    <div><label class="label" for="o-email">Correo</label><input class="input" id="o-email" type="email" required></div>
    <button class="btn-primary">Pre-registrarme</button><div data-ok hidden></div></form>
</div></section>
<section id="becas" class="sec bg-white scroll-mt-24"><div class="wrap">
  <p class="eyebrow">Movilidad</p><h2 class="sec-title mt-2">Quarks Abroad y becas internacionales</h2><p class="sec-lead">Convocatorias para estudiar o hacer estancias en el extranjero.</p>
  <div class="mt-8 grid gap-4 md:grid-cols-3">
    {"".join(f'<article class="card flex flex-col gap-2 p-6"><span class="badge self-start {b}">{e}</span><h3 class="text-lg font-bold">{t}</h3><p class="text-sm text-ink/70">{d}</p><a href="#" data-demo="En el sitio real se abre la convocatoria en PDF y el formulario." class="link mt-auto pt-2 text-sm">Ver convocatoria</a></article>' for t, d, e, b in [("Quarks Abroad", "Movilidad estudiantil internacional para alumnos regulares.", "Abierta (ejemplo)", "bg-ut-soft text-ut"), ("Becas internacionales", "Apoyos para programas de verano y estancias cortas.", "Próximamente", "bg-[#FFF6DF] text-[#5C4100]"), ("Becas institucionales", "Apoyos por promedio, situación económica o deporte.", "Consultar fechas", "bg-paper text-ink/70")])}
  </div>
</div></section>
<section id="kickoff" class="sec scroll-mt-24"><div class="wrap grid items-center gap-10 lg:grid-cols-2">
  <div class="media aspect-[4/3] rounded-3xl" style="--c:#35BAA4;--s:#E3F5EF" role="img" aria-label="Espacio para fotografía"></div>
  <div><h2 class="sec-title">Pasaportes Metropolitan KickOff</h2><p class="sec-lead">Programa para que los estudiantes tramiten su pasaporte y den el primer paso hacia la movilidad internacional.</p><a href="#" data-demo="En el sitio real se abre la información del programa." class="btn-ghost mt-6">Más información</a></div>
</div></section>
<section class="sec bg-white"><div class="wrap"><h2 class="sec-title">Noticias internacionales</h2><div class="mt-8 grid gap-4 md:grid-cols-3">{"".join(news_card(r, n) for n in intl)}</div></div></section>
'''

def p_empresas(r):
    return page_head(r, "Empresas y vinculación", "Talento técnico listo para tu empresa", "Convenios, estadías, bolsa de trabajo y educación continua para el sector productivo de Aguascalientes.", crumbs(r, ("Empresas", None)), "#B61F3E", "#FDECF0",
      '<div class="mt-6 flex flex-wrap gap-2"><a class="chip" href="#convenios">Convenios</a><a class="chip" href="#estadias">Estadías</a><a class="chip" href="#bolsa">Bolsa de trabajo</a><a class="chip" href="#educacion-continua">Educación continua</a><a class="chip" href="#contacto-empresas">Contacto</a></div>') + f'''
<section class="sec"><div class="wrap grid gap-4 md:grid-cols-2 lg:grid-cols-4">
  {"".join(f'<article id="{k}" class="card scroll-mt-24 flex flex-col gap-2 p-6"><h2 class="text-xl font-bold">{t}</h2><p class="text-ink/75">{d}</p><a href="{u}" {a} class="link mt-auto pt-2">{c}</a></article>' for k, t, d, u, a, c in [
    ("convenios", "Convenios", "Firma un convenio de colaboración para estadías, proyectos y capacitación.", "#contacto-empresas", "", "Solicitar convenio"),
    ("estadias", "Estadías", "Cada estudiante realiza dos estadías en empresa: al final del TSU y de la Ingeniería o Licenciatura.", "#contacto-empresas", "", "Recibir estudiantes"),
    ("bolsa", "Bolsa de trabajo", "Publica vacantes para egresados y estudiantes de las 16 carreras.", "#", 'data-demo="En el sitio real se abre la Bolsa de Trabajo (enlace corregido, sin la URL de edición)."', "Ir a la bolsa de trabajo"),
    ("educacion-continua", "Educación continua", "Cursos para empresas, como Costos y Presupuestos de Obra, y certificaciones de inglés.", "#cursos", "", "Ver cursos")])}
</div></section>
<section id="cursos" class="sec bg-white scroll-mt-24"><div class="wrap"><h2 class="sec-title">Cursos de educación continua</h2>
  <div class="mt-8 overflow-x-auto rounded-2xl border border-ink/10"><table class="tbl"><thead><tr><th>Curso</th><th>Dirigido a</th><th>Modalidad</th><th></th></tr></thead><tbody>
    <tr><td class="font-bold">Costos y Presupuestos de Obra</td><td>Profesionales de la construcción</td><td>Presencial</td><td><a href="#contacto-empresas" class="link">Informes</a></td></tr>
    <tr><td class="font-bold">Liderazgo: «Lidera e inspira con éxito»</td><td>Mandos medios</td><td>Por confirmar</td><td><a href="#contacto-empresas" class="link">Informes</a></td></tr>
    <tr><td class="font-bold">Oxford Test of English</td><td>Personal de empresas</td><td>Presencial</td><td><a href="{r}internacional.html#bilingue" class="link">Informes</a></td></tr>
  </tbody></table></div></div></section>
<section id="contacto-empresas" class="sec scroll-mt-24"><div class="wrap grid gap-10 lg:grid-cols-[1fr_1.4fr]">
  <div><h2 class="sec-title">Hablemos</h2><p class="sec-lead">El área de Vinculación te contacta en 2 días hábiles.</p></div>
  <form class="card grid gap-4 p-6 sm:grid-cols-2 sm:p-8" data-form="empresa" novalidate>
    <div><label class="label" for="e-emp">Empresa</label><input class="input" id="e-emp" required autocomplete="organization"></div>
    <div><label class="label" for="e-nom">Tu nombre</label><input class="input" id="e-nom" required autocomplete="name"></div>
    <div><label class="label" for="e-mail">Correo</label><input class="input" id="e-mail" type="email" required></div>
    <div><label class="label" for="e-tel">Teléfono</label><input class="input" id="e-tel" type="tel" data-rule="tel" required></div>
    <div class="sm:col-span-2"><label class="label" for="e-int">Me interesa</label><select class="input" id="e-int" required><option value="">Elige</option><option>Firmar un convenio</option><option>Recibir estudiantes en estadía</option><option>Publicar vacantes</option><option>Educación continua</option></select></div>
    <div class="sm:col-span-2"><label class="label" for="e-msg">Mensaje</label><textarea class="input min-h-[120px] py-3" id="e-msg"></textarea></div>
    <div class="sm:col-span-2"><button class="btn-primary">Enviar</button></div><div data-ok hidden class="sm:col-span-2"></div>
  </form>
</div></section>
'''

def p_conoce(r):
    rutas = "".join(f'<tr><td class="font-bold">{a}</td><td>{b}</td><td class="text-ink/60">{c}</td></tr>' for a, b, c in [("Ruta por confirmar", "Centro – UTMA", "Vigente ene–abr 2026"), ("Ruta por confirmar", "Norte – UTMA", "Vigente ene–abr 2026"), ("Ruta por confirmar", "Oriente – UTMA", "Vigente ene–abr 2026")])
    return page_head(r, "Conoce la UTMA", "Una universidad que creció de 120 a más de 1,500 estudiantes", "Rectoría, modelo educativo, misión y visión, calidad, prensa y cómo llegar.", crumbs(r, ("Conoce la UTMA", None)), "#81B4B8", "#EEF5F6",
      '<div class="mt-6 flex flex-wrap gap-2"><a class="chip" href="#rector">Rectoría</a><a class="chip" href="#modelo">Modelo educativo</a><a class="chip" href="#mision">Misión y visión</a><a class="chip" href="#calidad">Calidad</a><a class="chip" href="#como-llegar">Cómo llegar</a><a class="chip" href="#prensa">Prensa</a><a class="chip" href="#trabaja">Trabaja con nosotros</a></div>') + f'''
<section id="rector" class="sec scroll-mt-24"><div class="wrap grid items-center gap-10 lg:grid-cols-[.8fr_1.2fr]">
  <div class="media aspect-[4/5] max-w-sm rounded-3xl" style="--c:#235F83;--s:#E6F0F5" role="img" aria-label="Espacio para fotografía del Rector"></div>
  <div><p class="eyebrow">Mensaje del Rector</p><blockquote class="mt-4 font-display text-2xl font-bold leading-snug sm:text-3xl">El mensaje vigente del Rector se migra del sitio actual a esta sección.</blockquote><p class="mt-4 text-ink/70">Formato propuesto: cita breve destacada, foto y enlace al mensaje completo.</p></div>
</div></section>
<section id="modelo" class="sec bg-white scroll-mt-24"><div class="wrap grid gap-10 lg:grid-cols-2">
  <div><h2 class="sec-title">Modelo educativo</h2><div class="prose-u mt-4"><p>70% práctica y 30% teoría es la proporción de referencia del subsistema de Universidades Tecnológicas; validar con Académica la proporción de la UTMA.</p><p>Trayecto en dos niveles: Técnico Superior Universitario y continuidad a Ingeniería o Licenciatura, con estadías en empresa al final de cada nivel.</p><p>Modelo BIS: bilingüe, internacional y sostenible.</p></div></div>
  <div id="mision" class="scroll-mt-24 grid gap-4"><div class="card p-6"><h3 class="text-xl font-bold">Misión</h3><p class="mt-2 text-ink/70">Texto oficial a migrar desde «Misión y Visión» del sitio actual.</p></div><div class="card p-6"><h3 class="text-xl font-bold">Visión</h3><p class="mt-2 text-ink/70">Texto oficial a migrar desde «Misión y Visión» del sitio actual.</p></div>
  <div id="calidad" class="card scroll-mt-24 p-6"><h3 class="text-xl font-bold">Calidad</h3><p class="mt-2 text-ink/70">Certificaciones, acreditaciones y política de calidad vigentes (migrar de «Calidad»).</p></div></div>
</div></section>
<section id="como-llegar" class="sec scroll-mt-24"><div class="wrap grid gap-10 lg:grid-cols-2">
  <div><h2 class="sec-title">Cómo llegar</h2><p class="sec-lead">Av. Gerónimo de la Cueva S/N, Fracc. Villas del Río, C.P. 20126, Aguascalientes, Ags.</p>
    <dl class="mt-6 grid gap-3 sm:grid-cols-2"><div class="card p-4"><dt class="eyebrow">Teléfonos</dt><dd class="mt-1 font-bold tabular-nums">449 786 0951 · 449 786 0952</dd></div><div class="card p-4"><dt class="eyebrow">Horario de atención</dt><dd class="mt-1 font-bold">Por confirmar</dd></div></dl>
    <a class="btn-navy mt-6" target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query=Universidad+Tecnol%C3%B3gica+Metropolitana+de+Aguascalientes">{ic("pin")} Abrir en Google Maps</a></div>
  <div><h3 class="text-xl font-bold">Rutas de transporte</h3><div class="mt-4 overflow-x-auto rounded-2xl border border-ink/10 bg-white"><table class="tbl"><thead><tr><th>Ruta</th><th>Recorrido</th><th>Vigencia</th></tr></thead><tbody>{rutas}</tbody></table></div><p class="mt-2 text-sm text-ink/60">Capturar las rutas del banner «Rutas actualizadas ene–abr 2026» como texto.</p></div>
</div></section>
<section id="prensa" class="sec bg-white scroll-mt-24"><div class="wrap"><h2 class="sec-title">Sala de prensa</h2>
  <div class="mt-8 grid gap-4 md:grid-cols-3">
    <a href="#" data-demo="En el sitio real se reproduce el video institucional (YouTube)." class="card-hover overflow-hidden"><div class="media flex aspect-video items-center justify-center" style="--c:#173F57;--s:#E6F0F5"><span class="relative z-10 flex h-14 w-14 items-center justify-center rounded-full bg-white shadow-lg"><svg viewBox="0 0 24 24" class="ml-1 h-6 w-6" fill="#173F57" aria-hidden="true"><path d="M7 4v16l13-8z"/></svg></span></div><div class="p-5"><h3 class="font-bold">Video institucional</h3></div></a>
    <a href="#" data-demo="En el sitio real se reproducen los spots de radio." class="card-hover p-6"><h3 class="font-bold">Spots de radio</h3><p class="mt-2 text-sm text-ink/70">Campaña de admisión.</p></a>
    <a href="{r}noticias.html" class="card-hover p-6"><h3 class="font-bold">Noticias</h3><p class="mt-2 text-sm text-ink/70">Logros, convenios y vida universitaria.</p></a>
  </div></div></section>
<section id="trabaja" class="sec scroll-mt-24"><div class="wrap grid gap-10 lg:grid-cols-[1fr_1.4fr]">
  <div><h2 class="sec-title">Trabaja con nosotros</h2><p class="sec-lead">Vacantes para personal docente y administrativo.</p>
  <ul class="mt-6 space-y-2">{"".join(f'<li class="card flex items-center justify-between gap-3 p-4"><span><b>{a}</b><span class="block text-sm text-ink/60">{b}</span></span><span class="badge bg-paper text-ink/70">Ejemplo</span></li>' for a, b in [("Docente de inglés", "Asignatura"), ("Docente de Desarrollo de Software", "Tiempo completo"), ("Auxiliar de Servicios Escolares", "Administrativo")])}</ul></div>
  <form class="card grid gap-4 p-6 sm:grid-cols-2 sm:p-8" data-form="trabaja" novalidate>
    <div><label class="label" for="t-nom">Nombre</label><input class="input" id="t-nom" required></div><div><label class="label" for="t-mail">Correo</label><input class="input" id="t-mail" type="email" required></div>
    <div class="sm:col-span-2"><label class="label" for="t-area">Área de interés</label><select class="input" id="t-area" required><option value="">Elige</option><option>Docencia</option><option>Administración</option><option>Laboratorios y talleres</option></select></div>
    <div class="sm:col-span-2"><label class="label" for="t-cv">CV (PDF)</label><input class="input py-2.5" id="t-cv" type="file" accept="application/pdf"></div>
    <div class="sm:col-span-2"><button class="btn-primary">Enviar postulación</button></div><div data-ok hidden class="sm:col-span-2"></div></form>
</div></section>
'''

def p_noticias(r):
    cats = sorted(set(n["cat"] for n in NOTICIAS))
    chips = '<button class="chip" aria-pressed="true" data-cat="">Todas</button>' + "".join(f'<button class="chip" aria-pressed="false" data-cat="{c}">{c}</button>' for c in cats)
    return page_head(r, "Noticias", "Historias UTMA", "Logros de estudiantes, convenios, deportes y vida académica.", crumbs(r, ("Noticias", None))) + f'''
<section class="sec pt-10"><div class="wrap" data-news-filter>
  <div class="flex flex-wrap gap-2" role="group" aria-label="Filtrar por categoría">{chips}</div>
  <div class="mt-6">{news_card(r, NOTICIAS[8], True)}</div>
  <div class="mt-4 grid gap-4 md:grid-cols-2 lg:grid-cols-3" data-list>{"".join(news_card(r, n) for n in NOTICIAS if n is not NOTICIAS[8])}</div>
  <p data-empty hidden class="mt-6 rounded-xl bg-white p-6 text-center text-ink/70">No hay noticias en esta categoría.</p>
</div></section>'''

def p_noticia(n):
    def m(r):
        rel = [x for x in NOTICIAS if x["id"] != n["id"]][:3]
        return f'''<article><header class="border-b border-ink/10 bg-white"><div class="wrap max-w-4xl py-10 sm:py-14">
  {crumbs(r, ("Noticias", "noticias.html"), (n["titulo"][:40] + "…", None))}
  <p class="eyebrow mt-6">{E(n["cat"])} · {E(n["fecha"])}</p><h1 class="mt-3 font-display text-4xl font-extrabold leading-tight tracking-tight sm:text-5xl">{E(n["titulo"])}</h1>
  <p class="mt-4 text-xl text-ink/75">{E(n["resumen"])}</p></div></header>
<div class="wrap max-w-4xl py-10">
  <div class="media aspect-[16/9] rounded-3xl" style="--c:#235F83;--s:#E6F0F5" role="img" aria-label="Espacio para fotografía de la nota"></div>
  <div class="prose-u mt-8">{note("Resumen tomado del titular publicado en utma.edu.mx. En producción se migra el texto completo de la nota, sin «(copy)» en el título y con fotos con texto alternativo.")}
  <p>{E(n["resumen"])}</p><p>Formato propuesto para cada nota: un párrafo de entrada con qué, quién y cuándo; dos o tres párrafos de desarrollo; una cita de un estudiante o docente; y enlaces a la carrera o el programa relacionado.</p></div>
  <div class="mt-8 flex flex-wrap gap-3"><button class="btn-ghost btn-sm" data-share>Copiar enlace</button><a class="btn-ghost btn-sm" href="{r}noticias.html">Volver a noticias</a></div>
</div></article>
<section class="sec bg-white"><div class="wrap"><h2 class="sec-title">Más historias</h2><div class="mt-8 grid gap-4 md:grid-cols-3">{"".join(news_card(r, x) for x in rel)}</div></div></section>'''
    return m

def p_calendario(r):
    tipos = sorted(set(e["tipo"] for e in EVENTOS))
    return page_head(r, "Calendario", "Calendario UTMA", "Fechas escolares, admisiones, deportes y eventos. Agrega cualquier fecha a tu calendario.", crumbs(r, ("Calendario", None)), "#235F83", "#E6F0F5") + f'''
<section class="sec pt-10"><div class="wrap">{note("Fechas de ejemplo. En producción se alimenta del calendario escolar oficial (escolarizado y mixto).")}
<div class="mt-6" data-calendar data-types="{E(",".join(tipos))}"></div></div></section>'''

def portal(r, key, title, lead, tiles, extra=""):
    t = "".join(f'<a href="{u}" {a} class="card-hover flex flex-col gap-1 p-5 {"bg-ink text-white" if i==0 else ""}"><span class="font-display text-lg font-bold">{n}</span><span class="text-sm {"text-white/75" if i==0 else "text-ink/70"}">{d}</span></a>' for i, (n, d, u, a) in enumerate(tiles))
    return page_head(r, "Portal", title, lead, crumbs(r, (title, None))) + f'''
<section id="accesos" class="sec pt-10 scroll-mt-24"><div class="wrap"><h2 class="sec-title">Accesos rápidos</h2><div class="mt-6 grid grid-cols-2 gap-3 lg:grid-cols-4">{t}</div></div></section>{extra}'''

def asistente(r):
    return f'''<section id="tramites" class="sec bg-white scroll-mt-24"><div class="wrap"><h2 class="sec-title">¿Qué necesitas hacer?</h2><p class="sec-lead">Escribe con tus palabras: «seguro», «kárdex», «prácticas», «beca».</p>
<div class="mt-6 grid gap-6 lg:grid-cols-2" data-assistant>
  <div><label for="as-q" class="sr-only">Buscar trámite</label><div class="relative">{ic("search","absolute left-4 top-3.5 h-5 w-5 text-ink/50")}<input id="as-q" class="input pl-12" role="combobox" aria-expanded="true" aria-controls="as-list" aria-autocomplete="list" autocomplete="off" placeholder="Ej. seguro"></div>
  <ul id="as-list" role="listbox" class="mt-2 grid gap-1 rounded-2xl border border-ink/10 bg-white p-2"></ul></div>
  <div class="rounded-2xl bg-paper p-6" data-answer aria-live="polite"></div>
</div></div></section>'''

def p_alumnos(r):
    tiles = [("SAEKO", "Calificaciones y kárdex", "#", 'data-demo="En el sitio real se abre SAEKO."'), ("Calendario", "Escolarizado y mixto", f"{r}calendario.html", ""),
             ("Biblioteca digital", "Acceso con matrícula", "#", 'data-demo="En el sitio real se abre la Biblioteca Digital."'), ("IMSS", "Seguro facultativo", "#tramites", ""),
             ("Estadías", "Registro y reportes", f"{r}empresas.html#estadias", ""), ("Movilidad", "Quarks Abroad", f"{r}internacional.html#becas", ""),
             ("Bienestar", "Protocolos y apoyo", f"{r}vida-universitaria.html#bienestar", ""), ("Reglamentos", "Para alumnos", f"{r}transparencia.html?tipo=Normativa", "")]
    extra = asistente(r) + f'''<section class="sec"><div class="wrap grid gap-10 lg:grid-cols-[1fr_1.3fr]"><div><h2 class="sec-title">Próximas fechas</h2><a class="btn-navy mt-6" href="{r}calendario.html">Calendario completo</a></div><div data-events="5" data-types="Escolar,Internacional,Vinculación"></div></div></section>'''
    return portal(r, "alumnos", "Portal Alumnos", "Todo lo que usas cada cuatrimestre en una sola página.", tiles, extra)

def p_mixta(r):
    mix = [p for p in PROGRAMAS if "mix" in p["mods"]]
    return page_head(r, "Modalidad mixta", "Estudias y trabajas", "Sesiones presenciales reducidas, plataforma en línea y el mismo título. Pensado para adultos que trabajan.", crumbs(r, ("Estudias y trabajas", None)), "#00785F", "#E3F5EF",
       f'<div class="mt-6 flex flex-wrap gap-3"><a class="btn-primary" href="{r}admisiones.html#solicitud">Solicita tu examen</a><a href="#" data-demo="En el sitio real se abre la plataforma de educación mixta." class="btn-ghost">Entrar a la plataforma</a></div>') + f'''
<section class="sec pt-10"><div class="wrap"><h2 class="sec-title">Cómo funciona</h2><div class="mt-8 grid gap-4 md:grid-cols-3">
  {"".join(f'<article class="card p-6"><h3 class="text-xl font-bold">{t}</h3><p class="mt-2 text-ink/75">{d}</p></article>' for t, d in [("Presencial reducido", "Sesiones en la UTMA en horario compatible con el trabajo (días por confirmar)."), ("Plataforma en línea", "Materiales, tareas y evaluaciones en la plataforma de educación mixta."), ("Mismo título", "TSU e Ingeniería o Licenciatura con la misma validez que la modalidad escolarizada.")])}
</div></div></section>
<section class="sec bg-white"><div class="wrap"><h2 class="sec-title">Carreras en modalidad mixta</h2><div class="mt-8 grid gap-4 md:grid-cols-3">{"".join(prog_card(r, p) for p in mix)}</div></div></section>
<section class="sec"><div class="wrap grid gap-10 lg:grid-cols-[1fr_1.3fr]"><div><h2 class="sec-title">Calendario mixto</h2><a class="btn-navy mt-6" href="{r}calendario.html">Ver calendario</a></div><div data-events="4" data-types="Escolar"></div></div></section>
''' + asesor_cta(r, "¿Trabajas y quieres estudiar?", "Un asesor te explica horarios, costos y cómo combinar tu trabajo con la carrera.")

def p_docentes(r):
    tiles = [("SAEKO", "Captura de calificaciones", "#", 'data-demo="En el sitio real se abre SAEKO para docentes."'), ("Biblioteca digital", "Recursos para clase", "#", 'data-demo="En el sitio real se abre la Biblioteca Digital."'),
             ("Calendario", "Fechas de evaluación", f"{r}calendario.html", ""), ("Reglamento académico", "Ingreso, promoción y permanencia", f"{r}transparencia.html?q=personal", ""),
             ("Plataforma mixta", "Cursos en línea", "#", 'data-demo="En el sitio real se abre la plataforma de educación mixta."'), ("Laboratorios", "Reglamento de laboratorios y talleres", f"{r}transparencia.html?q=laboratorios", ""),
             ("Código de Ética", "Y Código de Conducta", f"{r}transparencia.html?q=codigo", ""), ("Directorio", "Áreas y contactos", f"{r}contacto.html#directorio", "")]
    return portal(r, "docentes", "Docentes", "Accesos y documentos para el personal académico.", tiles)

def p_egresados(r):
    tiles = [("Bolsa de trabajo", "Vacantes por carrera", "#", 'data-demo="En el sitio real se abre la Bolsa de Trabajo."'), ("Continúa tu Ingeniería", "De TSU a Ingeniería o Licenciatura", f"{r}oferta-educativa.html", ""),
             ("Maestría", "Gestión Gubernamental", f"{r}carreras/maestria-en-gestion-gubernamental.html", ""), ("Titulación", "Requisitos y trámites", "#actualiza", ""),
             ("Educación continua", "Cursos", f"{r}empresas.html#cursos", ""), ("Oxford Test", "Certifica tu inglés", f"{r}internacional.html#bilingue", ""),
             ("Noticias", "Historias de egresados", f"{r}noticias.html", ""), ("Actualiza tus datos", "Seguimiento de egresados", "#actualiza", "")]
    extra = f'''<section id="actualiza" class="sec bg-white scroll-mt-24"><div class="wrap grid gap-10 lg:grid-cols-[1fr_1.4fr]"><div><h2 class="sec-title">Actualiza tus datos</h2><p class="sec-lead">Nos ayuda a medir empleabilidad y a enviarte vacantes.</p></div>
<form class="card grid gap-4 p-6 sm:grid-cols-2 sm:p-8" data-form="egresado" novalidate>
<div><label class="label" for="g-nom">Nombre</label><input class="input" id="g-nom" required></div><div><label class="label" for="g-mat">Matrícula</label><input class="input" id="g-mat" required></div>
<div><label class="label" for="g-mail">Correo</label><input class="input" id="g-mail" type="email" required></div><div><label class="label" for="g-car">Carrera</label><select class="input" id="g-car" required><option value="">Elige</option>{"".join(f"<option>{E(p['nombre'])}</option>" for p in PROGRAMAS if 'nva' not in p['mods'])}</select></div>
<div class="sm:col-span-2"><label class="label" for="g-emp">¿Dónde trabajas?</label><input class="input" id="g-emp"></div>
<div class="sm:col-span-2"><button class="btn-primary">Guardar</button></div><div data-ok hidden class="sm:col-span-2"></div></form></div></section>'''
    return portal(r, "egresados", "Egresados", "Bolsa de trabajo, continuidad de estudios y titulación.", tiles, extra)

def p_transparencia(r):
    return page_head(r, "Información pública", "Transparencia", "Normativa, información financiera, adquisiciones, control interno y archivo histórico en un solo buscador.", crumbs(r, ("Transparencia", None)), "#173F57", "#E6F0F5",
      '<div class="mt-6 flex flex-wrap gap-3"><a class="btn-ghost" target="_blank" rel="noopener" href="https://www.plataformadetransparencia.org.mx/">Solicitud de información (PNT)</a><a class="btn-ghost" href="aviso-de-privacidad.html">Avisos de privacidad</a></div>') + f'''
<section class="sec pt-10"><div class="wrap" data-docs>
  <div class="grid gap-3 lg:grid-cols-[1fr_auto]"><div><label for="d-q" class="label">Buscar documento</label><input id="d-q" class="input" placeholder="Ej. reglamento, estados financieros, 2024"></div>
  <div><label for="d-y" class="label">Año</label><select id="d-y" class="input"><option value="">Todos</option></select></div></div>
  <div class="mt-4 flex flex-wrap gap-2" data-types role="group" aria-label="Tipo de documento"></div>
  <p class="mt-4 text-sm text-ink/60" data-count aria-live="polite"></p>
  <ul class="mt-2 grid gap-2" data-list></ul>
</div></section>
<section id="normativa" class="sec bg-white scroll-mt-24"><div class="wrap grid gap-4 md:grid-cols-3">
  <a href="?tipo=Normativa#contenido" class="card-hover p-6"><h2 class="text-xl font-bold">Normativa</h2><p class="mt-2 text-sm text-ink/70">Ley de creación, reglamentos, códigos, protocolos y manuales.</p></a>
  <a id="scii" href="?tipo=Control%20interno#contenido" class="card-hover scroll-mt-24 p-6"><h2 class="text-xl font-bold">SCII y Contraloría Social</h2><p class="mt-2 text-sm text-ink/70">Sistema de Control Interno Institucional.</p></a>
  <a href="?tipo=Archivo%20hist%C3%B3rico#contenido" class="card-hover p-6"><h2 class="text-xl font-bold">Archivo histórico</h2><p class="mt-2 text-sm text-ink/70">MECASUT/MECASUP 2018, PID 2020–2025.</p></a>
</div></section>'''

def p_contacto(r):
    return page_head(r, "Contacto", "Estamos para ayudarte", "Teléfonos, directorio por área, buzón de sugerencias y ubicación.", crumbs(r, ("Contacto", None))) + f'''
<section class="sec pt-10"><div class="wrap grid gap-4 md:grid-cols-3">
  <div class="card p-6"><p class="eyebrow">Conmutador</p><p class="mt-2 font-display text-2xl font-bold tabular-nums">449 786 0951</p><p class="font-display text-2xl font-bold tabular-nums">449 786 0952</p><button class="link mt-3 text-sm" data-copy="449 786 0951">Copiar número</button></div>
  <div class="card p-6"><p class="eyebrow">Asesor de admisiones</p><p class="mt-2 text-ink/75">Respuesta por WhatsApp en horario de oficina.</p><a href="#" data-asesor class="btn-primary mt-4">{ic("chat")} WhatsApp</a></div>
  <div class="card p-6"><p class="eyebrow">Dirección</p><p class="mt-2 text-ink/75">Av. Gerónimo de la Cueva S/N, Fracc. Villas del Río, C.P. 20126, Aguascalientes, Ags.</p><a class="link mt-3 inline-block text-sm" href="{r}conoce-la-utma.html#como-llegar">Cómo llegar</a></div>
</div></section>
<section id="directorio" class="sec bg-white scroll-mt-24"><div class="wrap" data-dir><h2 class="sec-title">Directorio por área</h2><p class="sec-lead">Antes era un PDF; ahora se puede buscar.</p>
  <div class="mt-6 max-w-md"><label for="dir-q" class="sr-only">Buscar área o trámite</label><input id="dir-q" class="input" placeholder="Ej. becas, titulación, pagos"></div>
  <ul class="mt-6 grid gap-3 md:grid-cols-2 lg:grid-cols-3" data-list></ul><p data-empty hidden class="mt-4 text-ink/70">No encontramos esa área. Prueba con otra palabra.</p></div></section>
<section id="buzon" class="sec scroll-mt-24"><div class="wrap grid gap-10 lg:grid-cols-[1fr_1.4fr]">
  <div><h2 class="sec-title">Buzón de sugerencias</h2><p class="sec-lead">Quejas, sugerencias o reconocimientos. Recibes un folio de seguimiento. Puedes enviarlo de forma anónima.</p></div>
  <form class="card grid gap-4 p-6 sm:grid-cols-2 sm:p-8" data-form="buzon" novalidate>
    <div class="sm:col-span-2"><label class="label" for="b-tipo">Tipo</label><select class="input" id="b-tipo" required><option value="">Elige</option><option>Sugerencia</option><option>Queja</option><option>Reconocimiento</option><option>Avísame cuando abra Psicología</option></select></div>
    <div><label class="label" for="b-nom">Nombre (opcional)</label><input class="input" id="b-nom"></div><div><label class="label" for="b-mail">Correo (opcional)</label><input class="input" id="b-mail" type="email"></div>
    <div class="sm:col-span-2"><label class="label" for="b-msg">Mensaje</label><textarea class="input min-h-[140px] py-3" id="b-msg" required minlength="10"></textarea><p class="hint">Mínimo 10 caracteres.</p></div>
    <div class="sm:col-span-2"><button class="btn-primary">Enviar</button></div><div data-ok hidden class="sm:col-span-2"></div></form>
</div></section>'''

def p_privacidad(r):
    docs = [d for d in DOCUMENTOS if d[0] == "Privacidad"]
    return page_head(r, "Datos personales", "Avisos de privacidad", "Cómo usa la UTMA tus datos personales y cómo ejercer tus derechos de acceso, rectificación, cancelación y oposición (ARCO).", crumbs(r, ("Aviso de privacidad", None)), "#173F57") + f'''
<section class="sec pt-10"><div class="wrap grid gap-10 lg:grid-cols-[1.2fr_1fr]">
  <div class="prose-u"><h2>Avisos vigentes</h2><ul>{"".join(f'<li><a href="#" class="link" data-demo="En el sitio real se abre el PDF del aviso (por https).">{E(d[1])}</a></li>' for d in docs)}</ul>
  <h2>Derechos ARCO</h2><p>Puedes solicitar el acceso, rectificación, cancelación u oposición al tratamiento de tus datos ante la Unidad de Transparencia de la UTMA o mediante la Plataforma Nacional de Transparencia.</p></div>
  <div class="card h-fit p-6"><h2 class="text-xl font-bold">Unidad de Transparencia</h2><p class="mt-2 text-ink/70">Datos de contacto a confirmar.</p><a class="btn-ghost mt-4" href="{r}transparencia.html">Ir a Transparencia</a></div>
</div></section>'''

def p_mapa(r):
    groups = [("Estudia", [("Oferta educativa", "oferta-educativa.html"), ("Admisiones", "admisiones.html"), ("Estudias y trabajas", "estudia-y-trabaja.html")] + [(p["nombre"], f'carreras/{p["id"]}.html') for p in PROGRAMAS]),
              ("Comunidad", [("Portal Alumnos", "alumnos.html"), ("Docentes", "docentes.html"), ("Egresados", "egresados.html"), ("Vida universitaria", "vida-universitaria.html"), ("Calendario", "calendario.html")]),
              ("Institucional", [("Conoce la UTMA", "conoce-la-utma.html"), ("Internacional", "internacional.html"), ("Empresas", "empresas.html"), ("Noticias", "noticias.html"), ("Transparencia", "transparencia.html"), ("Contacto", "contacto.html"), ("Aviso de privacidad", "aviso-de-privacidad.html"), ("Buscar", "buscar.html"), ("English", "en.html")]),
              ("Noticias", [(n["titulo"], f'noticias/{n["id"]}.html') for n in NOTICIAS])]
    def col(g, items):
        lis = "".join('<li><a class="link font-normal" href="' + r + u + '">' + E(t) + '</a></li>' for t, u in items)
        return '<div><h2 class="text-xl font-bold">' + g + '</h2><ul class="mt-3 space-y-1.5">' + lis + '</ul></div>'
    cols = "".join(col(g, items) for g, items in groups)
    return page_head(r, "Mapa del sitio", "Todas las páginas", "Índice completo del prototipo.", crumbs(r, ("Mapa del sitio", None))) + f'<section class="sec pt-10"><div class="wrap grid gap-10 md:grid-cols-2 lg:grid-cols-4">{cols}</div></section>'

def p_buscar(r):
    return f'''<section class="border-b border-ink/10 bg-white"><div class="wrap py-10">{crumbs(r, ("Buscar", None))}
<h1 class="page-title mt-6">Buscar</h1>
<form class="mt-6 flex max-w-2xl flex-col gap-2 sm:flex-row" role="search" data-search-page><label for="bq" class="sr-only">Buscar</label><input id="bq" name="q" class="input" placeholder="Carreras, trámites, documentos…"><button class="btn-navy">Buscar</button></form></div></section>
<section class="sec pt-10"><div class="wrap max-w-4xl"><p class="text-ink/70" data-count aria-live="polite"></p><ul class="mt-4 grid gap-2" data-results></ul></div></section>'''

def p_en(r):
    return f'''<section class="border-b border-ink/10 bg-white"><div class="wrap grid gap-8 py-12 lg:grid-cols-[1.4fr_1fr] lg:items-end">
<div><nav class="crumbs" aria-label="Breadcrumb"><a href="{r}index.html" lang="es">Inicio (español)</a></nav><p class="eyebrow mt-6">English</p>
<h1 class="page-title mt-2">Technological University of Aguascalientes</h1>
<p class="sec-lead">UTMA is a public university in Aguascalientes, Mexico, with a bilingual, international and sustainable model (BIS). Students earn two degrees: Advanced Technician (TSU) and a Bachelor's in Engineering or another field.</p></div>
<div class="media hidden aspect-[4/3] rounded-3xl lg:block" style="--c:#35BAA4;--s:#E3F5EF" role="img" aria-label="Photo placeholder"></div></div></section>
<section class="sec"><div class="wrap grid gap-4 md:grid-cols-3">
<article class="card p-6"><h2 class="text-xl font-bold">Programs</h2><p class="mt-2 text-ink/75">16 programs in technology, engineering, construction, business and health, plus a Master's in Government Management.</p><a class="link mt-3 inline-block" href="{r}oferta-educativa.html" lang="es">See programs (Spanish)</a></article>
<article class="card p-6"><h2 class="text-xl font-bold">International students</h2><p class="mt-2 text-ink/75">Exchange and short stays through our international agreements. Contact the International Office.</p><a class="link mt-3 inline-block" href="{r}contacto.html#directorio" lang="es">Contact</a></article>
<article class="card p-6"><h2 class="text-xl font-bold">Oxford Test of English</h2><p class="mt-2 text-ink/75">UTMA is a test center for the Oxford Test of English.</p><a class="link mt-3 inline-block" href="{r}internacional.html#bilingue" lang="es">Learn more</a></article>
</div><div class="wrap mt-6">{note("Proposal: key pages are written in English by UTMA staff, replacing the automatic translator.")}</div></section>'''

# ------------------------------------------------------------------ índice de búsqueda y datos JS
def build_data():
    S = []
    for p in PROGRAMAS:
        S.append(dict(t=p["nombre"], s=AREAS[p["area"]]["nombre"] + " · " + " y ".join(MODALIDADES[m] for m in p["mods"]), k=p["clave"], u=f'carreras/{p["id"]}.html', y="carrera"))
    for t in TRAMITES:
        S.append(dict(t=t["t"], s=t["a"], k=t["k"], u=t["u"], y="trámite"))
    for name, u, k in PAGINAS:
        S.append(dict(t=name, s="Página", k=k, u=u, y="página"))
    for n in NOTICIAS:
        S.append(dict(t=n["titulo"], s="Noticia · " + n["cat"], k=n["cat"], u=f'noticias/{n["id"]}.html', y="noticia"))
    for d in DOCUMENTOS:
        S.append(dict(t=d[1], s=d[0], k=d[2] + " documento pdf", u=f'transparencia.html?q={d[1]}', y="documento"))
    data = dict(AREAS=AREAS, MODALIDADES=MODALIDADES, PROGRAMAS=[{k: p[k] for k in ("id", "nombre", "area", "mods", "nivel", "resumen", "clave")} for p in PROGRAMAS],
                EVENTOS=EVENTOS, DOCUMENTOS=[dict(tipo=a, t=b, y=c, s=d) for a, b, c, d in DOCUMENTOS], DIRECTORIO=[dict(a=a, d=b, c=c) for a, b, c in DIRECTORIO],
                TRAMITES=TRAMITES, SEARCH=S, NOTICIAS=[dict(id=n["id"], t=n["titulo"], cat=n["cat"]) for n in NOTICIAS],
                WHATSAPP="https://wa.me/524497860951")  # EJEMPLO: confirmar número oficial del asesor
    js = "/* Generado por herramientas/generar.py — no editar a mano */\nwindow.UTMA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n"
    open(os.path.join(BASE, "js", "datos.js"), "w", encoding="utf-8").write(js)

# ------------------------------------------------------------------ generar
def main():
    build_data()
    L = layout
    L("index.html", "Inicio", "Estudia TSU e Ingeniería o Licenciatura en la UTMA, Aguascalientes. Modalidad escolarizada y mixta, Modelo BIS bilingüe, internacional y sostenible.", p_inicio, "", "inicio")
    L("oferta-educativa.html", "Oferta educativa", "16 carreras de la UTMA en tecnología, ingeniería, construcción, negocios y salud. Filtra y compara.", p_oferta, "oferta", "oferta")
    for p in PROGRAMAS:
        L(f'carreras/{p["id"]}.html', p["nombre"], f'{p["nombre"]} en la UTMA, Aguascalientes. {p["resumen"]}', p_carrera(p), "oferta", "carrera")
    L("admisiones.html", "Admisiones", "Convocatoria, requisitos, costos, solicitud de examen y resultados de admisión de la UTMA.", p_admisiones, "admisiones", "admisiones")
    L("vida-universitaria.html", "Vida universitaria", "Deportes Quarks, E-Sports, cultura y bienestar en la UTMA.", p_vida, "vida", "vida")
    L("internacional.html", "Internacional", "Modelo BIS, Oxford Test of English, Quarks Abroad y becas internacionales.", p_internacional, "internacional", "internacional")
    L("empresas.html", "Empresas y vinculación", "Convenios, estadías, bolsa de trabajo y educación continua de la UTMA.", p_empresas, "empresas", "empresas")
    L("conoce-la-utma.html", "Conoce la UTMA", "Rectoría, modelo educativo, misión y visión, calidad, cómo llegar y trabaja con nosotros.", p_conoce, "conoce", "conoce")
    L("noticias.html", "Noticias", "Noticias y logros de la comunidad UTMA.", p_noticias, "conoce", "noticias")
    for n in NOTICIAS:
        L(f'noticias/{n["id"]}.html', n["titulo"], n["resumen"], p_noticia(n), "conoce", "noticia")
    L("calendario.html", "Calendario", "Calendario escolar y de eventos de la UTMA.", p_calendario, "", "calendario")
    L("alumnos.html", "Portal Alumnos", "Accesos y trámites para alumnos de la UTMA.", p_alumnos, "", "alumnos")
    L("estudia-y-trabaja.html", "Estudias y trabajas", "Modalidad mixta de la UTMA para personas que trabajan.", p_mixta, "oferta", "mixta")
    L("docentes.html", "Docentes", "Accesos y documentos para docentes de la UTMA.", p_docentes, "", "docentes")
    L("egresados.html", "Egresados", "Bolsa de trabajo, titulación y continuidad para egresados UTMA.", p_egresados, "", "egresados")
    L("transparencia.html", "Transparencia", "Normativa, información financiera, adquisiciones y archivo de la UTMA.", p_transparencia, "", "transparencia")
    L("contacto.html", "Contacto", "Teléfonos, directorio, buzón de sugerencias y ubicación de la UTMA.", p_contacto, "", "contacto")
    L("aviso-de-privacidad.html", "Aviso de privacidad", "Avisos de privacidad y derechos ARCO de la UTMA.", p_privacidad, "", "privacidad")
    L("mapa-del-sitio.html", "Mapa del sitio", "Todas las páginas del sitio de la UTMA.", p_mapa, "", "mapa")
    L("buscar.html", "Buscar", "Busca carreras, trámites y documentos en el sitio de la UTMA.", p_buscar, "", "buscar")
    L("en.html", "English", "UTMA in English: programs, international students and Oxford Test of English.", p_en, "", "en", lang="en")
    print("Páginas generadas en", BASE)

if __name__ == "__main__":
    main()
