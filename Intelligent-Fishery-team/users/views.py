from django.shortcuts import render

from django.shortcuts import render, redirect
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

# 配置你的Neo4j数据库连接
neo4j_conn = Neo4jConnection(uri="bolt://localhost:7687",user="neo4j",password="12345678")

def index(request):
    query = """
    MATCH (u:User)-[:BELONG]->(r:Role), (u)-[:HAS_PASSWORD]->(p:Password)
    RETURN u.username AS username, r.name AS role, p.password AS password
    """
    users = neo4j_conn.query(query)
    print(users)
    context = {'users': users}
    return render(request, 'fishery/admin_management.html', context)

def edit(request, username):
    if request.method == 'POST':
        new_role = request.POST['role']
        query = """
        MATCH (u:User {username: $username})-[rel:BELONG]->(r:Role)
        DELETE rel,r
        WITH u
        CREATE (newRole:Role {name: $new_role})
        CREATE (u)-[:BELONG]->(newRole)
        RETURN u
        """
        neo4j_conn.query(query, parameters={"username": username, "new_role": new_role})
        return redirect('index')

def delete(request, username):
    if request.method == 'POST':
        query = """
        MATCH (u:User {username: $username})
        DETACH DELETE u
        """
        neo4j_conn.query(query, parameters={"username": username})
        return redirect('index')
