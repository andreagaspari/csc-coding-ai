def calcola_media(numeri):
    """
        Calcola la media aritmetica di una lista di numeri.
        Prova a convertire ogni elemento in float, se non possibile lo ignora.
    Args:
        numeri: Lista di numeri (o stringhe che rappresentano numeri)
    Returns:
        float: Media calcolata con precisione decimale, 0.0 se non ci sono numeri validi
    """ 
    numeri_validi = []
    for n in numeri:
        try :
            num = float(n)
            numeri_validi.append(num)
        except (ValueError, TypeError):
            # Ignora gli elementi che non possono essere convertiti in float
            continue
    if not numeri_validi:
        return 0.0
    return sum(numeri_validi) / len(numeri_validi)

def main():
    """
    Funzione principale per testare il calcolo della media.
    """
    numeri = []
    while True:
        input_numeri = input("Inserisci un numero o 0 per terminare): ")
        if input_numeri == "0":
            break
        numeri.append(input_numeri)
    media = calcola_media(numeri)
    print(f"La media dei numeri validi è: {media:.2f}")

if __name__ == "__main__":
    main()