from logins import openAI_api_key
import openai


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
