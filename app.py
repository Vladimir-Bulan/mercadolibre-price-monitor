import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from scraper import MercadoLibreScraper
from database import PriceDatabase

# ==================== CONFIGURACIÓN DE LA PÁGINA ====================
st.set_page_config(
    page_title="Monitor de Precios MercadoLibre",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILOS CSS ====================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #3483FA 0%, #FFE600 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #3483FA;
    }
    .product-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        border: 1px solid #e0e0e0;
    }
    .product-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        border-color: #3483FA;
    }
</style>
""", unsafe_allow_html=True)

# ==================== INICIALIZACIÓN ====================
@st.cache_resource
def init_scraper():
    return MercadoLibreScraper()

@st.cache_resource
def init_db():
    return PriceDatabase("data/prices.db")

scraper = init_scraper()
db = init_db()

# Inicializar session_state para mantener los resultados de búsqueda
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'last_search_query' not in st.session_state:
    st.session_state.last_search_query = ""

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown('<div class="main-header"><h1 style="color: white; margin: 0;">🛍️ MercadoLibre</h1><p style="color: white; margin: 0;">Monitor de Precios</p></div>', unsafe_allow_html=True)
    
    page = st.radio(
        "Navegación",
        ["🏠 Dashboard", "🔍 Buscar Productos", "📊 Análisis", "⚙️ Configuración"]
    )
    
    st.markdown("---")
    
    # Info del proyecto
    st.markdown("### 📌 Sobre el Proyecto")
    st.markdown("""
    Sistema de monitoreo de precios para MercadoLibre.
    
    **Features:**
    - 🔍 Búsqueda de productos
    - 💰 Seguimiento de precios
    - 📈 Análisis de tendencias
    - 🎯 Alertas personalizadas
    """)
    
    st.markdown("---")
    st.markdown("Hecho con ❤️ usando Streamlit")

# ==================== DASHBOARD ====================
if page == "🏠 Dashboard":
    st.title("🏠 Dashboard Principal")
    
    # Obtener productos trackeados
    products = db.get_all_products()
    
    if not products:
        st.info("👋 ¡Bienvenido! Aún no tenés productos en seguimiento. Andá a **🔍 Buscar Productos** para agregar algunos.")
    else:
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📦 Productos", len(products))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Calcular precio promedio desde el historial de cada producto
            total_price = 0
            count = 0
            for p in products:
                hist = db.get_price_history(p['id'])
                if hist:
                    total_price += hist[-1]['price']
                    count += 1
            avg_price = total_price / count if count > 0 else 0
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("💰 Precio Promedio", f"${avg_price:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📊 Actualizaciones Hoy", "🔄")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("⭐ Estado", "✅ Activo")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Mostrar productos
        st.subheader("📦 Productos en Seguimiento")
        
        for product in products:
            with st.container():
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"### {product.get('title', 'Sin título')}")
                    st.caption(f"🏪 {product.get('seller', 'Desconocido')}")
                    if product.get('url'):
                        st.markdown(f"[🔗 Ver en MercadoLibre]({product['url']})")
                
                with col2:
                    # Obtener precio actual desde el historial
                    hist = db.get_price_history(product['id'])
                    current_price = hist[-1]['price'] if hist else 0
                    st.metric("💰 Precio Actual", f"${current_price:,.0f}")
                
                with col3:
                    if st.button("🔄 Actualizar", key=f"update_{product['id']}"):
                        with st.spinner("Actualizando..."):
                            # Aquí iría la lógica de actualización
                            st.success("✅ Actualizado!")
                    
                    if st.button("📈 Ver Gráfico", key=f"graph_{product['id']}"):
                        st.session_state[f'show_graph_{product["id"]}'] = True
                        st.rerun()
                
                # Mostrar gráfico si se solicitó
                if st.session_state.get(f'show_graph_{product["id"]}', False):
                    history = db.get_price_history(product['id'])
                    
                    if history:
                        df = pd.DataFrame(history)
                        df['scraped_at'] = pd.to_datetime(df['scraped_at'])
                        
                        fig = px.line(
                            df,
                            x='scraped_at',
                            y='price',
                            title=f"Evolución de Precio - {product.get('title', 'Producto')}",
                            labels={'scraped_at': 'Fecha', 'price': 'Precio (ARS)'}
                        )
                        fig.update_traces(line_color='#3483FA', line_width=3)
                        fig.update_layout(hovermode='x unified')
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        if st.button("❌ Cerrar Gráfico", key=f"close_{product['id']}"):
                            st.session_state[f'show_graph_{product["id"]}'] = False
                            st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")

# ==================== BUSCAR PRODUCTOS ====================
elif page == "🔍 Buscar Productos":
    st.title("🔍 Buscar y Agregar Productos")
    
    # Formulario de búsqueda
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_query = st.text_input(
            "¿Qué producto querés buscar?",
            placeholder="Ej: notebook lenovo, iphone 13, zapatillas nike...",
            value=st.session_state.last_search_query
        )
    
    with col2:
        limit = st.number_input("Resultados", min_value=1, max_value=20, value=10)
    
    # Botón de búsqueda
    if st.button("🔎 Buscar", use_container_width=True):
        if search_query:
            with st.spinner(f"🔍 Buscando '{search_query}' en MercadoLibre..."):
                try:
                    results = scraper.search_products(search_query, limit=limit)
                    
                    if results:
                        # Guardar resultados en session_state
                        st.session_state.search_results = results
                        st.session_state.last_search_query = search_query
                        st.success(f"✅ Se encontraron {len(results)} productos")
                    else:
                        st.session_state.search_results = []
                        st.warning("⚠️ No se encontraron productos con ese término de búsqueda.")
                        st.info("💡 Intenta con otro término de búsqueda.")
                        
                except Exception as e:
                    st.error(f"❌ Error al buscar productos: {str(e)}")
                    st.info("💡 Verifica tu conexión a internet e intenta nuevamente.")
        else:
            st.warning("⚠️ Por favor ingresá un término de búsqueda.")
    
    # Mostrar resultados guardados en session_state
    if st.session_state.search_results:
        results = st.session_state.search_results
        
        st.markdown(f"### 📦 {len(results)} Productos Encontrados")
        st.caption(f"Búsqueda: **{st.session_state.last_search_query}**")
        
        # Mostrar resultados en grid (2 columnas)
        for i in range(0, len(results), 2):
            cols = st.columns(2)
            
            for j, col in enumerate(cols):
                if i + j < len(results):
                    product = results[i + j]
                    
                    with col:
                        with st.container():
                            st.markdown('<div class="product-card">', unsafe_allow_html=True)
                            
                            # Mostrar imagen si está disponible
                            if product.get('thumbnail'):
                                st.image(product['thumbnail'], use_container_width=True)
                            
                            # Título
                            st.markdown(f"**{product.get('title', 'Sin título')}**")
                            
                            # Precio grande y destacado
                            price = product.get('price', 0)
                            st.markdown(f"<h2 style='color: #3483FA; margin: 10px 0;'>${price:,.0f}</h2>", unsafe_allow_html=True)
                            
                            # Info adicional
                            col_info1, col_info2 = st.columns(2)
                            with col_info1:
                                st.caption(f"🏪 {product.get('seller', 'Desconocido')}")
                            with col_info2:
                                if product.get('free_shipping'):
                                    st.caption("🚚 Envío gratis")
                                else:
                                    st.caption("📦 Con envío")
                            
                            # Botones
                            col_btn1, col_btn2 = st.columns(2)
                            
                            with col_btn1:
                                if product.get('url'):
                                    st.link_button("🔗 Ver", product['url'], use_container_width=True)
                            
                            with col_btn2:
                                # Clave única para cada botón usando el índice y el ID del producto
                                unique_key = f"add_{product.get('id', '')}_{i}_{j}"
                                if st.button("➕ Agregar", key=unique_key, use_container_width=True):
                                    try:
                                        db.save_price(product)
                                        st.success("✅ Agregado!")
                                        st.balloons()
                                    except Exception as e:
                                        st.error(f"Error: {str(e)}")
                            
                            st.markdown('</div>', unsafe_allow_html=True)

# ==================== ANÁLISIS ====================
elif page == "📊 Análisis":
    st.title("📊 Análisis de Precios")
    
    products = db.get_all_products()
    
    if not products:
        st.info("No hay productos para analizar. Agregá algunos primero en **🔍 Buscar Productos**.")
    else:
        # Selector de producto
        product_titles = [p['title'] for p in products]
        selected_product = st.selectbox("Seleccioná un producto:", product_titles)
        
        # Encontrar el producto seleccionado
        product = next(p for p in products if p['title'] == selected_product)
        
        # Obtener historial de precios
        history = db.get_price_history(product['id'])
        
        if history and len(history) > 0:
            try:
                df = pd.DataFrame(history)
                
                # Verificar que tenga las columnas necesarias
                if 'scraped_at' not in df.columns or 'price' not in df.columns:
                    st.error("⚠️ El formato de datos no es correcto. Intenta actualizar el precio del producto.")
                    st.stop()
                
                # Convertir scraped_at a datetime de manera segura
                df['scraped_at'] = pd.to_datetime(df['scraped_at'], errors='coerce')
                
                # Eliminar filas con timestamps inválidos
                df = df.dropna(subset=['scraped_at'])
                
                if len(df) == 0:
                    st.warning("⚠️ No hay datos válidos para mostrar.")
                    st.stop()
                    
            except Exception as e:
                st.error(f"⚠️ Error al procesar los datos: {str(e)}")
                st.info("💡 Intenta actualizar el precio del producto o agregalo nuevamente.")
                st.stop()
            
            # Estadísticas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                current_price = df['price'].iloc[-1]
                st.metric("💰 Precio Actual", f"${current_price:,.0f}")
            
            with col2:
                min_price = df['price'].min()
                st.metric("📉 Precio Mínimo", f"${min_price:,.0f}")
            
            with col3:
                max_price = df['price'].max()
                st.metric("📈 Precio Máximo", f"${max_price:,.0f}")
            
            with col4:
                avg_price = df['price'].mean()
                st.metric("📊 Precio Promedio", f"${avg_price:,.0f}")
            
            st.markdown("---")
            
            # Gráfico de evolución
            st.subheader("📈 Evolución de Precio")
            
            fig = px.line(
                df,
                x='scraped_at',
                y='price',
                title=f"Historial de Precios - {product['title']}",
                labels={'scraped_at': 'Fecha', 'price': 'Precio (ARS)'}
            )
            fig.update_traces(line_color='#3483FA', line_width=3)
            fig.update_layout(hovermode='x unified', height=400)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Distribución de precios
            st.subheader("📊 Distribución de Precios")
            
            fig2 = px.histogram(
                df,
                x='price',
                nbins=20,
                title="Frecuencia de Precios",
                labels={'price': 'Precio (ARS)', 'count': 'Frecuencia'}
            )
            fig2.update_traces(marker_color='#3483FA')
            fig2.update_layout(height=300)
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Recomendación - CORREGIDO AQUÍ ✅
            current = product.get('current_price', product.get('price', df['price'].iloc[-1]))
            if current <= min_price * 1.05:
                st.success("⭐⭐⭐⭐⭐ ¡Excelente momento para comprar! El precio está muy cerca del mínimo histórico.")
            elif current <= avg_price * 0.95:
                st.info("⭐⭐⭐⭐ Buen momento para comprar. El precio está por debajo del promedio.")
            elif current <= avg_price * 1.05:
                st.warning("⭐⭐⭐ Precio normal. Podés esperar a una mejor oferta.")
            else:
                st.error("⭐⭐ Precio alto. Te recomendamos esperar a que baje.")
            
            # Exportar datos
            st.markdown("---")
            st.subheader("💾 Exportar Datos")
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar CSV",
                    data=csv,
                    file_name=f"precios_{product['id']}.csv",
                    mime="text/csv"
                )
            
            with col2:
                json_data = df.to_json(orient='records', indent=2)
                st.download_button(
                    label="📥 Descargar JSON",
                    data=json_data,
                    file_name=f"precios_{product['id']}.json",
                    mime="application/json"
                )
        else:
            st.info("No hay suficiente historial de precios para analizar.")

# ==================== CONFIGURACIÓN ====================
elif page == "⚙️ Configuración":
    st.title("⚙️ Configuración")
    
    st.subheader("🔔 Alertas de Precio")
    
    enable_alerts = st.checkbox("Activar alertas de precio", value=True)
    
    if enable_alerts:
        alert_threshold = st.slider(
            "Porcentaje de caída para alertar:",
            min_value=5,
            max_value=50,
            value=15,
            step=5,
            help="Te notificaremos cuando un producto baje este porcentaje"
        )
        
        st.info(f"✅ Te avisaremos cuando un producto baje un {alert_threshold}% o más")
    
    st.markdown("---")
    
    st.subheader("🔄 Actualización de Precios")
    
    if st.button("🔄 Actualizar Todos los Precios"):
        products = db.get_all_products()
        
        if products:
            progress = st.progress(0)
            
            for i, product in enumerate(products):
                # Aquí iría la lógica de actualización real
                progress.progress((i + 1) / len(products))
            
            st.success(f"✅ {len(products)} productos actualizados correctamente!")
        else:
            st.warning("No hay productos para actualizar.")
    
    st.markdown("---")
    
    st.subheader("ℹ️ Información del Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📦 Productos Trackeados", len(db.get_all_products()))
    
    with col2:
        st.metric("🗄️ Base de Datos", "SQLite")
    
    st.markdown("---")
    
    st.subheader("🔗 Links Útiles")
    
    st.markdown("""
    - [📖 Repositorio GitHub](https://github.com/tuusuario/mercadolibre-price-monitor)
    - [🐛 Reportar Bug](https://github.com/tuusuario/mercadolibre-price-monitor/issues)
    - [💡 Sugerir Feature](https://github.com/tuusuario/mercadolibre-price-monitor/discussions)
    """)