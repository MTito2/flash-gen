from functions import create_deck, run_anki, is_anki_running
import os, time

while True:
    if is_anki_running() is False:
        run_anki()
        time.sleep(5)
    
    os.system("cls")
    words = input("Informe palavras ou frases (Limite de 10): ")
    
    try:
        os.system("cls")
        create_deck(words)
        os.system("cls")
        print("FlashCards criados com sucesso!")

    except Exception:
        ...

