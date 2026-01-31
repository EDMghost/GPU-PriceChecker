from Runner.PriceCheck import run_price_check
from Scraper.ArukeresoScraper import ArukeresoScraper
from Scraper.PriceRoScraper import PriceScraper
from Scraper.GeizhalsScraper import GeizhalsScraper

# ---------------------- HUNGARY ----------------------

hun_gpu_targets = [
    ("rx 9070", 200_000),
    ("rx 9070 xt", 260_000),
    ("rtx 5070", 230_000),
    ("rtx 5070 ti", 320_000),
    ("rtx 5080", 400_000),
]

run_price_check(
    title="HUNGARIAN PRICES",
    scraper=ArukeresoScraper(headless=True),
    gpu_targets=hun_gpu_targets,
    currency="Ft"
)

# ---------------------- ROMANIA ----------------------

ro_gpu_targets = [
    ("radeon rx 9070", 3000),
    ("radeon rx 9070 xt", 3500),
    ("geforce rtx 5070", 3000),
    ("geforce rtx 5070 ti", 4500),
    ("geforce rtx 5080", 6000),
]

run_price_check(
    title="ROMANIAN PRICES",
    scraper=PriceScraper(headless=True),
    gpu_targets=ro_gpu_targets,
    currency="LEI"
)

# ---------------------- GERMANY ----------------------

de_gpu_targets = [
    ("RX 9070", 550),
    ("RX 9070 XT", 600),
    ("RTX 5070", 550),
    ("RTX 5070 Ti", 750),
    ("RTX 5080", 1000),
]

run_price_check(
    title="GERMAN PRICES",
    scraper=GeizhalsScraper(headless=True),
    gpu_targets=de_gpu_targets,
    currency="EUR"
)
