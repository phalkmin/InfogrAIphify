# InfogrAIphify 
<sub><sup>(former Extrator de Conteúdo e Gerador de Infográficos (Tabajara)) </sup></sub>

Este é um script em Python que extrai o conteúdo de texto de uma URL fornecida, utiliza a API da OpenAI para gerar uma descrição visual para um infográfico com base nesse conteúdo, e, em seguida, utiliza a API do DALL-E para gerar uma imagem correspondente à descrição visual. 

### Como Funciona

O script extrai o conteúdo de texto de uma URL fornecida. Por enquanto, o conteúdo d URL **deve** conter as tags `main` ou `article` para funcionar corretamente. Com a API da OpenAI ele gera uma descrição visual do contéudo, e novamente usa a API para gerar um infográfico referente à descrição visual.

### Como Usar

Clone este repositório:

    git clone https://github.com/phalkmin/InfogrAIphify.git

Instale as dependências:

    pip install -r requirements.txt

Crie um arquivo .env na mesma pasta do script Python e adicione sua chave API do OpenAI no formato 

    OPENAI_API_KEY=sua-chave-api-aqui.

Execute o script:

    python opengraphic.py <URL>

O script será executado no terminal e retornará no final a URL com o infográfico. Importante: o DALL-E é **burro** e gera textos muito mal. Use um editor de imagens para finalizar o trabalho, como Photoshop, Gimp, Canva, etc.

### Nota

Certifique-se de ter as chaves APIs da OpenAI e do DALL-E antes de executar o script - para obtê-las, acesse o [site da OpenAI](https://platform.openai.com/api-keys) e siga as instruções. Lembre-se também que o uso da ferramenta é pago.