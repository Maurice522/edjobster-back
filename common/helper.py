from .models import Country, State, City
from .serializer import CountrySerializer, StateSerializer, CitySerializer


def getAllData():

    countryList = Country.getAll()

    countries = CountrySerializer(countryList, many=True)

    stateList = State.getAll()

    states = StateSerializer(stateList, many=True)

    cityList = City.getAll()

    cities = CitySerializer(cityList, many=True)

    return {
        'code': 200,
        'countries': countries.data,
        'states': states.data,
        'cities': cities.data,
    }


def getCountries(request):

    countryList = Country.getAll()
    countries = CountrySerializer(countryList, many=True)
    return {
        'code': 200,
        'countries': countries.data,
    }


def getStatesForCountry(request):

    id = request.GET.get('id', None)

    if not id:
        return {
            'code': 400,
            'msg': 'Country id required'
        }

    stateList = State.getByCountry(id)
    states = StateSerializer(stateList, many=True)

    return {
        'code': 200,
        'states': states.data,
    }


def getCitiesForState(request):

    id = request.GET.get('id', None)

    if not id:
        return {
            'code': 400,
            'msg': 'State id required'
        }

    cityList = City.getByState(id)
    cities = CitySerializer(cityList, many=True)

    return {
        'code': 200,
        'cities': cities.data,
    }
