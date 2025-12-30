"""
Módulo de Base de Datos
Maneja el almacenamiento y recuperación de precios en SQLite
"""

import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
import os


class PriceDatabase:
    """
    Clase para manejar la base de datos de precios
    """
    
    def __init__(self, db_path: str = "data/prices.db"):
        """
        Inicializa la conexión a la base de datos
        
        Args:
            db_path: Ruta al archivo de base de datos
        """
        self.db_path = db_path
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Crear tablas si no existen
        self._create_tables()
    
    def _create_tables(self):
        """
        Crea las tablas necesarias en la base de datos
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabla de productos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    link TEXT,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla de precios (histórico)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id TEXT NOT NULL,
                    price REAL NOT NULL,
                    seller TEXT,
                    free_shipping BOOLEAN,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            """)
            
            # Índice para búsquedas rápidas
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_product_id 
                ON prices(product_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_scraped_at 
                ON prices(scraped_at)
            """)
            
            conn.commit()
            print("✓ Base de datos inicializada correctamente")
    
    def save_product(self, product: Dict) -> bool:
        """
        Guarda o actualiza un producto en la base de datos
        
        Args:
            product: Diccionario con información del producto
            
        Returns:
            True si se guardó correctamente
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR IGNORE INTO products (id, title, link)
                    VALUES (?, ?, ?)
                """, (
                    product['id'],
                    product['title'],
                    product.get('link', product.get('url', ''))
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error guardando producto: {e}")
            return False
    
    def save_price(self, product: Dict) -> bool:
        """
        Guarda un precio en el histórico
        
        Args:
            product: Diccionario con información del producto y precio
            
        Returns:
            True si se guardó correctamente
        """
        try:
            # Primero guardar el producto si no existe
            self.save_product(product)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO prices (product_id, price, seller, free_shipping, scraped_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    product['id'],
                    product['price'],
                    product.get('seller', 'Desconocido'),
                    product.get('free_shipping', False),
                    product.get('scraped_at', datetime.now().isoformat())
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error guardando precio: {e}")
            return False
    
    def get_price_history(self, product_id: str) -> List[Dict]:
        """
        Obtiene el histórico de precios de un producto
        
        Args:
            product_id: ID del producto
            
        Returns:
            Lista de diccionarios con histórico de precios
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        p.price,
                        p.seller,
                        p.free_shipping,
                        p.scraped_at,
                        prod.title
                    FROM prices p
                    JOIN products prod ON p.product_id = prod.id
                    WHERE p.product_id = ?
                    ORDER BY p.scraped_at ASC
                """, (product_id,))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            print(f"Error obteniendo histórico: {e}")
            return []
    
    def get_all_products(self) -> List[Dict]:
        """
        Obtiene todos los productos monitoreados
        
        Returns:
            Lista de productos
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        p.id,
                        p.title,
                        p.link as url,
                        p.first_seen,
                        COUNT(pr.id) as price_count,
                        MIN(pr.price) as min_price,
                        MAX(pr.price) as max_price,
                        AVG(pr.price) as avg_price
                    FROM products p
                    LEFT JOIN prices pr ON p.id = pr.product_id
                    GROUP BY p.id
                    ORDER BY p.first_seen DESC
                """)
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            print(f"Error obteniendo productos: {e}")
            return []
    
    def get_latest_prices(self, limit: int = 10) -> List[Dict]:
        """
        Obtiene los últimos precios registrados
        
        Args:
            limit: Número máximo de resultados
            
        Returns:
            Lista de precios recientes
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        p.id,
                        prod.title,
                        p.price,
                        p.seller,
                        p.scraped_at
                    FROM prices p
                    JOIN products prod ON p.product_id = prod.id
                    ORDER BY p.scraped_at DESC
                    LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            print(f"Error obteniendo precios recientes: {e}")
            return []
    
    def get_price_changes(self, threshold: float = 10.0) -> List[Dict]:
        """
        Detecta productos con cambios significativos de precio
        
        Args:
            threshold: Porcentaje de cambio para considerar significativo
            
        Returns:
            Lista de productos con cambios de precio
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    WITH latest_prices AS (
                        SELECT 
                            product_id,
                            price as current_price,
                            ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY scraped_at DESC) as rn
                        FROM prices
                    ),
                    previous_prices AS (
                        SELECT 
                            product_id,
                            price as previous_price,
                            ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY scraped_at DESC) as rn
                        FROM prices
                    )
                    SELECT 
                        p.id,
                        p.title,
                        lp.current_price,
                        pp.previous_price,
                        ((lp.current_price - pp.previous_price) / pp.previous_price * 100) as change_percent
                    FROM products p
                    JOIN latest_prices lp ON p.id = lp.product_id AND lp.rn = 1
                    JOIN previous_prices pp ON p.id = pp.product_id AND pp.rn = 2
                    WHERE ABS((lp.current_price - pp.previous_price) / pp.previous_price * 100) >= ?
                    ORDER BY ABS(change_percent) DESC
                """, (threshold,))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            print(f"Error detectando cambios: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """
        Obtiene estadísticas generales de la base de datos
        
        Returns:
            Diccionario con estadísticas
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total de productos
                cursor.execute("SELECT COUNT(*) FROM products")
                total_products = cursor.fetchone()[0]
                
                # Total de precios registrados
                cursor.execute("SELECT COUNT(*) FROM prices")
                total_prices = cursor.fetchone()[0]
                
                # Fecha del primer registro
                cursor.execute("SELECT MIN(scraped_at) FROM prices")
                first_record = cursor.fetchone()[0]
                
                # Fecha del último registro
                cursor.execute("SELECT MAX(scraped_at) FROM prices")
                last_record = cursor.fetchone()[0]
                
                return {
                    'total_products': total_products,
                    'total_prices': total_prices,
                    'first_record': first_record,
                    'last_record': last_record
                }
                
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {}
    
    def check_price_alerts(self, threshold_percent=15):
        """
        Detecta productos con caída de precio significativa
        threshold_percent: porcentaje mínimo de caída para alertar
        """
        alerts = []
        products = self.get_all_products()
        
        for product in products:
            history = self.get_price_history(product['id'])
            
            if len(history) >= 2:
                # Precio actual vs precio anterior
                current_price = history[-1]['price']
                previous_price = history[-2]['price']
                
                # Calcular porcentaje de caída
                if previous_price > 0:
                    price_drop = ((previous_price - current_price) / previous_price) * 100
                    
                    if price_drop >= threshold_percent:
                        alerts.append({
                            'product_id': product['id'],
                            'title': product['title'],
                            'previous_price': previous_price,
                            'current_price': current_price,
                            'drop_percent': price_drop,
                            'url': product.get('url', '')
                        })
        
        return alerts


# Funciones helper para facilitar el uso
def save_price(product: Dict, db_path: str = "data/prices.db") -> bool:
    """
    Función helper para guardar un precio
    """
    db = PriceDatabase(db_path)
    return db.save_price(product)


def get_price_history(product_id: str, db_path: str = "data/prices.db") -> List[Dict]:
    """
    Función helper para obtener histórico de precios
    """
    db = PriceDatabase(db_path)
    return db.get_price_history(product_id)


def get_all_products(db_path: str = "data/prices.db") -> List[Dict]:
    """
    Función helper para obtener todos los productos
    """
    db = PriceDatabase(db_path)
    return db.get_all_products()


if __name__ == "__main__":
    # Ejemplo de uso
    print("=== Ejemplo de uso de la base de datos ===\n")
    
    db = PriceDatabase("data/prices.db")
    
    # Ejemplo de producto
    product = {
        'id': 'MLA-123456',
        'title': 'Notebook Test',
        'price': 500000.0,
        'link': 'https://example.com',
        'seller': 'Vendedor Test',
        'free_shipping': True
    }
    
    # Guardar precio
    db.save_price(product)
    print("✓ Precio guardado")
    
    # Ver estadísticas
    stats = db.get_stats()
    print(f"\nEstadísticas:")
    for key, value in stats.items():
        print(f"  {key}: {value}")