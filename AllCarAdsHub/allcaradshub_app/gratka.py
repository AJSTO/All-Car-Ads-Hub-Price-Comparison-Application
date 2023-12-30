# Standard Library Imports
import time
import random
import logging

# Third-Party Library Imports
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Configure logging settings (you can customize this based on your needs)
logging.basicConfig(level=logging.INFO)


def scrape_subpage(subpage_url, brand, model):
    """
    Scrapes detailed information from a car advertisement subpage on Gratka.pl.

    Parameters:
        subpage_url (str): URL of the car advertisement subpage.

    Returns:
        dict or None: Dictionary containing extracted parameters from the subpage if successful, else None.
            Keys include 'marka_value', 'model_value', 'cena_value', 'waluta_value',
            'rok_produkcji_value', 'przebieg_value', 'pojemnosc_value', 'moc_value',
            'typ_nadwozia_value', 'liczba_drzwi_value', 'liczba_miejsc_value', 'kolor_value',
            'kraj_pochodzenia_value', 'zarejestrowany_w_polsce_value', 'stan_value',
            'lokalizacja_value', 'tytul_value', 'url_value', and 'strona_value'.
    """
    # Use a logger with the name of the current function
    logger = logging.getLogger(__name__)

    try:
        subpage_response = requests.get(subpage_url)
        logger.info(f"Scraping subpage: {subpage_url}")

        if subpage_response.status_code == 200:
            # Parse the HTML of the current page
            subpage_soup = BeautifulSoup(subpage_response.text, 'html.parser')

            # Find all <li> elements with <span> and <b> inside
            parameter_items = subpage_soup.find_all('li')

            # Dictionary to store extracted parameters
            parameters = {}

            for item in parameter_items:
                # Find <span> and <b> tags within each <li> element
                span = item.find('span')
                b = item.find('b', class_='parameters__value')

                if span and b:
                    # Extract parameter name and value
                    parameter_name = span.get_text(strip=True)
                    parameter_value = b.get_text(strip=True)

                    # Store in the dictionary
                    parameters[parameter_name] = parameter_value

            single_ad_dict = {
                "marka_value": brand,
                "model_value": model,
                "cena_value": float(subpage_soup.find('span', class_='priceInfo__value')
                                    .text.strip()
                                    .replace("\n", "")
                                    .replace(" ", "")
                                    .replace("zł", "")
                                    .replace(",", ".")
                                    ),
                "waluta_value": subpage_soup.find('span', class_='priceInfo__currency').text.strip(' ')
                .replace(" ", "")
                .replace("\n", "")
                .replace('zł', 'PLN'),
                "rok_produkcji_value": int(parameters.get('Rok produkcji', None)),
                "przebieg_value": float(parameters.get('Przebieg', None)),
                "pojemnosc_value": parameters.get('Pojemność silnika [cm3]', None)
                .replace(" ", "")
                .replace("cm3", ""),
                "moc_value": float(parameters.get('Moc silnika', None)),
                "typ_nadwozia_value": parameters.get('Typ nadwozia', None),
                "liczba_drzwi_value": parameters.get('Liczba drzwi', None),
                "liczba_miejsc_value": parameters.get('Liczba miejsc', None),
                "kolor_value": parameters.get('Kolor', None),
                "kraj_pochodzenia_value": parameters.get('Kraj pierwszej rejestracji', None),
                "zarejestrowany_w_polsce_value": parameters.get('Zarejestrowany w Polsce', None),
                "stan_value": parameters.get('Stan pojazdu', None),
                "lokalizacja_value": parameters.get('Lokalizacja', None),#.split(',')[0],
                "tytul_value": subpage_soup.find('h1', class_='sticker__title').text.strip(),
                "url_value": subpage_url,
                "strona_value": "gratka",
            }

            # Log the resulting dictionary
            logger.info(single_ad_dict)

            return single_ad_dict

        # If the request was not successful, log an error
        else:
            logger.error(f"Failed to retrieve subpage. Status code: {subpage_response.status_code}")

    except Exception as e:
        # Log any exception that occurs during scraping
        logger.error(f"Error processing subpage {subpage_url}: {e}")

    # Introduce a random delay between 0.5 and 1.5 seconds
    delay = random.uniform(0.5, 1.5)
    time.sleep(delay)

    return None


