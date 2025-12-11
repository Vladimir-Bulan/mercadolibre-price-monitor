"""
Módulo de Web Scraping para MercadoLibre
Contiene funciones para buscar productos y extraer información de precios
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from typing import List, Dict, Optional
from datetime import datetime


class MercadoLibreScraper:
    """
    Clase para realizar web scraping en MercadoLibre
    """
    
    def __init__(self):
        self.base_url = "https://listado.mercadolibre.com.ar"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.delay = 2  # Delay entre requests para ser respetuosos
    
    def search_products(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Busca productos en MercadoLibre
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados a retornar
            
        Returns:
            Lista de diccionarios con información de productos
        """
        products = []
        
        try:
            # Formatear query para URL
            search_query = query.replace(' ', '-')
            url = f"{self.base_url}/{search_query}"
            
            print(f"Buscando: {query}")
            print(f"URL: {url}")
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar elementos de productos
            items = soup.find_all('li', class_='ui-search-layout__item', limit=limit)
            
            for item in items:
                try:
                    product = self._extract_product_info(item)
                    if product:
                        products.append(product)
                        print(f"✓ Producto encontrado: {product['title'][:50]}...")
                except Exception as e:
                    print(f"Error extrayendo producto: {e}")
                    continue
            
            time.sleep(self.delay)  # Delay respetuoso
            
        except requests.RequestException as e:
            print(f"Error en la búsqueda: {e}")
        
        return products
    
    def _extract_product_info(self, item) -> Optional[Dict]:
        """
        Extrae información de un elemento de producto
        
        Args:
            item: Elemento BeautifulSoup del producto
            
        Returns:
            Diccionario con información del producto o None
        """
        try:
            # Título
            title_elem = item.find('h2', class_='ui-search-item__title')
            title = title_elem.get_text(strip=True) if title_elem else "Sin título"
            
            # Precio
            price_elem = item.find('span', class_='andes-money-amount__fraction')
            if not price_elem:
                return None
            
            price_text = price_elem.get_text(strip=True)
            price = self._clean_price(price_text)
            
            # Link
            link_elem = item.find('a', class_='ui-search-link')
            link = link_elem['href'] if link_elem else ""
            
            # Extraer ID del producto del link
            product_id = self._extract_product_id(link)
            
            # Vendedor (si está disponible)
            seller_elem = item.find('span', class_='ui-search-item__group__element')
            seller = seller_elem.get_text(strip=True) if seller_elem else "Desconocido"
            
            # Envío gratis
            shipping_elem = item.find('p', class_='ui-search-item__shipping')
            free_shipping = 'gratis' in shipping_elem.get_text().lower() if shipping_elem else False
            
            return {
                'id': product_id,
                'title': title,
                'price': price,
                'link': link,
                'seller': seller,
                'free_shipping': free_shipping,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error extrayendo información: {e}")
            return None
    
    def _clean_price(self, price_text: str) -> float:
        """
        Limpia el texto del precio y lo convierte a float
        
        Args:
            price_text: Texto del precio (ej: "45.999")
            
        Returns:
            Precio como float
        """
        # Remover puntos de miles y convertir a float
        cleaned = price_text.replace('.', '').replace(',', '.')
        return float(cleaned)
    
    def _extract_product_id(self, url: str) -> str:
        """
        Extrae el ID del producto de la URL
        
        Args:
            url: URL del producto
            
        Returns:
            ID del producto
        """
        # El ID suele estar en el formato MLA-XXXXXXXXX
        match = re.search(r'ML[A-Z]-?\d+', url)
        if match:
            return match.group(0)
        
        # Si no encuentra el formato estándar, usar hash de la URL
        return str(hash(url))
    
    def get_product_details(self, product_url: str) -> Optional[Dict]:
        """
        Obtiene detalles adicionales de un producto específico
        
        Args:
            product_url: URL del producto
            
        Returns:
            Diccionario con detalles del producto
        """
        try:
            response = requests.get(product_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer información adicional
            details = {
                'url': product_url,
                'scraped_at': datetime.now().isoformat()
            }
            
            # Aquí se pueden agregar más detalles según necesidad
            # (condición, stock, especificaciones, etc.)
            
            time.sleep(self.delay)
            return details
            
        except Exception as e:
            print(f"Error obteniendo detalles: {e}")
            return None


def search_product(query: str, limit: int = 10) -> List[Dict]:
    """
    Función helper para buscar productos
    
    Args:
        query: Término de búsqueda
        limit: Número máximo de resultados
        
    Returns:
        Lista de productos encontrados
    """
    scraper = MercadoLibreScraper()
    return scraper.search_products(query, limit)


def get_product_details(url: str) -> Optional[Dict]:
    """
    Función helper para obtener detalles de un producto
    
    Args:
        url: URL del producto
        
    Returns:
        Detalles del producto
    """
    scraper = MercadoLibreScraper()
    return scraper.get_product_details(url)


if __name__ == "__main__":
    # Ejemplo de uso
    print("=== Ejemplo de uso del scraper ===\n")
    
    # Buscar notebooks
    products = search_product("notebook", limit=5)
    
    print(f"\n✓ Se encontraron {len(products)} productos")
    
    if products:
        print("\nPrimer producto:")
        first = products[0]
        for key, value in first.items():
            print(f"  {key}: {value}")
