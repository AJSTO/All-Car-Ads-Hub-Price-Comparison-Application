[![All_Car_Ads_Hub](https://i.postimg.cc/BvFSbYRn/All-Car-Ads-Hub-2.png)](https://carads-wkpgtdbwmq-lm.a.run.app)


# 🔗 Link to web app: [All_Car_Ads_Hub](https://carads-wkpgtdbwmq-lm.a.run.app) <img src="https://img.shields.io/badge/version-1.0-green" />

## 👨‍💻 Built with:

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/>  <img src="https://sysdig.com/wp-content/uploads/google-cloud-run.png" width="100" height="27,5" /> <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white" />  <img src="https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white" /> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" /> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />

## 📖 Descripction about project:

The project is a web application built on the Django framework and deployed on CloudRun. Its main purpose is to facilitate users in finding relevant car listings by inputting specific search parameters. The application utilizes the BeautifulSoup (bs4) library to scrape data from popular online classified platforms such as otomoto.pl and gratka.pl.

Users can input various parameters like brand, model, year of production, or mileage. The application then searches through the classified pages to find listings that match the specified criteria. The discovered listings are presented on a single page along with key parameters and visualized graphs, making it easier for users to quickly compare available options.

In future iterations of the project, there are plans to expand the functionality to include scraping data from other classified platforms such as Allegro. However, due to the volume of data being collected and the time required for scraping, the initial idea of storing data in BigQuery was abandoned. Currently, the application operates in real-time, meaning that data is scraped on-the-fly and presented to the user without the need for storage in a database.

## 🔍 App preview:

![Project Screenshot](/All_Car_Ads_Hub.gif)

## 🔪 Beautiful Soup:

The scraper collects data from each advertisement from automotive listings on [otomoto.pl](https://www.otomoto.pl) and [gratka.pl](https://gratka.pl) and organizes it into dictionaries. The structure of each dictionary is as follows:

```python
{
    'marka_value': 'Toyota',
    'model_value': 'Corolla',
    'cena_value': 7500.0,
    'waluta_value': 'PLN',
    'rok_produkcji_value': 2005,
    'przebieg_value': 205000.0,
    'pojemnosc_value': '1398',
    'moc_value': 97.0,
    'typ_nadwozia_value': 'Auta małe',
    'liczba_drzwi_value': '3',
    'liczba_miejsc_value': '5',
    'kolor_value': 'Granatowy',
    'kraj_pochodzenia_value': None,
    'zarejestrowany_w_polsce_value': None,
    'stan_value': 'Używane',
    'lokalizacja_value': 'Brwinów, pruszkowski, Mazowieckie',
    'tytul_value': 'Toyota Corolla 1.4 VVT-i Terra',
    'url_value': 'https://www.otomoto.pl/osobowe/oferta/toyota-corolla-toyota-corolla-2005-1-4-ID6G3GIP.html',
    'strona_value': 'otomoto'
}
```
The last key, `strona_value` (page), indicates the source of the scraped data, either `otomoto` or `gratka`. This value is dynamic and depends on the website being scraped.

Once the script collects all possible advertisements, it compiles them into a list of dictionaries, and the data is then sent to a Django web application in JSON format. This allows the Django application to process and display the scraped automotive listings effectively.

The structure of the dictionary is designed to capture key details about each car listing, facilitating easy integration with the Django application and providing users with comprehensive information about available vehicles.

## 🖥️ Frontend:

Basic frontend has been developed to complement the car listings scraper. Frontend is a simple, single-page interface, due to the lack of experience in frontend development. While not flawless, it serves the purpose of interacting with the underlying scraper.

### Features:
* Search Form:
  * The default page consists of a fieldset with options to select various search parameters:
    ```bash
    Brand, Model, Year Range, Engine Capacity Range, Price Range, Fuel Type, Mileage Range,
    Gearbox Type, Engine Power Range, Town, Distance from Town and Voivodship.
    ```
  * Voivodship options are currently reserved for future use when data is sourced from Allegro.
* Search Results Table:
  * Clicking the "Search" button yields a table of results.
  * Each row includes information about the source page, a link with the advertisement title, and details such as year of production, mileage, location, engine capacity, engine power, and the advertised price.
  * Sorting functionality is available by clicking the icon next to the column header.
  * Additional information about the median price and median mileage is provided.
* Interactive Scatterplot:
  * A scatterplot visually represents the dispersion of prices against mileage.
  * Clicking on a data point corresponding to an advertisement redirects to the respective listing page.
* Price Histogram:
  * A histogram divides prices into 10 bins, providing an overview of the distribution of prices.
### Note on Voivodships:
Voivodships functionality is intended for future use, particularly when data is successfully acquired from Allegro.

While the frontend may lack sophistication, it serves its purpose in presenting and interacting with the scraped car listings data. Future improvements and refinements are anticipated as the project evolves.

## 🌳 Project Scructure: 
```bash
.
├── AllCarAdsHub
│   ├── AllCarAdsHub
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── allcaradshub_app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── gratka.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── otomoto.py
│   │   ├── templates
│   │   │   └── home.html
│   │   ├── tests.py
│   │   └── views.py
│   ├── db.sqlite3
│   └── manage.py
├── Dockerfile
└── requirements.txt

```

## ☁️ Deploying project on CloudRun:

### 1. Build and Tag Docker Image:
* Build your Docker image using the docker buildx command. For example:
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t your-image-name:v1 .
```
* Tag the image:
```bash
docker tag your-image-name:v1 gcr.io/your-project-id/your-image-name:v1
```
### 2. Push Docker Image to Google Cloud Registry:
* Allow gcloud to use service account credentials to make requests:
```bash
 gcloud auth activate-service-account [ACCOUNT] --key-file=KEY_FILE
```
* Authenticate Docker with Google Cloud Registry:
```bash
gcloud auth configure-docker
```
* Push the Docker image to the Google Cloud Registry:
```bash
docker push gcr.io/your-project-id/your-image-name:v1
```
### 3. Deploy on Cloud Run:
* Deploy the Docker image to Cloud Run:
```bash
gcloud run deploy your-service-name \
  --image gcr.io/your-project-id/your-image-name:v1 \
  --platform managed \
  --port 8000
```
* Follow the prompts to set additional configurations, such as allowing unauthenticated access or specifying environment variables.
### 4. Access the Deployed Service:
Once the deployment is complete, you will receive a URL for your Cloud Run service. You can access your application by navigating to that URL in a web browser.
Now, your Docker image is deployed to Google Cloud Registry, and your service is running on Cloud Run. Remember to replace placeholders like your-project-id, your-image-name, and your-service-name with your actual project ID, image name, and desired service name. Adjust the version tag (v1) and other configurations as needed for your project.

You can also deploy application locally.
