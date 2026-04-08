# IMDb Top 250 Movies Scraper

## Integrantes del grupo

* David Conesa Muiña

---

## Estructura del repositorio

```
.
├── source/
│   └── scraper.py              # Script principal de scraping
├── dataset/
│   └── dataset_imdb.csv        # Dataset generado con las películas del Top 250
├── memoria/
│   └── memoria_practica1.pdf   # Memoria del trabajo
└── README.md
```

---

## Descripción del proyecto

Este proyecto realiza **web scraping del Top 250 de IMDb** para generar un dataset estructurado con información relevante de cada película.

El scraper:

1. Accede al ranking Top 250.
2. Descubre automáticamente los enlaces de cada película.
3. Navega a cada página individual.
4. Extrae los datos desde el **JSON-LD embebido** en la página (método robusto frente a cambios en el HTML).
5. Genera un dataset en formato CSV listo para análisis posterior.

Sitio web utilizado:
[https://www.imdb.com/chart/top/](https://www.imdb.com/chart/top/)

---

## Requisitos

* Python 3.10+
* Google Chrome instalado
* ChromeDriver compatible con tu versión de Chrome

Instalar dependencias:

```bash
pip install selenium
```

---

## Cómo ejecutar el scraper

Desde la carpeta `source`:

```bash
python scraper.py
```

El script:

* Abre un navegador Chrome automatizado
* Recorre las 250 películas del ranking
* Genera el archivo:

```
dataset_imdb.csv
```

---

## Funcionamiento del script

El proceso sigue estos pasos:

1. **Inicialización del driver** con un User-Agent realista.
2. **Descubrimiento automático de enlaces** de las películas del Top 250.
3. Para cada película:

   * Carga la página.
   * Extrae el bloque `<script type="application/ld+json">`.
   * Parsea el JSON y obtiene los datos estructurados.
4. Guarda el dataset en CSV.

Este enfoque evita depender de selectores HTML frágiles y es más resistente a cambios en el diseño de la web.

---

## Campos del dataset

Cada fila del dataset contiene:

* `title` — Título de la película
* `year` — Año de publicación
* `duration` — Duración
* `genres` — Géneros
* `rating` — Puntuación media
* `votes` — Número de votos
* `director` — Director(es)
* `stars` — Actores principales

---

## Parámetros modificables

En `scraper.py` puedes modificar fácilmente:

### Número de películas a scrapear

```python
for link in links[:250]:
```

Por ejemplo, para solo 50:

```python
for link in links[:50]:
```

### Tiempo de espera entre peticiones (uso responsable)

```python
time.sleep(2)
```

---

## Ejemplo reproducible

```bash
cd source
python scraper.py
```

Resultado esperado:

```
Encontradas 250 películas del Top 250
Scrapeado: The Shawshank Redemption
Scrapeado: The Godfather
...
Dataset guardado en dataset_imdb.csv
```

---

## Consideraciones éticas y técnicas

* Se respeta el `robots.txt` de IMDb.
* Se usa un retardo entre peticiones para no saturar el servidor.
* No se utilizan APIs, cumpliendo las condiciones de la práctica.
* Se emplea Selenium para interactuar con contenido dinámico.
* Se usa información estructurada pública (JSON-LD).

---

## Resultado

El resultado es un dataset estructurado y listo para análisis en R o Python, que será utilizado en la Práctica 2 para limpieza y visualización de datos.

## Zenodo link: https://doi.org/10.5281/zenodo.19476345
