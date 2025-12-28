# 🚀 Guía Rápida - Web App

## ¿Qué es esto?

Una interfaz web visual para el monitor de precios. Busca productos, ve gráficos interactivos y recibe alertas. Todo desde el navegador.

## Instalación Express

```bash
# 1. Instalar Streamlit (si no lo tienes)
pip install streamlit

# 2. Ejecutar la app
streamlit run app.py
```

Se abrirá automáticamente en tu navegador: `http://localhost:8501`

## Características

### 🏠 Dashboard
- Vista general de todos los productos
- Métricas de ahorro y ofertas
- Gráficos por producto

### 🔍 Buscar
- Busca cualquier producto de MercadoLibre
- Agrega productos al seguimiento con un click
- Ve resultados en tiempo real

### 📊 Análisis
- Gráficos interactivos de evolución de precio
- Estadísticas (min, max, promedio)
- Sistema de recomendación (1-5 ⭐)
- Exporta datos en CSV/JSON

### ⚙️ Configuración
- Alertas de precio personalizables
- Actualización masiva de productos
- Info del sistema

## Uso Típico

1. **Primera vez:**
   - Abre la app
   - Ve a "🔍 Buscar Productos"
   - Busca algo (ej: "notebook lenovo")
   - Agrega los productos que te interesen

2. **Seguimiento diario:**
   - Entra al Dashboard
   - Revisa las ofertas activas
   - Actualiza precios con un click
   - Ve gráficos de evolución

3. **Análisis profundo:**
   - Ve a "📊 Análisis"
   - Selecciona un producto
   - Revisa estadísticas y recomendaciones
   - Exporta datos si necesitas

## Tips

- Los gráficos son **interactivos**: hace zoom, hover para ver detalles
- El **dashboard** se actualiza automáticamente cuando agregas productos
- Las **alertas** te avisan cuando hay grandes cambios de precio
- Podés **exportar** toda la data en CSV o JSON

## Troubleshooting

**No se abre el navegador:**
```bash
# Abrí manualmente: http://localhost:8501
```

**Error de importación:**
```bash
# Instalá todas las dependencias
pip install -r requirements.txt
```

**Base de datos no encontrada:**
```bash
# Creá la carpeta data
mkdir data
```

## Próximos Pasos

1. Agregar autenticación de usuarios
2. Sistema de notificaciones (email/Telegram)
3. Comparador de múltiples productos
4. Predicción de precios con ML
5. Deploy en la nube (Streamlit Cloud/Heroku)

---

**¿Problemas?** Abre un issue en GitHub: https://github.com/Vladimir-Bulan/mercadolibre-price-monitor/issues
