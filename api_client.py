import requests


def get_new_data(patient_id):
    uri = f"http://tesla.iem.pw.edu.pl:9080/v2/monitor/{patient_id}"
    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"
    jResponse = uResponse.json()

    return {
        "birthdate": jResponse["birthdate"],
        "disabled": jResponse["disabled"],
        "firstname": jResponse["firstname"],
        "lastname": jResponse["lastname"],
        "name": jResponse["trace"]["name"],
        "timestamp": jResponse["trace"]["id"],
        "values": [x["value"] for x in jResponse["trace"]["sensors"]],
        "anomalies": [x["anomaly"] for x in jResponse["trace"]["sensors"]]
    }
