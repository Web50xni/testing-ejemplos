# Importa el módulo os para configurar el entorno de Django
import os

# Configura el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airline.settings")

# Importa el módulo Django
import django
django.setup()

# Importa los modelos que quieres usar
from flights.models import Airport, Flight, Passenger

# Función para registrar datos
def registrar_datos():
    # Crea instancias de Airport
    tokyo = Airport.objects.create(code="HND", city="Tokyo")
    milan = Airport.objects.create(code="MXP", city="Milan")
    taipei = Airport.objects.create(code="TPE", city="Taipei")
    bogota = Airport.objects.create(code="BOG", city="Bogota")

    # Crea una instancia de Flight para el vuelo de Tokio a Milán
    flight_tokyo_milan = Flight.objects.create(origin=tokyo, destination=milan, duration=12)

    # Crea una instancia de Flight para el vuelo de Taipei a Bogotá
    flight_taipei_bogota = Flight.objects.create(origin=taipei, destination=bogota, duration=18)

    # Guarda los cambios
    flight_tokyo_milan.save()
    flight_taipei_bogota.save()

# Llama a la función para registrar los datos
def registrar_pasajeros():
    # Obtén los vuelos de la base de datos
    vuelo_tokyo_milan = Flight.objects.get(origin__city="Tokyo", destination__city="Milan")
    vuelo_taipei_bogota = Flight.objects.get(origin__city="Taipei", destination__city="Bogota")

    # Crea instancias de pasajeros
    pasajero1 = Passenger.objects.create(first="Enrique", last="Alemany")
    pasajero2 = Passenger.objects.create(first="Alexander", last="Lopez")
    pasajero3 = Passenger.objects.create(first="Maria", last="Martinez")
    pasajero4 = Passenger.objects.create(first="Cristopher", last="Suazo")

    # Asocia los pasajeros con los vuelos
    vuelo_tokyo_milan.passengers.add(pasajero1, pasajero2)
    vuelo_taipei_bogota.passengers.add(pasajero3, pasajero4)

    # Guarda los cambios
    vuelo_tokyo_milan.save()
    vuelo_taipei_bogota.save()

# Llama a la función para registrar los pasajeros
registrar_datos()
registrar_pasajeros()

