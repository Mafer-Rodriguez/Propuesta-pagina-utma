/* UTMA · interacciones del sitio (sin dependencias).
   Cada módulo se activa sólo si su elemento existe en la página. */
(function () {
  'use strict';
  const D = window.UTMA;
  const ROOT = document.body.dataset.root || '';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const norm = s => String(s).normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();
  const params = new URLSearchParams(location.search);
  const store = {
    get(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* almacenamiento no disponible */ } }
  };
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const parseD = s => { const [y, m, d] = s.split('-').map(Number); return new Date(y, m - 1, d); };
  const MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
  const fmt = s => { const d = parseD(s); return `${d.getDate()} de ${MESES[d.getMonth()]} de ${d.getFullYear()}`; };
  const AREA_TXT = k => (k === 'ti' || k === 'sal') ? D.AREAS[k].color : '#1D191A';

  /* ---------------- aviso (toast) ---------------- */
  const toastEl = $('#toast'); let toastT;
  function toast(msg) { if (!toastEl) return; toastEl.textContent = msg; toastEl.dataset.open = 'true'; clearTimeout(toastT); toastT = setTimeout(() => toastEl.dataset.open = 'false', 3800); }
  document.addEventListener('click', e => {
    const d = e.target.closest('[data-demo]'); if (d) { e.preventDefault(); toast(d.dataset.demo); return; }
    const a = e.target.closest('[data-asesor]'); if (a) { e.preventDefault(); window.open(D.WHATSAPP, '_blank', 'noopener'); toast('Abriendo WhatsApp del asesor. Número de ejemplo: confirmar el oficial.'); return; }
    const c = e.target.closest('[data-copy]'); if (c) { navigator.clipboard?.writeText(c.dataset.copy).then(() => toast('Número copiado.'), () => toast(c.dataset.copy)); return; }
    const s = e.target.closest('[data-share]'); if (s) { navigator.clipboard?.writeText(location.href).then(() => toast('Enlace copiado.'), () => toast(location.href)); }
  });

  /* ---------------- header: mega menú ---------------- */
  const navBtns = $$('.nav-btn');
  const closeMega = () => navBtns.forEach(b => { b.setAttribute('aria-expanded', 'false'); $('#' + b.getAttribute('aria-controls')).dataset.open = 'false'; });
  navBtns.forEach(b => b.addEventListener('click', e => {
    e.stopPropagation(); const open = b.getAttribute('aria-expanded') === 'true'; closeMega();
    if (!open) { b.setAttribute('aria-expanded', 'true'); $('#' + b.getAttribute('aria-controls')).dataset.open = 'true'; }
  }));
  document.addEventListener('click', e => { if (!e.target.closest('#mainnav')) closeMega(); });

  /* ---------------- header: menú móvil ---------------- */
  const drawer = $('#drawer'), scrim = $('#scrim'), mBtn = $('#openMenu');
  function openDrawer() { drawer.dataset.open = 'true'; scrim.style.opacity = 1; scrim.style.pointerEvents = 'auto'; mBtn.setAttribute('aria-expanded', 'true'); document.body.style.overflow = 'hidden'; $('#closeMenu').focus(); }
  function closeDrawer() { if (drawer.dataset.open !== 'true') return; drawer.dataset.open = 'false'; scrim.style.opacity = 0; scrim.style.pointerEvents = 'none'; mBtn.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; mBtn.focus(); }
  if (mBtn) { mBtn.onclick = openDrawer; $('#closeMenu').onclick = closeDrawer; scrim.onclick = closeDrawer; }

  /* ---------------- búsqueda ---------------- */
  const TYPE_CLS = { carrera: 'bg-navy-soft text-navy', 'trámite': 'bg-naranja-soft text-naranja-text', 'página': 'bg-ut-soft text-ut', noticia: 'bg-[#FDECF0] text-carmin', documento: 'bg-paper text-ink/70' };
  function search(q, scope, limit = 8) {
    const n = norm(q.trim()); if (!n) return [];
    const words = n.split(/\s+/);
    return D.SEARCH.filter(x => (scope !== 'programas' || x.y === 'carrera'))
      .map(x => { const hay = norm(x.t + ' ' + x.s + ' ' + x.k); const title = norm(x.t); let sc = 0;
        for (const w of words) { if (!hay.includes(w)) return null; sc += title.startsWith(w) ? 3 : title.includes(w) ? 2 : 1; }
        return [sc + (x.y === 'carrera' ? .5 : 0) + (x.y === 'trámite' ? .3 : 0), x]; })
      .filter(Boolean).sort((a, b) => b[0] - a[0]).slice(0, limit).map(a => a[1]);
  }
  function hl(t, q) { const w = norm(q.trim()).split(/\s+/)[0]; const i = w ? norm(t).indexOf(w) : -1; if (i < 0) return esc(t); return esc(t.slice(0, i)) + '<mark class="rounded bg-sol/70 px-0.5 text-ink">' + esc(t.slice(i, i + w.length)) + '</mark>' + esc(t.slice(i + w.length)); }
  const go = x => { location.href = ROOT + x.u; };

  function combobox(input) {
    const list = $('#' + input.getAttribute('aria-controls')); const scope = input.dataset.combobox; const popup = input.hasAttribute('data-popup');
    let items = [], active = -1;
    const popular = ['Solicitar examen de admisión', 'Entrar a SAEKO (calificaciones y kárdex)', 'Calendario escolar', 'Alta en el IMSS (seguro facultativo)', 'Bolsa de trabajo'].map(t => D.SEARCH.find(x => x.t === t)).filter(Boolean);
    function render() {
      const q = input.value; items = q.trim() ? search(q, scope) : (popup ? [] : popular);
      if (q.trim() && !items.length) list.innerHTML = `<li class="px-3 py-3 text-ink/70">Sin resultados para «${esc(q)}». Prueba «examen», «SAEKO» o «becas».</li>`;
      else list.innerHTML = (!q.trim() && !popup ? '<li class="eyebrow px-3 pb-1 pt-2">Lo más buscado</li>' : '') + items.map((x, i) =>
        `<li id="${list.id}-${i}" role="option" aria-selected="${i === active}" data-i="${i}" class="flex cursor-pointer items-center justify-between gap-3 rounded-xl px-3 py-2.5 ${i === active ? 'bg-paper' : ''} hover:bg-paper"><span class="min-w-0"><span class="block font-bold">${hl(x.t, q)}</span><span class="block text-xs text-ink/60">${esc(x.s)}</span></span><span class="badge shrink-0 ${TYPE_CLS[x.y] || ''}">${x.y}</span></li>`).join('') +
        (q.trim() && items.length ? `<li><a class="block rounded-xl px-3 py-2.5 text-sm font-bold text-navy hover:bg-paper" href="${ROOT}buscar.html?q=${encodeURIComponent(q)}">Ver todos los resultados de «${esc(q)}»</a></li>` : '');
      const open = popup ? !!q.trim() : true; input.setAttribute('aria-expanded', open);
      if (popup) list.dataset.open = open;
      input.setAttribute('aria-activedescendant', active >= 0 ? `${list.id}-${active}` : '');
    }
    input.addEventListener('input', () => { active = -1; render(); });
    input.addEventListener('keydown', e => {
      if (e.key === 'ArrowDown') { e.preventDefault(); active = Math.min(active + 1, items.length - 1); render(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); active = Math.max(active - 1, 0); render(); }
      else if (e.key === 'Enter') { if (items[active]) { e.preventDefault(); go(items[active]); } else if (popup && items[0]) { e.preventDefault(); go(items[0]); } }
      else if (e.key === 'Escape' && popup) { list.dataset.open = 'false'; input.setAttribute('aria-expanded', 'false'); }
    });
    list.addEventListener('mousedown', e => { const li = e.target.closest('[data-i]'); if (li) { e.preventDefault(); go(items[+li.dataset.i]); } });
    if (popup) document.addEventListener('click', e => { if (!input.closest('.relative').contains(e.target)) { list.dataset.open = 'false'; input.setAttribute('aria-expanded', 'false'); } });
    render();
  }
  $$('[data-combobox]').forEach(combobox);

  const dlg = $('#searchDlg'), gq = $('#gq'); let lastFocus = null;
  function openSearch() { lastFocus = document.activeElement; dlg.dataset.open = 'true'; setTimeout(() => gq.focus(), 20); }
  function closeSearch() { dlg.dataset.open = 'false'; lastFocus && lastFocus.focus(); }
  if (dlg) {
    $('#openSearch').onclick = openSearch;
    dlg.addEventListener('click', e => { if (e.target === dlg) closeSearch(); });
  }
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openSearch(); }
    if (e.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) { e.preventDefault(); openSearch(); }
    if (e.key === 'Escape') { if (dlg && dlg.dataset.open === 'true') closeSearch(); closeMega(); closeDrawer(); }
  });

  /* página de resultados */
  const sp = $('[data-search-page]');
  if (sp) {
    const q = params.get('q') || ''; $('#bq').value = q;
    const res = q.trim() ? search(q, 'todo', 60) : [];
    $('[data-count]').textContent = q.trim() ? `${res.length} resultado${res.length === 1 ? '' : 's'} para «${q}»` : 'Escribe qué buscas.';
    $('[data-results]').innerHTML = res.length ? res.map(x => `<li><a href="${ROOT}${esc(x.u)}" class="card-hover flex items-center justify-between gap-4 p-4"><span><span class="block font-bold">${hl(x.t, q)}</span><span class="text-sm text-ink/60">${esc(x.s)}</span></span><span class="badge ${TYPE_CLS[x.y] || ''}">${x.y}</span></a></li>`).join('')
      : (q.trim() ? `<li class="card p-6 text-ink/75">No encontramos «${esc(q)}». Revisa la ortografía, usa una palabra más general o <a class="link" href="#" data-asesor>pregunta a un asesor</a>.</li>` : '');
  }

  /* ---------------- rayos de identidad ---------------- */
  $$('[data-rays]').forEach(g => {
    const C = ['#FDC24E', '#F57E26', '#F2705A', '#B61F3E', '#235F83', '#81B4B8', '#35BAA4', '#00A884'];
    for (let i = 0; i < 16; i++) {
      const r = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      const len = 112 + (i % 3) * 20;
      Object.entries({ x: 44, y: -11, width: len, height: 22, rx: 11, fill: C[i % 8], opacity: .92, transform: `rotate(${i * 22.5})` }).forEach(([k, v]) => r.setAttribute(k, v));
      g.appendChild(r);
    }
  });

  /* ---------------- pestañas ---------------- */
  $$('[data-tabs]').forEach(w => {
    const tabs = $$('[role=tab]', w);
    const sel = t => tabs.forEach(x => { const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; $('#' + x.getAttribute('aria-controls')).hidden = !on; });
    tabs.forEach((t, i) => { t.onclick = () => sel(t); t.onkeydown = e => { const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (d) { const n = tabs[(i + d + tabs.length) % tabs.length]; sel(n); n.focus(); } }; });
  });

  /* ---------------- pasos de admisión ---------------- */
  $$('[data-steps]').forEach(ol => {
    let marked = false;
    $$('li', ol).forEach(li => {
      const a = parseD(li.dataset.desde), b = parseD(li.dataset.hasta), st = $('[data-state]', li), num = $('[data-num]', li);
      $('[data-range]', li).textContent = li.dataset.desde === li.dataset.hasta ? fmt(li.dataset.desde) : `${fmt(li.dataset.desde)} – ${fmt(li.dataset.hasta)}`;
      if (b < today) { st.textContent = 'Concluido'; st.className = 'badge bg-paper text-ink/60'; li.classList.add('opacity-70'); }
      else if (!marked) { marked = true; const now = a <= today; st.textContent = now ? 'Ahora' : 'Próximo'; st.className = 'badge ' + (now ? 'bg-ut text-white' : 'bg-naranja-soft text-naranja-text'); li.classList.add('ring-2', 'ring-ut'); num.className = 'flex h-9 w-9 items-center justify-center rounded-full bg-ut font-display font-bold text-white'; }
    });
  });

  /* ---------------- eventos próximos ---------------- */
  const evBtn = (e) => `<button type="button" class="btn-ghost btn-sm" data-ics="${esc(e.f)}|${esc(e.t)}|${esc(e.lugar)}" aria-label="Agregar «${esc(e.t)}» a mi calendario">${'+ Calendario'}</button>`;
  $$('[data-events]').forEach(w => {
    const n = +w.dataset.events, types = w.dataset.types ? w.dataset.types.split(',') : null;
    let ev = D.EVENTOS.filter(e => parseD(e.f) >= today && (!types || types.includes(e.tipo))).slice(0, n);
    if (!ev.length) ev = D.EVENTOS.slice(-n);
    w.innerHTML = '<ul class="grid gap-2">' + ev.map(e => { const d = parseD(e.f); return `<li class="card grid grid-cols-[60px_1fr_auto] items-center gap-3 p-3 sm:p-4"><span class="text-center font-display leading-none"><b class="block text-2xl tabular-nums">${d.getDate()}</b><span class="text-[11px] font-bold uppercase tracking-wider text-ink/60">${MESES[d.getMonth()].slice(0, 3)}</span></span><span class="min-w-0"><b class="block leading-snug">${esc(e.t)}</b><span class="text-sm text-ink/60">${esc(e.tipo)} · ${esc(e.lugar)}</span></span>${evBtn(e)}</li>`; }).join('') + '</ul><p class="mt-2 text-xs text-ink/50">Fechas de ejemplo.</p>';
  });
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-ics]'); if (!b) return;
    const [f, t, l] = b.dataset.ics.split('|'); const d = f.replace(/-/g, ''); const nd = parseD(f); nd.setDate(nd.getDate() + 1);
    const d2 = `${nd.getFullYear()}${String(nd.getMonth() + 1).padStart(2, '0')}${String(nd.getDate()).padStart(2, '0')}`;
    const ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//UTMA//Calendario//ES', 'BEGIN:VEVENT', `UID:${d}-${Date.now()}@utma.edu.mx`, `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, '').split('.')[0]}Z`, `DTSTART;VALUE=DATE:${d}`, `DTEND;VALUE=DATE:${d2}`, `SUMMARY:${t}`, `LOCATION:${l} · UTMA`, 'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([ics], { type: 'text/calendar' })); a.download = `utma-${d}.ics`; document.body.appendChild(a); a.click(); a.remove();
    toast('Descargamos el evento: ábrelo para agregarlo a tu calendario.');
  });

  /* ---------------- calendario mensual ---------------- */
  const cal = $('[data-calendar]');
  if (cal) {
    const types = cal.dataset.types.split(','); const TC = { Escolar: '#235F83', Admisiones: '#00785F', Deportes: '#F57E26', 'Vida universitaria': '#B61F3E', Internacional: '#35BAA4', 'Vinculación': '#81B4B8' };
    let on = new Set(types); let cur = new Date(today.getFullYear(), today.getMonth(), 1); let selDay = null;
    const first = D.EVENTOS.map(e => parseD(e.f)).find(d => d >= today); if (first) cur = new Date(first.getFullYear(), first.getMonth(), 1);
    cal.innerHTML = `<div class="flex flex-wrap items-center justify-between gap-3"><div class="flex items-center gap-2"><button class="btn-ghost btn-sm" data-m="-1" aria-label="Mes anterior">‹</button><h2 class="min-w-[12ch] text-center font-display text-2xl font-bold" data-title aria-live="polite"></h2><button class="btn-ghost btn-sm" data-m="1" aria-label="Mes siguiente">›</button><button class="btn-ghost btn-sm" data-m="0">Hoy</button></div>
      <div class="flex flex-wrap gap-2" data-f>${types.map(t => `<button class="chip" aria-pressed="true" data-t="${t}"><span class="dot" style="background:${TC[t] || '#999'}"></span>${t}</button>`).join('')}</div></div>
      <div class="mt-6 grid gap-6 lg:grid-cols-[1.5fr_1fr]"><div class="card overflow-hidden"><div class="grid grid-cols-7 border-b border-ink/10 bg-paper text-center text-xs font-bold uppercase tracking-wider text-ink/60">${['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'].map(d => `<div class="py-2">${d}</div>`).join('')}</div><div class="grid grid-cols-7" data-grid></div></div>
      <div><h3 class="font-display text-xl font-bold" data-lt></h3><ul class="mt-3 grid gap-2" data-l></ul></div></div>`;
    const draw = () => {
      $('[data-title]', cal).textContent = MESES[cur.getMonth()][0].toUpperCase() + MESES[cur.getMonth()].slice(1) + ' ' + cur.getFullYear();
      const ev = D.EVENTOS.filter(e => on.has(e.tipo)); const y = cur.getFullYear(), m = cur.getMonth();
      const start = (new Date(y, m, 1).getDay() + 6) % 7, days = new Date(y, m + 1, 0).getDate(); let h = '';
      for (let i = 0; i < start; i++) h += '<div class="min-h-[64px] border-b border-r border-ink/5 bg-paper/50 sm:min-h-[88px]"></div>';
      for (let d = 1; d <= days; d++) {
        const key = `${y}-${String(m + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`; const de = ev.filter(e => e.f === key);
        const isT = +parseD(key) === +today, isS = selDay === key;
        h += `<button class="relative flex min-h-[64px] flex-col items-start gap-1 border-b border-r border-ink/5 p-1.5 text-left hover:bg-navy-soft sm:min-h-[88px] sm:p-2 ${isS ? 'bg-navy-soft' : ''}" data-d="${key}" aria-label="${d} de ${MESES[m]}${de.length ? ', ' + de.length + ' evento(s)' : ''}"><span class="flex h-7 w-7 items-center justify-center rounded-full text-sm font-bold tabular-nums ${isT ? 'bg-ink text-white' : ''}">${d}</span>${de.map(e => `<span class="hidden w-full truncate rounded px-1.5 py-0.5 text-[11px] font-bold sm:block" style="background:${TC[e.tipo]}22;color:#1D191A;border-left:3px solid ${TC[e.tipo]}">${esc(e.t)}</span><span class="dot sm:hidden" style="background:${TC[e.tipo]}"></span>`).join('')}</button>`;
      }
      $('[data-grid]', cal).innerHTML = h;
      const list = selDay ? ev.filter(e => e.f === selDay) : ev.filter(e => { const d = parseD(e.f); return d.getMonth() === m && d.getFullYear() === y; });
      $('[data-lt]', cal).textContent = selDay ? fmt(selDay) : 'Eventos del mes';
      $('[data-l]', cal).innerHTML = list.length ? list.map(e => `<li class="card flex items-center justify-between gap-3 p-4" style="border-left:4px solid ${TC[e.tipo]}"><span><b class="block">${esc(e.t)}</b><span class="text-sm text-ink/60">${fmt(e.f)} · ${esc(e.lugar)}</span></span>${evBtn(e)}</li>`).join('') : '<li class="card p-4 text-ink/70">No hay eventos con estos filtros.</li>';
    };
    cal.addEventListener('click', e => {
      const mb = e.target.closest('[data-m]'); if (mb) { const v = +mb.dataset.m; cur = v ? new Date(cur.getFullYear(), cur.getMonth() + v, 1) : new Date(today.getFullYear(), today.getMonth(), 1); selDay = null; draw(); return; }
      const t = e.target.closest('[data-t]'); if (t) { const k = t.dataset.t; on.has(k) ? on.delete(k) : on.add(k); t.setAttribute('aria-pressed', on.has(k)); draw(); return; }
      const d = e.target.closest('[data-d]'); if (d) { selDay = selDay === d.dataset.d ? null : d.dataset.d; draw(); }
    });
    draw();
  }

  /* ---------------- explorador de oferta ---------------- */
  $$('[data-explorer]').forEach(w => {
    const full = w.dataset.explorer === 'full';
    let area = params.get('area') || '', mod = '', q = '', cmp = new Set(store.get('utma_cmp', []));
    const P = D.PROGRAMAS;
    w.innerHTML = `<div class="flex flex-wrap gap-2" data-a role="group" aria-label="Área">${[['', 'Todas', P.length], ...Object.entries(D.AREAS).map(([k, a]) => [k, a.nombre, P.filter(p => p.area === k).length])].map(([k, n, c]) => `<button class="chip" data-k="${k}" aria-pressed="${k === area}">${k ? `<span class="dot" style="background:${D.AREAS[k].color}"></span>` : ''}${n}<span class="text-xs font-normal opacity-70">${c}</span></button>`).join('')}</div>
      ${full ? `<div class="mt-3 flex flex-wrap items-center gap-2"><span class="eyebrow mr-1">Modalidad</span><div class="flex flex-wrap gap-2" data-mo role="group" aria-label="Modalidad">${[['', 'Todas'], ...Object.entries(D.MODALIDADES)].map(([k, n]) => `<button class="chip" data-k="${k}" aria-pressed="${k === ''}">${n}</button>`).join('')}</div>
        <div class="relative ml-auto w-full sm:w-72"><label for="ex-q" class="sr-only">Buscar carrera</label><input id="ex-q" class="input" placeholder="Buscar: robots, impuestos…"></div></div>` : ''}
      <p class="mt-4 text-sm text-ink/60" data-c aria-live="polite"></p>
      <div class="mt-3 grid gap-4 sm:grid-cols-2 lg:grid-cols-3" data-g></div>
      ${full ? `<div class="pointer-events-none fixed inset-x-0 bottom-0 z-30 p-4" data-tray hidden><div class="pointer-events-auto mx-auto flex max-w-3xl flex-wrap items-center justify-between gap-3 rounded-2xl bg-ink p-3 pl-5 text-white shadow-2xl"><span data-tl class="text-sm"></span><span class="flex gap-2"><button class="btn-sm btn bg-white/10 text-white hover:bg-white/20" data-clr>Limpiar</button><button class="btn-sm btn bg-white text-ink" data-cmp>Comparar</button></span></div></div>
        <dialog class="w-[min(96vw,980px)] rounded-2xl p-0 backdrop:bg-ink/50" data-dlg><div class="flex items-center justify-between border-b border-ink/10 p-5"><h2 class="font-display text-2xl font-bold">Comparar carreras</h2><button class="btn-ghost btn-sm" data-close>Cerrar</button></div><div class="overflow-x-auto p-5" data-tbl></div></dialog>` : ''}`;
    const draw = () => {
      let L = P.filter(p => (!area || p.area === area) && (!mod || p.mods.includes(mod)) && (!q || norm(p.nombre + ' ' + p.clave + ' ' + p.resumen + ' ' + D.AREAS[p.area].nombre).includes(norm(q))));
      if (!full) L = L.slice(0, 6);
      $('[data-c]', w).textContent = full ? `${L.length} de ${P.length} programas` : (area ? `${D.AREAS[area].nombre}` : 'Algunas opciones');
      $('[data-g]', w).innerHTML = L.length ? L.map(p => { const a = D.AREAS[p.area]; return `<article class="card-hover relative flex flex-col gap-2 overflow-hidden p-5"><span class="absolute inset-x-0 top-0 h-1.5" style="background:${a.color}"></span><span class="eyebrow">${a.nombre}</span>
        <h3 class="font-display text-lg font-bold leading-snug"><a class="after:absolute after:inset-0" href="${ROOT}carreras/${p.id}.html">${esc(p.nombre)}</a></h3><p class="text-sm text-ink/70">${esc(p.resumen)}</p>
        <div class="mt-auto flex flex-wrap items-center gap-1.5 pt-2">${p.mods.map(m => `<span class="badge border border-ink/10 bg-paper text-ink/80">${D.MODALIDADES[m]}</span>`).join('')}
        ${full && !p.mods.includes('nva') ? `<label class="relative z-10 ml-auto inline-flex cursor-pointer items-center gap-1.5 text-sm font-bold"><input type="checkbox" class="h-4 w-4 accent-[#00785F]" data-cb="${p.id}" ${cmp.has(p.id) ? 'checked' : ''}>Comparar</label>` : ''}</div></article>`; }).join('')
        : `<div class="card col-span-full p-8 text-center"><p class="font-bold">No hay carreras con esos filtros.</p><button class="btn-ghost btn-sm mt-3" data-reset>Quitar filtros</button></div>`;
      if (full) { const tr = $('[data-tray]', w); tr.hidden = !cmp.size; $('[data-tl]', w).textContent = `${cmp.size} de 3 seleccionadas`; $('[data-cmp]', w).disabled = cmp.size < 2; store.set('utma_cmp', [...cmp]); }
    };
    w.addEventListener('click', e => {
      const a = e.target.closest('[data-a] [data-k]'); if (a) { area = a.dataset.k; $$('[data-a] [data-k]', w).forEach(x => x.setAttribute('aria-pressed', x === a)); draw(); return; }
      const m = e.target.closest('[data-mo] [data-k]'); if (m) { mod = m.dataset.k; $$('[data-mo] [data-k]', w).forEach(x => x.setAttribute('aria-pressed', x === m)); draw(); return; }
      if (e.target.closest('[data-reset]')) { area = mod = q = ''; const i = $('#ex-q'); if (i) i.value = ''; $$('[data-k]', w).forEach(x => x.setAttribute('aria-pressed', x.dataset.k === '')); draw(); return; }
      if (e.target.closest('[data-clr]')) { cmp.clear(); draw(); return; }
      if (e.target.closest('[data-close]')) { $('[data-dlg]', w).close(); return; }
      if (e.target.closest('[data-cmp]')) {
        const S = [...cmp].map(id => P.find(p => p.id === id)).filter(Boolean);
        const rows = [['Área', p => D.AREAS[p.area].nombre], ['Modalidad', p => p.mods.map(m => D.MODALIDADES[m]).join(', ')], ['Título', p => (p.mods.includes('pos') ? '' : 'TSU + ') + p.nivel], ['De qué trata', p => p.resumen], ['', p => `<a class="link" href="${ROOT}carreras/${p.id}.html">Ver carrera</a>`]];
        $('[data-tbl]', w).innerHTML = `<table class="tbl min-w-[560px]"><thead><tr><th></th>${S.map(p => `<th class="normal-case tracking-normal text-ink"><span class="font-display text-base">${esc(p.nombre)}</span></th>`).join('')}</tr></thead><tbody>${rows.map(([l, f]) => `<tr><td class="font-bold">${l}</td>${S.map(p => `<td>${f(p)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
        $('[data-dlg]', w).showModal();
      }
    });
    w.addEventListener('change', e => { const c = e.target.closest('[data-cb]'); if (!c) return; if (c.checked) { if (cmp.size >= 3) { c.checked = false; toast('Puedes comparar hasta 3 carreras.'); return; } cmp.add(c.dataset.cb); } else cmp.delete(c.dataset.cb); draw(); });
    const qi = $('#ex-q', w); if (qi) qi.addEventListener('input', () => { q = qi.value.trim(); draw(); });
    draw();
    w.__setArea = k => { area = k; $$('[data-a] [data-k]', w).forEach(x => x.setAttribute('aria-pressed', x.dataset.k === k)); draw(); };
  });

  /* ---------------- test vocacional ---------------- */
  const quiz = $('[data-quiz]');
  if (quiz) {
    let i = 0, score = {};
    const qs = $$('[data-q]', quiz), res = $('[data-quiz-result]', quiz), prog = $('[data-quiz-progress]', quiz);
    const show = () => { qs.forEach((f, k) => f.hidden = k !== i); prog.textContent = i < qs.length ? `Pregunta ${i + 1} de ${qs.length}` : 'Resultado'; };
    quiz.addEventListener('click', e => {
      const b = e.target.closest('[data-a]'); if (b && i < qs.length) {
        score[b.dataset.a] = (score[b.dataset.a] || 0) + 1; i++;
        if (i === qs.length) {
          const k = Object.entries(score).sort((a, b) => b[1] - a[1])[0][0], A = D.AREAS[k]; const L = D.PROGRAMAS.filter(p => p.area === k && !p.mods.includes('nva'));
          qs.forEach(f => f.hidden = true); res.hidden = false;
          res.innerHTML = `<p class="eyebrow">Tu área sugerida</p><p class="mt-2 font-display text-3xl font-extrabold"><span class="dot mr-2 h-4 w-4 align-middle" style="background:${A.color}"></span>${A.nombre}</p><ul class="mt-4 grid gap-2">${L.map(p => `<li><a class="card-hover flex items-center justify-between p-4 font-bold" href="${ROOT}carreras/${p.id}.html">${esc(p.nombre)}<span aria-hidden="true">→</span></a></li>`).join('')}</ul><div class="mt-4 flex flex-wrap gap-2"><button class="btn-navy btn-sm" data-see="${k}">Filtrar el explorador</button><a href="#" data-asesor class="btn-ghost btn-sm">Hablar con un asesor</a></div>`;
        }
        show(); return;
      }
      const s = e.target.closest('[data-see]'); if (s) { const ex = $('[data-explorer="full"]'); ex.__setArea(s.dataset.see); ex.scrollIntoView({ behavior: 'smooth' }); }
      if (e.target.closest('[data-quiz-reset]')) { i = 0; score = {}; res.hidden = true; show(); }
    });
    show();
  }

  /* ---------------- validación de formularios ---------------- */
  const RULES = {
    curp: [v => /^[A-Z][AEIOUX][A-Z]{2}\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])[HMX](AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d]\d$/.test(v.toUpperCase()), 'La CURP debe tener 18 caracteres con el formato oficial (ej. GOAM050312HASRRR09).'],
    tel: [v => /^\d{10}$/.test(v.replace(/\D/g, '')), 'Escribe 10 dígitos, sin lada internacional.'],
    promedio: [v => { const n = parseFloat(v.replace(',', '.')); return n >= 6 && n <= 10; }, 'Escribe un promedio entre 6 y 10.']
  };
  function validate(el) {
    let msg = '';
    if (el.type === 'checkbox') { if (el.required && !el.checked) msg = 'Debes aceptar para continuar.'; }
    else {
      const v = el.value.trim();
      if (el.required && !v) msg = 'Este campo es obligatorio.';
      else if (v && el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) msg = 'Revisa el correo: debe verse como nombre@dominio.com.';
      else if (v && el.minLength > 0 && v.length < el.minLength) msg = `Escribe al menos ${el.minLength} caracteres.`;
      else if (v && el.dataset.rule && !RULES[el.dataset.rule][0](v)) msg = RULES[el.dataset.rule][1];
    }
    const id = el.id + '-err'; let er = document.getElementById(id);
    if (msg) { el.setAttribute('aria-invalid', 'true'); el.setAttribute('aria-describedby', id); if (!er) { er = document.createElement('p'); er.id = id; er.className = 'err'; (el.type === 'checkbox' ? el.closest('label') : el).insertAdjacentElement('afterend', er); } er.textContent = msg; }
    else { el.removeAttribute('aria-invalid'); if (er) er.remove(); }
    return !msg;
  }
  const fields = c => $$('input,select,textarea', c).filter(x => x.type !== 'file' && !x.closest('[hidden]'));
  function check(c) { const fs = fields(c); const ok = fs.map(validate).every(Boolean); if (!ok) fs.find(x => x.getAttribute('aria-invalid') === 'true')?.focus(); return ok; }
  document.addEventListener('blur', e => { if (e.target.matches?.('[aria-invalid="true"]')) validate(e.target); }, true);
  const folio = p => `${p}-${String(Date.now()).slice(-6)}`;

  $$('form[data-form]').forEach(f => f.addEventListener('submit', e => {
    e.preventDefault(); if (!check(f)) return;
    const ok = $('[data-ok]', f); const fo = folio({ buzon: 'BZ', empresa: 'VIN', visita: 'VIS', oxford: 'OX', trabaja: 'CH', egresado: 'EG' }[f.dataset.form] || 'UT');
    const msg = { buzon: 'Recibimos tu mensaje.', empresa: 'Vinculación te contactará en 2 días hábiles.', visita: 'Tu visita quedó reservada. Te enviaremos un recordatorio.', oxford: 'Quedaste pre-registrado. Te avisaremos la fecha de pago.', trabaja: 'Recibimos tu postulación.', egresado: 'Gracias, tus datos quedaron actualizados.' }[f.dataset.form] || 'Enviado.';
    $$('input,select,textarea,button', f).forEach(x => x.disabled = true);
    ok.hidden = false; ok.innerHTML = `<div class="step-panel flex gap-3 rounded-xl bg-ut-soft p-4 text-ink"><span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-ut font-bold text-white">✓</span><div><p class="font-bold">${msg}</p><p class="text-sm">Folio: <b class="tabular-nums">${fo}</b> · Prototipo: no se envió a ningún servidor.</p><button type="button" class="link mt-1 text-sm" data-again>Enviar otro</button></div></div>`;
    ok.querySelector('[data-again]').onclick = () => { f.reset(); $$('input,select,textarea,button', f).forEach(x => x.disabled = false); ok.hidden = true; };
    ok.querySelector('[data-again]').focus();
  }));

  /* ---------------- solicitud de examen (asistente por pasos) ---------------- */
  const wz = $('form[data-wizard]');
  if (wz) {
    const steps = $$('[data-step]', wz), dots = $$('[data-dot]', wz), next = $('[data-next]', wz), prev = $('[data-prev]', wz); let i = 0;
    wz.addEventListener('submit', e => e.preventDefault());
    const pre = params.get('carrera'); if (pre) { $('#s-carrera').value = pre; }
    const draft = store.get('utma_borrador', {}); Object.entries(draft).forEach(([k, v]) => { const el = wz.elements[k]; if (el && el.type !== 'checkbox' && !(k === 'carrera' && pre)) el.value = v; });
    wz.addEventListener('input', () => { const d = {}; [...wz.elements].forEach(el => { if (el.name && el.type !== 'checkbox') d[el.name] = el.value; }); store.set('utma_borrador', d); });
    const show = () => { steps.forEach((s, k) => s.hidden = k !== i); dots.forEach((d, k) => d.className = 'rounded-lg px-2 py-2 text-center ' + (k < i ? 'bg-ut-soft text-ut' : k === i ? 'bg-ink text-white' : 'bg-paper text-ink/60')); prev.hidden = i === 0; next.textContent = i === steps.length - 1 ? 'Enviar solicitud' : 'Continuar'; };
    prev.onclick = () => { i--; show(); };
    next.onclick = () => {
      if (!check(steps[i])) return;
      if (i < steps.length - 1) { i++; show(); steps[i].querySelector('input,select')?.focus(); return; }
      const all = store.get('utma_solicitudes', []); const fo = `UTMA-27-${String(all.length + 2).padStart(4, '0')}`;
      const data = Object.fromEntries([...wz.elements].filter(x => x.name).map(x => [x.name, x.type === 'checkbox' ? x.checked : x.value]));
      all.push({ folio: fo, fecha: new Date().toISOString(), ...data }); store.set('utma_solicitudes', all); store.set('utma_borrador', {});
      const p = D.PROGRAMAS.find(x => x.id === data.carrera);
      steps.forEach(s => s.hidden = true); $('[data-nav]', wz).hidden = true; dots.forEach(d => d.className = 'rounded-lg px-2 py-2 text-center bg-ut-soft text-ut');
      const done = $('[data-done]', wz); done.hidden = false;
      done.innerHTML = `<div class="flex items-start gap-3"><span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-ut text-lg font-bold text-white">✓</span><div><h3 class="font-display text-2xl font-bold">¡Listo, ${esc(data.nombre)}!</h3><p class="mt-1 text-ink/75">Recibimos tu solicitud para <b>${esc(p ? p.nombre : '')}</b>.</p></div></div>
        <div class="mt-5 rounded-xl bg-paper p-4"><p class="eyebrow">Tu folio</p><p class="mt-1 font-display text-3xl font-extrabold tabular-nums" tabindex="-1" data-f>${fo}</p><p class="mt-1 text-sm text-ink/60">Guárdalo: lo necesitas para consultar resultados.</p></div>
        <ol class="mt-5 grid gap-2 text-sm"><li>1. Te enviaremos a <b>${esc(data.email)}</b> la referencia de pago de ficha.</li><li>2. Al pagar, descarga tu pase al examen.</li><li>3. Presenta el examen en la fecha indicada en la convocatoria.</li></ol>
        <div class="mt-5 flex flex-wrap gap-2"><a class="btn-navy btn-sm" href="#resultados" data-fill="${fo}">Consultar este folio</a><button type="button" class="btn-ghost btn-sm" data-copy="${fo}">Copiar folio</button></div>
        <p class="mt-4 text-xs text-ink/50">Prototipo: la solicitud se guardó sólo en este navegador.</p>`;
      $('[data-f]', done).focus();
      $('[data-fill]', done).onclick = () => { $('#r-folio').value = fo; };
    };
    show();
  }

  /* ---------------- resultados ---------------- */
  const rf = $('form[data-results]');
  if (rf) rf.addEventListener('submit', e => {
    e.preventDefault(); const inp = $('#r-folio'); const out = $('[data-out]', rf); const v = inp.value.trim().toUpperCase();
    if (!v) { validate(inp); return; }
    const all = store.get('utma_solicitudes', []); const s = all.find(x => x.folio === v);
    if (v === 'UTMA-27-0001') out.innerHTML = `<div class="step-panel rounded-xl bg-ut-soft p-5"><p class="badge bg-ut text-white">Aceptado · ejemplo</p><p class="mt-3 font-display text-2xl font-bold">¡Felicidades! Fuiste aceptado en Desarrollo de Software.</p><p class="mt-2 text-ink/75">Sigue los pasos de inscripción antes de la fecha límite.</p><a class="btn-primary btn-sm mt-4" href="${ROOT}alumnos.html">Pasos de inscripción</a></div>`;
    else if (s) { const p = D.PROGRAMAS.find(x => x.id === s.carrera); out.innerHTML = `<div class="step-panel rounded-xl bg-navy-soft p-5"><p class="badge bg-navy text-white">Solicitud recibida</p><p class="mt-3 text-lg font-bold">${esc(s.nombre)} ${esc(s.apellidos)} · ${esc(p ? p.nombre : '')}</p><p class="mt-1 text-ink/75">Aún no hay resultados. Se publican según el calendario de la convocatoria.</p></div>`; }
    else out.innerHTML = `<div class="step-panel rounded-xl border-2 border-carmin/30 bg-[#FDECF0] p-5"><p class="font-bold text-carmin">No encontramos el folio ${esc(v)}.</p><p class="mt-1 text-ink/75">Revisa que esté completo (UTMA-27-0000). Si el problema sigue, <a href="#" data-asesor class="link">escribe a un asesor</a>.</p></div>`;
  });

  /* ---------------- asistente de trámites ---------------- */
  const as = $('[data-assistant]');
  if (as) {
    const inp = $('#as-q'), list = $('#as-list'), ans = $('[data-answer]', as); let act = 0, res = [];
    const draw = () => {
      const q = norm(inp.value.trim()); res = q ? D.TRAMITES.filter(t => norm(t.t + ' ' + t.k + ' ' + t.a).includes(q)) : D.TRAMITES.slice(0, 6); act = Math.min(act, Math.max(res.length - 1, 0));
      list.innerHTML = res.length ? res.map((t, i) => `<li role="option" id="as-${i}" data-i="${i}" aria-selected="${i === act}" class="cursor-pointer rounded-xl px-3 py-2.5 ${i === act ? 'bg-paper' : ''} hover:bg-paper"><b class="block">${hl(t.t, inp.value)}</b><span class="text-xs text-ink/60">${esc(t.a)}</span></li>`).join('') : `<li class="px-3 py-3 text-ink/70">No encontramos «${esc(inp.value)}». Prueba otra palabra o <a href="#" class="link" data-asesor>pregunta a un asesor</a>.</li>`;
      inp.setAttribute('aria-activedescendant', res.length ? 'as-' + act : '');
      const t = res[act]; ans.innerHTML = t ? `<p class="eyebrow">${esc(t.a)}</p><h3 class="mt-1 font-display text-2xl font-bold">${esc(t.t)}</h3><ol class="mt-4 grid gap-2">${t.p.map((s, k) => `<li class="flex gap-3"><span class="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-white text-sm font-bold">${k + 1}</span><span class="pt-0.5">${esc(s)}</span></li>`).join('')}</ol><div class="mt-5 flex flex-wrap gap-2"><a class="btn-primary btn-sm" href="${ROOT}${t.u}">Ir al trámite</a><a href="#" data-asesor class="btn-ghost btn-sm">Preguntar al asesor</a></div>` : '';
    };
    inp.addEventListener('input', () => { act = 0; draw(); });
    inp.addEventListener('keydown', e => { if (e.key === 'ArrowDown') { e.preventDefault(); act = Math.min(act + 1, res.length - 1); draw(); } if (e.key === 'ArrowUp') { e.preventDefault(); act = Math.max(act - 1, 0); draw(); } if (e.key === 'Enter' && res[act]) { e.preventDefault(); location.href = ROOT + res[act].u; } });
    list.addEventListener('click', e => { const li = e.target.closest('[data-i]'); if (li) { act = +li.dataset.i; draw(); } });
    draw();
  }

  /* ---------------- transparencia ---------------- */
  const docs = $('[data-docs]');
  if (docs) {
    const T = [...new Set(D.DOCUMENTOS.map(d => d.tipo))]; let tipo = params.get('tipo') || '';
    const qi = $('#d-q', docs), ys = $('#d-y', docs); qi.value = params.get('q') || '';
    [...new Set(D.DOCUMENTOS.map(d => d.y).filter(Boolean))].sort().reverse().forEach(y => ys.insertAdjacentHTML('beforeend', `<option>${y}</option>`));
    $('[data-types]', docs).innerHTML = [['', 'Todos'], ...T.map(t => [t, t])].map(([k, n]) => `<button class="chip" data-k="${k}" aria-pressed="${k === tipo}">${n} <span class="text-xs font-normal opacity-70">${k ? D.DOCUMENTOS.filter(d => d.tipo === k).length : D.DOCUMENTOS.length}</span></button>`).join('');
    const draw = () => {
      const q = norm(qi.value.trim()), y = ys.value;
      const L = D.DOCUMENTOS.filter(d => (!tipo || d.tipo === tipo) && (!y || d.y === y) && (!q || norm(d.t + ' ' + d.tipo + ' ' + d.y).includes(q)));
      $('[data-count]', docs).textContent = `${L.length} documento${L.length === 1 ? '' : 's'}`;
      $('[data-list]', docs).innerHTML = L.length ? L.map(d => `<li class="card flex items-center justify-between gap-4 p-4"><span class="flex min-w-0 items-start gap-3"><svg aria-hidden="true" class="mt-0.5 h-5 w-5 shrink-0 text-ink/50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5"/></svg><span class="min-w-0"><b class="block">${hl(d.t, qi.value)}</b><span class="text-sm text-ink/60">${esc(d.tipo)}${d.y ? ' · ' + d.y : ''} · PDF</span></span></span><a href="#" class="btn-ghost btn-sm shrink-0" data-demo="En el sitio real se abre «${esc(d.t)}» en PDF (por https).">Abrir</a></li>`).join('')
        : `<li class="card p-6 text-center text-ink/70">No hay documentos con esos filtros. <button class="link" data-reset>Quitar filtros</button></li>`;
    };
    docs.addEventListener('click', e => { const b = e.target.closest('[data-types] [data-k]'); if (b) { tipo = b.dataset.k; $$('[data-types] [data-k]', docs).forEach(x => x.setAttribute('aria-pressed', x === b)); draw(); } if (e.target.closest('[data-reset]')) { tipo = ''; qi.value = ''; ys.value = ''; $$('[data-types] [data-k]', docs).forEach(x => x.setAttribute('aria-pressed', x.dataset.k === '')); draw(); } });
    qi.addEventListener('input', draw); ys.addEventListener('change', draw); draw();
  }

  /* ---------------- directorio ---------------- */
  const dir = $('[data-dir]');
  if (dir) {
    const qi = $('#dir-q', dir);
    const draw = () => { const q = norm(qi.value.trim()); const L = D.DIRECTORIO.filter(d => !q || norm(d.a + ' ' + d.d).includes(q));
      $('[data-list]', dir).innerHTML = L.map(d => `<li class="card p-5"><b class="block font-display text-lg">${hl(d.a, qi.value)}</b><span class="mt-1 block text-sm text-ink/70">${esc(d.d)}</span><span class="mt-3 block text-sm font-bold tabular-nums">449 786 0951 · ${esc(d.c.split('·')[1] || '').trim()}</span></li>`).join(''); $('[data-empty]', dir).hidden = !!L.length; };
    qi.addEventListener('input', draw); draw();
  }

  /* ---------------- filtro de noticias ---------------- */
  const nf = $('[data-news-filter]');
  if (nf) nf.addEventListener('click', e => {
    const b = e.target.closest('[data-cat]:not(a)'); if (!b) return; const c = b.dataset.cat;
    $$('button[data-cat]', nf).forEach(x => x.setAttribute('aria-pressed', x === b));
    let n = 0; $$('[data-list] > a', nf).forEach(a => { const show = !c || a.dataset.cat === c; a.hidden = !show; n += show; });
    $('[data-empty]', nf).hidden = n > 0;
  });
})();
