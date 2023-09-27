from logins import openAI_api_key
import openai

prompt_system = 'Twoim zadaniem jest wypisać po przecinku nazwy wszystkich zespołów które będą brały udział w wydarzeniu bazując na podanym ci opisie wydarzenia. Twoja odpowiedź ma być w formacie: "Zespół1, Zespół2, Zespół3"'
description = 'Australijskie trio Altars, pogrobowcy Death Metalu zagranego ze swoistą pasją i charakterystyczną dla Antypodów oryginalnością w znakomitym towarzystwie nowej brazylijskiej nadziei Fossilization wystąpią 23.09. w Warszawie. Ich najnowsza płyta "Ascetic Reflection" ukazała się pod koniec zeszłego roku, nakładem prężnie funkcjonującej włoskiej wytwórni Everlasting Spew Records. Zawarta na niej muzyka potwierdza nietuzinkowe umiejętności i nieszablonowe podejście do metalowej materii. W zderzeniu z taką masą, niewielu ma szanse wyjść bez szwanku!'
messages = [{"role": "system", "content": prompt_system},{"role": "user", "content": description}]

def bands_from_description(description):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        api_key=openAI_api_key(),
        temperature=0
    )

    return response.choices[0].message.content

# print(response)
# print("-"*100)
# print(response.choices[0].message.content)