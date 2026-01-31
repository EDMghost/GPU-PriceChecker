from playwright.sync_api import sync_playwright
import re

from Runner.Delay import human_delay


class PriceScraper:
    def __init__(self, headless=False):
        self.headless = headless

    def scrape_gpu(self, gpu_model: str, target_price: int):
        """Scrape Price.ro for a GPU and return top 10 closest matches."""
        search_query = gpu_model.replace(" ", "+")
        url = f"https://www.price.ro/index.php?action=produse&f=1&categ_url=placi-grafice&chipset={search_query}&orderBy=pret&asc=1"

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=self.headless,
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1366, "height": 768}
            )
            page.goto(url)
            human_delay(3, 6)

            # Wait a little for JS to load
            page.wait_for_timeout(2000)

            # Grab product containers
            product_elements = page.query_selector_all("div.produs-lista.box-shadow")

            products_list = []
            for product in product_elements:
                name_el = product.query_selector("b.titlu.-std")
                price_el = product.query_selector("a.price.-std.mt\\:full")
                if not name_el or not price_el:
                    continue

                name = name_el.inner_text().strip()
                price_text = price_el.inner_text().strip()  # "2.640,99lei"
                price_clean = re.sub(r"[^\d,\.]", "", price_text)  # remove everything except digits, comma, dot
                price = int(float(price_clean.replace(".", "").replace(",", ".")))

                products_list.append((name, price))
                human_delay(0.1, 0.25)

            browser.close()

        if not products_list:
            return gpu_model, target_price, []

        # Sort by closest to target price
        products_list.sort(key=lambda x: abs(x[1] - target_price))

        return gpu_model, target_price, products_list[:10]
