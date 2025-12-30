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

# ==================== ESTILOS CSS MEJORADOS ====================
st.markdown("""
<style>
    /* Gradiente principal */
    .main-header {
        background: linear-gradient(135deg, #3483FA 0%, #FFE600 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Cards de métricas mejoradas */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #3483FA;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }
    
    /* Cards de productos mejoradas */
    .product-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border: 2px solid #f0f0f0;
        transition: all 0.3s ease;
    }
    
    .product-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(52, 131, 250, 0.2);
        border-color: #3483FA;
    }
    
    /* Animación de alertas */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    .alert-badge {
        animation: pulse 2s infinite;
    }
    
    /* Botones mejorados */
    .stButton > button {
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
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

# Inicializar session_state
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
    
    # Verificar alertas de precio
    threshold = 15
    alerts = db.check_price_alerts(threshold_percent=threshold)
    
    if alerts:
        st.markdown('<div class="alert-badge">', unsafe_allow_html=True)
        st.warning(f"🔔 **{len(alerts)} Alerta(s) de Precio**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        for alert in alerts:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{alert['title'][:60]}...**")
                st.caption(f"Precio anterior: ${alert['previous_price']:,.0f} → Ahora: ${alert['current_price']:,.0f}")
            with col2:
                st.metric("📉 Bajó", f"{alert['drop_percent']:.1f}%", delta=f"-${alert['previous_price'] - alert['current_price']:,.0f}")
        st.markdown("---")
    
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
            st.metric("🔔 Alertas", len(alerts))
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
                    hist = db.get_price_history(product['id'])
                    current_price = hist[-1]['price'] if hist else 0
                    st.metric("💰 Precio Actual", f"${current_price:,.0f}")
                
                with col3:
                    if st.button("🔄 Actualizar", key=f"update_{product['id']}"):
                        with st.spinner("🔍 Actualizando precio..."):
                            try:
                                results = scraper.search_products(product['title'][:50], limit=1)
                                
                                if results and len(results) > 0:
                                    updated_product = results[0]
                                    updated_product['id'] = product['id']
                                    db.save_price(updated_product)
                                    st.success(f"✅ Precio actualizado: ${updated_product['price']:,.0f}")
                                    st.rerun()
                                else:
                                    st.warning("⚠️ No se pudo actualizar el precio")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                    
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
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_query = st.text_input(
            "¿Qué producto querés buscar?",
            placeholder="Ej: notebook lenovo, iphone 13, zapatillas nike...",
            value=st.session_state.last_search_query
        )
    
    with col2:
        limit = st.number_input("Resultados", min_value=1, max_value=20, value=10)
    
    if st.button("🔎 Buscar", use_container_width=True):
        if search_query:
            with st.spinner(f"🔍 Buscando '{search_query}' en MercadoLibre..."):
                try:
                    results = scraper.search_products(search_query, limit=limit)
                    
                    if results:
                        st.session_state.search_results = results
                        st.session_state.last_search_query = search_query
                        st.success(f"✅ Se encontraron {len(results)} productos")
                    else:
                        st.session_state.search_results = []
                        st.warning("⚠️ No se encontraron productos con ese término de búsqueda.")
                        
                except Exception as e:
                    st.error(f"❌ Error al buscar productos: {str(e)}")
        else:
            st.warning("⚠️ Por favor ingresá un término de búsqueda.")
    
    if st.session_state.search_results:
        results = st.session_state.search_results
        
        st.markdown(f"### 📦 {len(results)} Productos Encontrados")
        st.caption(f"Búsqueda: **{st.session_state.last_search_query}**")
        
        for i in range(0, len(results), 2):
            cols = st.columns(2)
            
            for j, col in enumerate(cols):
                if i + j < len(results):
                    product = results[i + j]
                    
                    with col:
                        with st.container():
                            st.markdown('<div class="product-card">', unsafe_allow_html=True)
                            
                            if product.get('thumbnail'):
                                st.image(product['thumbnail'], use_container_width=True)
                            
                            st.markdown(f"**{product.get('title', 'Sin título')}**")
                            
                            price = product.get('price', 0)
                            st.markdown(f"<h2 style='color: #3483FA; margin: 10px 0;'>${price:,.0f}</h2>", unsafe_allow_html=True)
                            
                            col_info1, col_info2 = st.columns(2)
                            with col_info1:
                                st.caption(f"🏪 {product.get('seller', 'Desconocido')}")
                            with col_info2:
                                if product.get('free_shipping'):
                                    st.caption("🚚 Envío gratis")
                                else:
                                    st.caption("📦 Con envío")
                            
                            col_btn1, col_btn2 = st.columns(2)
                            
                            with col_btn1:
                                if product.get('url'):
                                    st.link_button("🔗 Ver", product['url'], use_container_width=True)
                            
                            with col_btn2:
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
        product_titles = [p['title'] for p in products]
        selected_product = st.selectbox("Seleccioná un producto:", product_titles)
        
        product = next(p for p in products if p['title'] == selected_product)
        history = db.get_price_history(product['id'])
        
        if history and len(history) > 0:
            try:
                df = pd.DataFrame(history)
                
                if 'scraped_at' not in df.columns or 'price' not in df.columns:
                    st.error("⚠️ El formato de datos no es correcto.")
                    st.stop()
                
                df['scraped_at'] = pd.to_datetime(df['scraped_at'], errors='coerce')
                df = df.dropna(subset=['scraped_at'])
                
                if len(df) == 0:
                    st.warning("⚠️ No hay datos válidos para mostrar.")
                    st.stop()
                    
            except Exception as e:
                st.error(f"⚠️ Error al procesar los datos: {str(e)}")
                st.stop()
            
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
            
            current = product.get('current_price', product.get('price', df['price'].iloc[-1]))
            if current <= min_price * 1.05:
                st.success("⭐⭐⭐⭐⭐ ¡Excelente momento para comprar!")
            elif current <= avg_price * 0.95:
                st.info("⭐⭐⭐⭐ Buen momento para comprar.")
            elif current <= avg_price * 1.05:
                st.warning("⭐⭐⭐ Precio normal.")
            else:
                st.error("⭐⭐ Precio alto.")
            
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
    
    if st.button("🔄 Actualizar Todos los Precios", use_container_width=True):
        products = db.get_all_products()
        
        if products:
            st.info(f"🔍 Actualizando {len(products)} productos...")
            progress = st.progress(0)
            status = st.empty()
            
            updated_count = 0
            
            for i, product in enumerate(products):
                status.text(f"Actualizando: {product['title'][:40]}...")
                
                try:
                    results = scraper.search_products(product['title'][:50], limit=1)
                    
                    if results and len(results) > 0:
                        updated_product = results[0]
                        updated_product['id'] = product['id']
                        db.save_price(updated_product)
                        updated_count += 1
                except:
                    pass
                
                progress.progress((i + 1) / len(products))
            
            status.empty()
            progress.empty()
            st.success(f"✅ {updated_count} de {len(products)} productos actualizados correctamente!")
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
    - [📖 Repositorio GitHub](https://github.com/Vladimir-Bulan/mercadolibre-price-monitor)
    - [🐛 Reportar Bug](https://github.com/Vladimir-Bulan/mercadolibre-price-monitor/issues)
    - [💡 Sugerir Feature](https://github.com/Vladimir-Bulan/mercadolibre-price-monitor/discussions)
    """)