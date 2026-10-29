# SoloTCG - Comparador de Precios TCG Chile ⚡

Plataforma y cotizador web inspirado en el modelo de **SoloTodo**, diseñado para comparar precios, disponibilidad y stock de cartas y productos coleccionables (Pokémon TCG, One Piece TCG, Magic: The Gathering) a través de distintas tiendas en Chile.

## 🚀 Características
- **Catálogo Multi-Tienda estilo SoloTodo:** Filtro por juego, categoría (ETB, Booster Box, Bundles, etc.), búsqueda por texto y ordenamiento por menor precio (*"Desde $XX.XXX"*).
- **Desglose Comparativo:** Modal con tabla comparativa de tiendas (Collector Center, Magic4Ever, La Guarida, Geekers, etc.) con stock y enlace directo de compra.
- **Scraper Inteligente (`tcg_scraper.py`):**
  - Detección de endpoints JSON nativos en tiendas basadas en Shopify (`/products/<slug>.json`).
  - Fallback con extracción de metaetiquetas OpenGraph y Schema.org con `BeautifulSoup`.
  - Modo resiliente con fallback simulado en caso de bloqueos por firewalls corporativos o errores de conexión.
- **Importador de Enlaces:** Permite ingresar URLs individuales para extraer e indexar productos directamente al catálogo.

## 📦 Estructura del Proyecto
```text
coti/
├── app.py             # Servidor web FastAPI y frontend interactivo
├── tcg_scraper.py     # Motor de scraping y extracción de datos
├── requirements.txt   # Dependencias de Python
├── run.bat            # Script de ejecución rápida para Windows
├── .gitignore         # Exclusión de archivos temporales y entornos
└── README.md          # Documentación del proyecto
```

## 🛠️ Instalación y Uso Local

1. **Clonar el repositorio:**
   ```bash
   git clone <tu-repositorio-url>
   cd coti
   ```

2. **Crear y activar un entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```
   *O en Windows haciendo doble clic en `run.bat`.*

5. **Abrir en el navegador:**
   [http://localhost:8000](http://localhost:8000)

## 📄 Licencia
MIT
