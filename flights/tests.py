from django.db.models import Max
from django.test import Client, TestCase

from .models import Airport, Flight, Passenger



# Create your tests here.
class FlightsTestCase(TestCase):

    def setUp(self):

        # Create airports.
        a1 = Airport.objects.create(code="AKL", city="Auckland")
        a2 = Airport.objects.create(code="LHR", city="Londres")

        # Create flights.
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)

    # Prueba que cuenta el número de salidas desde un aeropuerto.
    def test_departures_count(self):
        a = Airport.objects.get(code="AKL")
        self.assertEqual(a.departures.count(), 2)

    # Prueba que cuenta el número de llegadas a un aeropuerto.
    def test_arrivals_count(self):
        a = Airport.objects.get(code="AKL")
        self.assertEqual(a.arrivals.count(), 1)

    # Prueba si un vuelo es válido.
    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AKL")
        a2 = Airport.objects.get(code="LHR")
        f = Flight.objects.get(origin=a1, destination=a2)
        self.assertTrue(f.is_valid_flight())

    # Prueba si un vuelo es inválido debido a que su destino es el mismo que el origen.
    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AKL")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    # Prueba si un vuelo es inválido debido a una duración negativa.
    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AKL")
        a2 = Airport.objects.get(code="LHR")
        f = Flight.objects.get(origin=a1, destination=a2)
        f.duration = -100
        self.assertFalse(f.is_valid_flight())

    # Prueba la página de inicio.
    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 2)

    # Prueba si la página de un vuelo válido se carga correctamente.
    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AKL")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)

    # Prueba si la página de un vuelo inválido devuelve un error 404.
    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    # Prueba si la página de un vuelo muestra correctamente los pasajeros.
    def test_flight_page_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    # Prueba si la página de un vuelo muestra correctamente los no pasajeros.
    def test_flight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)
