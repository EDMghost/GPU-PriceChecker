from playwright.sync_api import sync_playwright
import re


class ArukeresoScraper:
    def __init__(self, headless=True):
        self.headless = headless

    def scrape_gpu(self, gpu_model: str, target_price: int):
        """Scrape Arukereso for a GPU and return top 10 closest matches."""
        search_query = gpu_model.replace(" ", "-")
        url = f"https://www.arukereso.hu/videokartya-c3142/{search_query}/?orderby=1"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(url)

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

            browser.close()

        if not products:
            return gpu_model, target_price, []

        # Sort by closest to target price
        products.sort(key=lambda x: abs(x[1] - target_price))

        return gpu_model, target_price, products[:10]
