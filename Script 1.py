import requests
import json

headers = {"Authorization": "Bearer YOUR TOKEN KEY"}


def run_query(query): #Função que executa uma request pela api graphql 
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers) #efetua uma requisição post determinando o json com a query recebida
    if request.status_code == 200:
        return request.json() #json que retorna da requisição
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


#Respostas das perguntas na Query:
#Questão 1 - Métrica: idade do repositório - "nameWithOwner" e "createdAt"
#Questão 2 - Métrica: total de pull requests aceitas - "questão 1 + pullRequests(states: MERGED){totalCount}" 
#Questão 3 - Métrica: total de releases - "releases{totalCount}"
#Questão 4 - Métrica: tempo até a última atualização - "updatedAt"
#Questão 5 - Métrica: linguagem primária de cada um desses repositórios - "questão 4 + primaryLanguage{name}"
#Questão 5 - Métrica: razão entre número de issues fechadas pelo total de issues - "closedIssues : issues(states: CLOSED){totalCount}" / "totalIssues: issues{totalCount}"


query = """
{
  search (query:"stars:>100",type: REPOSITORY, first:100) {
    nodes {
        ... on Repository {
          nameWithOwner
          createdAt
          pullRequests(states: MERGED){
            totalCount
          }
          releases{
            totalCount
          }
          updatedAt
          primaryLanguage{
            name
          }
          closedIssues : issues(states: CLOSED){
            totalCount
          }
          totalIssues: issues{
            totalCount
          }
        }
      }
  }
}
"""

result = run_query(query)  #executa a função enviando o formato e quais variávies que o json vai retornar
cleanJson = result["data"]["search"]["nodes"]
print("\n\n ------------- Retorno da consulta com graphQL para responder as Questões de 1 a 6 ------------- \n" )
print(json.dumps(cleanJson, indent=3)) # imprime o json retornado sem os campos de data, search e nodes e identado

