# 💡 Ejemplos de Uso

Este archivo contiene ejemplos prácticos de cómo usar el proyecto.

## 🔍 Ejemplo 1: Buscar y Guardar un Producto

```python
from src.scraper import search_product
from src.database import save_price
from src.utils import format_price

# Buscar notebooks
productos = search_product("notebook lenovo", limit=5)

# Mostrar resultados
for i, prod in enumerate(productos, 1):
    print(f"{i}. {prod['title']}")
    print(f"   Precio: {format_price(prod['price'])}")
    print()

# Guardar el más barato
mas_barato = min(productos, key=lambda x: x['price'])
save_price(mas_barato)
print(f"✓ Guardado: {mas_barato['title']}")
```

## 📊 Ejemplo 2: Ver Evolución de Precio

```python
from src.database import get_price_history
from src.analyzer import PriceAnalyzer

# Obtener histórico (usa el ID de un producto guardado)
historial = get_price_history('MLA-123456789')

if len(historial) >= 2:
    # Crear analizador
    analyzer = PriceAnalyzer(historial)
    
    # Ver estadísticas
    stats = analyzer.get_statistics()
    print(f"Precio actual: ${stats['precio_actual']:,.0f}")
    print(f"Precio mínimo: ${stats['precio_minimo']:,.0f}")
    print(f"Variación: {stats['variacion_porcentual']:.2f}%")
    
    # Crear gráfico
    analyzer.plot_price_evolution(interactive=True)
else:
    print("Necesitas más registros de precio")
```

## 🤖 Ejemplo 3: Monitoreo Diario

```python
from src.scraper import MercadoLibreScraper
from src.database import PriceDatabase
import time

def actualizar_todos_los_precios():
    scraper = MercadoLibreScraper()
    db = PriceDatabase("data/prices.db")
    
    productos = db.get_all_products()
    
    for producto in productos:
        print(f"Actualizando: {producto['title'][:50]}...")
        
        # Buscar producto
        resultados = scraper.search_products(producto['title'], limit=5)
        
        # Buscar el mismo producto por ID
        encontrado = None
        for res in resultados:
            if res['id'] == producto['id']:
                encontrado = res
                break
        
        if encontrado:
            db.save_price(encontrado)
            print(f"  ✓ Actualizado")
        else:
            print(f"  ✗ No encontrado")
        
        time.sleep(2)  # Delay respetuoso
    
    print("✓ Actualización completa")

# Ejecutar
actualizar_todos_los_precios()
```

## 🎯 Ejemplo 4: Detectar Mejores Ofertas

```python
from src.database import PriceDatabase
from src.analyzer import PriceAnalyzer

db = PriceDatabase("data/prices.db")
productos = db.get_all_products()

mejores_ofertas = []

for producto in productos:
    historial = db.get_price_history(producto['id'])
    
    if len(historial) >= 7:  # Necesitamos datos suficientes
        analyzer = PriceAnalyzer(historial)
        recomendacion = analyzer.detect_best_time_to_buy()
        
        mejores_ofertas.append({
            'titulo': producto['title'],
            'score': recomendacion['score'],
            'precio': recomendacion['current_price'],
            'mensaje': recomendacion['recommendation']
        })

# Ordenar por score
mejores_ofertas.sort(key=lambda x: x['score'], reverse=True)

# Mostrar top 3
print("🏆 TOP 3 MEJORES OFERTAS:\n")
for i, oferta in enumerate(mejores_ofertas[:3], 1):
    estrellas = "⭐" * oferta['score']
    print(f"{i}. {oferta['titulo'][:50]}")
    print(f"   {estrellas} ({oferta['score']}/5)")
    print(f"   ${oferta['precio']:,.0f}")
    print(f"   {oferta['mensaje']}")
    print()
```

## 📈 Ejemplo 5: Comparar Productos

```python
from src.database import PriceDatabase
from src.analyzer import compare_products

db = PriceDatabase("data/prices.db")
productos = db.get_all_products()

# Seleccionar primeros 3 productos para comparar
datos_comparacion = []

for producto in productos[:3]:
    historial = db.get_price_history(producto['id'])
    if len(historial) >= 2:
        datos_comparacion.append({
            'name': producto['title'][:40],
            'history': historial
        })

# Crear gráfico comparativo
if datos_comparacion:
    compare_products(datos_comparacion)
else:
    print("Necesitas más datos históricos")
```

## 🔔 Ejemplo 6: Sistema de Alertas

