from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from allcaradshub_app.gratka import scrape_main_page as gratka_scrap
from allcaradshub_app.otomoto import scrape_main_page as otomoto_scrap
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

gearbox_translate_gratka = {
    'manual': 'manualna',
    'automatic': 'automatyczna',
}
fuel_translate_gratka = {
    'petrol': 'benzyna',
    'diesel': 'diesel',
    'hybrid': 'hybryda',
    'electric': 'elektryczne',
}


def home(request):
    context = {}

    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            #'''
            # Access individual form fields using data dictionary for gratka

            # Show loading bar
            #context = show_loading_bar(context)
            list_of_ads = []
            #'''
            gratka_list = gratka_scrap(
                brand=data.get('brand', '').lower(),
                model=data.get('model', '').lower(),
                year_from=data.get('yearFrom', ''),
                year_to=data.get('yearTo', ''),
                engine_cap_from=data.get('engineCapFrom', ''),
                engine_cap_to=data.get('engineCapTo', ''),
                price_from=data.get('priceFrom', ''),
                price_to=data.get('priceTo', ''),
                fuel=fuel_translate_gratka.get(data.get('fuelType', '')),
                mileage_from=data.get('mileageFrom', ''),
                mileage_to=data.get('mileageTo', ''),
                gearbox=gearbox_translate_gratka.get(data.get('gearboxType', '')),
                engine_power_from=data.get('enginePowerFrom', ''),
                engine_power_to=data.get('enginePowerTo', ''),
                town=data.get('town', ''),
                distance=data.get('distanceFromTown', ''),
                # voivodship = data.get('voivodship', '')
            )
            list_of_ads.extend(gratka_list)

            #'''
            otomoto_list = otomoto_scrap(
                brand=data.get('brand', '').lower(),
                model=data.get('model', '').lower(),
                year_from=data.get('yearFrom', ''),
                year_to=data.get('yearTo', ''),
                engine_cap_from=data.get('engineCapFrom', ''),
                engine_cap_to=data.get('engineCapTo', ''),
                price_from=data.get('priceFrom', ''),
                price_to=data.get('priceTo', ''),
                fuel=data.get('fuelType', ''),
                mileage_from=data.get('mileageFrom', ''),
                mileage_to=data.get('mileageTo', ''),
                gearbox=data.get('gearboxType', ''),
                engine_power_from=data.get('enginePowerFrom', ''),
                engine_power_to=data.get('enginePowerTo', ''),
                town=data.get('town', ''),
                distance=data.get('distanceFromTown', ''),
                # voivodship = data.get('voivodship', '')
            )
            list_of_ads.extend(otomoto_list)
            #'''

            # Add the list_of_ads to the context
            context['list_of_ads'] = list_of_ads

            print(context)

            return JsonResponse(context)

            # Hide loading bar and show success message
            #context = hide_loading_bar(context, 'Success')

        except json.JSONDecodeError:
            response_data = {'status': 'error', 'message': 'Invalid JSON data in the request.'}
            return JsonResponse(response_data, status=400)

    # Call your imported function with the dictionary
    # scrape_main_page(search_params)

    # Pass the context to the template and render it
    return render(request, 'home.html', context)


# Helper function to show the loading bar
def show_loading_bar(context):
    context['show_loading_bar'] = True
    return context


# Helper function to hide the loading bar and show a message
def hide_loading_bar(context, message):
    context['hide_loading_bar'] = True
    context['message'] = message
    return context

# to delete!!!!
def trying(request):
    context = {}

    if request.method == 'POST':
        try:
            print('0xd')
            # Simulating a long-running task (for loop)
            for x in range(1, 300000):
                print(x)

            # Send a success response to the client
            response_data = {'status': 'success', 'message': 'Search completed successfully!'}
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            # Handle JSON decode error
            response_data = {'status': 'error', 'message': 'Invalid JSON data in the request.'}
            return JsonResponse(response_data, status=400)

    # Render the template for GET requests
    return render(request, 'trying.html', context)