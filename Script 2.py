import requests
import json
import time
import os


headers = {"Authorization": "Bearer YOUR KEY HERE"}



def run_query(json, headers): #Função que executa uma request pela api graphql 
    request = requests.post('https://api.github.com/graphql', json=json, headers=headers) #efetua uma requisição post determinando o json com a query recebida
    while (request.status_code == 502):
      time.sleep(2)
      request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
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
query example{
  search (query:"stars:>100",type: REPOSITORY, first:20{AFTER}) {
      pageInfo{
       hasNextPage
        endCursor
      }
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

print("\n\n ------------- Começo da consulta com graphQL para responder as Questões de 1 a 6 ------------- \n" )

finalQuery = query.replace("{AFTER}", "")

json = {
    "query":finalQuery, "variables":{}
}

total_pages = 1

result = run_query(json, headers)

#print(result)
nodes = result['data']['search']['nodes']
next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]

#paginating
while (next_page and total_pages < 50):
    total_pages += 1
    cursor = result["data"]["search"]["pageInfo"]["endCursor"]
    next_query = query.replace("{AFTER}", ", after: \"%s\"" % cursor)
    json["query"] = next_query
    result = run_query(json, headers)
    nodes += result['data']['search']['nodes']
    next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]


print("\n\n ------------- Retorno da consulta com graphQL para responder as Questões de 1 a 6 ------------- \n" )
#print(nodes)

#saving data

if os.path.exists("repos.csv"):
  os.remove("repos.csv")

with open("repos.csv", 'w') as the_file:
        the_file.write("nameWithOwner" + ";" + "createdAt" + ";" + "pullRequests/totalCount" + ";" 
        + "releases/totalCount" + ";" + "updatedAt" + ";" + "primaryLanguage/name" + ";" 
        + "closedIssues/totalCount" + ";" + "totalIssues/totalCount" + "\n")
for node in nodes:
    if node['primaryLanguage'] is None:
            primaryLanguage = "none"
    else:
        primaryLanguage = str(node['primaryLanguage']['name'])

    with open("repos.csv", 'a') as the_file:
        the_file.write(node['nameWithOwner'] + ";" + node['createdAt'] + ";" + str(node['pullRequests']['totalCount']) + ";"
        + str(node['releases']['totalCount']) + ";" + node['updatedAt'] + ";" + primaryLanguage + ";" 
        + str(node['closedIssues']['totalCount']) + ";" + str(node['totalIssues']['totalCount']) +  "\n") 


print("\n\n ------------- Retorno do print com graphQL para responder as Questões de 1 a 6 ------------- \n" )