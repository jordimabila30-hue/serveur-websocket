"""Pour chaque wifi au quel je ne suis pas connecté, je vais essayer de trouver le mot de passe en essayant toutes les combinaisons possibles de caractères jusqu'à ce que je trouve le bon mot de passe ou que j'ai essayé toutes les combinaisons possibles."""
import itertools
import string

def crack_password(wifi_name, max_length=10):
    characters = string.ascii_letters + string.digits + string.punctuation + "1234567890" + "&é'(-è_çà)=+*µ£¤^¨$ù!ù?./:;.,<>|@#~`°" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "abcdefghijklmnopqrstuvwxyz" + "0123456789"
    for length in range(10, max_length + 10):
        for combination in itertools.product(characters, repeat=length):
            password = ''.join(combination)
            # Here you would test the password against the WiFi network
            # For demonstration purposes, we'll just print it
            print(f"Trying password: {password} : wifi_name = {wifi_name}")
# recuper le wifi de mon pc et lance la fonction crack_password pour chaque wifi trouvé
import subprocess
def get_wifi_networks():
    result = subprocess.run(['netsh', 'wlan', 'show', 'network'], capture_output=True, text=True)
    networks = []
    for line in result.stdout.splitlines():
        if "SSID" in line and "BSSID" not in line:
            ssid = line.split(":")[1].strip()
            networks.append(ssid)
    return networks

if __name__ == "__main__":
    wifi_networks = get_wifi_networks()
    for network in wifi_networks:
        print(f"Cracking password for WiFi network: {network} : wifi_name = {network}")
        crack_password(network)

#affiche le nom du wifi qu'on essaye de cracker et tout les mots de passe qu'on essaye pour ce wifi.

