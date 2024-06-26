from django.shortcuts import render, redirect
from django.http import JsonResponse
from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship, NodeMatcher
import json

# 连接到 Neo4j 数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))


# 注册
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # 判断用户名是否存在于 User 节点
        if graph.nodes.match("User", username=username).first():
            return JsonResponse({"message": "Username already exists"}, status=400)

        # 创建一个新的 User 节点
        user = Node("User", username=username)
        graph.create(user)

        # 创建一个新的 Password 节点
        password_node = Node("Password", password=password)
        graph.create(password_node)

        role_node = Node("Role", name=role)
        graph.create(role_node)

        # 建立 User 节点和 Password 节点之间的关系
        rel = Relationship(user, "HAS_PASSWORD", password_node)
        graph.create(rel)

        belong = Relationship(user, "BELONG", role_node)
        graph.create(belong)

        return redirect("../login")  # 注册成功后跳转到登录页面

    return render(request, "fishery/register.html")


# 登录
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 查找带有给定用户名的 User 节点
        user = graph.nodes.match("User", username=username).first()

        if user:
            # 获取与 User 节点关联的 Password 节点
            rel = graph.match((user,), r_type="HAS_PASSWORD").first()
            role = graph.match((user,), r_type="BELONG").first().end_node["name"]
            if rel != None and (rel.end_node["password"] == password):
                user_info = {"username": username, "role": role}

                request.session["user_info"] = user_info

                return redirect("../homepage")
            else:
                return JsonResponse({"message": "Invalid credentials"}, status=401)
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=401)

    return render(request, "fishery/login.html")


def homepage(request):
    # 从会话中获取用户信息
    user_info = request.session.get("user_info", None)

    return render(
        request,
        "fishery/homepage.html",
        {"user_info": user_info},
    )


def user(request):
    user_info = request.session.get("user_info", None)
    if request.method == "POST":
        username = user_info["username"]
        password = request.POST.get("password")

        # 查找带有给定用户名的 User 节点
        user = graph.nodes.match("User", username=username).first()

        if user:
            # 获取与 User 节点关联第一个关系
            rel = graph.match((user,), r_type="HAS_PASSWORD").first()
            if rel != None and (rel.end_node["password"] == password):
                return JsonResponse(
                    {"message": "Same password,please retry"}, status=401
                )
            else:
                # 更新已有的密码节点
                rel.end_node["password"] = password
                graph.push(rel.end_node)
                return redirect("../login")
    return render(request, "fishery/user.html", {"user_info": user_info})


def illustration(request):
    user_info = request.session.get("user_info", None)
    return render(request, "fishery/illustration.html", {"user_info": user_info})


def main_info(request):
    user_info = request.session.get("user_info", None)
    return render(request, "fishery/main_info.html", {"user_info": user_info})


def underwater_system(request):
    user_info = request.session.get("user_info", None)
    return render(request, "fishery/underwater_system.html", {"user_info": user_info})


def data_center(request):
    user_info = request.session.get("user_info", None)
    return render(request, "fishery/data_center.html", {"user_info": user_info})


def intelligence_center(request):
    user_info = request.session.get("user_info", None)
    return render(request, "fishery/intelligence_center.html", {"user_info": user_info})


def admin_management(request):
    user_info = request.session.get("user_info", None)
    return render(request, "fishery/admin_management.html", {"user_info": user_info})



