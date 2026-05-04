from dronekit import connect, VehicleMode, LocationGlobalRelative
from geopy.geocoders import Nominatim
import time
from math import radians, sin, cos, sqrt, atan2

# --- Fonctions Utilitaires ---
def get_distance_metres(loc1, loc2):
    lat1, lon1, lat2, lon2 = map(radians, [loc1.lat, loc1.lon, loc2.lat, loc2.lon])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6371000 * c

def goto_position_target_global_relative(lat, lon, alt):
    vehicle.simple_goto(LocationGlobalRelative(lat, lon, alt))

# --- Connexion et Initialisation ---
print("Connexion au drone...")
vehicle = connect('tcp:127.0.0.1:5763', wait_ready=True)
print("Drone connecté!")

print("Recherche d'un signal GPS valide...")
while vehicle.gps_0.fix_type < 2:
    time.sleep(1)
print("GPS valide détecté!\n")
home = vehicle.location.global_frame

# --- Configuration du vol par l'utilisateur ---
while True:
    try:
        altitude = float(input("Hauteur de vol souhaitée (m, ex. 20): "))
        speed = float(input("Vitesse de vol souhaitée (m/s, ex. 5): "))
        if altitude > 0 and speed > 0: break
    except ValueError:
        print("Entrée invalide.")

# --- Préparation au décollage ---
vehicle.mode = VehicleMode("GUIDED")
while not vehicle.mode.name == "GUIDED": time.sleep(0.5)

vehicle.armed = True
while not vehicle.armed: time.sleep(0.5)

# --- Décollage ---
print(f"Décollage à {altitude}m...")
vehicle.simple_takeoff(altitude)
vehicle.airspeed = speed

while vehicle.location.global_relative_frame.alt < altitude * 0.95:
    time.sleep(1)
print("Altitude atteinte!\n")

# --- Gestion des Destinations Multiples ---
num_destinations = int(input("Combien d'adresses souhaitez-vous visiter? "))
geolocator = Nominatim(user_agent="drone_locator", timeout=3)

for i in range(num_destinations):
    address = input(f"Entrez l'adresse #{i+1}: ").strip()
    print(f"\nRecherche de coordonnées pour {address}...")
    location = geolocator.geocode(address)

    if location:
        dest_lat, dest_lon = location.latitude, location.longitude
        print(f"Coordonnées trouvées. En route vers {address}...")
        goto_position_target_global_relative(dest_lat, dest_lon, altitude)

        while vehicle.mode.name == "GUIDED":
            dist = get_distance_metres(vehicle.location.global_frame, LocationGlobalRelative(dest_lat, dest_lon, altitude))
            print(f"Distance restante de {address}: {dist:.2f} m")
            if dist < 1:
                print(f"{address} atteinte.")
                break
            time.sleep(1)
    else:
        print(f"Impossible de localiser l'adresse {address}. Passage à la suivante.")

# --- Retour et Atterrissage ---
print("\nRetour à la base (RTL)...")
vehicle.mode = VehicleMode("RTL")

while vehicle.armed:
    dist_home = get_distance_metres(vehicle.location.global_frame, home)
    print(f"Distance à la base: {dist_home:.1f} m | Altitude actuelle: {vehicle.location.global_relative_frame.alt:.2f}")
    if dist_home < 1 and vehicle.location.global_relative_frame.alt < 0.1:
         break
    time.sleep(1)

print("Atterrissage terminé.")

# --- Fin ---
print("Déconnexion du véhicule.")
vehicle.close()
