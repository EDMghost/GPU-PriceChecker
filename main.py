import asyncio
from concurrent.futures import ThreadPoolExecutor

from playwright.async_api import async_playwright

from Scraper.DE_IdealoScraper import IdealoScraper
from Scraper.HUN_ArukeresoScraper import ArukeresoScraper
from Scraper.RO_PriceScraper import PriceScraper

#  ----------------------  HUNGARIAN PRICES  ---------------------------

print(f"\n -----------------------------------------  HUNGARIAN PRICES  ----------------------------------------- \n")

hun_gpu_targets = [
    ("rx 9070", 200_000),
    ("rx 9070 xt", 260_000),
    ("rtx 5070", 230_000),
    ("rtx 5070 ti", 320_000),
    ("rtx 5080", 400_000),
]

scraper = ArukeresoScraper(headless=True)

# Use threads
hun_results = []
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(scraper.scrape_gpu, gpu, price) for gpu, price in hun_gpu_targets]
    for f in futures:
        hun_results.append(f.result())

# Print in original order
NAME_WIDTH = 75
for gpu_model, target_price, products in hun_results:
    if not products:
        print(f"No products found for {gpu_model}.\n")
        continue
    print(f"Closest matches for {gpu_model.upper()} to {target_price:,} Ft:")
    for name, price in products:
        diff = price - target_price
        sign = "+" if diff >= 0 else "-"
        print(f"{name:<{NAME_WIDTH}} → {price:>10,} Ft ({sign}{abs(diff):,} Ft)")
    print("\n")

#  ----------------------  ROMANIAN PRICES  ---------------------------

print(f"\n -----------------------------------------  ROMANIAN PRICES  ----------------------------------------- \n")

ro_gpu_targets = [
    ("radeon rx 9070", 3000),
    ("radeon rx 9070 xt", 3500),
    ("geforce rtx 5070", 3000),
    ("geforce rtx 5070 ti", 4500),
    ("geforce rtx 5080", 6000)
]

scraper = PriceScraper(headless=True)

# Use threads
ro_results = []
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(scraper.scrape_gpu, gpu, price) for gpu, price in ro_gpu_targets]
    for f in futures:
        ro_results.append(f.result())

# Print in original order
NAME_WIDTH = 75
for gpu_model, target_price, products in ro_results:
    if not products:
        print(f"No products found for {gpu_model}.\n")
        continue
    print(f"Closest matches for {gpu_model.upper()} to {target_price:,} LEI:")
    for name, price in products:
        diff = price - target_price
        sign = "+" if diff >= 0 else "-"
        print(f"{name:<{NAME_WIDTH}} → {price:>10,} LEI ({sign}{abs(diff):,} LEI)")
    print("\n")

#  ----------------------  GERMAN PRICES  ---------------------------

de_gpu_targets = [
    ("106595217", 550),  # RX 9070
    ("106595216", 600),  # RX 9070 XT
    ("106595215", 550),  # RTX 5070
    ("106572994", 750),  # RTX 5070 TI
    ("105524075", 1000)  # RTX 5080
]
