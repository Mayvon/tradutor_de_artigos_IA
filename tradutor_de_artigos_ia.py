 !pip install requests beautifulsoup4 openai langchain-openai

import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for script_or_style in soup(["script", "style"]):
           script_or_style.decompose()
        texto = soup.get_text(separator=' ')
        #Limpar Texto
        linhas = (line.strip() for line in texto.splitlines())
        chunks = (phrase.strip() for line in linhas for phrase in line.split("  "))
        texto_limpo = '\n'.join(chunk for chunk in chunks if chunk)
        return texto_limpo
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None


    text = soup.get_text()
    return text

from langchain_openai.chat_models.azure import AzureChatOpenAI

client = AzureChatOpenAI (
    azure_endpoint= "SEU_ENDPOINT_AQUI",
    api_key= "SUA_CHAVE_AQUI",
    api_version= "SUA_VERSAO_AQUI",
    deployment_name= "NOME_DA_VERSAO_AQUI",
    max_retries=0
)

def translate_article(text, lang):
  messeges = [
      ("system", "Você atua como tradutor de textos"),
      ("user", f"Traduza o {text} para o idioma {lang} e responda em markdown")
  ]

  response = client.invoke(messeges)
  print(response.content)
  return response.content

url = 'https://dev.to/kellycodeschaos/ux-engineering-for-design-systems-274d'
text = extract_text_from_url(url)
article = translate_article(text, "pt-br")

print(article)
