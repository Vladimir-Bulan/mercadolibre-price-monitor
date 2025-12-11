# 🚀 Guía de Inicio Rápido

Esta guía te ayudará a empezar con el Monitor de Precios en 5 minutos.

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (viene con Python)
- Jupyter Notebook o JupyterLab
- Conexión a internet

## 🔧 Instalación Rápida

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Instalar Jupyter (si no lo tienes)

```bash
pip install jupyter
```

## 🎯 Primeros Pasos

### Opción A: Usar Jupyter Notebooks (Recomendado)

1. **Iniciar Jupyter:**
   ```bash
   jupyter notebook
   ```

2. **Abrir los notebooks en orden:**
   - `01_setup_and_test.ipynb` - Configuración y prueba
   - `02_scraping_basics.ipynb` - Búsqueda de productos
   - `03_price_tracking.ipynb` - Seguimiento de precios
   - `04_data_analysis.ipynb` - Análisis y visualizaciones

3. **Ejecutar las celdas:**
   - Presiona `Shift + Enter` para ejecutar cada celda
   - Sigue las instrucciones en cada notebook

### Opción B: Usar Scripts de Python

```python
from src.scraper import search_product
from src.database import save_price
from src.analyzer import plot_price_evolution

# Buscar productos
products = search_product("notebook lenovo", limit=5)

# Guardar el primero
save_price(products[0])

# Ver evolución (después de tener varios registros)
# plot_price_evolution(history)
```

## 📝 Ejemplo Rápido

```python
# 1. Buscar un producto
from src import search_product, save_price

products = search_product("auriculares bluetooth")
print(f"Encontrados: {len(products)} productos")

# 2. Guardar el más barato
cheapest = min(products, key=lambda x: x['price'])
save_price(cheapest)
print(f"✓ Guardado: {cheapest['title']}")

# 3. Repetir esto diariamente para ver evolución
```

## 🤖 Automatización

Para monitorear precios automáticamente:

```bash
# Ejecutar el script de monitoreo
python monitor.py
```

Para programarlo diariamente:

**Linux/Mac (crontab):**
```bash
crontab -e
# Agregar esta línea para ejecutar a las 9 AM:
0 9 * * * cd /ruta/al/proyecto && python monitor.py
```

**Windows (Task Scheduler):**
1. Abrir "Programador de tareas"
2. Crear tarea básica
3. Configurar para ejecutar `python monitor.py` diariamente

## 🎨 Visualizaciones

Después de tener varios registros de precio:

```python
from src import get_price_history, PriceAnalyzer

# Obtener histórico
history = get_price_history('MLA-123456')

# Crear gráfico
analyzer = PriceAnalyzer(history)
analyzer.plot_price_evolution(interactive=True)
```

## 💡 Tips

1. **Ejecuta el monitoreo regularmente** (diario o cada 2 días)
2. **Empieza con pocos productos** (3-5) para familiarizarte
3. **Espera unos días** antes de hacer análisis complejos
4. **Revisa los notebooks** - están muy bien documentados

## ❓ Problemas Comunes

### "Module not found"
```bash
# Asegúrate de estar en el directorio correcto
cd mercadolibre-price-monitor
pip install -r requirements.txt
```

### "No se encontraron productos"
- Verifica tu conexión a internet
- Prueba con otros términos de búsqueda
- MercadoLibre puede haber cambiado su estructura

### "Database is locked"
- Cierra otros notebooks/scripts que usen la base de datos
- Reinicia Jupyter

## 🆘 Ayuda

Si tienes problemas:

1. Lee el README.md completo
2. Revisa los comentarios en el código
3. Verifica que todas las dependencias estén instaladas
4. Consulta los notebooks - tienen ejemplos detallados

## 📚 Siguiente Paso

**Ve al notebook 01_setup_and_test.ipynb** y empieza tu viaje! 🚀

---

¡Disfruta del proyecto!
