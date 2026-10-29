import json
from dataclasses import dataclass, asdict
from typing import Optional
from bs4 import BeautifulSoup
import httpx


@dataclass
class TCGProductData:
  title: str
  price_clp: int
  in_stock: bool
  currency: str
  source_url: str
  image_url: Optional[str] = None
  vendor: Optional[str] = None
  is_simulated: bool = False

  def to_dict(self):
    return asdict(self)


class TCGScraper:

  def __init__(self):
    self.headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "es-CL,es;q=0.9",
    }

  def _generate_mock_data(self, url: str) -> TCGProductData:
    """Genera datos de simulación basados en la URL cuando la red bloquea la petición."""
    slug = url.split("?")[0].rstrip("/").split("/")[-1].replace("-", " ").title()
    if not slug or slug.startswith("Http"):
      slug = "Pokemon TCG Booster Bundle / ETB Especial"

    # Imagen representativa por defecto de alta calidad
    mock_image = "https://images.pokemontcg.io/sv3pt5/logo.png"
    if "phantasmal" in url.lower() or "mega" in url.lower():
      slug = "Preventa: Mega Evolution Phantasmal Flames - Elite Trainer Box (Español)"
      mock_image = "https://assets.pokemon.com/assets/cms2/img/cards/web/SV04/SV04_EN_223.png"

    return TCGProductData(
        title=slug,
        price_clp=54990,
        in_stock=True,
        currency="CLP",
        source_url=url,
        image_url=mock_image,
        vendor="Collector Center (Simulado)",
        is_simulated=True,
    )

  def fetch_product(self, url: str, allow_simulation: bool = False) -> Optional[TCGProductData]:
    clean_url = url.split("?")[0].rstrip("/")
    blocked_by_network = False

    # 1. Endpoint .json (Shopify)
    if "/products/" in clean_url:
      json_url = f"{clean_url}.json"
      try:
        with httpx.Client(
            headers=self.headers, timeout=10.0, verify=False
        ) as client:
          resp = client.get(json_url)
          if resp.status_code == 200:
            product = resp.json().get("product", {})
            variants = product.get("variants", [{}])
            first_variant = variants[0] if variants else {}

            price = int(float(first_variant.get("price", 0)))
            available = first_variant.get("available", False)
            title = product.get("title", "")
            vendor = product.get("vendor", "")

            # Obtener imagen si existe
            images = product.get("images", [])
            image_url = images[0].get("src") if images else None

            if title and price > 0:
              return TCGProductData(
                  title=title,
                  price_clp=price,
                  in_stock=available,
                  currency="CLP",
                  source_url=url,
                  image_url=image_url,
                  vendor=vendor,
              )
          elif resp.status_code == 403:
            blocked_by_network = True
      except Exception as e:
        print(f"Intento por JSON falló: {e}")

    # 2. Si no es Shopify o falla el JSON, analizamos el HTML estándar
    try:
      with httpx.Client(
          headers=self.headers, timeout=15.0, follow_redirects=True, verify=False
      ) as client:
        response = client.get(url)
        if response.status_code == 403:
          blocked_by_network = True
        response.raise_for_status()

      soup = BeautifulSoup(response.text, "html.parser")
      og_title = soup.find("meta", property="og:title")
      title = (
          og_title["content"].strip()
          if og_title
          else (soup.title.string.strip() if soup.title else "Producto TCG")
      )

      og_image = soup.find("meta", property="og:image")
      image_url = og_image["content"].strip() if og_image else None

      og_price = soup.find("meta", property="product:price:amount") or soup.find("meta", property="og:price:amount")
      price = int(float(og_price["content"])) if og_price else 0

      return TCGProductData(
          title=title,
          price_clp=price,
          in_stock=True,
          currency="CLP",
          source_url=url,
          image_url=image_url,
      )

    except Exception as e:
      print(f"Error al conectar con la URL: {e}")
      if (blocked_by_network or allow_simulation):
        print("Activando respuesta simulada debido al bloqueo de red o solicitud de simulación.")
        return self._generate_mock_data(url)
      return None


if __name__ == "__main__":
  scraper = TCGScraper()
  url_prueba = "https://collectorcenter.cl/products/preventa-14-11-25-mega-evolution-phantasmal-flames-elite-trainer-box-espanol"

  print("Consultando producto en Collector Center...")
  resultado = scraper.fetch_product(url_prueba, allow_simulation=True)

  if resultado:
    print("\n===============================")
    print(f"Producto:   {resultado.title}")
    print(f"Precio:     ${resultado.price_clp:,.0f} {resultado.currency}")
    print(f"Disponible: {'Sí' if resultado.in_stock else 'Agotado'}")
    print(f"URL:        {resultado.source_url}")
    if resultado.is_simulated:
      print("(Nota: Datos de demostración visual por filtro FortiGuard)")
    print("===============================\n")
  else:
    print("No se pudo obtener la información.")
