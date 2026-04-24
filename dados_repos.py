#importando bibliotecas para importar e tratar dados
import requests
import pandas as pd
import os

#declarando classe
class DadosRepositorios:

    #objeto construtor com os atributos da classe, recebe no atributo usuario qual é a conta que será verificada no github
    def __init__(self, usuario):
        self.usuario = usuario
        self.api_base_url = 'https://api.github.com'
        self.token_acesso='token'
        self.headers = {'Authorization': 'Bearer ' + self.token_acesso, 'X-GitHub-Api-Version': '2022-11-28'}

    #método que lista os repositórios da conta do github (usuario)
    def lista_repositorios (self):
        repos_lista = []

        url = f'{self.api_base_url}/users/{self.usuario}'
        response = requests.get(url, headers = self.headers)
        quantidade_repositorios = response.json()['public_repos']
        numero_paginas = int(round(( quantidade_repositorios / 30),0))

        for numero_pagina in range(1, numero_paginas + 1):
            try:
                url = f'{self.api_base_url}/users/{self.usuario}/repos?page={numero_pagina}'
                response = requests.get(url, headers=self.headers)
                repos_lista.append(response.json())
            except:
                repos_lista.append(None)

        return repos_lista

    def nomes_repos(self, repos_lista): 
        repo_names=[] 
        for pagina in repos_lista:
            for repositorio in pagina:
                try:
                    repo_names.append(repositorio['name'])
                except: 
                    pass

        return repo_names

    def nomes_linguagens(self, repos_lista):
        repo_languages=[]
        for pagina in repos_lista:
            for repositorio in pagina:
                try:
                    repo_languages.append(repositorio['language'])
                except:
                    pass

        return repo_languages

    def cria_df_linguagens (self):

        repositorios = self.lista_repositorios()
        nomes = self.nomes_repos (repositorios)
        linguagens = self.nomes_linguagens (repositorios)

        dados = pd.DataFrame()
        dados['nome_repositorio'] = nomes
        dados['linguagem'] = linguagens

        caminho = f'dados/linguagens_{self.usuario}.csv'
        dados.to_csv(caminho)


        print(f'Linguagens do repositório {self.usuario} coletados com sucesso!')

        return dados
