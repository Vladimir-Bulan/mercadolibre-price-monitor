"""
Módulo de Utilidades
Funciones auxiliares y helpers generales
"""

import json
from datetime import datetime
from typing import Dict, List
import os


def format_price(price: float) -> str:
    """
    Formatea un precio para mostrar en pesos argentinos
    
    Args:
        price: Precio como float
        
    Returns:
        String formateado (ej: "$45.999")
    """
    return f"${price:,.0f}".replace(",", ".")


def calculate_percentage_change(old_price: float, new_price: float) -> float:
    """
    Calcula el cambio porcentual entre dos precios
    
    Args:
        old_price: Precio anterior
        new_price: Precio nuevo
        
    Returns:
        Cambio en porcentaje
    """
    if old_price == 0:
        return 0
    
    return ((new_price - old_price) / old_price) * 100


def export_to_json(data: List[Dict], filepath: str):
    """
    Exporta datos a un archivo JSON
    
    Args:
        data: Lista de diccionarios a exportar
        filepath: Ruta del archivo de destino
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"✓ Datos exportados a: {filepath}")
        
    except Exception as e:
        print(f"Error exportando a JSON: {e}")


def import_from_json(filepath: str) -> List[Dict]:
    """
    Importa datos desde un archivo JSON
    
    Args:
        filepath: Ruta del archivo a importar
        
    Returns:
        Lista de diccionarios con los datos
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✓ Datos importados desde: {filepath}")
        return data
        
    except Exception as e:
        print(f"Error importando desde JSON: {e}")
        return []


def print_product_summary(product: Dict):
    """
    Imprime un resumen formateado de un producto
    
    Args:
        product: Diccionario con información del producto
    """
    print("\n" + "="*60)
    print(f"📦 {product.get('title', 'Sin título')}")
    print("="*60)
    print(f"💰 Precio: {format_price(product.get('price', 0))}")
    print(f"🏪 Vendedor: {product.get('seller', 'Desconocido')}")
    print(f"🚚 Envío gratis: {'Sí' if product.get('free_shipping', False) else 'No'}")
    print(f"🔗 ID: {product.get('id', 'N/A')}")
    print(f"📅 Fecha: {product.get('scraped_at', 'N/A')}")
    
    if product.get('link'):
        print(f"🌐 Link: {product['link']}")
    
    print("="*60 + "\n")


def create_price_alert(current_price: float, threshold: float, 
                       product_title: str) -> str:
    """
    Crea un mensaje de alerta de precio
    
    Args:
        current_price: Precio actual
        threshold: Umbral de precio deseado
        product_title: Título del producto
        
    Returns:
        Mensaje de alerta formateado
    """
    if current_price <= threshold:
        return f"""
🔔 ¡ALERTA DE PRECIO!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Producto: {product_title}
💰 Precio actual: {format_price(current_price)}
🎯 Tu objetivo: {format_price(threshold)}
✅ El producto está dentro de tu rango de precio!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
    else:
        difference = current_price - threshold
        percentage = (difference / threshold) * 100
        return f"""
📊 Actualización de precio
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Producto: {product_title}
💰 Precio actual: {format_price(current_price)}
🎯 Tu objetivo: {format_price(threshold)}
📈 Diferencia: {format_price(difference)} ({percentage:.1f}% más caro)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """


def generate_report(products: List[Dict]) -> str:
    """
    Genera un reporte de texto con resumen de productos
    
    Args:
        products: Lista de productos
        
    Returns:
        String con el reporte formateado
    """
    report = []
    report.append("\n" + "="*70)
    report.append("📊 REPORTE DE PRECIOS - MERCADOLIBRE")
    report.append("="*70)
    report.append(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    report.append(f"📦 Total de productos: {len(products)}")
    report.append("="*70 + "\n")
    
    for i, product in enumerate(products, 1):
        report.append(f"{i}. {product.get('title', 'Sin título')[:60]}")
        report.append(f"   💰 Precio: {format_price(product.get('price', 0))}")
        report.append(f"   🏪 Vendedor: {product.get('seller', 'Desconocido')}")
        report.append(f"   🔗 ID: {product.get('id', 'N/A')}")
        report.append("")
    
    report.append("="*70)
    
    return "\n".join(report)


def save_report(content: str, filepath: str):
    """
    Guarda un reporte en un archivo de texto
    
    Args:
        content: Contenido del reporte
        filepath: Ruta del archivo de destino
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Reporte guardado en: {filepath}")
        
    except Exception as e:
        print(f"Error guardando reporte: {e}")


def get_price_change_emoji(change_percent: float) -> str:
    """
    Retorna un emoji según el cambio de precio
    
    Args:
        change_percent: Porcentaje de cambio
        
    Returns:
        Emoji apropiado
    """
    if change_percent < -10:
        return "📉💚 ¡Gran bajada!"
    elif change_percent < -5:
        return "📉 Bajó"
    elif change_percent < 5:
        return "➡️ Estable"
    elif change_percent < 10:
        return "📈 Subió"
    else:
        return "📈🔴 ¡Gran subida!"


def validate_product_data(product: Dict) -> bool:
    """
    Valida que un producto tenga los campos mínimos necesarios
    
    Args:
        product: Diccionario del producto
        
    Returns:
        True si es válido, False si no
    """
    required_fields = ['id', 'title', 'price']
    
    for field in required_fields:
        if field not in product or product[field] is None:
            print(f"⚠️ Producto inválido: falta el campo '{field}'")
            return False
    
    if not isinstance(product['price'], (int, float)) or product['price'] < 0:
        print(f"⚠️ Producto inválido: precio no válido")
        return False
    
    return True


def clean_title(title: str, max_length: int = 100) -> str:
    """
    Limpia y trunca el título de un producto
    
    Args:
        title: Título original
        max_length: Longitud máxima
        
    Returns:
        Título limpio
    """
    # Remover espacios extras
    title = " ".join(title.split())
    
    # Truncar si es muy largo
    if len(title) > max_length:
        title = title[:max_length-3] + "..."
    
    return title


if __name__ == "__main__":
    # Ejemplos de uso
    print("=== Ejemplos de utilidades ===\n")
    
    # Formato de precio
    print(f"Precio formateado: {format_price(45999.50)}")
    
    # Cambio porcentual
    change = calculate_percentage_change(50000, 45000)
    print(f"Cambio porcentual: {change:.2f}%")
    print(f"Emoji: {get_price_change_emoji(change)}")
    
    # Producto de ejemplo
    product = {
        'id': 'MLA-123',
        'title': 'Notebook Test',
        'price': 45000,
        'seller': 'Tienda Test',
        'free_shipping': True
    }
    
    print_product_summary(product)
