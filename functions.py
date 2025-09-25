from openai import OpenAI
from config import FILES_PATH
import base64, json, requests, time, os, subprocess, psutil
from keys import UNSPLASH_KEY, OPENAI_KEY
from datetime import datetime
from pathlib import Path

def actually_date():
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return now

def read_json(file_name):
    path = FILES_PATH / file_name

    with open (path, "r", encoding="utf-8") as file:
        content = json.load(file)

    return content

def export_json(content, file_name):
    path = FILES_PATH / file_name
    
    with open(path, "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False, indent=4)

def save_log(error):
    path = FILES_PATH / "log.txt"
    now = actually_date()

    with open(path, "a", encoding="utf-8") as file:
        file.write(f"{now}| {error}\n")

def save_txt_append(content, file_name):
    path = FILES_PATH / file_name

    with open(path, "a", encoding="utf-8") as file:
        file.write(f"{content}\n\n")

def run_anki():
    user_name = Path.home().name
    subprocess.Popen([f"C:\\Users\\{user_name}\\AppData\\Local\\Programs\\Anki\\anki.exe"])

def is_anki_running():
    app_name = "anki"

    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and app_name.lower() in proc.info['name'].lower():
            return True
    return False
    
def cards_generate(words):
    client = OpenAI(api_key=OPENAI_KEY)

    response = client.responses.create(
        input=words,
        model="gpt-4.1-mini",
        prompt={
            "id": "pmpt_68d343723d9881908337b65bc3c8442a013466a52e4e59ce",
            "version": "14"
        }
    )

    output_text = response.output_text
    output_text = json.loads(output_text)

    return output_text

def create_deck(words):
    print(f"Progresso: [0%]")
    
    show_error = ""
    cards_saved = 0
    cards_error = []

    try:
        anki_connect_url = "http://127.0.0.1:8765"
        payload_creat_deck = {
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": "Word by Word",
            }
        }

        response_deck = requests.post(anki_connect_url, json=payload_creat_deck).json()

    except Exception as error:
        save_log(error)

    try:
        terms = cards_generate(words)
        cards_numbers = len(terms)

    except Exception as error:
        terms = ""
        save_log(error)

    if terms:
        for item in terms:
            try:
                front = item["front"].strip()
                back = item["back"].strip()

                if item["possible_img"]:
                    img_name = download_img(front)
                    back += f"<img src='{img_name}'>"

                payload_creat_card = {
                "action": "addNote",
                "version": 6,
                "params": {
                    "note": {
                    "deckName": "Word by Word",
                    "modelName": "Básico",
                    "fields": {
                        "Frente": front,
                        "Verso": back
                    },
                    "tags": ["vocab"]
                    }
                }
                }

                response_card = requests.post(anki_connect_url, json=payload_creat_card).json()

                if response_deck["error"] is None and response_card["error"] is None:
                    cards_saved += 1
                    progress = int((cards_saved / cards_numbers) * 100)
                    
                    os.system("cls")
                    print(f"Progresso: [{progress}%]")

                else:
                    cards_error.append({
                        "front": f"{front}",
                        "error_deck": response_deck["error"],
                        "error_card": response_card["error"],
                    })

                time.sleep(2)

            except Exception as error:
                save_log(error)
                
        os.system("cls")
        
        if cards_error:
            for error in cards_error:
                front = error["front"]
                error_deck = error["error_deck"]
                error_card = error["error_card"]

                show_error += f"Card '{front}' | Error deck: {error_deck} | Error Card: {error_card}\n"
        
        if show_error != "":
            print(show_error)


def get_link_img(word):
    unsplash_url = "https://api.unsplash.com/search/photos"

    payload = {
        "query": word,
        "client_id": UNSPLASH_KEY
    }

    response = requests.get(unsplash_url, params=payload)
    response = response.json()
    results = sorted(response["results"], key= lambda x: x["likes"], reverse=True)

    #Resultado com mais like
    url_img = results[0]["urls"]["small"]
    name_img = results[0]["alternative_slugs"]["pt"][:20]
    
    return url_img, name_img

def download_img(word):
    url_img, name_img = get_link_img(word)
    name_img = f"{name_img}.jpeg"

    response = requests.get(url_img)
    img_base64 = base64.b64encode(response.content).decode("utf-8")

    anki_connect_url = "http://127.0.0.1:8765"

    payload = {
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": name_img,
            "data": img_base64
        }
    }

    requests.post(anki_connect_url, json=payload)

    return name_img