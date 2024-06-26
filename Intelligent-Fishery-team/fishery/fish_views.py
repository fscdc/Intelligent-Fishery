from django.http import JsonResponse
from django.shortcuts import render

from fishery.views import driver


def get_data(request):
    with driver.session() as session:
        result = session.run("MATCH (a:Fish)"
                             "RETURN a.Species as Species, count(a.Species) AS total")

        data = [{key: value for key, value in record.items()} for record in result]
    return JsonResponse(data, safe=False)


def fish_list(request):
    return render(
        request,
        "fishery/fish/fish_list.html",
    )


def get_weight_data(request):
    with driver.session() as session:
        # 执行Cypher查询
        result = session.run("MATCH (a:Fish) RETURN a.Species as Species, a.Weight as Weight,"
                             "a.Length1, a.Length2,a.Length3, a.Height,a.Width")

        data = [{key: value for key, value in record.items()} for record in result]

    # 返回查询结果
    return JsonResponse(data, safe=False)


def water_list(request):
    return render(
        request,
        "fishery/fish/water.html",
    )


def get_water_data(request):
    with driver.session() as session:
        result = session.run("MATCH (a:water) RETURN a.date as date,a.dd as dd,"
                             "a.ad as ad,a.address as address,a.ry as ry,a.kmzs as kmzs,"
                             "a.zd as zd,a.water_type as water_type,a.ntu as ntu,"
                             "a.zl as zl,a.temperature as temperature,a.ph as ph,"
                             "a.weather as weather,a.zdqk as zdqk"
                             "")

        data = [{key: value for key, value in record.items()} for record in result]

    # 返回查询结果
    return JsonResponse(data, safe=False)
