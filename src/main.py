import os
import re
import csv
import json
import argparse
from typing import List
import logging
import requests

USAGE = "%(prog)s -i <input> -o <output>"
DESCRIPTION = "Webscrap Shopify stores"


def init_argparse() -> argparse.ArgumentParser:
    """Parse script arguments.

    Returns:
        ArgumentParser: parser object to read entered arguments

    """
    parser = argparse.ArgumentParser(
        usage=USAGE,
        description=DESCRIPTION
    )
    parser.add_argument("-i", "--input", action="store",
                        type=str, required=True)
    parser.add_argument("-o", "--output", action="store",
                        type=str, required=True)

    return parser


def file_exists(path: str) -> bool:
    """Check existance of the specified file

    Parameters:
        path (str): File path

    Returns:
        bool: True if the file path if file and if the file is readable

    """
    return os.path.isfile(path) and os.access(path, os.R_OK)


def load_page(url: str) -> str:
    """Load web page content from specified URL

    Parameters:
        url (str): Web page url

    Returns:
        str: Web page content

    """
    response = requests.get(url)

    if response.status_code < 200 or response.status_code >= 300:
        return None

    return response.text


def extract_pattern(pattern: str, text: str) -> str:
    """Extract first matching regex occurance in the text

    Parameters:
        pattern (str): Regex pattern
        text (str): Text to match pattern

    Returns:
        str: First matching occurance

    """
    finds = re.findall(pattern, text, re.IGNORECASE)

    if len(finds) < 1:
        return None

    return finds[0]


def extract_email(text: str) -> str:
    """Extract first email address occurance in the text

    Parameters:
        text (str): Text to search emails

    Returns:
        str: First found email address

    """
    pattern = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"

    finds = re.findall(pattern, text)

    if len(finds) < 1:
        return None

    for find in finds:
        # Return first non-image
        if not find.lower().endswith(("jpg", "jpeg", "png", "gif", "bmp")):
            return find

    return None


def extract_twitter_link(text: str) -> str:
    """Extract first twitter link occurance in the text

    Parameters:
        text (str): Text to search links

    Returns:
        str: First found twitter link

    """
    pattern = r"(http(?:s)?:\/\/(?:www\.)?twitter\.com\/[a-zA-Z0-9_]+)"

    return extract_pattern(pattern, text)


def extract_facebook_link(text: str) -> str:
    """Extract first facebook link occurance in the text

    Parameters:
        text (str): Text to search links

    Returns:
        str: First found facebook link

    """
    pattern = r"(http(?:s)?:\/\/(?:www\.)?facebook\.com\/[a-zA-Z0-9_]+)"

    return extract_pattern(pattern, text)


def extract_product_handles(text: str, limit: int) -> List[str]:
    """Extract first <limit> product handles

    Parameters:
        text (str): Text to search product handles

    Returns:
        List[str]: List of found product handles

    """
    pattern = r"\/collections\/all\/products\/([a-zA-Z0-9_-]+)\""

    handles = re.findall(pattern, text)

    if len(handles) < 1:
        return []

    # Remove duplicates
    handles = list(dict.fromkeys(handles))

    return handles[:limit]


def parse_product(text: str) -> dict:
    """Parse JSON product information

    Parameters:
        text (str): JSON text with product info

    Returns:
        dict: Dictionary containing product title and featured image URL

    """
    product = {
        "title": None,
        "image": None
    }

    data = json.loads(text)

    if not "product" in data:
        return product

    if "title" in data["product"]:
        product["title"] = data["product"]["title"]

    if "images" in data["product"] and len(data["product"]["images"]) > 0:
        if "src" in data["product"]["images"][0]:
            product["image"] = data["product"]["images"][0]["src"]

    return product


def load_store_domains(path: str) -> List[str]:
    """Load Shopify store domains from CSV file

    Parameters:
        path (str): CSV file path

    Returns:
        List[str]: List of shopify stores domain names from CSV file

    """
    if not file_exists(path):
        raise FileNotFoundError("Input file does not exist")

    domains: List[str] = []

    with open(path, "r") as file:
        reader = csv.DictReader(file)

        if "url" not in reader.fieldnames:
            raise ValueError("CSV does not contain 'url' column")

        for row in reader:
            domains.append(row["url"])

    return domains


