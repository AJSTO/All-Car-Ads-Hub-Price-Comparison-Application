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

        # Check if the request was successful (status code 200)
        if subpage_response.status_code == 200:
            logger.debug("Request successful. Parsing HTML.")

            # Parse the HTML of the current page
            subpage_soup = BeautifulSoup(subpage_response.text, 'html.parser')

            page_not_found_element = subpage_soup.find('h4', {'class': 'ooa-1o6s6g2 er34gjf0'})

            if page_not_found_element and page_not_found_element.text.strip() == '404 Strona nie została odnaleziona':
                logger.info("Page not found... Going to the next page.")
            else:
                logger.debug("Page HTML parsed successfully. Extracting details.")
                # Find the div elements containing details
                details_divs = subpage_soup.find_all('div', {'data-testid': 'advert-details-item'})

                # Initialize dictionary with None to store values
                single_ad_dict = {
                    "marka_value": brand,
                    "model_value": model,
                    "cena_value": None,
                    "waluta_value": None,
                    "rok_produkcji_value": None,
                    "przebieg_value": None,
                    "pojemnosc_value": None,
                    "moc_value": None,
                    "typ_nadwozia_value": None,
                    "liczba_drzwi_value": None,
                    "liczba_miejsc_value": None,
                    "kolor_value": None,
                    "kraj_pochodzenia_value": None,
                    "zarejestrowany_w_polsce_value": None,
                    "stan_value": None,
                    "lokalizacja_value": None,
                    "tytul_value": None,
                    "url_value": subpage_url,
                    "strona_value": "otomoto",
                }
                try:
                    # Finding title of the advertisement
                    single_ad_dict["tytul_value"] = subpage_soup.find(
                        'h3',
                        class_='offer-title big-text ezl3qpx2 ooa-ebtemw er34gjf0'
                    ).text.strip()
                except Exception as e:
                    # Log any exception that occurs during scraping
                    logger.error(f"Error when tring to get title of page")

                try:
                    # Finding location
                    location_element = subpage_soup.find(
                        'a',
                        {
                            'class': 'edhv9y51 ooa-oxkwx3', 'color': 'text-global-highlight',
                            'href': lambda x: x and (x.startswith('https://maps') or x.startswith('#map'))
                        }
                    )

                    single_ad_dict["lokalizacja_value"] = location_element.find('svg').find_parent().text.strip()
                except Exception as e:
                    # Log any exception that occurs during scraping
                    logger.error(f"Error when tring to get localisation of advertisement")

                try:
                    # Find the price and currency of the offer
                    price_number = subpage_soup.find('h3', class_='offer-price__number')
                    currency = subpage_soup.find('p', class_='offer-price__currency')

                    single_ad_dict["cena_value"] = float(price_number.text.strip().replace(" ", "")) if price_number else None
                    single_ad_dict["waluta_value"] = currency.text.strip() if currency else None
                except Exception as e:
                    # Log any exception that occurs during scraping
                    logger.error(f"Error when tring to get price of advertisement")

                # Iterate through details_divs
                for details_div in details_divs:

                    title = details_div.find('p', {'class': 'e18eslyg4 ooa-12b2ph5'}).text.strip()
                    try:
                        if title == 'Marka pojazdu':
                            single_ad_dict["marka_value"] = details_div.find(
                                'p', {'class': 'e16lfxpc0 ooa-1pe3502 er34gjf0'}
                            ).text.strip()
                    except Exception as e:
                        # Log any exception that occurs during scraping
                        logger.error(f"Error when tring to get brand of car")

                    try:
                        if title == 'Model pojazdu':
                            single_ad_dict["model_value"] = details_div.find(
                                'p', {'class': 'e16lfxpc0 ooa-1pe3502 er34gjf0'}
                            ).text.strip()
                    except Exception as e:
                        # Log any exception that occurs during scraping
                        logger.error(f"Error when tring to get model of car")

                    try:
                        if title == 'Rok produkcji':
                            single_ad_dict["rok_produkcji_value"] = int(
                                details_div.find('p', {'class': 'e16lfxpc0 ooa-1pe3502 er34gjf0'}).text.strip()
                            )
                    except Exception as e:
                        # Log any exception that occurs during scraping
                        logger.error(f"Error when tring to get year of production of car")

                    try:
                        if title == 'Przebieg':
                            single_ad_dict["przebieg_value"] = float(
                                details_div.find('p', {'class': 'e16lfxpc0 ooa-1pe3502 er34gjf0'}).text.strip().replace(" ",
                                                                                                                       "").replace(
                                    "km", "")
                            )
                    except Exception as e:
                        # Log any exception that occurs during scraping
                        logger.error(f"Error when tring to get mileage of car")

                    try:
                        if title == 'Pojemność skokowa':
                            single_ad_dict["pojemnosc_value"] = details_div.find(
                                'p', {'class': 'e16lfxpc0 ooa-1pe3502 er34gjf0'}
                            ).text.strip().replace(" ", "").replace("cm3", "")
                    except Exception as e:
                        # Log any exception that occurs during scraping
                        logger.error(f"Error when tring to get capacity of car")

                    try:
                        if title == 'Moc':
                            single_ad_dict["moc_value"] = float(
                                details_div.find('p', {'class': 'e16lfxpc0 ooa-1pe3502 er34gjf0'}).text.strip().replace("KM",
                                                                                                                           "").replace(
                                    " ", "")
                            )
                    except Exception as e:
                        # Log any exception that occurs during scraping
                        logger.error(f"Error when tring to get power of car")

                    try:
                        if title == 'Typ nadwozia':
                            single_ad_dict["typ_nadwozia_value"] = details_div.find(
                                'a', {'class': 'e16lfxpc1 ooa-1ftbcn2'}
                            ).text.strip()
                    except Exception as e:
                        # Log any exception that occurs during scraping
                        logger.error(f"Error when tring to get type of body of car")

                    try:
                        if title == 'Liczba drzwi':
                            single_ad_dict["liczba_drzwi_value"] = details_div.find(
                                'p', {'class': 'e16lfxpc0 ooa-1pe3502 er34gjf0'}
                            ).text.strip()
                    except Exception as e:
                        # Log any exception that occurs during scraping
                        logger.error(f"Error when tring to get number of doors of car")

                    try:
                        if title == 'Liczba miejsc':
                            single_ad_dict["liczba_miejsc_value"] = details_div.find(
                                'p', {'class': 'e16lfxpc0 ooa-1pe3502 er34gjf0'}
                            ).text.strip()
                    except Exception as e:
                        # Log any exception that occurs during scraping
                        logger.error(f"Error when tring to get number of seats of car")

                    try:
                        if title == 'Kolor':
                            single_ad_dict["kolor_value"] = details_div.find(
                                'a', {'class': 'e16lfxpc1 ooa-1ftbcn2'}
                            ).text.strip()
                    except Exception as e:
                        # Log any exception that occurs during scraping
                        logger.error(f"Error when tring to get color of car")

                    try:
                        if title == 'Kraj pochodzenia':
                            single_ad_dict["kraj_pochodzenia_value"] = details_div.find(
                                'a', {'class': 'e16lfxpc1 ooa-1ftbcn2'}
                            ).text.strip()
                    except Exception as e:
                        # Log any exception that occurs during scraping
                        logger.error(f"Error when tring to get country of origin of car")

                    try:
                        if title == 'Zarejestrowany w Polsce':
                            single_ad_dict["zarejestrowany_w_polsce_value"] = details_div.find(
                                'p', {'class': 'e16lfxpc0 ooa-1pe3502 er34gjf0'}
                            ).text.strip()
                    except Exception as e:
                        # Log any exception that occurs during scraping
                        logger.error(f"Error when tring to get country of registration of car")

                    try:
                        if title == 'Stan':
                            single_ad_dict["stan_value"] = details_div.find(
                                'a', {'class': 'e16lfxpc1 ooa-1ftbcn2'}
                            ).text.strip()
                    except Exception as e:
                        # Log any exception that occurs during scraping
                        logger.error(f"Error when tring to get condition of car")

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
    delay = random.uniform(0.3, 0.8)
    time.sleep(delay)

    return None


