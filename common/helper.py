from .models import Country, NoteType, State, City
from .serializer import CountrySerializer, NoteTypeSerializer, StateSerializer, CitySerializer
from common import serializer


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
    query = request.GET.get("query", None)

    if not id and not query:
        return {
            'code': 400,
            'msg': 'State info required'
        }
    
    if id:
        cityList = City.getByState(id)
    
    if query: 
        cityList = City.search(query)
    
    cities = CitySerializer(cityList, many=True)
    return {
        'code': 200,
        'cities': cities.data,
    }

def getNoteTypes(request):

    notes = NoteType.getAll()
    serializer = NoteTypeSerializer(notes, many=True)

    return {
        'code': 200,
        'types': serializer.data,
    }