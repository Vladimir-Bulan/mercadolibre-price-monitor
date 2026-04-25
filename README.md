# MercadoLibre Price Monitor Pro

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.52-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://selenium.dev/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)]()

Sistema profesional de **web scraping, persistencia y análisis de precios** para el marketplace MercadoLibre Argentina. Combina una capa de extracción de datos basada en Selenium con Brave Browser, persistencia dual (SQLite + Streamlit Session State), motor de análisis estadístico con Pandas/NumPy, y una interfaz web interactiva de múltiples páginas construida en Streamlit.

---

## Tabla de Contenidos

- [Arquitectura General](#arquitectura-general)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Stack Tecnológico](#stack-tecnológico)
- [Módulos del Sistema](#módulos-del-sistema)
  - [scraper.py / scraper\_brave.py](#scraperpy--scraper_bravepy)
  - [database.py](#databasepy)
  - [analyzer.py](#analyzerpy)
  - [utils.py](#utilspy)
  - [app.py](#apppy)
  - [config.py](#configpy)
- [Esquema de Base de Datos](#esquema-de-base-de-datos)
- [Flujo de Datos](#flujo-de-datos)
- [API Pública del Paquete src/](#api-pública-del-paquete-src)
- [Notebooks de Exploración](#notebooks-de-exploración)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación y Puesta en Marcha](#instalación-y-puesta-en-marcha)
- [Uso de la Aplicación Web](#uso-de-la-aplicación-web)
- [Configuración](#configuración)
- [Limitaciones Conocidas](#limitaciones-conocidas)
- [Autor](#autor)

---

## 🖼️ Screenshots

### Dashboard
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/7ac5ac93-be15-4bde-a835-1af0ba0750e2" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c73619ef-294d-4734-a7a4-fdc80093fc18" />



### Búsqueda
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/521a67d8-626d-4370-a828-1bbb9dfdcba7" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/634a113b-5712-479a-8f6c-91e676b8f890" />



### Analytics
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1da8bd96-ef07-4d28-851c-4bb19cada143" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/42be3220-9775-415b-bd18-6f3bb6048ac6" />

### Settings

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d197c412-62a4-4deb-b98d-51b14495a4e6" />





## Arquitectura General

El proyecto está organizado en dos capas diferenciadas con responsabilidades bien delimitadas:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CAPA DE PRESENTACIÓN                        │
│                         app.py  (Streamlit)                         │
│    Dashboard │ Search Products │ Analytics │ Settings               │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ import / function calls
┌──────────────────────────▼──────────────────────────────────────────┐
│                        CAPA DE DOMINIO  (src/)                      │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │  scraper.py │  │ database.py │  │ analyzer.py │  │ utils.py  │ │
│  │             │  │             │  │             │  │           │ │
│  │ Selenium +  │  │  SQLite +   │  │  Pandas +   │  │ Formateo  │ │
│  │ Brave/Chrome│  │ CRUD ops    │  │  Plotly +   │  │ Alertas   │ │
│  │ WebDriver   │  │ Alertas DB  │  │  Matplotlib │  │ Reportes  │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └─────┬─────┘ │
└─────────┼────────────────┼────────────────┼───────────────┼────────┘
          │                │                │               │
          ▼                ▼                │               │
   mercadolibre.com   data/prices.db        └───────────────┘
   (HTML scraping)    (SQLite file)           Composición interna
```

La aplicación Streamlit actúa como orquestador: delega el scraping al módulo `scraper`, la persistencia al módulo `database`, el análisis al módulo `analyzer`, y el formateo/utilidades al módulo `utils`. Adicionalmente, la app mantiene un estado de sesión volátil (`st.session_state`) que actúa como caché en memoria para la sesión activa del usuario, independiente de la base de datos SQLite.

---

## Estructura del Proyecto

```
mercadolibre-price-monitor/
│
├── app.py                      # Entrypoint de la aplicación Streamlit
├── scraper.py                  # Scraper principal (Brave Browser)
├── scraper_brave.py            # Variante alternativa del scraper
├── config.py                   # Constantes y parámetros globales de configuración
├── requirements.txt            # Dependencias pip del proyecto
│
├── src/                        # Paquete Python reutilizable (librería interna)
│   ├── __init__.py             # Exports públicos del paquete
│   ├── scraper.py              # Clase MercadoLibreScraper + helper search_product()
│   ├── database.py             # Clase PriceDatabase + helpers funcionales
│   ├── analyzer.py             # Clase PriceAnalyzer + funciones de visualización
│   └── utils.py                # Helpers de formateo, alertas, reportes, I/O
│
├── notebooks/                  # Notebooks Jupyter de exploración y aprendizaje
│   ├── 01_setup_and_test.ipynb # Verificación de dependencias y prueba de scraping
│   ├── 02_scraping_basics.ipynb# Búsqueda avanzada y almacenamiento en BD
│   ├── 03_price_tracking.ipynb # Seguimiento de precios y sistema de alertas
│   └── 04_data_analysis.ipynb  # Análisis estadístico, visualizaciones y reportes
│
├── data/
│   └── prices.db               # Base de datos SQLite (generada en runtime)
│
├── output/                     # Directorio de salida para gráficos y reportes
│   ├── price_evolution_*.png   # Gráficos estáticos exportados
│   ├── price_distribution_*.png
│   └── reporte_*.txt           # Reportes en texto plano generados por utils
│
└── .streamlit/
    └── config.toml             # Configuración del servidor Streamlit (tema, puerto, etc.)
```

---

## Stack Tecnológico

| Categoría | Tecnología | Versión | Propósito |
|-----------|-----------|---------|-----------|
| Lenguaje | Python | 3.13 | Runtime principal |
| Frontend/UI | Streamlit | 1.52 | Interfaz web multi-página |
| Web Scraping | Selenium WebDriver | 4.x | Automatización del navegador |
| Browser Engine | Brave Browser (Chromium) | Latest | Evasión de detección de bots |
| WebDriver Management | selenium (auto chromedriver) | 4.x | Gestión automática de drivers |
| Base de Datos | SQLite 3 | Built-in | Persistencia local sin servidor |
| Análisis de Datos | Pandas | Latest | Manipulación de DataFrames |
| Álgebra Numérica | NumPy | Latest | Cálculos estadísticos |
| Visualización Interactiva | Plotly | 5.x | Gráficos interactivos en Streamlit |
| Visualización Estática | Matplotlib + Seaborn | Latest | Exportación de gráficos a PNG |
| Parser HTML | BeautifulSoup4 + lxml | Latest | Fallback de parsing HTML |
| HTTP | Requests | Latest | Llamadas HTTP auxiliares |
| Serialización | json (stdlib) | Built-in | Exportación/importación de datos |

---

## Módulos del Sistema

### scraper.py / scraper_brave.py

**Responsabilidad:** Extracción de datos de producto directamente desde el DOM renderizado de MercadoLibre Argentina mediante automatización de navegador.

#### Clase `MercadoLibreScraper`

```python
class MercadoLibreScraper:
    def __init__(self, debug: bool = False, headless: bool = True)
    def _find_brave_path(self) -> Optional[str]
    def _init_driver(self) -> None
    def search_products(self, query: str, limit: int = 10) -> List[Dict]
    def _extract_product_info(self, element) -> Optional[Dict]
    def close(self) -> None
```

**Detalles de implementación:**

- **Detección de Brave:** `_find_brave_path()` itera sobre tres rutas canónicas de instalación de Brave en Windows (`Program Files`, `Program Files (x86)`, `AppData/Local`). Si ninguna existe, lanza una excepción descriptiva con instrucciones de alternativa.

- **Inicialización del WebDriver:** `_init_driver()` configura `ChromeOptions` con la ruta binaria de Brave. Añade flags críticos para evasión de detección de bots: `--disable-blink-features=AutomationControlled`, exclusión del switch `enable-automation`, y sobreescritura de la propiedad `navigator.webdriver` via JavaScript injection post-init.

- **Proceso de scraping en `search_products()`:**
  1. Construye la URL de búsqueda: `https://listado.mercadolibre.com.ar/{query-con-guiones}`
  2. Espera la presencia del selector CSS `li.ui-search-layout__item` con timeout de 20 segundos (WebDriverWait + EC)
  3. Agrega un `time.sleep(3)` adicional para rendering completo de contenido dinámico/lazy-loaded
  4. Itera sobre los elementos encontrados invocando `_extract_product_info()` por cada uno
  5. Filtra resultados con `price > 0` y respeta el `limit` solicitado

- **Estructura de producto extraído:**
  ```python
  {
      'id': str,           # ID extraído del atributo data del elemento o posición
      'title': str,        # Título del producto
      'price': float,      # Precio como float (ARS)
      'url': str,          # URL del listing
      'thumbnail': str,    # URL de la imagen miniatura
      'seller': str,       # Nombre del vendedor
      'free_shipping': bool, # Detección via texto "gratis"/"envío gratis"
      'scraped_at': str    # ISO 8601 timestamp del momento de extracción
  }
  ```

- **Singleton global:** La función helper `search_product()` mantiene una instancia global `_global_scraper` para reutilizar el WebDriver entre llamadas y evitar el overhead de inicialización repetida del navegador.

- **`scraper_brave.py`** es una variante estructuralmente idéntica con imports y lógica ligeramente refactorizados, provisto como alternativa modular.

---

### database.py

**Responsabilidad:** Capa de acceso a datos sobre SQLite. Gestiona la persistencia de productos, histórico de precios e índices de búsqueda.

#### Clase `PriceDatabase`

```python
class PriceDatabase:
    def __init__(self, db_path: str = "data/prices.db")
    def _create_tables(self) -> None
    def save_product(self, product: Dict) -> bool
    def save_price(self, product: Dict) -> bool
    def get_price_history(self, product_id: str) -> List[Dict]
    def get_all_products(self) -> List[Dict]
    def get_latest_prices(self, limit: int = 10) -> List[Dict]
    def get_stats(self) -> Dict
    def check_alerts(self, threshold_percent: float) -> List[Dict]
```

#### Esquema de Base de Datos

**Tabla `products`** — Catálogo maestro de productos únicos:
```sql
CREATE TABLE IF NOT EXISTS products (
    id         TEXT PRIMARY KEY,
    title      TEXT NOT NULL,
    link       TEXT,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Tabla `prices`** — Serie temporal de precios (append-only):
```sql
CREATE TABLE IF NOT EXISTS prices (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id    TEXT      NOT NULL,
    price         REAL      NOT NULL,
    seller        TEXT,
    free_shipping BOOLEAN,
    scraped_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

**Índices:**
```sql
CREATE INDEX IF NOT EXISTS idx_product_id ON prices(product_id);
CREATE INDEX IF NOT EXISTS idx_scraped_at  ON prices(scraped_at);
```

**Notas de diseño:**
- La tabla `products` usa `INSERT OR IGNORE` para garantizar idempotencia en upserts.
- Cada llamada a `save_price()` inserta un nuevo registro en `prices` preservando el histórico completo (modelo append-only, sin UPDATE).
- `conn.row_factory = sqlite3.Row` en queries de lectura permite acceso por nombre de columna.
- El directorio padre de `db_path` es creado automáticamente con `os.makedirs(..., exist_ok=True)`.
- `check_alerts()` compara el último precio con el penúltimo para cada producto y retorna aquellos cuya caída supere el umbral porcentual configurado.

**Funciones helper de módulo** (wrappers funcionales sobre `PriceDatabase`):
```python
def save_price(product: Dict, db_path: str = "data/prices.db") -> bool
def get_price_history(product_id: str, db_path: str = "data/prices.db") -> List[Dict]
def get_all_products(db_path: str = "data/prices.db") -> List[Dict]
```

---

### analyzer.py

**Responsabilidad:** Análisis estadístico del histórico de precios y generación de visualizaciones interactivas (Plotly) y estáticas (Matplotlib).

#### Clase `PriceAnalyzer`

```python
class PriceAnalyzer:
    def __init__(self, price_history: List[Dict])
    def get_statistics(self) -> Dict
    def _calculate_variation(self) -> float
    def plot_price_evolution(self, save_path: Optional[str] = None, interactive: bool = True)
    def _plot_plotly(self, save_path: Optional[str] = None)
    def _plot_matplotlib(self, save_path: Optional[str] = None)
    def get_buy_recommendation(self) -> Dict
```

**Estadísticas calculadas por `get_statistics()`:**
```python
{
    'precio_actual':         float,  # Último precio registrado
    'precio_minimo':         float,  # Mínimo histórico
    'precio_maximo':         float,  # Máximo histórico
    'precio_promedio':       float,  # Media aritmética
    'precio_mediana':        float,  # Mediana
    'desviacion_estandar':   float,  # Desviación estándar
    'variacion_porcentual':  float,  # ((last - first) / first) * 100
    'total_registros':       int,    # Número de snapshots
    'fecha_primer_registro': datetime,
    'fecha_ultimo_registro': datetime
}
```

**Visualización Plotly (`_plot_plotly()`):**
- Traza principal: `go.Scatter` con `mode='lines+markers'` para la serie temporal de precios.
- Línea horizontal discontinua verde: precio promedio histórico (con anotación).
- Línea horizontal discontinua roja: precio mínimo histórico (con anotación).
- Template: `plotly_white`. Layout con altura 600px y `hovermode='x unified'`.
- Si `save_path` termina en `.html`: exporta con `fig.write_html()`.

**Visualización Matplotlib (`_plot_matplotlib()`):**
- Usa estilo `seaborn-v0_8-darkgrid` y paleta `husl`.
- Genera gráfico estático exportable a PNG.

**Sistema de recomendación de compra (`get_buy_recommendation()`):**

| Condición | Score | Recomendación |
|-----------|-------|---------------|
| Precio actual ≤ precio mínimo | 5 | Comprar ahora. Precio en mínimo histórico |
| Precio actual ≤ promedio × 0.90 | 4 | Buen momento. Precio bajo el promedio |
| Precio actual ≤ promedio × 1.05 | 3 | Momento aceptable. Precio cerca del promedio |
| Precio actual ≤ promedio × 1.15 | 2 | Considera esperar. Precio sobre el promedio |
| Precio actual > promedio × 1.15 | 1 | Esperar. Precio muy alto vs. histórico |

**Funciones de módulo:**
```python
def plot_price_evolution(price_history: List[Dict], save_path=None, interactive=True)
def get_price_statistics(price_history: List[Dict]) -> Dict
def compare_products(products_data: List[Dict], save_path: Optional[str] = None)
```

`compare_products()` genera un gráfico Plotly multi-traza sobreponiendo las curvas de precio de múltiples productos en un único eje, con `hovermode='x unified'` para comparación temporal sincronizada.

---

### utils.py

**Responsabilidad:** Funciones auxiliares transversales: formateo, alertas, reportes, serialización I/O y helpers de presentación por consola.

```python
def format_price(price: float) -> str
# Formatea float como "$45.999" (separador de miles con punto, sin decimales)

def calculate_percentage_change(old_price: float, new_price: float) -> float
# ((new - old) / old) * 100 con guard para old == 0

def get_price_change_emoji(change_percent: float) -> str
# Retorna emoji + texto descriptivo según umbrales: <-10%, <-5%, <5%, <10%, ≥10%

def create_price_alert(current_price: float, threshold: float, product_title: str) -> str
# Genera mensaje de alerta formateado con ASCII art según si precio <= umbral o no

def generate_report(products: List[Dict]) -> str
# Genera reporte de texto plano con timestamp, total de productos y detalle por item

def save_report(content: str, filepath: str) -> None
# Escribe el reporte en archivo .txt creando directorios intermedios si faltan

def export_to_json(data: List[Dict], filepath: str) -> None
# Serializa lista de dicts a JSON con ensure_ascii=False, indent=2, default=str

def import_from_json(filepath: str) -> List[Dict]
# Deserializa JSON a lista de dicts con manejo de excepciones

def print_product_summary(product: Dict) -> None
# Imprime resumen formateado con ASCII box art por consola/notebook
```

---

### app.py

**Responsabilidad:** Entrypoint de la aplicación Streamlit. Orquesta todas las capas del sistema y expone cuatro vistas de usuario.

#### Session State

La app inicializa y mantiene tres claves en `st.session_state`:

| Clave | Tipo | Descripción |
|-------|------|-------------|
| `tracked_products` | `Dict[str, Dict]` | Mapa `product_id → {product, history}`. Historia simulada con 7 puntos iniciales al agregar un producto. |
| `search_results` | `List[Dict]` | Resultados del último scraping ejecutado. |
| `last_search_query` | `str` | Query de la última búsqueda para mostrar en UI. |

#### Funciones internas de gestión de estado

```python
def save_product_to_session(product: Dict) -> None
# Inicializa entrada en tracked_products con historial simulado de 7 puntos
# (variación aleatoria ±15% sobre precio actual, distribuida en los últimos 30 días)

def get_all_tracked_products() -> List[Dict]
# Extrae y retorna la lista de productos del session state

def get_price_history(product_id: str) -> List[Dict]
# Retorna el historial del producto o lista vacía

def check_price_alerts(threshold_percent: float = 15) -> List[Dict]
# Itera tracked_products, compara último precio vs. penúltimo
# Retorna lista de alertas para caídas ≥ threshold_percent
```

#### Páginas de la Aplicación

**Dashboard**
- Métricas resumidas: total de productos, precio promedio, alertas activas, estado del sistema.
- Panel de alertas de precio con caídas ≥ 15% destacadas en banner.
- Tabla filtrable y ordenable de productos trackeados (filtro por texto, orden por precio ascendente/descendente, nombre o reciente).
- Botón de redirección a Search Products cuando no hay datos.

**Search Products**
- Input de búsqueda + selector de cantidad de resultados (1–20).
- Invoca `scraper.search_products()` en un spinner.
- Muestra resultados en grid de 2 columnas con card por producto (imagen, título, precio, vendedor, envío gratis).
- Botón `+ Track` por producto que llama a `save_product_to_session()`.

**Analytics**
- Selector de producto (dropdown de trackeados).
- Gráfico Plotly interactivo de evolución de precio con las tres series: precio real, promedio y mínimo.
- Métricas estadísticas: precio actual, mínimo, máximo, promedio, variación porcentual.
- Sistema de recomendación de compra con rating de 5 estrellas.
- Exportación de datos a CSV y JSON via `st.download_button`.

**Settings**
- Toggle de alertas de precio con slider de umbral (5%–50%, step 5%).
- Botón de actualización masiva (re-scraping de todos los productos trackeados).
- Información del sistema: cantidad de productos, tipo de almacenamiento.
- Links a documentación y recursos.

---

### config.py

**Responsabilidad:** Centralización de todas las constantes y parámetros de configuración del sistema.

```python
DATABASE_PATH = "data/prices.db"

SCRAPING_CONFIG = {
    "delay_between_requests": 2,   # segundos entre requests
    "max_retries": 3,              # reintentos ante fallo
    "timeout": 10,                 # timeout HTTP en segundos
    "user_agent": "Mozilla/5.0 ..."# UA string para requests directos
}

ALERT_CONFIG = {
    "default_threshold": 10,       # % de cambio para disparar alerta
    "min_records_for_alert": 2,    # mínimo de registros para calcular
}

CHART_CONFIG = {
    "default_color":   "#3483FA",  # Azul corporativo MercadoLibre
    "secondary_color": "#FFE600",  # Amarillo corporativo MercadoLibre
    "success_color":   "#00A650",
    "warning_color":   "#F7B32B",
    "danger_color":    "#F23D4F"
}

LIMITS = {
    "max_search_results": 20,      # Máximo resultados por búsqueda
    "max_products_tracked": 100,   # Máximo productos en tracking
    "max_history_days": 365        # Días máximos de historial
}
```

---

## Flujo de Datos

```
Usuario ingresa query
        │
        ▼
app.py :: Search Products
        │
        ├──► MercadoLibreScraper.search_products(query, limit)
        │         │
        │         ├─ _init_driver()        → Brave + ChromeDriver
        │         ├─ driver.get(url)       → HTTP GET a MercadoLibre
        │         ├─ WebDriverWait(20s)    → Espera DOM cargado
        │         ├─ time.sleep(3)         → Buffer de rendering
        │         └─ _extract_product_info() × N → List[Dict]
        │
        ▼
st.session_state.search_results = results
        │
        │ Usuario clickea "+ Track"
        ▼
save_product_to_session(product)
        │
        ├─ Genera historial simulado (7 puntos, 30 días, ±15% variación)
        └─ st.session_state.tracked_products[id] = {product, history}
        │
        │ Usuario navega a Analytics
        ▼
PriceAnalyzer(history)
        │
        ├─ get_statistics()        → Pandas describe + custom calcs
        ├─ plot_price_evolution()  → Plotly Figure (3 series)
        └─ get_buy_recommendation()→ Score 1-5 + texto
```

---

## API Pública del Paquete `src/`

El paquete `src/` puede usarse de forma independiente como librería Python:

```python
from src import (
    MercadoLibreScraper,    # Clase principal de scraping
    search_product,          # Helper funcional de búsqueda
    PriceDatabase,           # Clase de acceso a datos
    save_price,              # Helper: guardar precio
    get_price_history,       # Helper: obtener historial
    PriceAnalyzer,           # Clase de análisis estadístico
    plot_price_evolution,    # Helper: graficar evolución
    get_price_statistics,    # Helper: obtener estadísticas
    format_price,            # Formateador de precios ARS
    print_product_summary    # Impresión de resumen por consola
)
```

**Ejemplo de uso completo (programático):**
```python
from src import search_product, PriceDatabase, PriceAnalyzer, format_price

# 1. Scraping
products = search_product("notebook gamer", limit=5)

# 2. Persistencia
db = PriceDatabase("data/prices.db")
for product in products:
    db.save_price(product)

# 3. Análisis
history = db.get_price_history(products[0]['id'])
analyzer = PriceAnalyzer(history)

stats = analyzer.get_statistics()
print(f"Precio actual: {format_price(stats['precio_actual'])}")
print(f"Variación: {stats['variacion_porcentual']:.2f}%")

recommendation = analyzer.get_buy_recommendation()
print(f"Recomendación ({recommendation['score']}/5): {recommendation['recommendation']}")

# 4. Visualización
analyzer.plot_price_evolution(save_path="output/evolucion.html", interactive=True)
```

---

## Notebooks de Exploración

El directorio `notebooks/` contiene cuatro Jupyter Notebooks diseñados como material didáctico progresivo:

| Notebook | Contenido |
|----------|-----------|
| `01_setup_and_test.ipynb` | Verificación de dependencias instaladas, primera búsqueda de prueba, inicialización de BD e inserción del primer producto. |
| `02_scraping_basics.ipynb` | Búsqueda con múltiples queries, extracción de campos específicos, filtrado por condiciones (precio, envío gratis), almacenamiento masivo. |
| `03_price_tracking.ipynb` | Actualización periódica de precios, visualización de cambios, sistema de alertas por umbral, automatización con `time.sleep()`. |
| `04_data_analysis.ipynb` | Visualización de evolución temporal, comparación multi-producto, análisis estadístico avanzado con NumPy, generación y exportación de reportes. |

Todos los notebooks usan `sys.path.append('../src')` para importar el paquete interno, y asumen ejecución desde el directorio `notebooks/`.

---

## Requisitos del Sistema

**Software:**
- Python 3.10+ (desarrollado y probado en 3.13)
- Brave Browser instalado en rutas estándar de Windows, **o** Google Chrome como alternativa
- Jupyter Notebook/Lab (opcional, solo para los notebooks)

**Hardware mínimo:**
- RAM: 2 GB (el WebDriver de Chromium en modo headless consume ~300–500 MB)
- Almacenamiento: 50 MB para la aplicación + espacio variable para `prices.db`
- Conexión a internet activa para el scraping

**Sistema Operativo:**
- Windows 10/11 (rutas de Brave hardcodeadas para Windows)
- Linux/macOS: requiere ajuste de `_find_brave_path()` con rutas del SO correspondiente

---

## Instalación y Puesta en Marcha

```bash
# 1. Clonar el repositorio
git clone https://github.com/Vladimir-Bulan/mercadolibre-price-monitor.git
cd mercadolibre-price-monitor

# 2. (Opcional) Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar instalación (opcional)
python -c "from scraper import MercadoLibreScraper; print('OK')"

# 5. Lanzar la aplicación web
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501` por defecto.

**Dependencias (`requirements.txt`):**
```
streamlit
pandas
plotly
requests
beautifulsoup4
lxml
selenium
numpy
matplotlib
seaborn
```

> **Nota:** `selenium` 4.x gestiona el ChromeDriver automáticamente via `selenium-manager`. No es necesario descargar ni configurar manualmente el driver.

---

## Uso de la Aplicación Web

### Flujo de trabajo recomendado

1. **Search Products** → Ingresar query (ej: `"notebook lenovo"`) → Definir cantidad de resultados → Click **Search**
2. En los resultados, hacer click en **+ Track** sobre los productos de interés
3. Navegar a **Analytics** → Seleccionar un producto → Explorar el gráfico interactivo y las estadísticas
4. Revisar el **Dashboard** periódicamente para detectar alertas de caída de precio
5. En **Settings** → **Bulk Update** para refrescar precios de todos los productos trackeados

### Exportación de datos

Desde la página **Analytics**, después de seleccionar un producto con historial suficiente:
- **Download CSV**: descarga el historial completo como `.csv` compatible con Excel/Sheets
- **Download JSON**: descarga el historial como `.json` para integración con otras herramientas

---

## Configuración

El comportamiento del sistema puede ajustarse editando `config.py`:

- **`SCRAPING_CONFIG["delay_between_requests"]`**: aumentar si MercadoLibre bloquea requests frecuentes
- **`ALERT_CONFIG["default_threshold"]`**: umbral porcentual de caída para disparar alertas (default: 10%)
- **`LIMITS["max_search_results"]`**: máximo de resultados por búsqueda (default: 20, máximo UI: 20)
- **`LIMITS["max_products_tracked"]`**: límite de productos en tracking simultáneo (default: 100)

El archivo `.streamlit/config.toml` controla el servidor Streamlit (puerto, tema, etc.).

---

## Limitaciones Conocidas

- **Volatilidad del scraper:** MercadoLibre puede modificar su estructura HTML sin previo aviso. Los selectores CSS (`li.ui-search-layout__item`) pueden dejar de funcionar y requerir actualización.
- **Detección de bots:** A pesar de las medidas de evasión implementadas (flags anti-detección, user-agent personalizado), scraping intensivo puede resultar en bloqueos temporales por IP.
- **Historial simulado:** Al agregar un producto al tracking en la app Streamlit, el historial inicial de 7 puntos es generado sintéticamente con variación aleatoria ±15%. Solo los precios obtenidos mediante actualizaciones reales (botón "Update All Products") son datos auténticos.
- **Session State volátil:** Los datos del `st.session_state` se pierden al cerrar o recargar la pestaña del navegador. Para persistencia real entre sesiones, usar el módulo `database.py` directamente o vía notebooks.
- **Rutas de Brave hardcodeadas para Windows:** En Linux o macOS, `_find_brave_path()` debe ser extendido con las rutas correspondientes (`/usr/bin/brave-browser`, `/Applications/Brave Browser.app/...`).
- **Sin paginación:** El scraper actualmente extrae solo la primera página de resultados de MercadoLibre.
- **Ausencia de rate limiting configurable en UI:** El delay entre requests está definido en `config.py` y no es ajustable desde la interfaz web.

---

## Autor

**Vladimir Bulan**
GitHub: [@Vladimir-Bulan](https://github.com/Vladimir-Bulan)

---

> Si este proyecto te resultó útil, considera dejar una ⭐ en el repositorio.
