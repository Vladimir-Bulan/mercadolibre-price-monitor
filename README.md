# 🛒 Monitor de Precios de MercadoLibre

Un sistema automatizado de seguimiento y análisis de precios de productos en MercadoLibre, desarrollado con Python y Jupyter Notebooks.

## 📋 Descripción

Este proyecto permite:
- 🔍 Buscar y rastrear productos de MercadoLibre
- 💾 Almacenar histórico de precios
- 📊 Visualizar evolución de precios en el tiempo
- 🔔 Detectar cambios significativos de precio
- 📈 Comparar precios entre vendedores
- 🤖 Automatizar el monitoreo diario

## 🚀 Características

- **Web Scraping inteligente**: Extrae información de productos (precio, título, vendedor, etc.)
- **Base de datos local**: SQLite para almacenar histórico
- **Visualizaciones interactivas**: Gráficos con Plotly y Matplotlib
- **Análisis estadístico**: Precio promedio, mínimo, máximo, tendencias
- **Notebooks documentados**: Paso a paso con explicaciones
- **Código modular**: Fácil de extender y mantener

## 📁 Estructura del Proyecto

```
mercadolibre-price-monitor/
│
├── notebooks/              # Jupyter Notebooks
│   ├── 01_setup_and_test.ipynb          # Configuración inicial
│   ├── 02_scraping_basics.ipynb         # Fundamentos de scraping
│   ├── 03_price_tracking.ipynb          # Sistema de tracking
│   └── 04_data_analysis.ipynb           # Análisis y visualizaciones
│
├── src/                    # Código fuente Python
│   ├── scraper.py         # Funciones de web scraping
│   ├── database.py        # Manejo de base de datos
│   ├── analyzer.py        # Análisis de datos
│   └── utils.py           # Utilidades generales
│
├── data/                   # Datos y base de datos
│   └── prices.db          # Base de datos SQLite
│
├── output/                 # Gráficos y reportes generados
│
├── docs/                   # Documentación adicional
│
├── requirements.txt        # Dependencias del proyecto
└── README.md              # Este archivo
```

## 🔧 Instalación

### Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Jupyter Notebook o JupyterLab

### Pasos de instalación

1. **Clonar o descargar el proyecto**
```bash
cd mercadolibre-price-monitor
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Iniciar Jupyter Notebook**
```bash
jupyter notebook
```

## 📚 Uso

### Opción 1: Notebooks interactivos (Recomendado para empezar)

Abre los notebooks en orden:

1. **01_setup_and_test.ipynb**: Verifica que todo funcione
2. **02_scraping_basics.ipynb**: Aprende los fundamentos
3. **03_price_tracking.ipynb**: Rastrea productos
4. **04_data_analysis.ipynb**: Analiza los datos

### Opción 2: Scripts Python

```python
from src.scraper import search_product, get_product_details
from src.database import save_price, get_price_history
from src.analyzer import plot_price_evolution

# Buscar un producto
products = search_product("notebook lenovo")

# Obtener detalles
details = get_product_details(products[0]['url'])

# Guardar precio
save_price(details)

# Ver histórico
history = get_price_history(details['id'])
plot_price_evolution(history)
```

## 📊 Ejemplos de Análisis

El proyecto incluye ejemplos de:
- Evolución de precios en el tiempo
- Comparación entre vendedores
- Detección de mejores ofertas
- Análisis estadístico de precios
- Predicción de tendencias

## ⚠️ Consideraciones Éticas y Legales

- Este proyecto es **exclusivamente educativo**
- Respeta los términos de servicio de MercadoLibre
- Implementa delays entre requests para no sobrecargar servidores
- No está diseñado para uso comercial masivo
- Usa los datos de forma responsable

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal
- **Jupyter Notebook**: Entorno interactivo
- **Requests + BeautifulSoup**: Web scraping
- **Pandas**: Manipulación de datos
- **SQLite**: Base de datos
- **Matplotlib/Plotly**: Visualizaciones
- **Seaborn**: Gráficos estadísticos

## 🔮 Mejoras Futuras

- [ ] Notificaciones por email/Telegram
- [ ] Dashboard web con Streamlit/Flask
- [ ] Machine Learning para predicción de precios
- [ ] Soporte para múltiples sitios (Amazon, etc.)
- [ ] API REST para consultar datos
- [ ] Comparador de precios históricos

## 📝 Licencia

Este proyecto es de código abierto para fines educativos.

## 👨‍💻 Autor

Proyecto desarrollado como ejemplo educativo de web scraping y análisis de datos con Python.

## 🤝 Contribuciones

Las sugerencias y mejoras son bienvenidas. Por favor, abre un issue o pull request.

---

⭐ Si te resulta útil este proyecto, no olvides darle una estrella!
