from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from tcg_scraper import TCGScraper

app = FastAPI(title="SoloTCG - El Comparador de Precios TCG de Chile", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scraper = TCGScraper()

# Catálogo centralizado tipo SoloTodo
CATALOG = [
    {
        "id": "etb-phantasmal-flames",
        "name": "Elite Trainer Box Mega Evolution: Phantasmal Flames (Español)",
        "game": "Pokemon TCG",
        "category": "Elite Trainer Box (ETB)",
        "set": "Mega Evolution Series",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/SV04/SV04_EN_223.png",
        "stores": [
            {
                "name": "Collector Center",
                "price": 54990,
                "in_stock": True,
                "url": "https://collectorcenter.cl/products/preventa-14-11-25-mega-evolution-phantasmal-flames-elite-trainer-box-espanol",
                "shipping": "Envío a todo Chile"
            },
            {
                "name": "Magic4Ever",
                "price": 52990,
                "in_stock": True,
                "url": "https://magic4ever.cl",
                "shipping": "Despacho 24/48 hrs"
            },
            {
                "name": "La Guarida TCG",
                "price": 56990,
                "in_stock": False,
                "url": "https://laguaridatcg.cl",
                "shipping": "Retiro en Santiago"
            }
        ]
    },
    {
        "id": "bb-surging-sparks",
        "name": "Surging Sparks Booster Box (36 Sobres)",
        "game": "Pokemon TCG",
        "category": "Booster Box",
        "set": "Scarlet & Violet",
        "image": "https://images.pokemontcg.io/sv8/logo.png",
        "stores": [
            {
                "name": "Magic4Ever",
                "price": 139990,
                "in_stock": True,
                "url": "https://magic4ever.cl",
                "shipping": "Despacho gratuito"
            },
            {
                "name": "Collector Center",
                "price": 142990,
                "in_stock": True,
                "url": "https://collectorcenter.cl",
                "shipping": "Envío a todo Chile"
            },
            {
                "name": "Portal Magic",
                "price": 145000,
                "in_stock": True,
                "url": "https://portalmagic.cl",
                "shipping": "Envíos por Starken"
            }
        ]
    },
    {
        "id": "upc-151",
        "name": "Scarlet & Violet 151: Ultra Premium Collection (UPC)",
        "game": "Pokemon TCG",
        "category": "Colecciones Especiales",
        "set": "Pokemon 151",
        "image": "https://images.pokemontcg.io/sv3pt5/logo.png",
        "stores": [
            {
                "name": "Geekers Chile",
                "price": 118990,
                "in_stock": True,
                "url": "https://geekers.cl",
                "shipping": "Retiro en Providencia"
            },
            {
                "name": "Collector Center",
                "price": 124990,
                "in_stock": False,
                "url": "https://collectorcenter.cl",
                "shipping": "Envío a regiones"
            },
            {
                "name": "Zmart TCG",
                "price": 129990,
                "in_stock": True,
                "url": "https://zmart.cl",
                "shipping": "Despacho a domicilio"
            }
        ]
    },
    {
        "id": "bb-one-piece-op08",
        "name": "Two Legends Booster Box [OP-08]",
        "game": "One Piece TCG",
        "category": "Booster Box",
        "set": "OP-08 Two Legends",
        "image": "https://en.onepiece-cardgame.com/images/products/boosters/op08/package.png",
        "stores": [
            {
                "name": "La Guarida TCG",
                "price": 94990,
                "in_stock": True,
                "url": "https://laguaridatcg.cl",
                "shipping": "Envío a todo Chile"
            },
            {
                "name": "Magic4Ever",
                "price": 98990,
                "in_stock": True,
                "url": "https://magic4ever.cl",
                "shipping": "Retiro en local"
            }
        ]
    },
    {
        "id": "charizard-super-premium",
        "name": "Charizard ex Super Premium Collection",
        "game": "Pokemon TCG",
        "category": "Colecciones Especiales",
        "set": "Scarlet & Violet Specials",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/SV03/SV03_EN_125.png",
        "stores": [
            {
                "name": "Collector Center",
                "price": 79990,
                "in_stock": True,
                "url": "https://collectorcenter.cl",
                "shipping": "Envío a todo Chile"
            },
            {
                "name": "Sniper TCG",
                "price": 84990,
                "in_stock": True,
                "url": "https://snipertcg.cl",
                "shipping": "Despacho Starken / Chilexpress"
            }
        ]
    },
    {
        "id": "mtg-bloomburrow-bb",
        "name": "Bloomburrow Play Booster Box (36 Sobres)",
        "game": "Magic The Gathering",
        "category": "Booster Box",
        "set": "Bloomburrow 2024",
        "image": "https://media.wizards.com/2024/blb/en_header.png",
        "stores": [
            {
                "name": "Portal Magic",
                "price": 139990,
                "in_stock": True,
                "url": "https://portalmagic.cl",
                "shipping": "Envío gratis RM"
            },
            {
                "name": "Magic4Ever",
                "price": 144990,
                "in_stock": True,
                "url": "https://magic4ever.cl",
                "shipping": "Despacho inmediato"
            }
        ]
    },
    {
        "id": "bundle-stellar-crown",
        "name": "Stellar Crown Booster Bundle (6 Sobres)",
        "game": "Pokemon TCG",
        "category": "Booster Bundle",
        "set": "Scarlet & Violet",
        "image": "https://images.pokemontcg.io/sv7/logo.png",
        "stores": [
            {
                "name": "Collector Center",
                "price": 28990,
                "in_stock": True,
                "url": "https://collectorcenter.cl",
                "shipping": "Envío a regiones"
            },
            {
                "name": "Geekers Chile",
                "price": 29990,
                "in_stock": True,
                "url": "https://geekers.cl",
                "shipping": "Despacho 48 hrs"
            }
        ]
    }
]


class ScrapeRequest(BaseModel):
  url: str
  allow_simulation: bool = True


@app.get("/")
def index():
  return FileResponse("index.html")


@app.get("/api/catalog")
def get_catalog():
  return CATALOG


@app.post("/api/scrape")
def scrape_product(req: ScrapeRequest):
  result = scraper.fetch_product(req.url, allow_simulation=req.allow_simulation)
  if not result:
    raise HTTPException(status_code=404, detail="No se pudo obtener información del producto")
  return result.to_dict()


if __name__ == "__main__":
  uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)
