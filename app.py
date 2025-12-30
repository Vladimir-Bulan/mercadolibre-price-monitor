import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from scraper import MercadoLibreScraper
from database import PriceDatabase

# ==================== CONFIGURACIÓN DE LA PÁGINA ====================
st.set_page_config(
    page_title="MercadoLibre Price Monitor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILOS CSS PROFESIONALES ====================
st.markdown("""
<style>
    /* Imports */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables */
    :root {
        --primary: #2563eb;
        --primary-dark: #1e40af;
        --secondary: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
        --dark: #1f2937;
        --light: #f9fafb;
        --border: #e5e7eb;
    }
    
    /* Global */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    
    /* Header profesional */
    .pro-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    .pro-header h1 {
        color: white;
        font-weight: 700;
        font-size: 2rem;
        margin: 0;
        letter-spacing: -0.025em;
    }
    
    .pro-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: var(--primary);
    }
    
    .metric-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--dark);
        line-height: 1;
    }
    
    /* Product Cards */
    .product-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: var(--primary);
    }
    
    .product-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--dark);
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .product-meta {
        font-size: 0.875rem;
        color: #6b7280;
        margin-bottom: 1rem;
    }
    
    .price-tag {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin: 1rem 0;
    }
    
    /* Alert Badge */
    .alert-badge {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 1px solid #fbbf24;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        animation: subtle-pulse 3s ease-in-out infinite;
    }
    
    @keyframes subtle-pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.95; }
    }
    
    .alert-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #92400e;
        margin-bottom: 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        transition: all 0.2s;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    .stButton > button:hover {
        background: var(--primary-dark);
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-success {
        background: #d1fae5;
        color: #065f46;
    }
    
    .badge-warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .badge-info {
        background: #dbeafe;
        color: #1e40af;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid var(--border);
        margin: 2rem 0;
    }
    
    /* Section Title */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--dark);
        margin-bottom: 1.5rem;
        letter-spacing: -0.025em;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    /* Link */
    a {
        color: var(--primary);
        text-decoration: none;
        transition: color 0.2s;
    }
    
    a:hover {
        color: var(--primary-dark);
        text-decoration: underline;
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
    st.markdown("""
    <div class="pro-header">
        <h1>MercadoLibre</h1>
        <p>Price Monitor Pro</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["Dashboard", "Search Products", "Analytics", "Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### About")
    st.markdown("""
    Professional price monitoring system for MercadoLibre.
    
    **Features:**
    - Real-time product tracking
    - Price history analysis
    - Automated alerts
    - Data export
    """)
    
    st.markdown("---")
    st.caption("Built with Streamlit • v1.0.0")

# ==================== DASHBOARD ====================
if page == "Dashboard":
    st.markdown('<h1 class="section-title">Dashboard</h1>', unsafe_allow_html=True)
    
    # Verificar alertas
    threshold = 15
    alerts = db.check_price_alerts(threshold_percent=threshold)
    
    if alerts:
        st.markdown(f"""
        <div class="alert-badge">
            <div class="alert-title">⚠ {len(alerts)} Price Alert(s)</div>
            <p style="margin: 0; color: #92400e;">Significant price drops detected</p>
        </div>
        """, unsafe_allow_html=True)
        
        for alert in alerts:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{alert['title'][:60]}...**")
                st.caption(f"Previous: ${alert['previous_price']:,.0f} → Current: ${alert['current_price']:,.0f}")
            with col2:
                st.metric("Price Drop", f"{alert['drop_percent']:.1f}%", 
                         delta=f"-${alert['previous_price'] - alert['current_price']:,.0f}")
        st.markdown("---")
    
    # Obtener productos
    products = db.get_all_products()
    
    if not products:
        st.info("👋 Welcome! No products tracked yet. Go to Search Products to add some.")
    else:
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Products</div>
                <div class="metric-value">{len(products)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_price = sum(db.get_price_history(p['id'])[-1]['price'] 
                            for p in products if db.get_price_history(p['id']))
            count = len([p for p in products if db.get_price_history(p['id'])])
            avg_price = total_price / count if count > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Price</div>
                <div class="metric-value">${avg_price:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Active Alerts</div>
                <div class="metric-value">{len(alerts)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Status</div>
                <div class="metric-value" style="color: #10b981;">Active</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Productos
        st.markdown('<h2 class="section-title">Tracked Products</h2>', unsafe_allow_html=True)
        
        for product in products:
            with st.container():
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f'<div class="product-title">{product.get("title", "Untitled")}</div>', 
                               unsafe_allow_html=True)
                    st.markdown(f'<div class="product-meta">Seller: {product.get("seller", "Unknown")}</div>', 
                               unsafe_allow_html=True)
                    if product.get('url'):
                        st.markdown(f"[View on MercadoLibre →]({product['url']})")
                
                with col2:
                    hist = db.get_price_history(product['id'])
                    current_price = hist[-1]['price'] if hist else 0
                    st.markdown(f'<div class="price-tag">${current_price:,.0f}</div>', 
                               unsafe_allow_html=True)
                
                with col3:
                    if st.button("Update", key=f"update_{product['id']}", use_container_width=True):
                        with st.spinner("Updating..."):
                            try:
                                results = scraper.search_products(product['title'][:50], limit=1)
                                if results and len(results) > 0:
                                    updated_product = results[0]
                                    updated_product['id'] = product['id']
                                    db.save_price(updated_product)
                                    st.success(f"Updated: ${updated_product['price']:,.0f}")
                                    st.rerun()
                                else:
                                    st.warning("Could not update")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                    
                    if st.button("Chart", key=f"graph_{product['id']}", use_container_width=True):
                        st.session_state[f'show_graph_{product["id"]}'] = True
                        st.rerun()
                
                # Mostrar gráfico
                if st.session_state.get(f'show_graph_{product["id"]}', False):
                    history = db.get_price_history(product['id'])
                    
                    if history:
                        df = pd.DataFrame(history)
                        df['scraped_at'] = pd.to_datetime(df['scraped_at'])
                        
                        fig = px.line(
                            df,
                            x='scraped_at',
                            y='price',
                            title=f"Price Evolution - {product.get('title', 'Product')}",
                            labels={'scraped_at': 'Date', 'price': 'Price (ARS)'}
                        )
                        fig.update_traces(
                            line_color='#2563eb', 
                            line_width=3,
                            mode='lines+markers',
                            marker=dict(size=6)
                        )
                        fig.update_layout(
                            hovermode='x unified',
                            height=350,
                            font=dict(family='Inter, sans-serif'),
                            plot_bgcolor='white',
                            paper_bgcolor='white',
                            xaxis=dict(
                                showgrid=True,
                                gridcolor='#f0f0f0',
                                showline=True,
                                linecolor='#e5e7eb'
                            ),
                            yaxis=dict(
                                showgrid=True,
                                gridcolor='#f0f0f0',
                                showline=True,
                                linecolor='#e5e7eb'
                            ),
                            margin=dict(l=60, r=20, t=60, b=60)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                        
                        if st.button("Close", key=f"close_{product['id']}"):
                            st.session_state[f'show_graph_{product["id"]}'] = False
                            st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)

# ==================== BUSCAR PRODUCTOS ====================
elif page == "Search Products":
    st.markdown('<h1 class="section-title">Search Products</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_query = st.text_input(
            "Search",
            placeholder="e.g. lenovo notebook, iphone 13...",
            value=st.session_state.last_search_query,
            label_visibility="collapsed"
        )
    
    with col2:
        limit = st.number_input("Results", min_value=1, max_value=20, value=10)
    
    if st.button("Search", use_container_width=True, type="primary"):
        if search_query:
            with st.spinner(f"Searching '{search_query}'..."):
                try:
                    results = scraper.search_products(search_query, limit=limit)
                    
                    if results:
                        st.session_state.search_results = results
                        st.session_state.last_search_query = search_query
                        st.success(f"Found {len(results)} products")
                    else:
                        st.session_state.search_results = []
                        st.warning("No products found")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a search term")
    
    if st.session_state.search_results:
        results = st.session_state.search_results
        
        st.markdown(f'<h2 class="section-title">{len(results)} Products Found</h2>', 
                   unsafe_allow_html=True)
        st.caption(f"Search: **{st.session_state.last_search_query}**")
        
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
                            
                            st.markdown(f'<div class="product-title">{product.get("title", "Untitled")}</div>', 
                                       unsafe_allow_html=True)
                            
                            price = product.get('price', 0)
                            st.markdown(f'<div class="price-tag">${price:,.0f}</div>', 
                                       unsafe_allow_html=True)
                            
                            col_info1, col_info2 = st.columns(2)
                            with col_info1:
                                st.markdown(f'<span class="badge badge-info">{product.get("seller", "Unknown")}</span>', 
                                           unsafe_allow_html=True)
                            with col_info2:
                                if product.get('free_shipping'):
                                    st.markdown('<span class="badge badge-success">Free Shipping</span>', 
                                               unsafe_allow_html=True)
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            
                            col_btn1, col_btn2 = st.columns(2)
                            
                            with col_btn1:
                                if product.get('url'):
                                    st.link_button("View", product['url'], use_container_width=True)
                            
                            with col_btn2:
                                unique_key = f"add_{product.get('id', '')}_{i}_{j}"
                                if st.button("Track", key=unique_key, use_container_width=True):
                                    try:
                                        db.save_price(product)
                                        st.success("Added!")
                                        st.balloons()
                                    except Exception as e:
                                        st.error(f"Error: {str(e)}")
                            
                            st.markdown('</div>', unsafe_allow_html=True)

# ==================== ANÁLISIS ====================
elif page == "Analytics":
    st.markdown('<h1 class="section-title">Analytics</h1>', unsafe_allow_html=True)
    
    products = db.get_all_products()
    
    if not products:
        st.info("No products to analyze. Add some first.")
    else:
        product_titles = [p['title'] for p in products]
        selected_product = st.selectbox("Select Product", product_titles)
        
        product = next(p for p in products if p['title'] == selected_product)
        history = db.get_price_history(product['id'])
        
        if history and len(history) > 0:
            try:
                df = pd.DataFrame(history)
                df['scraped_at'] = pd.to_datetime(df['scraped_at'], errors='coerce')
                df = df.dropna(subset=['scraped_at'])
                
                if len(df) == 0:
                    st.warning("No valid data")
                    st.stop()
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.stop()
            
            # Stats
            col1, col2, col3, col4 = st.columns(4)
            
            stats = [
                ("Current", df['price'].iloc[-1]),
                ("Minimum", df['price'].min()),
                ("Maximum", df['price'].max()),
                ("Average", df['price'].mean())
            ]
            
            for col, (label, value) in zip([col1, col2, col3, col4], stats):
                with col:
                    col.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">${value:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Gráfico
            st.markdown('<h2 class="section-title">Price Evolution</h2>', unsafe_allow_html=True)
            
            fig = px.line(
                df,
                x='scraped_at',
                y='price',
                title="",
                labels={'scraped_at': 'Date', 'price': 'Price (ARS)'}
            )
            fig.update_traces(
                line_color='#2563eb', 
                line_width=3,
                mode='lines+markers',
                marker=dict(size=6)
            )
            fig.update_layout(
                hovermode='x unified',
                height=400,
                font=dict(family='Inter, sans-serif'),
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#f0f0f0',
                    showline=True,
                    linecolor='#e5e7eb'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#f0f0f0',
                    showline=True,
                    linecolor='#e5e7eb'
                ),
                margin=dict(l=60, r=20, t=20, b=60)
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # Distribution
            st.markdown('<h2 class="section-title">Price Distribution</h2>', unsafe_allow_html=True)
            
            fig2 = px.histogram(
                df,
                x='price',
                nbins=20,
                title="",
                labels={'price': 'Price (ARS)', 'count': 'Frequency'}
            )
            fig2.update_traces(marker_color='#2563eb', marker_line_color='#1e40af', marker_line_width=1)
            fig2.update_layout(
                height=300,
                font=dict(family='Inter, sans-serif'),
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#f0f0f0',
                    showline=True,
                    linecolor='#e5e7eb'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#f0f0f0',
                    showline=True,
                    linecolor='#e5e7eb'
                ),
                margin=dict(l=60, r=20, t=20, b=60),
                bargap=0.1
            )
            
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
            
            # Recommendation
            current = df['price'].iloc[-1]
            min_price = df['price'].min()
            avg_price = df['price'].mean()
            
            if current <= min_price * 1.05:
                st.success("★★★★★ Excellent time to buy! Price near historical minimum.")
            elif current <= avg_price * 0.95:
                st.info("★★★★ Good time to buy. Price below average.")
            elif current <= avg_price * 1.05:
                st.warning("★★★ Normal price. You can wait for a better offer.")
            else:
                st.error("★★ High price. We recommend waiting.")
            
            # Export
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">Export Data</h2>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"prices_{product['id']}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                json_data = df.to_json(orient='records', indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"prices_{product['id']}.json",
                    mime="application/json",
                    use_container_width=True
                )
        else:
            st.info("Insufficient price history")

# ==================== CONFIGURACIÓN ====================
elif page == "Settings":
    st.markdown('<h1 class="section-title">Settings</h1>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title">Price Alerts</h2>', unsafe_allow_html=True)
    
    enable_alerts = st.checkbox("Enable price alerts", value=True)
    
    if enable_alerts:
        alert_threshold = st.slider(
            "Alert threshold (% drop):",
            min_value=5,
            max_value=50,
            value=15,
            step=5
        )
        
        st.info(f"You'll be notified when a product drops {alert_threshold}% or more")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title">Bulk Update</h2>', unsafe_allow_html=True)
    
    if st.button("Update All Products", use_container_width=True, type="primary"):
        products = db.get_all_products()
        
        if products:
            st.info(f"Updating {len(products)} products...")
            progress = st.progress(0)
            status = st.empty()
            
            updated_count = 0
            
            for i, product in enumerate(products):
                status.text(f"Updating: {product['title'][:40]}...")
                
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
            st.success(f"✓ Updated {updated_count} of {len(products)} products")
        else:
            st.warning("No products to update")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title">System Info</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Tracked Products</div>
            <div class="metric-value">{len(db.get_all_products())}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Database</div>
            <div class="metric-value" style="font-size: 1.5rem;">SQLite</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title">Resources</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    - [Documentation](https://github.com/Vladimir-Bulan/mercadolibre-price-monitor)
    - [Report Issue](https://github.com/Vladimir-Bulan/mercadolibre-price-monitor/issues)
    - [Request Feature](https://github.com/Vladimir-Bulan/mercadolibre-price-monitor/discussions)
    """)