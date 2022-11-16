from task_modules.PHtask_mouse_screen_coords import MouseListener
from task_modules.PHtask_openCV import take_webcam_picture
from task_modules.PHtask_SQLite import SQLiteObj

import asyncio
import websockets

all_clients, x_values_List, y_values_List = [], [], []


async def read_data_from_SQLite_db(db_name, value_of_interest, id_data):
    my_database = SQLiteObj(db_name)
    fetched_data = my_database.execute_select_database_by_name(value_of_interest, id_data)
    return fetched_data


def list_of_int_to_string(list_int):
    result_string = ','.join(str(item) for item in list_int)
    return result_string

def populate_sqlite_db(x_coords, y_coords, image_as_np_array):
    # First I convert my x_coord from [int] to string
    # Not the best solution -> 0(N)
    x_coords_as_string = list_of_int_to_string(x_coords)
    y_coords_as_string = list_of_int_to_string(y_coords)
    # Note: SQLiteOBJ(:memory:) to store in RAM
    my_database = SQLiteObj("parcel_hive_data.db")
    my_database.create_database()
    my_database.execute_insert_database(x_coords_as_string, y_coords_as_string, image_as_np_array)
    # Note: I need to add (name.db). Comment if name == ":memory:"
    # my_database.delete_table()
    my_database.close_db()


# This Function I use to retrieve and send mouse(x, y) coord. Upon LMB click, take pic and populate database
async def send_coord_take_pic():
    # Here I create my MouseListener object which reports mouse(X,Y) coord and listens for LMB click
    my_listener = MouseListener()
    while True:
        # Not sure if I need to put this in a function, but the problem is that I get too many values
        await asyncio.sleep(0.1)
        x_values_List.append(my_listener.coord_X)
        y_values_List.append(my_listener.coord_Y)
        for client in all_clients.copy():
            try:
                await client.send(f"{str(my_listener.coord_X)} - {str(my_listener.coord_Y)}")
            except websockets.WebSocketException:

                all_clients.remove(client)
        if my_listener.cv_photo:
            image_value = await take_webcam_picture()
            populate_sqlite_db(x_values_List, y_values_List, image_value)
            my_listener.reset_listening()


# Here I confirm client connection, wait for "Client"
async def new_client_connect(client_socket, path):
    print("New client connected")
    all_clients.append(client_socket)

    while True:
        new_message = await client_socket.recv()
        print("Client sent: ", new_message)
        if new_message == "Client_Connected":
            await send_coord_take_pic()


async def start_server():
    print("Server started!")
    await websockets.serve(new_client_connect, "localhost", 12345)


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(start_server())
    event_loop.run_forever()
