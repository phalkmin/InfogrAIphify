import sys
import os
import requests
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def extrair_texto_da_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    main_content = soup.find('main')
    article_content = soup.find('article')

    texto_extraido = ""

    if main_content:
        texto_extraido += main_content.get_text().strip() + "\n"

    if article_content:
        texto_extraido += article_content.get_text().strip() + "\n"

    return texto_extraido

# Função para chamar a API do OpenAI
def chamar_openai_api(texto):
    
    chave_api = os.getenv("OPENAI_API_KEY")

    if chave_api is None:
        print("Chave API do OpenAI não encontrada. Certifique-se de definir OPENAI_API_KEY no arquivo .env.")
        return None

    prompt = "Meu trabalho é criar infográficos que engajem visualmente para conteúdos na web. Preciso que você assuma a persona de um criador de infográficos profissional e gere uma descrição visual para o infográfico, para que o designer gráfico possa então criá-lo. Use o texto abaixo para isso: \n" + texto

    client = OpenAI(
        api_key=chave_api,
    )


    resposta = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
    return resposta.choices[0].message.content


def dalle_lek(texto):
    
    chave_api = os.getenv("OPENAI_API_KEY")

    if chave_api is None:
        print("Chave API do OpenAI não encontrada. Certifique-se de definir OPENAI_API_KEY no arquivo .env.")
        return None

    prompt = "Crie um infográfico para um post de blog usando a seguinte descrição visual: \n" + texto

    client = OpenAI(
        api_key=chave_api,
    )

    resposta = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      size="1024x1024",
      quality="standard",
      n=1,
    )

    return resposta.data[0].url


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Por favor, forneça a URL como argumento da linha de comando.")
        url = input("Digite a URL para extrair o conteúdo: ")
    else:
        url = sys.argv[1]

    conteudo_extraido = extrair_texto_da_url(url)

    if conteudo_extraido:
        resposta_openai = chamar_openai_api(conteudo_extraido)
        if resposta_openai:
            print("Resposta do OpenAI:")
            print(resposta_openai)
            url_imagem = dalle_lek(resposta_openai)
            if url_imagem:
                print("URL da imagem gerada:", url_imagem)
    else:
        print("Não foi possível extrair o conteúdo da URL.")
