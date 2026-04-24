#importando bibliotecas
import requests
import base64

#criando classe
class ManipulaRepositorios:

    def __init__(self, usuario):
        self.usuario = usuario
        self.api_base_url = 'https://api.github.com'
        self.token_acesso = 'token'
        self.headers = {'Authorization':"Bearer " + self.token_acesso, 'X-GitHub-Api-Version': '2022-11-28'}

    def cria_repo(self, nome_repo):
        data = {
            "name": nome_repo,
            "description": "Dados dos repositórios de algumas empresas",
            "private": False
        }
        response = requests.post(f"{self.api_base_url}/user/repos", json=data, headers=self.headers)

        print(f'Status_code da criação do repositório: {response.status_code}')

    def add_arquivo(self, nome_repo, nome_arquivo, caminho_arquivo):

        # Codificando o arquivo
        with open(caminho_arquivo, "rb") as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content)

        # Realizando o upload
        url = f"{self.api_base_url}/repos/{self.usuario}/{nome_repo}/contents/{nome_arquivo}"
        data = {
            "message": "Adicionando um novo arquivo",
            "content": encoded_content.decode("utf-8")
        }

        response = requests.put(url, json=data, headers=self.headers)
        print(f'Status_code do upload do arquivo: {response.status_code}')
