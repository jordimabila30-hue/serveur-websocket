# -*- coding: utf-8 -*-
"""
Created on Mar 2 2026

Auteur: Jordi
"""

from PIL import Image
import os

# --- Chemin de l'image à convertir ---
image_path = r"C:\Users\jordi\Documents\Vs Code\projet S\jordi.png"  # <-- Mettez ici le chemin de votre image

# --- Charger l'image ---
img = Image.open(image_path).convert("L")  # convert en grayscale
pixels = img.load()
cols, rows = img.size  # width, height

# --- Créer le fichier texte ---
output_txt = os.path.join(os.path.dirname(image_path), "image_to_txt.txt")

with open(output_txt, "w") as f:
    # Écrire d'abord les dimensions
    f.write(f"{rows}\n")
    f.write(f"{cols}\n")
    
    # Écrire les pixels ligne par ligne
    for y in range(rows):
        row_values = [str(pixels[x, y]) for x in range(cols)]
        f.write(" ".join(row_values) + "\n")

print(f"Fichier texte généré avec succès ici : {output_txt}")