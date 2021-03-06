## Table of Contents
* [Description](#description)
* [MQTTClient](#mqttclient)
* [connect](#connect)
* [close](#close)
* [set_uplink_callback](#set_uplink_callback)
  * [uplink_callback](#uplink_callback)
* [set_connect_callback](#set_connect_callback)
  * [connect_callback](#connect_callback)
* [set_downlink_callback](#set_downlink_callback)
  * [downlink_callback](#downlink_callback)
* [set_close_callback](#set_close_callback)
  * [close_callback](#close_callback)
* [send](#send)
* [Errors](#errors)
* [UplinkMessage](#uplinkmessage)

## Description

This package provides you an easy way to connect to The Things Network via MQTT.

### MQTTClient

The class constructor can be called following this scheme:
```python
MQTTClient(app_id, app_access_key, [mqtt_address], [discovery_address])
```
- `app_id`: **string**  this the name given to the application when it was created.
![Screenshot of the console with app section](./images/app-console.png?raw=true)
- `app_access_key`: **string**  this can be found at the bottom of the application page under **ACCESS KEYS**.
![Screenshot of the console with accesskey section](./images/accesskey-console.png?raw=true)
- `mqtt_address`: **string**  this  is the address of the handler to which the application was registered. It needs to be provided as an `mqtt_address=value` argument when calling the constructor.
- `discovery_address`: **string** this is the address of the discovery server to use in order to find back the address of the MQTT handler. It needs to be provided as an `discovery_address=value` argument when calling the constructor.
The constructor returns an **MQTTClient object** set up with the application informations, ready to be connected to The Things Network.

### connect
Connects and starts the client in the background. This function also re-establishes the client's connection in case it was closed.
```python
client.connect()
```

### close
Disconnects and stops the client from which the method is called.
```python
client.close()
```

### Using Callbacks

The callback functions are functions which are executed when a trigger event happens.

#### set_uplink_callback
Add a callback function, to be called when an uplink message is received.
```python
client.set_uplink_callback(uplink_callback)
```

##### uplink_callback
The callback function must be declared in the script following this structure:
* `uplink_callback(msg, client)`
  * `msg`: **UplinkMessage object**  the message received by the client.
  * `client`: **MQTTClient object**  the client from which the callback is executed.

#### set_connect_callback
Add a connection callback function to be executed when the client connects to the broker.
```python
client.set_connect_callback(connect_callback)
```
##### connect_callback
- `connect_callback(res, client)`: the function which will be executed on connection to the broker.
  - `res`: **boolean**  the result of the connection. If it's true, the connection succeeded. If not, it means the connection failed.
  - `client`: **MQTTClient object**  the TTN client from which the callback is called.

#### set_downlink_callback
Add a downlink callback function, with actions to execute when a downlink message is sent.
```python
client.set_downlink_callback(downlinkCallback)
```
##### downlink_callback
- `downlink_callback(mid, client)`: the function which will be a new publish behavior for our MQTT client.
  - `mid`: **int**  this is the message ID for the downlink request. It can be used to track the request.
  - `client`: **MQTTClient object**  the TTN client from which the callback is called.

#### set_close_callback
Add a callback to be executed when the connection to the TTN broker is closed.
```python
client.set_close_callback(close_callback)
```
##### close_callback
- `close_callback(res, client)`: the function which will be executed when the connection is closed.
  - `res`: **boolean**  the result of the disconnection. If it's true, it went all as expected. If not, it means the disconnection was unexpected.
  - `client`: **MQTTClient object**  the TTN client from which we call the callback.

### send
Sends a downlink to the device.
```python
client.send(dev_id, payload, [port], [confirmation], [schedule])
```
- `dev_id`: **string**  the ID of the device which will receive the message.
- `payload`: the payload of the message to be published to the broker. It can be an hexadecimal **string**, a base64 **string** like `AQ==` (this will send the raw payload `01` to your device) or a **dictionary** of JSON nature. Here is an example of a **dictionary** argument that could be passed to the method:
```json
{"led_state": "on", "counter": 1}
```
In case it's a **dictionary** with fields, please make sure the **encoder** function (Payload Formats section) of the application is set to make sense of the informations transmitted in each field.
![Screenshot of an encoder function in the console](./images/encoder-function.png?raw=true)
- `port`: **int**  the port of the device to which the message will be sent. Default value to 1.
- `confirmation`: **boolean**  this boolean indicates if you wish to receive a confirmation after sending the downlink message. Default value to False.
- `schedule`: **string**  this string provides the type of schedule on which the message should be sent. It can take values such as `first` or `last`. Default value to `replace`.

### Errors
Errors can happen on connection for different reasons:
* Wrong `app_id`, `access_key` or `mqtt_address` were provided to the constructor.
* The machine may not have access to the network/The MQTT server could be down/Firewall restrictions could prevent connection
* The client process doesn't have system capabilities to open a socket
* The MQTT server uses MQTTS, but the client won't accept the TLS certificate
Errors could also happen when closing connection, in case the disconnection is unexpected.
It's possible to catch those exceptions using `except RuntimeError as` and print the error.

### UplinkMessage
This type of object is constructed dynamically from the message received by the client, so this means some attributes can change from one message to another. However here are some constant attributes usually found in UplinkMessage objects:
* app_id: the application ID to which the device is registered
* dev_id: the ID of the device
* port: the port number on which the message was sent
* payload_raw: a buffer which contains the payload in hexadecimal
* metadata: this field is another object which contains all the metadata of the message. Such as: the date, the frequency, the data rate and the list of gateways.
