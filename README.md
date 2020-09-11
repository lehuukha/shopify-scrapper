# PYTHON DEVELOPER TEST SCRIPT

## Description

The Python script should do the following tasks.

1. Load a list of Shopify store domains from an input CSV file.

2. For each store, check the following pages for an email address and links to Facebook and Twitter pages:
    - http://storedomain.com/ (home page)
    - http://storedomain.com/pages/about
    - http://storedomain.com/pages/about-us
    - http://storedomain.com/pages/contact
    - http://storedomain.com/pages/contact-us

3. Load a list of the first 5 links to product pages from
    - http://storedomain.com/collections/all

4. Load JSON data for each product from
    - http://storedomain.com/products/product-handle.json

5. Get product title and featured (first) image URL from product JSON data.

6. Save store domains together with emails, Facebook and Twitter links, product titles and image URLs (2 columns per product) into a new CSV file.

The script should be implemented in Python 3.