def scrape_main_page(
    brand, model, year_from, year_to, engine_cap_from, engine_cap_to, price_from, price_to,
    fuel, mileage_from, mileage_to, gearbox, engine_power_from, engine_power_to, town, distance
):
    """
    Scrapes car advertisements from Gratka.pl based on specified search criteria.

    Parameters:
        brand (str): Car brand.
        model (str): Car model.
        year_from (int): Minimum production year.
        year_to (int): Maximum production year.
        engine_cap_from (float): Minimum engine capacity.
        engine_cap_to (float): Maximum engine capacity.
        price_from (float): Minimum price.
        price_to (float): Maximum price.
        fuel (str): Fuel type (e.g., 'benzyna', 'diesel').
        mileage_from (int): Minimum mileage.
        mileage_to (int): Maximum mileage.
        gearbox (str): Gearbox type (e.g., 'manual', 'automatic').
        engine_power_from (int): Minimum engine power.
        engine_power_to (int): Maximum engine power.
        town (str): Location.
        distance (int): Search radius around the specified town.

    Returns:
        list of dict: List of dictionaries containing information about scraped car advertisements.
    """
    all_ads = []
    page_num = 1
    while True:
        current_url = (
            f'https://gratka.pl/motoryzacja/osobowe/{brand}/{model}/{fuel}/od-{year_from}/{town}?'
            f'page={page_num}&skrzynia-biegow[0]={gearbox}&'
            f'cena-calkowita:min={price_from}&cena-calkowita:max={price_to}&'
            f'rok-produkcji:max={year_to}&przebieg:min={mileage_from}&przebieg:max={mileage_to}&'
            f'pojemnosc-silnika:min={engine_cap_from}&pojemnosc-silnika:max={engine_cap_to}&'
            f'moc-silnika:min={engine_power_from}&moc-silnika:max={engine_power_to}&promien={distance}'
        )

        # Request the current page
        main_page_response = requests.get(current_url)
        logging.info(f"Using url: {current_url}")

        if main_page_response.status_code == 200:
            # Parse the HTML of the current page
            main_page_soup = BeautifulSoup(main_page_response.text, 'html.parser')
            offer_count = main_page_soup.find('span', {'data-cy': 'offersCount'}).text.strip()
            print(offer_count)
            if offer_count != '(0)':
                try:
                    # Find the input element with the id 'pagination__input-1746878645'
                    input_element = main_page_soup.find('input', {'aria-label': 'Numer strony wyników'})
                    # Extract the value of the 'max' attribute
                    max_page = int(input_element.get('maxlength'))
                except (IndexError, AttributeError, ValueError):
                    max_page = 1
                    logging.warning("Error occurred while extracting max_page. Setting max_page to 1.")

                logging.info(f"Maximum Page Number: {max_page}, actual page: {page_num}")


                processed_links = set()

                offers_soup = main_page_soup.find('div', {'class': 'listing'})

                # Find and iterate through links to subpages
                subpage_links = offers_soup.find_all('a', href=True)

                for subpage_link in subpage_links:
                    subpage_url = subpage_link['href']

                    # Check if the href attribute contains the desired pattern
                    if subpage_url not in processed_links \
                            and subpage_url.startswith('https://gratka.pl/motoryzacja/') \
                            and "/osobowe/" not in subpage_url:
                        processed_links.add(subpage_url)
                        # Step 4: Open and scrape the subpage
                        subpage_response = requests.get(subpage_url)

                        print(subpage_response)

                        if subpage_response.status_code == 200:
                            result = scrape_subpage(subpage_url, brand, model)
                            if result is not None:
                                all_ads.append(result)
                            else:
                                logging.info(f"Failed to fetch details for subpage: {subpage_url}")

                # Increment the page number
                page_num += 1

                # Check if we reached the maximum page number
                if page_num > max_page:
                    ads_df = pd.DataFrame(all_ads)
                    logging.info(ads_df)
                    logging.info("Reached maximum page number. Stopping.")
                    break
            else:
                logging.info('There is no offers when considering searching details.')
                break
        else:
            logging.error(f"Failed to fetch main page. Status code: {main_page_response.status_code}")
            break

    return all_ads