def find_store_contact(domain: str) -> dict:
    """Scrape shopify domain contact pages for contact informations

    Parameters:
        domain (str): Shopify store domain

    Returns:
        dict: Dict with domain contact information (email, twitter link, facebook link)

    """
    pages = [
        "/",
        "/pages/about",
        "/pages/about-us",
        "/pages/contact",
        "/pages/contact-us"
    ]

    contact = {
        "email": None,
        "facebook": None,
        "twitter": None
    }

    for page in pages:
        url = f"https://{domain}{page}"

        content = load_page(url)

        if content is None:
            continue

        if contact["email"] is None:
            contact["email"] = extract_email(content)

        if contact["twitter"] is None:
            contact["twitter"] = extract_twitter_link(content)

        if contact["facebook"] is None:
            contact["facebook"] = extract_facebook_link(content)

        if None not in contact.values():
            break

    return contact

#
# def load_product_handles(domain: str, limit: int = 5) -> List[str]:
#     """Find shopify product handles on specified domain

#     Parameters:
#         domain (str): Shopify store domain
#         limit (int): Max number of returned products

#     Returns:
#         List[str]: List of shopify product handles

#     """
#     url = f"https://{domain}/collections/all"

#     content = load_page(url)

#     if content is None:
#         raise ValueError(f"Product list '{url}' could not be loaded")

#     handles = extract_product_handles(content, limit)

#     return handles


# def load_product_json(domain: str, handle: str) -> dict:
#     """Download shopify product data in JSON format

#     Parameters:
#         domain (str): Shopify store domain
#         handle (str): Shopify product handle

#     Returns:
#         dict: Dict of shopify product info

#     """
#     url = f"https://{domain}/products/{handle}.json"

#     content = load_page(url)

#     if content is None:
#         raise ValueError(f"Product JSON '{url}' could not be loaded")

#     product = parse_product(content)

#     return product

#
def load_product_json(domain: str)


request.get("https://{domain}/products.json")
Print(response.csv())


def save_stores_to_csv(stores: List[dict], path: str) -> None:
    """Save shopify stores extracted information to CSV file

    Parameters:
        stores (List[dict]): List of shopify stores informations
        path (str): Output CSV file

    Returns:
        None

    """
    if len(stores) < 1:
        raise ValueError("Stores are empty")

    fieldnames = stores[0].keys()

    with open(path, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for store in stores:
            writer.writerow(store)


def load_store(domain: str) -> dict:
    """Load shopify store information from domain

    Parameters:
        domain (str): Shopify store domain

    Returns:
        dict: Dict of shopify store info

    """
    store = {
        "url": domain
    }

    # 2. Find store contacts
    contact = find_store_contact(domain)

    store.update(contact)

    # 3. Load 5 product handles
    handles = load_product_handles(domain, 5)

    for i in range(5):
        product = {
            "title": None,
            "image": None
        }

        if len(handles) > i:
            # 4. Load product JSON data
            product = load_product_json(domain, handles[i])

        store[f"title {i+1}"] = product["title"]
        store[f"image {i+1}"] = product["image"]

    return store


def main() -> None:
    """Main function working according to the description in the README.md file
    """
    logging.basicConfig(filename="error.log",
                        format="%(asctime)s %(message)s", level=logging.ERROR)

    # Parse arguments
    parser = init_argparse()
    args = parser.parse_args()

    stores = []

    # 1. Load stores domains
    try:
        domains = load_store_domains(args.input)

        print(f"Found {len(domains)} store domains")
    except ValueError as ex:
        logging.error(str(ex))
        return

    for domain in domains:
        print(f"Loading '{domain}' ...", end=" ")

        try:
            store = load_store(domain)
            stores.append(store)

            print("OK")

        except ValueError as ex:
            logging.error(str(ex))
            print("KO")

    # 5. Save stores to CSV
    save_stores_to_csv(stores, args.output)


if __name__ == "__main__":
    main()
