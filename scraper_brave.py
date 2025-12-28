"""
Scraper de MercadoLibre con Selenium + Brave Browser
Datos 100% REALES
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import time
import re
import os
from typing import List, Dict
from datetime import datetime


class MercadoLibreScraper:
    """
    Scraper usando Selenium con Brave Browser
    """
    
    def __init__(self, debug=False, headless=True):
        self.debug = debug
        self.headless = headless
        self.base_url = "https://listado.mercadolibre.com.ar"
        self.driver = None
    
    def _find_brave_path(self):
        """Encuentra la ruta de Brave Browser"""
        possible_paths = [
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _init_driver(self):
        """Inicializa el driver con Brave"""
        if self.driver:
            return
        
        brave_path = self._find_brave_path()
        
        if not brave_path:
            print("❌ No se encontró Brave Browser")
            print("\n💡 OPCIONES:")
            print("   1. Instalar Chrome: https://www.google.com/chrome/")
            print("   2. O decime dónde está instalado Brave")
            raise Exception("Brave no encontrado")
        
        print(f"✅ Brave encontrado: {brave_path}")
        
        chrome_options = Options()
        chrome_options.binary_location = brave_path
        
        if self.headless:
            chrome_options.add_argument('--headless=new')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Evitar detección
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Navegador iniciado correctamente")
        except Exception as e:
            print(f"❌ Error iniciando navegador: {e}")
            print("\n💡 SOLUCIÓN:")
            print("   Brave usa ChromeDriver igual que Chrome.")
            print("   Selenium debería descargarlo automáticamente.")
            raise
    
    def search_products(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca productos en MercadoLibre"""
        print(f"🔍 Buscando: {query}")
        
        try:
            self._init_driver()
            
            search_url = f"{self.base_url}/{query.replace(' ', '-')}"
            print(f"🌐 Accediendo a: {search_url}")
            
            self.driver.get(search_url)
            
            wait = WebDriverWait(self.driver, 20)
            
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.ui-search-layout__item")))
                print("✅ Productos cargados")
            except TimeoutException:
                print("⏱️ Timeout esperando productos, intentando de todas formas...")
            
            time.sleep(3)
            
            products_elements = self.driver.find_elements(By.CSS_SELECTOR, "li.ui-search-layout__item")
            
            if not products_elements:
                print("❌ No se encontraron productos")
                return []
            
            print(f"📦 {len(products_elements)} elementos encontrados")
            
            results = []
            
            for i, elem in enumerate(products_elements[:limit * 2]):
                try:
                    product = self._extract_product_info(elem)
                    
                    if product and product.get('price', 0) > 0:
                        results.append(product)
                        
                        if self.debug:
                            print(f"   ✓ {len(results)}: {product['title'][:50]}")
                    
                    if len(results) >= limit:
                        break
                        
                except Exception as e:
                    if self.debug:
                        print(f"   ⚠️ Error: {e}")
                    continue
            
            print(f"✅ {len(results)} productos extraídos correctamente")
            
            for i, p in enumerate(results[:3], 1):
                print(f"   {i}. {p['title'][:55]}... - ${p['price']:,.0f}")
            
            return results
            
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return []
        
        # NO cerrar el driver aquí - mantenerlo abierto para búsquedas siguientes
        # finally:
        #     if self.driver:
        #         self.driver.quit()
    
    def _extract_product_info(self, element) -> Dict:
        """Extrae información de un producto"""
        try:
            # Título - múltiples estrategias
            title = ""
            title_selectors = [
                "h2.poly-box",
                "h2.ui-search-item__title",
                "h2",
                "a.ui-search-link"
            ]
            
            for sel in title_selectors:
                try:
                    title_elem = element.find_element(By.CSS_SELECTOR, sel)
                    title = title_elem.text.strip()
                    if title and len(title) > 10:
                        break
                except:
                    continue
            
            # Si no hay título, intentar desde el link
            if not title or len(title) < 10:
                try:
                    link = element.find_element(By.CSS_SELECTOR, "a")
                    title = link.get_attribute('title') or link.text.strip()
                except:
                    pass
            
            if not title or len(title) < 10:
                if self.debug:
                    print(f"   ⚠️ Sin título válido")
                return None
            
            # Precio - múltiples estrategias
            price = 0
            price_selectors = [
                "span.andes-money-amount__fraction",
                "span.price-tag-fraction",
                "span.andes-money-amount-combo__fraction",
                "div.ui-search-price span.andes-money-amount__fraction"
            ]
            
            for sel in price_selectors:
                try:
                    price_elem = element.find_element(By.CSS_SELECTOR, sel)
                    price_text = price_elem.text.strip()
                    
                    # Limpiar texto
                    price_text = price_text.replace('.', '').replace(',', '.').replace('$', '').strip()
                    price = float(re.sub(r'[^\d.]', '', price_text))
                    
                    if price > 100:
                        break
                except:
                    continue
            
            # Si no encontró precio, buscar en todo el texto
            if price < 100:
                try:
                    text = element.text
                    matches = re.findall(r'\$\s*(\d{1,3}(?:\.\d{3})*)', text)
                    if matches:
                        price = float(matches[0].replace('.', ''))
                except:
                    pass
            
            if price < 100:
                if self.debug:
                    print(f"   ⚠️ Precio inválido: {title[:30]}")
                return None
            
            # URL
            url = ""
            try:
                url = element.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
            except:
                pass
            
            # ID
            product_id = f"MLA{hash(url or title) % 10000000000}"
            match = re.search(r'ML[A-Z]-?(\d+)', url or "")
            if match:
                product_id = match.group(0)
            
            # Imagen
            thumbnail = ""
            try:
                img = element.find_element(By.CSS_SELECTOR, "img")
                thumbnail = (img.get_attribute('src') or img.get_attribute('data-src') or "")
                if thumbnail:
                    thumbnail = thumbnail.replace('http://', 'https://')
            except:
                pass
            
            # Vendedor
            seller = "Vendedor"
            seller_selectors = [
                "span.ui-search-item__brand-discoverability",
                "p.ui-search-item__group__element",
                "span.ui-search-item__shipping"
            ]
            
            for sel in seller_selectors:
                try:
                    seller_elem = element.find_element(By.CSS_SELECTOR, sel)
                    seller_text = seller_elem.text.strip()
                    if seller_text and len(seller_text) < 50:
                        seller = seller_text
                        break
                except:
                    continue
            
            # Envío gratis
            free_shipping = False
            try:
                text = element.text.lower()
                free_shipping = 'gratis' in text or 'envío gratis' in text
            except:
                pass
            
            if self.debug:
                print(f"   ✅ {title[:40]}... - ${price:,.0f}")
            
            return {
                'id': product_id,
                'title': title,
                'price': float(price),
                'url': url,
                'thumbnail': thumbnail,
                'seller': seller,
                'free_shipping': free_shipping,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            if self.debug:
                print(f"   ❌ Error extrayendo: {e}")
            return None


    def close(self):
        """Cierra el navegador"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                print("🔒 Navegador cerrado")
            except:
                pass


def search_product(query: str, limit: int = 10, debug: bool = False) -> List[Dict]:
    """Función helper - Usa una instancia global para mantener el navegador abierto"""
    global _global_scraper
    
    if '_global_scraper' not in globals():
        _global_scraper = MercadoLibreScraper(debug=debug, headless=True)
    
    return _global_scraper.search_products(query, limit)


if __name__ == "__main__":
    print("="*70)
    print("  SCRAPER MERCADOLIBRE - BRAVE BROWSER")
    print("  Datos 100% REALES")
    print("="*70 + "\n")
    
    products = search_product("notebook", limit=5, debug=True)
    
    print(f"\n" + "="*70)
    print(f"  RESULTADO: {len(products)} productos REALES")
    print("="*70)
    
    if products:
        p = products[0]
        print(f"\n📦 Primer producto:")
        print(f"   ID: {p['id']}")
        print(f"   Título: {p['title']}")
        print(f"   Precio: ${p['price']:,.0f}")
        print(f"   Vendedor: {p['seller']}")
        print(f"   Envío gratis: {'Sí' if p['free_shipping'] else 'No'}")
        print(f"   URL: {p['url'][:60]}...")
        if p['thumbnail']:
            print(f"   Imagen: {p['thumbnail'][:60]}...")
    else:
        print("\n⚠️ No se encontraron productos")