```python
from src.database import PriceDatabase
from src.utils import create_price_alert

db = PriceDatabase("data/prices.db")
productos = db.get_all_products()

# Configurar alertas
alertas = {
    'MLA-123456': 450000,  # ID del producto: precio objetivo
    'MLA-789012': 300000,
}

for producto in productos:
    if producto['id'] in alertas:
        historial = db.get_price_history(producto['id'])
        
        if historial:
            precio_actual = historial[-1]['price']
            precio_objetivo = alertas[producto['id']]
            
            mensaje = create_price_alert(
                precio_actual, 
                precio_objetivo, 
                producto['title']
            )
            print(mensaje)
```

## 📊 Ejemplo 7: Generar Reporte

```python
from src.database import PriceDatabase
from src.utils import generate_report, save_report
from datetime import datetime

db = PriceDatabase("data/prices.db")

# Obtener últimos precios
ultimos_precios = db.get_latest_prices(limit=10)

# Generar reporte
reporte = generate_report(ultimos_precios)

# Mostrar
print(reporte)

# Guardar
fecha = datetime.now().strftime('%Y%m%d')
save_report(reporte, f"output/reporte_{fecha}.txt")
```

## 💾 Ejemplo 8: Exportar Datos

```python
from src.database import PriceDatabase
from src.utils import export_to_json
import pandas as pd

db = PriceDatabase("data/prices.db")

# Exportar productos a JSON
productos = db.get_all_products()
export_to_json(productos, "output/productos.json")

# Exportar a CSV
todos_los_precios = []
for producto in productos:
    historial = db.get_price_history(producto['id'])
    for registro in historial:
        todos_los_precios.append({
            'producto_id': producto['id'],
            'titulo': producto['title'],
            'precio': registro['price'],
            'fecha': registro['scraped_at']
        })

df = pd.DataFrame(todos_los_precios)
df.to_csv("output/precios.csv", index=False)
print(f"✓ Exportados {len(todos_los_precios)} registros")
```

## 🎨 Ejemplo 9: Dashboard Personalizado

```python
from src.database import PriceDatabase
from src.analyzer import PriceAnalyzer
import pandas as pd

db = PriceDatabase("data/prices.db")
productos = db.get_all_products()

# Crear resumen
resumen = []

for producto in productos:
    historial = db.get_price_history(producto['id'])
    
    if historial:
        analyzer = PriceAnalyzer(historial)
        stats = analyzer.get_statistics()
        
        resumen.append({
            'Producto': producto['title'][:40],
            'Actual': f"${stats['precio_actual']:,.0f}",
            'Mínimo': f"${stats['precio_minimo']:,.0f}",
            'Máximo': f"${stats['precio_maximo']:,.0f}",
            'Variación': f"{stats['variacion_porcentual']:.1f}%",
            'Registros': stats['total_registros']
        })

# Mostrar como tabla
df = pd.DataFrame(resumen)
print(df.to_string(index=False))
```

## 🔄 Ejemplo 10: Actualización Selectiva

```python
from src.scraper import MercadoLibreScraper
from src.database import PriceDatabase

def actualizar_producto(product_id):
    """Actualiza un producto específico por ID"""
    scraper = MercadoLibreScraper()
    db = PriceDatabase("data/prices.db")
    
    # Obtener info del producto
    productos = db.get_all_products()
    producto = next((p for p in productos if p['id'] == product_id), None)
    
    if not producto:
        print(f"Producto {product_id} no encontrado")
        return False
    
    print(f"Actualizando: {producto['title'][:50]}...")
    
    # Buscar
    resultados = scraper.search_products(producto['title'], limit=5)
    encontrado = next((r for r in resultados if r['id'] == product_id), None)
    
    if encontrado:
        db.save_price(encontrado)
        print(f"✓ Actualizado: ${encontrado['price']:,.0f}")
        return True
    else:
        print("✗ No encontrado en la búsqueda")
        return False

# Usar
actualizar_producto('MLA-123456789')
```

---

## 💡 Tips de Uso

1. **Ejecuta los notebooks primero** - están muy bien documentados
2. **Empieza simple** - busca 3-5 productos al principio
3. **Espera unos días** antes de hacer análisis complejos
4. **Automatiza** - programa el script de monitoreo diariamente
5. **Experimenta** - prueba diferentes productos y análisis

## 📚 Más Recursos

- Ver notebooks para ejemplos interactivos
- Leer docstrings en el código fuente
- Consultar README.md para info general
- QUICKSTART.md para inicio rápido

---

¡Disfruta explorando los datos! 🚀
