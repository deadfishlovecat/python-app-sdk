# coding: Latin-1
# Copyright © 2017 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


import os
import time
import json
from ttn import MQTTClient as mqtt

appID = "guest"
accessKey = "guest"
mqttAddress = "localhost:1883"

uplink = {
  "dev_id": "guest",
  "port": 1,
  "counter": 5,
  "payload_raw": "AQ==",
  "payload_fields": {
    "led": True,
  },
  "metadata": {
    "time": "2016-09-14T14:19:20.272552952Z",
    "frequency": 868.1,
    "modulation": "LORA",
    "data_rate": "SF7BW125",
    "coding_rate": "4/5",
    "gateways": [{
      "eui": "B827EBFFFE87BD22",
      "timestamp": 1960494347,
      "time": "2016-09-14T14:19:20.258723Z",
      "rssi": -49,
      "snr": 9.5,
      "rf_chain": 1,
    }],
  },
}


def test_connect_disconnect():

    def connectcallback(res, client):
        print(res)
        assert res

    def closecallback(res, client):
        print(res)
        assert res

    ttn_client = mqtt(appID, accessKey, mqtt_address=mqttAddress)
    ttn_client.set_connect_callback(connectcallback)
    ttn_client.set_close_callback(closecallback)
    ttn_client.connect()
    time.sleep(2)
    ttn_client.close()


def test_uplink():

    def uplinkcallback(message, client):
        print(message)
        assert message.payload_raw == 'AQ=='

    ttn_client = mqtt(appID, accessKey, mqtt_address=mqttAddress)
    ttn_client.set_uplink_callback(uplinkcallback)
    ttn_client.connect()
    time.sleep(2)
    ttn_client._MQTTClient__client.publish(
        'guest/devices/guest/up',
        json.dumps(uplink))
    time.sleep(2)
    ttn_client.close()


def test_connect_error():

    def connectcallback(res, client):
        print(res)
        assert res is False

    ttn_client = mqtt(appID, accessKey, mqtt_address='badAddress:5555')
    ttn_client.set_connect_callback(connectcallback)
    try:
        ttn_client.connect()
    except:
        ttn_client.close()


def test_downlink_payloadraw():

    def downlinkcallback(mid, client):
        print(mid)
        assert mid == 2

    ttn_client = mqtt(appID, accessKey, mqtt_address=mqttAddress)
    ttn_client.set_downlink_callback(downlinkcallback)
    ttn_client.connect()
    time.sleep(2)
    ttn_client.send('guest', "AQ==")
    time.sleep(2)
    ttn_client.close()


def test_downlink_payloadfields():

    def downlinkcallback(mid, client):
        print(mid)
        assert mid == 2

    ttn_client = mqtt(appID, accessKey, mqtt_address=mqttAddress)
    ttn_client.set_downlink_callback(downlinkcallback)
    ttn_client.connect()
    time.sleep(2)
    ttn_client.send('guest', {"field1": 1, "field2": 2})
    time.sleep(2)
    ttn_client.close()


def test_providing_all_downlink_options():

    def downlinkcallback(mid, client):
        print(mid)
        assert mid == 2

    ttn_client = mqtt(appID, accessKey, mqtt_address=mqttAddress)
    ttn_client.set_downlink_callback(downlinkcallback)
    ttn_client.connect()
    time.sleep(2)
    ttn_client.send('guest', "AQ==", 2, True, "first")
    time.sleep(2)
    ttn_client.close()
