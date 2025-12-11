"""
Módulo de Análisis y Visualización
Contiene funciones para analizar datos de precios y crear gráficos
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import numpy as np


# Configuración de estilo para matplotlib
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class PriceAnalyzer:
    """
    Clase para analizar datos de precios
    """
    
    def __init__(self, price_history: List[Dict]):
        """
        Inicializa el analizador con histórico de precios
        
        Args:
            price_history: Lista de diccionarios con precios históricos
        """
        self.df = pd.DataFrame(price_history)
        
        if not self.df.empty:
            # Convertir scraped_at a datetime
            self.df['scraped_at'] = pd.to_datetime(self.df['scraped_at'])
            self.df = self.df.sort_values('scraped_at')
    
    def get_statistics(self) -> Dict:
        """
        Calcula estadísticas básicas del precio
        
        Returns:
            Diccionario con estadísticas
        """
        if self.df.empty:
            return {}
        
        return {
            'precio_actual': self.df['price'].iloc[-1],
            'precio_minimo': self.df['price'].min(),
            'precio_maximo': self.df['price'].max(),
            'precio_promedio': self.df['price'].mean(),
            'precio_mediana': self.df['price'].median(),
            'desviacion_estandar': self.df['price'].std(),
            'variacion_porcentual': self._calculate_variation(),
            'total_registros': len(self.df),
            'fecha_primer_registro': self.df['scraped_at'].iloc[0],
            'fecha_ultimo_registro': self.df['scraped_at'].iloc[-1]
        }
    
    def _calculate_variation(self) -> float:
        """
        Calcula la variación porcentual del precio
        
        Returns:
            Variación en porcentaje
        """
        if len(self.df) < 2:
            return 0.0
        
        first_price = self.df['price'].iloc[0]
        last_price = self.df['price'].iloc[-1]
        
        return ((last_price - first_price) / first_price) * 100
    
    def plot_price_evolution(self, save_path: Optional[str] = None, interactive: bool = True):
        """
        Genera gráfico de evolución de precios
        
        Args:
            save_path: Ruta para guardar el gráfico (opcional)
            interactive: Si True, usa Plotly (interactivo), sino Matplotlib
        """
        if self.df.empty:
            print("No hay datos para graficar")
            return
        
        if interactive:
            self._plot_plotly(save_path)
        else:
            self._plot_matplotlib(save_path)
    
    def _plot_plotly(self, save_path: Optional[str] = None):
        """
        Crea gráfico interactivo con Plotly
        """
        fig = go.Figure()
        
        # Línea de precios
        fig.add_trace(go.Scatter(
            x=self.df['scraped_at'],
            y=self.df['price'],
            mode='lines+markers',
            name='Precio',
            line=dict(color='#2E86AB', width=2),
            marker=dict(size=8),
            hovertemplate='<b>Fecha:</b> %{x}<br><b>Precio:</b> $%{y:,.0f}<extra></extra>'
        ))
        
        # Línea de precio promedio
        avg_price = self.df['price'].mean()
        fig.add_hline(
            y=avg_price,
            line_dash="dash",
            line_color="green",
            annotation_text=f"Promedio: ${avg_price:,.0f}",
            annotation_position="right"
        )
        
        # Línea de precio mínimo
        min_price = self.df['price'].min()
        fig.add_hline(
            y=min_price,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mínimo: ${min_price:,.0f}",
            annotation_position="right"
        )
        
        title = self.df['title'].iloc[0] if 'title' in self.df.columns else 'Producto'
        
        fig.update_layout(
            title=f'Evolución de Precio - {title}',
            xaxis_title='Fecha',
            yaxis_title='Precio (ARS)',
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        if save_path:
            fig.write_html(save_path)
            print(f"✓ Gráfico guardado en: {save_path}")
        else:
            fig.show()
    
    def _plot_matplotlib(self, save_path: Optional[str] = None):
        """
        Crea gráfico estático con Matplotlib
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Línea de precios
        ax.plot(self.df['scraped_at'], self.df['price'], 
                marker='o', linewidth=2, markersize=6, label='Precio')
        
        # Línea de precio promedio
        avg_price = self.df['price'].mean()
        ax.axhline(y=avg_price, color='green', linestyle='--', 
                   label=f'Promedio: ${avg_price:,.0f}')
        
        # Línea de precio mínimo
        min_price = self.df['price'].min()
        ax.axhline(y=min_price, color='red', linestyle='--', 
                   label=f'Mínimo: ${min_price:,.0f}')
        
        title = self.df['title'].iloc[0] if 'title' in self.df.columns else 'Producto'
        
        ax.set_title(f'Evolución de Precio - {title}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel('Precio (ARS)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Gráfico guardado en: {save_path}")
        else:
            plt.show()
    
    def plot_price_distribution(self, save_path: Optional[str] = None):
        """
        Genera histograma de distribución de precios
        
        Args:
            save_path: Ruta para guardar el gráfico
        """
        if self.df.empty:
            print("No hay datos para graficar")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(self.df['price'], bins=20, edgecolor='black', alpha=0.7)
        ax.axvline(self.df['price'].mean(), color='red', linestyle='--', 
                   linewidth=2, label=f"Media: ${self.df['price'].mean():,.0f}")
        ax.axvline(self.df['price'].median(), color='green', linestyle='--', 
                   linewidth=2, label=f"Mediana: ${self.df['price'].median():,.0f}")
        
        ax.set_title('Distribución de Precios', fontsize=14, fontweight='bold')
        ax.set_xlabel('Precio (ARS)', fontsize=12)
        ax.set_ylabel('Frecuencia', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Gráfico guardado en: {save_path}")
        else:
            plt.show()
    
    def detect_best_time_to_buy(self) -> Dict:
        """
        Analiza el mejor momento para comprar basándose en patrones
        
        Returns:
            Diccionario con recomendación
        """
        if len(self.df) < 7:
            return {'recommendation': 'Necesitas más datos históricos'}
        
        current_price = self.df['price'].iloc[-1]
        avg_price = self.df['price'].mean()
        min_price = self.df['price'].min()
        
        percentage_below_avg = ((avg_price - current_price) / avg_price) * 100
        percentage_above_min = ((current_price - min_price) / min_price) * 100
        
        if current_price <= min_price * 1.05:  # Dentro del 5% del mínimo
            recommendation = "¡EXCELENTE momento para comprar! Precio cerca del mínimo histórico"
            score = 5
        elif current_price <= avg_price * 0.95:  # 5% debajo del promedio
            recommendation = "Buen momento para comprar. Precio por debajo del promedio"
            score = 4
        elif current_price <= avg_price * 1.05:  # Cerca del promedio
            recommendation = "Momento aceptable. Precio cerca del promedio"
            score = 3
        elif current_price <= avg_price * 1.15:  # Hasta 15% sobre promedio
            recommendation = "Considera esperar. Precio sobre el promedio"
            score = 2
        else:
            recommendation = "Mejor esperar. Precio muy alto comparado con el histórico"
            score = 1
        
        return {
            'recommendation': recommendation,
            'score': score,
            'current_price': current_price,
            'average_price': avg_price,
            'min_price': min_price,
            'percentage_below_avg': percentage_below_avg,
            'percentage_above_min': percentage_above_min
        }


def plot_price_evolution(price_history: List[Dict], save_path: Optional[str] = None, 
                        interactive: bool = True):
    """
    Función helper para graficar evolución de precios
    
    Args:
        price_history: Lista de diccionarios con histórico
        save_path: Ruta para guardar (opcional)
        interactive: Usar gráfico interactivo o estático
    """
    analyzer = PriceAnalyzer(price_history)
    analyzer.plot_price_evolution(save_path, interactive)


def get_price_statistics(price_history: List[Dict]) -> Dict:
    """
    Función helper para obtener estadísticas
    
    Args:
        price_history: Lista de diccionarios con histórico
        
    Returns:
        Diccionario con estadísticas
    """
    analyzer = PriceAnalyzer(price_history)
    return analyzer.get_statistics()


def compare_products(products_data: List[Dict], save_path: Optional[str] = None):
    """
    Compara precios de múltiples productos
    
    Args:
        products_data: Lista de diccionarios con datos de productos
        save_path: Ruta para guardar el gráfico
    """
    if not products_data:
        print("No hay datos para comparar")
        return
    
    fig = go.Figure()
    
    for product in products_data:
        df = pd.DataFrame(product['history'])
        df['scraped_at'] = pd.to_datetime(df['scraped_at'])
        
        fig.add_trace(go.Scatter(
            x=df['scraped_at'],
            y=df['price'],
            mode='lines+markers',
            name=product['name'][:30] + '...',
            hovertemplate='<b>%{fullData.name}</b><br>Fecha: %{x}<br>Precio: $%{y:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Comparación de Precios entre Productos',
        xaxis_title='Fecha',
        yaxis_title='Precio (ARS)',
        hovermode='x unified',
        template='plotly_white',
        height=600
    )
    
    if save_path:
        fig.write_html(save_path)
        print(f"✓ Gráfico de comparación guardado en: {save_path}")
    else:
        fig.show()


if __name__ == "__main__":
    # Ejemplo de uso
    print("=== Ejemplo de análisis ===\n")
    
    # Datos de ejemplo
    example_data = [
        {'price': 50000, 'scraped_at': '2024-01-01', 'title': 'Producto Test'},
        {'price': 48000, 'scraped_at': '2024-01-02', 'title': 'Producto Test'},
        {'price': 52000, 'scraped_at': '2024-01-03', 'title': 'Producto Test'},
        {'price': 47000, 'scraped_at': '2024-01-04', 'title': 'Producto Test'},
    ]
    
    analyzer = PriceAnalyzer(example_data)
    stats = analyzer.get_statistics()
    
    print("Estadísticas:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
