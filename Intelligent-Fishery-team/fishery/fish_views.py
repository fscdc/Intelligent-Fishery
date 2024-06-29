from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from fishery.views import driver


def check_for_anomalies(data, ph_threshold, temp_threshold, oxygen_threshold):
    anomalies = []
    for record in data:
        ph = float(record['ph'])
        temperature = float(record['temperature'])
        ry = float(record['ry'])
        anomaly = False
        if ph > ph_threshold:
            anomaly = True
            record['ph_anomaly'] = ph
        if temperature > temp_threshold:
            anomaly = True
            record['temperature_anomaly'] = temperature
        if ry < oxygen_threshold:
            anomaly = True
            record['ry_anomaly'] = ry
        if anomaly:
            anomalies.append(record)
    return anomalies


@csrf_exempt
def get_data(request):
    with driver.session() as session:
        result = session.run("MATCH (a:Fish) RETURN a.Species as Species, count(a.Species) AS total")
        data = [{key: value for key, value in record.items()} for record in result]
    return JsonResponse(data, safe=False)

@csrf_exempt
def fish_list(request):
    return render(
        request,
        "fishery/fish/fish_list.html",
    )

@csrf_exempt
def get_weight_data(request):
    with driver.session() as session:
        result = session.run("MATCH (a:Fish) RETURN a.Species as Species, a.Weight as Weight,"
                             "a.Length1, a.Length2, a.Length3, a.Height, a.Width")
        data = [{key: value for key, value in record.items()} for record in result]
    return JsonResponse(data, safe=False)

@csrf_exempt
def water_list(request):
    return render(
        request,
        "fishery/fish/water.html",
    )

@csrf_exempt
def get_water_data(request):
    ph_threshold = float(request.GET.get('ph_threshold', 8.5))
    temp_threshold = float(request.GET.get('temp_threshold', 25))
    oxygen_threshold = float(request.GET.get('oxygen_threshold', 5))

    with driver.session() as session:
        result = session.run("MATCH (a:water) RETURN a.date as date, a.dd as dd,"
                             "a.ad as ad, a.address as address, a.ry as ry, a.kmzs as kmzs,"
                             "a.zd as zd, a.water_type as water_type, a.ntu as ntu,"
                             "a.zl as zl, a.temperature as temperature, a.ph as ph,"
                             "a.weather as weather, a.zdqk as zdqk")

        data = [{key: value for key, value in record.items()} for record in result]

    anomalies = check_for_anomalies(data, ph_threshold, temp_threshold, oxygen_threshold)

    return JsonResponse({'data': data, 'anomalies': anomalies}, safe=False)