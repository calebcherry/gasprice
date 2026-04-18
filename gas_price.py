#!/usr/bin/env python3
"""
Fetch today's average gas price from AAA.
Usage: python gas_price.py or ./gas_price.py
"""

import requests
from bs4 import BeautifulSoup
import sys
import re


def get_gas_price():
    """Fetch the national average gas price from AAA."""
    try:
        # Headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        url = 'https://gasprices.aaa.com'
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Strategy 1: Look for price in common span patterns
        price_spans = soup.find_all('span', class_=lambda x: x and 'price' in x.lower())
        for span in price_spans:
            text = span.get_text(strip=True)
            if '$' in text:
                price = re.search(r'\$\d+\.\d{2}', text)
                if price:
                    return price.group()
        
        # Strategy 2: Look for any span containing dollar amounts
        for span in soup.find_all('span'):
            text = span.get_text(strip=True)
            if '$' in text:
                price = re.search(r'\$\d+\.\d{2}', text)
                if price:
                    return price.group()
        
        # Strategy 3: Search entire page for price pattern
        page_text = soup.get_text()
        prices = re.findall(r'\$\d+\.\d{2}', page_text)
        if prices:
            # Return the first match (typically the national average)
            return prices[0]
        
        return None
        
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing the data: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    price = get_gas_price()
    
    if price:
        print(f"National Average Gas Price (AAA): {price}")
        sys.exit(0)
    else:
        print("Error: Could not find gas price on AAA website.", file=sys.stderr)
        print("The website structure may have changed.", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
