"""
Módulo de búsqueda de productos en MercadoLibre
Versión optimizada para Streamlit Cloud (sin Selenium)
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from typing import List, Dict, Optional
from datetime import datetime
import random


class MercadoLibreScraper:
    """
    Clase para buscar productos en MercadoLibre usando requests
    """
    
    def __init__(self, debug=False):
        self.base_url = "https://listado.mercadolibre.com.ar"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-AR,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.delay = 2
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.debug = debug
    
    def search_products(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Busca productos en MercadoLibre
        """
        products = []
        
        try:
            # Limpiar query
            search_query = query.replace(' ', '-').lower()
            search_query = re.sub(r'[^a-z0-9\-]', '', search_query)
            url = f"{self.base_url}/{search_query}"
            
            print(f"🔍 Buscando: {query}")
            print(f"🌐 Accediendo a: {url}")
            
            # Delay random para evitar bloqueos
            time.sleep(random.uniform(1, 2))
            
            # Hacer request
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ Error {response.status_code}")
                return []
            
            print("✅ Productos cargados")
            
            # Parsear HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar productos (múltiples selectores)
            items = soup.find_all('li', class_='ui-search-layout__item')
            
            if not items:
                items = soup.find_all('div', class_='ui-search-result__wrapper')
            
            if not items:
                items = soup.find_all('div', class_='andes-card')
            
            print(f"📦 {len(items)} elementos encontrados")
            
            for item in items[:limit]:
                try:
                    product = self._extract_product_info(item)
                    if product and product.get('price', 0) > 0:
                        products.append(product)
                        if self.debug:
                            print(f"   {len(products)}. {product.get('title', 'Sin título')[:50]}... - ${product.get('price', 0):,.0f}")
                except Exception as e:
                    if self.debug:
                        print(f"⚠️ Error extrayendo producto: {e}")
                    continue
            
            print(f"✅ {len(products)} productos extraídos correctamente")
            
        except requests.exceptions.Timeout:
            print("⏱️ Timeout - La búsqueda tomó demasiado tiempo")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        
        return products
    
    def _extract_product_info(self, item) -> Optional[Dict]:
        """
        Extrae información de un producto
        """
        try:
            # Título
            title_elem = item.find('h2', class_='ui-search-item__title')
            if not title_elem:
                title_elem = item.find('a', class_='ui-search-link')
            title = title_elem.get_text(strip=True) if title_elem else "Sin título"
            
            # Precio
            price = 0
            price_elem = item.find('span', class_='andes-money-amount__fraction')
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_text = price_text.replace('.', '').replace(',', '')
                try:
                    price = float(price_text)
                except:
                    price = 0
            
            # URL
            link_elem = item.find('a', class_='ui-search-link')
            url = link_elem.get('href', '') if link_elem else ''
            
            # ID (extraer de la URL)
            product_id = ''
            if url:
                match = re.search(r'MLA-?(\d+)', url)
                if match:
                    product_id = f"MLA{match.group(1)}"
                else:
                    product_id = f"MLA{hash(title) % 1000000}"
            else:
                product_id = f"MLA{hash(title) % 1000000}"
            
            # Imagen/Thumbnail
            thumbnail = None
            img_elem = item.find('img')
            if img_elem:
                thumbnail = img_elem.get('src') or img_elem.get('data-src')
            
            # Vendedor
            seller_elem = item.find('span', class_='ui-search-item__brand-discoverability')
            seller = seller_elem.get_text(strip=True) if seller_elem else "Desconocido"
            
            # Envío gratis
            shipping_elem = item.find('span', class_='ui-search-item__shipping')
            free_shipping = False
            if shipping_elem:
                shipping_text = shipping_elem.get_text(strip=True).lower()
                free_shipping = 'gratis' in shipping_text
            
            return {
                'id': product_id,
                'title': title,
                'price': price,
                'url': url,
                'thumbnail': thumbnail,
                'seller': seller,
                'free_shipping': free_shipping,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            if self.debug:
                print(f"Error extrayendo info: {e}")
            return None