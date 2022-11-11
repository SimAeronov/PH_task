import sqlite3


class SQLiteObj:
    """ This class is used to run operate SQLite"""

    def __init__(self, name_of_db_file):
        self.db_conn = sqlite3.connect(f'{name_of_db_file}')
        self.db_cursor = self.db_conn.cursor()

    # TODO: I need to add name of table and name+type for columns
    def create_database(self):
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS PHtask_table(
                            id_data integer primary key autoincrement,
                            X_coordinate text,
                            Y_coordinate text,
                            PNG_image blob
                            )""")

    # TODO: Note, here the name of the table must match existing name!
    def execute_insert_database(self, x_coordinate, y_coordinate, png_image):
        # Here I use %s
        self.db_cursor.execute("INSERT INTO PHtask_table(X_coordinate, Y_coordinate, PNG_image)"
                               " VALUES(:x_coordinate_val, :y_coordinate_val, :png_image_val)",
                               {'x_coordinate_val': x_coordinate, 'y_coordinate_val': y_coordinate,
                                'png_image_val': sqlite3.Binary(png_image)});
        self.db_conn.commit()

    def execute_select_database_by_name(self, value_interest,  value_of_data):
        self.db_cursor.execute("SELECT PNG_image FROM PHtask_table WHERE id_data = :value_of_id_data",
                               {'value_of_id_data': value_of_data})
        fetched_data = self.db_cursor.fetchone()
        self.db_conn.commit()
        return fetched_data

    def close_db(self):
        self.db_conn.close()
        print("NOTE: DataBase closed!")

    def delete_table(self):
        self.db_cursor.execute("DROP TABLE IF EXISTS PHtask_table;")
        print("NOTE: Table was deleted!")
