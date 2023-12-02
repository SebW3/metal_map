from logins import openAI_api_key
import openai
from datetime import datetime

def bands_from_description(description):
    prompt_system = 'Twoim zadaniem jest wypisać po przecinku nazwy wszystkich zespołów które będą brały udział w wydarzeniu bazując na podanym ci opisie wydarzenia. Twoja odpowiedź ma być w formacie: "Zespół1, Zespół2, Zespół3". Jeśli nie znajdziesz informacji napisz tylko "n/a"'
    messages = [{"role": "system", "content": prompt_system}, {"role": "user", "content": description}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        api_key=openAI_api_key(),
        temperature=0
    )

    return response.choices[0].message.content

def create_short_description(description):
    prompt_system = 'Twoim zadaniem jest stworzyć krótki opis wydarzenia na podstawie podanego ci długiego opisu'
    messages = [{"role": "system", "content": prompt_system}, {"role": "user", "content": description}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        api_key=openAI_api_key(),
        temperature=0
    )

    return response.choices[0].message.content

def get_info_from_fb_desc(description):
    prompt_system = f"Twoim zadaniem jest wypisanie ważnych informacji z tego opisu koncertu. Napisz jakie zespoły będą grać i w nawiasie napisz ich gatunki jeśli zostały podane. Jeśli nie będzie informacji to napisz w jej miejsce 'n/a', a jeśli nie będzie tylko części np jest data a nie ma godzint to wypisz tylko to co jest. Datę napisz w formacie dd.mm.yyyy a jeśli nie ma podanego roku to wpisz {datetime.now().year} rok. Stosuj podany ci format odpowiedzi oddzielając każdą część średnikami: Zepoły: Zespół1 (gatunek), Zespół2 (gatunek); Data i godzina: (data, godzina rozpoczęcia koncertu); Lokalizacja: (tylko ulica, miasto, kraj); Cena biletu: (cena); Miasto koncertu: (tylko miasto)"
    messages = [{"role": "system", "content": prompt_system}, {"role": "user", "content": description}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        api_key=openAI_api_key(),
        temperature=0
    )

    return response.choices[0].message.content
