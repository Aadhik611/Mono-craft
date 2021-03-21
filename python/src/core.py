from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

import threading, random

import esp, client as clientlib

# $Connection portal
IP = "192.168.100.245"

RECV_HEADER = 1024

# Recv thread controls
global recv_thread_status
recv_thread_status = True

global latest_recv_message
latest_recv_message = ""


client = clientlib.app(IP, 80, "|")
client.connect()

app = Ursina()


class Voxel(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model="cube",
            origin_y=0.5,
            texture="white_cube",
            color=color.rgb(0, random.randrange(200, 240), 8),
            highlight_color=color.lime,
        )

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                new_block_pos = self.position + mouse.normal
                client.send(
                    f"CREATE-BLOCK {str(int(new_block_pos.x))} {str(int(new_block_pos.y))} {str(int(new_block_pos.z))} "
                )
                # voxel = Voxel(position=new_block_pos)

            if key == "right mouse down":
                destroy(self)


def constant_recv():

    while recv_thread_status:

        print("Thread still running!")

        latest_recv_message = str(client.recv(RECV_HEADER).decode("utf-8"))
        print(latest_recv_message)
        if latest_recv_message.startswith("CREATE-BLOCK "):

            print(latest_recv_message[len("CREATE-BLOCK ") :])

            new_voxel_pos = latest_recv_message[len("CREATE-BLOCK ") :].split(" ")
            print(new_voxel_pos)

            print(new_voxel_pos[0], new_voxel_pos[1], new_voxel_pos[2])

            new_voxel = Voxel(
                position=(
                    int(new_voxel_pos[0]),
                    int(new_voxel_pos[1]),
                    int(new_voxel_pos[2]),
                )
            )

            print(
                f"[RECV-FROM-SERVER]: added new block at {latest_recv_message[len('CREATE-BLOCK '):]}"
            )


constant_recv_thread = threading.Thread(target=constant_recv)
constant_recv_thread.start()


def input(key):
    if key == "q":
        recv_thread_status = False
        client.close()
        app.closeWindow()


for z in range(8):
    for x in range(8):
        voxel = Voxel(position=(x, 0, z))


player = FirstPersonController()
app.run()