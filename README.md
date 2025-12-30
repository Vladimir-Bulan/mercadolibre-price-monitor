# 🛍️ MercadoLibre Price Monitor Pro

**Sistema profesional de monitoreo de precios** para MercadoLibre con interfaz web moderna, tracking automático y análisis visual en tiempo real.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52-red)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## ✨ Características

🔍 **Búsqueda Real** - Scraping con Selenium + Brave  
📊 **Historial Automático** - 7 puntos generados al trackear  
📈 **Gráficos Profesionales** - 3 líneas: precio/promedio/mínimo  
🔔 **Alertas Inteligentes** - Detecta caídas ≥15%  
🎨 **Diseño Moderno** - Interfaz profesional sin emojis  
💾 **Session-Based** - Sin base de datos, todo en memoria  

---

## 🖼️ Screenshots

### Dashboard
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/7ac5ac93-be15-4bde-a835-1af0ba0750e2" />


### Búsqueda
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/634a113b-5712-479a-8f6c-91e676b8f890" />



### Analytics
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/42be3220-9775-415b-bd18-6f3bb6048ac6" />


---

## 🚀 Instalación

```bash
# Clonar
git clone https://github.com/Vladimir-Bulan/mercadolibre-price-monitor.git
cd mercadolibre-price-monitor

# Instalar
pip install -r requirements.txt

# Ejecutar
streamlit run app.py
```

---

## 📖 Uso

1. **Search Products** → Buscar "notebook"
2. **+ Track** → Agregar a tracking (historial automático)
3. **Analytics** → Ver gráficos completos
4. **Dashboard** → Filtrar y ordenar productos

---

## 🛠️ Stack

- Streamlit (Frontend)
- Selenium + Brave (Scraping)
- Plotly (Gráficos)
- Pandas (Data)
- Session State (Storage)

---

## 📂 Estructura

```
mercadolibre-price-monitor/
├── app.py              # App principal
├── scraper.py          # Selenium scraper
├── .streamlit/
│   └── config.toml
├── screenshots/
└── requirements.txt
```

---

## 👨‍💻 Autor

**Vladimir Bulan**  
GitHub: [@Vladimir-Bulan](https://github.com/Vladimir-Bulan)

---

⭐ Si te gustó, dale una estrella!
