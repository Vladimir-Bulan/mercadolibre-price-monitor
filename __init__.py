"""
Monitor de Precios de MercadoLibre
Sistema de web scraping y análisis de precios
"""

__version__ = "1.0.0"
__author__ = "Tu Nombre"

from .scraper import MercadoLibreScraper, search_product
from .database import PriceDatabase, save_price, get_price_history
from .analyzer import PriceAnalyzer, plot_price_evolution, get_price_statistics
from .utils import format_price, print_product_summary

__all__ = [
    'MercadoLibreScraper',
    'search_product',
    'PriceDatabase',
    'save_price',
    'get_price_history',
    'PriceAnalyzer',
    'plot_price_evolution',
    'get_price_statistics',
    'format_price',
    'print_product_summary'
]
