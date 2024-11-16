from enum import IntEnum, unique
import asyncio


import requests

from bleak import BleakClient


DEVICE_ADDRESS = "C7:EE:68:12:B0:98"


@unique
class MessageType(IntEnum):
    """Pixel dices Bluetooth messages identifiers"""
    _None = 0
    WhoAreYou = 1
    IAmADie = 2
    State = 3
    Telemetry = 4
    BulkSetup = 5
    BulkSetupAck = 6
    BulkData = 7
    BulkDataAck = 8
    TransferAnimSet = 9
    TransferAnimSetAck = 10
    TransferSettings = 11
    TransferSettingsAck = 12
    DebugLog = 13
    PlayAnim = 14
    PlayAnimEvent = 15
    StopAnim = 16
    RequestState = 17
    RequestAnimSet = 18
    RequestSettings = 19
    RequestTelemetry = 20
    ProgramDefaultAnimSet = 21
    ProgramDefaultAnimSetFinished = 22
    Flash = 23
    FlashFinished = 24
    RequestDefaultAnimSetColor = 25
    DefaultAnimSetColor = 26
    RequestBatteryLevel = 27
    BatteryLevel = 28
    Calibrate = 29
    CalibrateFace = 30
    NotifyUser = 31
    NotifyUserAck = 32
    TestHardware = 33
    SetStandardState = 34
    SetLEDAnimState = 35
    SetBattleState = 36
    ProgramDefaultParameters = 37
    ProgramDefaultParametersFinished = 38

    # TESTING
    SetAllLEDsToColor = 41
    AttractMode = 42
    PrintNormals = 43
    PrintA2DReadings = 44
    LightUpFace = 45
    SetLEDToColor = 46

    Count = 47


def print_state(msg):
    state = msg[1]
    print(f'face state {state}')
    # face = face + 1 if state == 1 else 0
    # if self._face_up != face:
    #     self._face_up = face
    #     self.face_up_changed.notify(face)


async def process_message(msg):
    """Processes a message coming for the device and routes it to the proper message handler"""
    state = MessageType(msg[0]).name
    #print(f'dice => {state}: {", ".join([format(i, "02x") for i in msg[1:]])}')
    #print(str(state))
    print(state)
    if (state == "ProgramDefaultAnimSetFinished"):
        print("nat20 babyyyy")
        #send request to turn lights off
        requests.get("http://arduino.pyhub.com/stoplights")
        #sedn request to trun lights on 
        await asyncio.sleep(5)
        requests.get("http://arduino.pyhub.com/startlights")
    # handlers = self._message_map.get(msg[0])
    # for handler in handlers:
    #     if handler != None:
    #         # Pass the message to the handler
    #         handler(self, msg)


async def notification_handler(sender, data):
    """
    Callback function that gets called when a notification is received.

    :param sender: The characteristic that sent the notification.
    :param data: The data received from the device.
    """
    #print(f"Notification from {sender}: {data}")
    await process_message(list(data))

async def connect_to_device(address):
    async with BleakClient(address) as client:
        is_connected= await client.is_connected()
        print(f"connected to device : {is_connected}")

        services = await client.get_services()
        print(f"Services and characteristics for device {address}:\n")


        #Iterate through all services and characteristics
        for service in services:
            print(f"Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid}")
                # Check if characteristic supports "notify"
                if "notify" in char.properties:
                    print(f"    --> Supports notifications!")
                # List other properties for completeness
                print(f"    Properties: {char.properties}")
    

        await client.start_notify("6e400001-b5a3-f393-e0a9-e50e24dcca9e", notification_handler)

        await asyncio.sleep(3600)  
# notify
#6e400001-b5a3-f393-e0a9-e50e24dcca9e


bytearray()

asyncio.run(connect_to_device(DEVICE_ADDRESS))