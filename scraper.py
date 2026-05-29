import json
import requests
from bs4 import BeautifulSoup

def scrape_all_telcos():
    # Define your 3 target websites, their structures, and specific HTML configurations
    targets = [
        {
            "id": "telco_1",
            "name": "Xfinity",
            "url": "https://www.xfinity.com/learn/internet-service", # Example Target 1
            "card_tag": "div", "card_class": "promo-card",
            "title_tag": "h3", "title_class": "promo-title",
            "desc_tag": "p", "desc_class": "promo-desc"
        },
        {
            "id": "telco_2",
            "name": "Xfinity Mobile",
            "url": "https://www.xfinity.com/mobile/", # Example Target 2
            "card_tag": "div", "card_class": "deal-wrapper",
            "title_tag": "h2", "title_class": "deal-heading",
            "desc_tag": "div", "desc_class": "deal-copy"
        },
        {
            "id": "telco_3",
            "name": "Xfinity Now",
            "url": "https://www.xfinity.com/now", # Example Target 3
            "card_tag": "section", "card_class": "offer-tile",
            "title_tag": "span", "title_class": "tile-title",
            "desc_tag": "p", "desc_class": "tile-description"
        }
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    master_promo_list = []

    for target in targets:
        print(f"Scraping active deals from: {target['name']}...")
        try:
            response = requests.get(target["url"], headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"Skipping {target['name']}: Received status code {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all(target["card_tag"], class_=target["card_class"])
            
            for card in cards:
                title_el = card.find(target["title_tag"], class_=target["title_class"])
                desc_el = card.find(target["desc_tag"], class_=target["desc_class"])
                
                if title_el:
                    title = title_el.text.strip()
                    desc = desc_el.text.strip() if desc_el else "Click to view deal specs."
                    
                    master_promo_list.append({
                        "provider": target["name"],
                        "title": title,
                        "description": desc,
                        "source_url": target["url"] # Saves origin link for the frontend hyperlink
                    })
        except Exception as e:
            print(f"Failed parsing {target['name']}: {str(e)}")

    # Overwrite the shared database file with findings across all 3 platforms
    with open('promos.json', 'w', encoding='utf-8') as f:
        json.dump(master_promo_list, f, indent=4, ensure_ascii=False)
        
    print(f"Master Sync Complete. {len(master_promo_list)} total promotions stored.")

if __name__ == "__main__":
    scrape_all_telcos()