def scrape_main_page(
    brand, model, year_from, year_to, engine_cap_from, engine_cap_to, price_from, price_to,
    fuel, mileage_from, mileage_to, gearbox, engine_power_from, engine_power_to, town, distance
):
    """
    Scrapes car advertisements from Otomoto.pl based on specified search criteria.

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
            f'https://www.otomoto.pl/osobowe/{brand}/{model}/od-{year_from}/{town}?'
            f'search%5Bdist%5D={distance}&search%5Bfilter_enum_fuel_type%5D={fuel}&search%5Bfilter_enum_gearbox%5D={gearbox}&'
            f'search%5Bfilter_float_engine_capacity%3Afrom%5D={engine_cap_from}&search%5Bfilter_float_engine_capacity%3Ato%5D={engine_cap_to}&'
            f'search%5Bfilter_float_engine_power%3Afrom%5D={engine_power_from}&search%5Bfilter_float_engine_power%3Ato%5D={engine_power_to}&'
            f'search%5Bfilter_float_mileage%3Afrom%5D={mileage_from}&search%5Bfilter_float_mileage%3Ato%5D={mileage_to}&'
            f'search%5Bfilter_float_price%3Afrom%5D={price_from}&search%5Bfilter_float_price%3Ato%5D={price_to}&'
            f'search%5Bfilter_float_year%3Ato%5D={year_to}&page={page_num}'
        )
        print(current_url)

        # Request the current page
        main_page_response = requests.get(current_url)

        if main_page_response.status_code == 200:
            # Parse the HTML of the current page
            main_page_soup = BeautifulSoup(main_page_response.text, 'html.parser')

            # Find the maximum page number within the provided HTML snippet
            pagination_list = main_page_soup.find('ul', {'class': 'pagination-list'})

            try:
                max_page_element = pagination_list.find_all('a', {'class': 'ooa-xdlax9'})[-1]
                max_page = int(max_page_element.text)
            except (IndexError, AttributeError, ValueError):
                max_page = 1
                logging.warning("Error occurred while extracting max_page. Setting max_page to 1.")

            logging.info(f"Maximum Page Number: {max_page}, actual page: {page_num}")
            logging.info(f"Using url: {current_url}")

            processed_links = set()

            # Find and iterate through links to subpages
            subpage_links = main_page_soup.find_all('a', href=True)

            for subpage_link in subpage_links:
                subpage_url = subpage_link['href']

                # Check if the href attribute contains the desired pattern
                if subpage_url not in processed_links and 'otomoto.pl/osobowe/oferta/' in subpage_url:
                    processed_links.add(subpage_url)
                    # Open and scrape the subpage
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
            logging.error(f"Failed to fetch main page. Status code: {main_page_response.status_code}")
            break

    return all_ads
