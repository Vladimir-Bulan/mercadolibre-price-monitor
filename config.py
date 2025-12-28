"""
Configuración de la aplicación Streamlit
"""

# Configuración de la base de datos
DATABASE_PATH = "data/prices.db"

# Configuración de scraping
SCRAPING_CONFIG = {
    "delay_between_requests": 2,  # segundos
    "max_retries": 3,
    "timeout": 10,  # segundos
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Configuración de alertas
ALERT_CONFIG = {
    "default_threshold": 10,  # porcentaje de cambio para alertar
    "min_records_for_alert": 2,  # mínimo de registros para calcular alertas
}

# Configuración de visualización
CHART_CONFIG = {
    "default_color": "#3483FA",  # Azul de MercadoLibre
    "secondary_color": "#FFE600",  # Amarillo de MercadoLibre
    "success_color": "#00A650",
    "warning_color": "#F7B32B",
    "danger_color": "#F23D4F"
}

# Límites de la aplicación
LIMITS = {
    "max_search_results": 20,
    "max_products_tracked": 100,
    "max_history_days": 365
}
