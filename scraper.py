"""
Scraper de MercadoLibre usando API oficial
100% confiable, sin bloqueos
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime


class MercadoLibreScraper:
    """
    Scraper usando la API oficial de MercadoLibre
    """
    
    def __init__(self, debug=False):
        self.base_url = "https://api.mercadolibre.com"
        self.site_id = "MLA"
        self.debug = debug
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MercadoLibre Price Monitor/1.0',
            'Accept': 'application/json'
        })
    
    def search_products(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Busca productos usando la API oficial
        """
        products = []
        
        try:
            url = f"{self.base_url}/sites/{self.site_id}/search"
            params = {'q': query, 'limit': min(limit, 50)}
            
            print(f"🔍 Buscando: {query}")
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ Error {response.status_code}")
                return []
            
            data = response.json()
            results = data.get('results', [])
            
            print(f"✅ {len(results)} productos encontrados")
            
            for item in results[:limit]:
                try:
                    product = self._parse_product(item)
                    if product and product.get('price', 0) > 0:
                        products.append(product)
                except:
                    continue
            
            print(f"✅ {len(products)} productos OK")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        return products
    
    def _parse_product(self, item: Dict) -> Optional[Dict]:
        try:
            thumbnail = item.get('thumbnail', '')
            if thumbnail:
                thumbnail = thumbnail.replace('-I.jpg', '-O.jpg')
            
            return {
                'id': item.get('id', ''),
                'title': item.get('title', 'Sin título'),
                'price': float(item.get('price', 0)),
                'url': item.get('permalink', ''),
                'thumbnail': thumbnail,
                'seller': item.get('seller', {}).get('nickname', 'Vendedor'),
                'free_shipping': item.get('shipping', {}).get('free_shipping', False),
                'scraped_at': datetime.now().isoformat()
            }
        except:
            return None