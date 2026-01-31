from concurrent.futures import ThreadPoolExecutor

def run_price_check(
    *,
    title: str,
    scraper,
    gpu_targets: list[tuple[str, int]],
    currency: str,
    max_workers: int = 1,
    name_width: int = 100
):
    print(f"\n{'-' * 41}  {title}  {'-' * 41}\n")

    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(scraper.scrape_gpu, gpu, price)
            for gpu, price in gpu_targets
        ]
        for f in futures:
            results.append(f.result())

    for gpu_model, target_price, products in results:
        if not products:
            print(f"No products found for {gpu_model}.\n")
            continue

        print(f"Closest matches for {gpu_model.upper()} to {target_price:,} {currency}:")
        for name, price in products:
            diff = price - target_price
            sign = "+" if diff >= 0 else "-"
            print(
                f"{name:<{name_width}} → {price:>10,} {currency} "
                f"({sign}{abs(diff):,} {currency})"
            )
        print()
