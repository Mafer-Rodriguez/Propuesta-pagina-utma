# UTMA · Prototipo navegable del nuevo sitio

Prototipo de Frontend completo del rediseño de utma.edu.mx (Área de TI, noviembre 2026).
45 páginas enlazadas entre sí, con buscador, filtros, formularios y calendario funcionando.

## Cómo probarlo

**Abre `index.html` con doble clic.** No necesita instalar nada ni servidor.
El CSS ya está compilado (`css/styles.css`); no se usa el CDN de Tailwind.

Prueba esto:
- **Buscador global:** botón «Buscar» o `Ctrl + K` / `/`. Escribe «seguro», «robot», «reglamento».
- **Oferta educativa:** filtra por área y modalidad, marca 2–3 carreras y pulsa «Comparar». Haz el test vocacional.
- **Admisiones › Solicita tu examen:** llena los 3 pasos (CURP de prueba: `GOAM050312HASRRR09`).
  Recibes un folio; búscalo en «Consulta tus resultados». Folio de ejemplo «aceptado»: `UTMA-27-0001`.
- **Calendario:** cambia de mes, filtra por tipo y pulsa «+ Calendario» para descargar el evento (.ics).
- **Transparencia:** busca entre los 38 documentos por texto, tipo y año.
- **Portal Alumnos:** asistente de trámites con sinónimos.
- **Celular:** F12 → modo dispositivo, o reduce la ventana: menú lateral y botón de asesor fijo.

## Qué es real y qué es de ejemplo

| Funciona en el navegador | Se conecta en la fase de desarrollo |
|---|---|
| Navegación, buscador, filtros, comparador, test, calendario, validación de formularios, folios | Envío real de formularios (hoy se guardan sólo en el navegador con localStorage) |
| Todas las carreras, noticias, documentos y trámites del sitio actual | SAEKO, Biblioteca digital, plataforma mixta, PDFs (hoy muestran un aviso) |

Contenido marcado como **ejemplo** que debe validarse: fechas del calendario y de la convocatoria,
costos, materias del mapa curricular, perfil y campo laboral de cada carrera, rutas de transporte,
número de WhatsApp del asesor, misión/visión/mensaje del Rector (se migran del sitio actual) y fotografías
(los recuadros con rayos de color marcan dónde va cada foto).

## Estructura

```
index.html, admisiones.html, …   Páginas principales (19)
carreras/                        Una página por programa (16)
noticias/                        Una página por nota (10)
css/styles.css                   Tailwind compilado (no editar a mano)
js/app.js                        Todas las interacciones
js/datos.js                      Datos generados (carreras, eventos, documentos, búsqueda)
img/                             Logotipo
src/input.css                    Fuente del CSS: componentes UTMA (.btn, .card, .chip…)
tailwind.config.js               Colores y tipografías de marca
herramientas/datos.py            ← Aquí se edita el contenido (carreras, noticias, eventos…)
herramientas/generar.py          Genera todas las páginas a partir de datos.py
```

## Editar contenido y volver a generar

Requiere Python 3.9+ y Node.js 18+.

```bash
npm install          # una sola vez (instala tailwindcss 3.4.17)
npm run todo         # genera las páginas y compila el CSS
```

- Sólo cambiaste textos o datos: `python herramientas/generar.py` (y `npm run build` si agregaste clases nuevas).
- Editando estilos: `npm run dev` recompila el CSS automáticamente.

En producción, `datos.py` se sustituye por las colecciones del CMS elegido
(programas, noticias, eventos, documentos, directorio, avisos).
