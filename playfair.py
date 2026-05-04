import string

def preparer_cle(cle):
    cle = cle.upper().replace("J", "I")
    resultat = ""
    for lettre in cle:
        if lettre in string.ascii_uppercase and lettre not in resultat:
            resultat += lettre
    return resultat


def creer_matrice(cle):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    cle = preparer_cle(cle)

    matrice = []

    for lettre in cle:
        if lettre not in matrice:
            matrice.append(lettre)

    for lettre in alphabet:
        if lettre not in matrice:
            matrice.append(lettre)

    return [matrice[i:i+5] for i in range(0, 25, 5)]


def afficher_matrice(matrice):
    print("\nMatrice Playfair :")
    for ligne in matrice:
        print(" ".join(ligne))


def trouver_position(matrice, lettre):
    for i in range(5):
        for j in range(5):
            if matrice[i][j] == lettre:
                return i, j


def preparer_texte(texte):
    texte = texte.upper().replace("J", "I")

    texte_nettoye = ""
    for lettre in texte:
        if lettre in string.ascii_uppercase:
            texte_nettoye += lettre

    resultat = ""
    i = 0

    while i < len(texte_nettoye):
        a = texte_nettoye[i]

        if i + 1 < len(texte_nettoye):
            b = texte_nettoye[i+1]

            if a == b:
                resultat += a + "X"
                i += 1
            else:
                resultat += a + b
                i += 2
        else:
            resultat += a + "X"
            i += 1

    return resultat


def chiffrer(texte, matrice):
    texte = preparer_texte(texte)
    chiffre = ""

    for i in range(0, len(texte), 2):
        a = texte[i]
        b = texte[i+1]

        ligne_a, col_a = trouver_position(matrice, a)
        ligne_b, col_b = trouver_position(matrice, b)

        if ligne_a == ligne_b:
            chiffre += matrice[ligne_a][(col_a + 1) % 5]
            chiffre += matrice[ligne_b][(col_b + 1) % 5]

        elif col_a == col_b:
            chiffre += matrice[(ligne_a + 1) % 5][col_a]
            chiffre += matrice[(ligne_b + 1) % 5][col_b]

        else:
            chiffre += matrice[ligne_a][col_b]
            chiffre += matrice[ligne_b][col_a]

    return chiffre


def dechiffrer(texte_chiffre, matrice):
    texte = ""
    texte_chiffre = texte_chiffre.upper()

    for i in range(0, len(texte_chiffre), 2):
        a = texte_chiffre[i]
        b = texte_chiffre[i+1]

        ligne_a, col_a = trouver_position(matrice, a)
        ligne_b, col_b = trouver_position(matrice, b)

        if ligne_a == ligne_b:
            texte += matrice[ligne_a][(col_a - 1) % 5]
            texte += matrice[ligne_b][(col_b - 1) % 5]

        elif col_a == col_b:
            texte += matrice[(ligne_a - 1) % 5][col_a]
            texte += matrice[(ligne_b - 1) % 5][col_b]

        else:
            texte += matrice[ligne_a][col_b]
            texte += matrice[ligne_b][col_a]

    return texte


# programme principal

cle = input("Entrez la clé pour la matrice : ")
matrice = creer_matrice(cle)

afficher_matrice(matrice)

texte = input("\nEntrez le texte à chiffrer : ")

texte_chiffre = chiffrer(texte, matrice)
print("\nTexte chiffré :", texte_chiffre)

texte_dechiffre = dechiffrer(texte_chiffre, matrice)
print("Texte déchiffré :", texte_dechiffre)