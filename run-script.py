import sys
import os
import requests
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


def extrair_texto_da_url(url):

    '''The function `extrair_texto_da_url` extracts the text content from a given URL and returns it along
    with the language of the webpage.
    
    Parameters
    ----------
    url
        The `url` parameter is the URL of the webpage from which you want to extract the text.
    
    Returns
    -------
        a tuple containing two values: the extracted text from the URL and the language of the webpage.
    
    '''

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    idioma_pagina = soup.html.get('lang')
    main_content = soup.find('main')
    article_content = soup.find('article')

    texto_extraido = ""

    if main_content:
        texto_extraido += main_content.get_text().strip() + "\n"

    if article_content:
        texto_extraido += article_content.get_text().strip() + "\n"

    return texto_extraido, idioma_pagina


def chamar_openai_api(texto, idioma_pagina): 
    '''
        The function `chamar_openai_api` takes in a `texto` and `idioma_pagina` as input parameters. It uses
        the OpenAI API to generate a visual description for an infographic based on the given text. The
        function returns the generated description.
        
        Parameters
        ----------
        texto
            The "texto" parameter is the input text that you want to provide to the OpenAI API. It should
        contain the content or information that you want to generate a visual description for.
        idioma_pagina
            The parameter "idioma_pagina" represents the language of the webpage. It is used to provide context
        to the OpenAI API so that it can generate a description in the appropriate language.
        
        Returns
        -------
            The function `chamar_openai_api` returns the generated description for the infographic based on the
        input text and language of the page.
    
    '''   
 
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )


    if os.getenv("OPENAI_API_KEY") is None:
        print("Chave API do OpenAI não encontrada. Certifique-se de definir OPENAI_API_KEY no arquivo .env.")
        return None

    prompt = "Meu trabalho é criar infográficos que engajem visualmente para conteúdos na web." #curta se você também odeia scroll horiontal em código
    prompt += "Preciso que você assuma a persona de um criador de infográficos profissional e "
    prompt += "gere uma descrição visual para o infográfico, para que o designer gráfico possa então criá-lo. Use o texto abaixo para isso: \n"
    if idioma_pagina is not None:
        prompt += f"Considere que o idioma da página é {idioma_pagina}, "
    prompt += "mas mantenha as instruções em portugês do Brasil. " #curta se você faz debug burro 
    prompt += texto
    
    resposta = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
    return resposta.choices[0].message.content


def dalle_lek(texto, estilo):
    '''The `dalle_lek` function generates an infographic based on a given text description and style using
    the OpenAI DALL-E model.
    
    Parameters
    ----------
    texto
        The "texto" parameter is a string that represents the visual description of the infographic you
    want to create for a blog post. It should provide details about the content, layout, and design
    elements you want to include in the infographic.
    estilo
        The "estilo" parameter is used to specify the desired style for the infographic. It can be any
    valid style option supported by the DALL-E model, such as "natural", "abstract", "cartoon", etc.
    
    Returns
    -------
        The function `dalle_lek` returns the URL of the generated infographic image.
    
    '''
    
    chave_api = os.getenv("OPENAI_API_KEY")

    if chave_api is None:
        print("Chave API do OpenAI não encontrada. Certifique-se de definir OPENAI_API_KEY no arquivo .env.")
        return None

    prompt = "Crie um infográfico para um post de blog usando a seguinte descrição visual: \n" + texto

    if estilo:
        prompt += "O infográfico deve ser feito com o estilo desejado: " + estilo + "."

    client = OpenAI(
        api_key=chave_api,
    )

    resposta = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      size="1024x1792",
      quality="hd",
      style="natural",
      n=1,
    )

    return resposta.data[0].url


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Por favor, forneça a URL como argumento da linha de comando.")
        url = input("Digite a URL para extrair o conteúdo: ")
    else:
        url = sys.argv[1]

    estilo = input("OK, se quiser, inclua instruções de como você gostaria que o infográfico fosse gerado (estilo, cor, fonte, etc.) ou só aperte ENTER para prosseguir: ")

    if not estilo:
        print("sem estilo, então vamos confiar no coração das cartas!")
    
    print("Transformando em infográfico o texto do site: ", url)
    conteudo_extraido, idioma_pagina = extrair_texto_da_url(url)

    if conteudo_extraido:
        resposta_openai = chamar_openai_api(conteudo_extraido, idioma_pagina)
        if resposta_openai:
            print("Aí sim, já temos o necessário para criar o infográfico, aguarde só mais um pouco!")
            url_imagem = dalle_lek(resposta_openai, estilo)
            if url_imagem:
                print("URL da imagem gerada:", url_imagem)
    else:
        print("Não foi possível extrair o conteúdo da URL.")
