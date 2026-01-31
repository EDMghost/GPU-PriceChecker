from playwright.sync_api import sync_playwright
import re

from Runner.Delay import human_delay


class ArukeresoScraper:
    def __init__(self, headless=False):
        self.headless = headless

    def scrape_gpu(self, gpu_model: str, target_price: int):
        """Scrape Arukereso for a GPU and return top 10 closest matches."""
        search_query = gpu_model.replace(" ", "-")
        url = f"https://www.arukereso.hu/videokartya-c3142/{search_query}/?orderby=1"

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
            human_delay(2, 5)

            page.wait_for_selector("a.price")

            products = []
            for a in page.query_selector_all("a.price"):
                name = a.get_attribute("title")
                if not name:
                    continue
                # Remove last 35 characters
                name = name[:-35].strip()

                price_text = a.inner_text().strip()
                price = int(re.sub(r"[^\d]", "", price_text))
                products.append((name, price))
                human_delay(0.05, 0.15)

            browser.close()

        if not products:
            return gpu_model, target_price, []

        # Sort by closest to target price
        products.sort(key=lambda x: abs(x[1] - target_price))

        return gpu_model, target_price, products[:10]
