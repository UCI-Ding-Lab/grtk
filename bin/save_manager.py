import sqlite3
from sqlite3 import Error
import pathlib
import os 
from bin.data_plot_new import line_container
class SaveManager():
    
    def __init__(self, GUI):
        self.GUI = GUI
        
    def _create_db(self, file_path: str) -> None:
        fp = pathlib.Path(file_path)
        if fp.exists():
            os.remove(fp)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.touch()

        sql_create_curve_table = \
            """
                CREATE TABLE IF NOT EXISTS curve 
                (
                    file_path text NOT NULL,
                    type text NOT NULL CHECK (type='system' OR type='background' OR type='real'),
                    curve_id int NOT NULL,

                    pref_show_on_graph int NOT NULL CHECK (pref_show_on_graph=1 OR pref_show_on_graph=0),
                    pref_line_color text,
                    pref_line_size float,
                    pref_marker_style text,
                    pref_marker_size float,
                    pref_marker_color text,
                    
                    PRIMARY KEY (file_path, type, curve_id)

                );
            """
        
        sql_create_coords_table = \
            """
                CREATE TABLE IF NOT EXISTS coords 
                (
                    file_path text NOT NULL,
                    type text NOT NULL CHECK (type='system' OR type='background' OR type='real'),
                    curve_id int NOT NULL,

                    x_coord float NOT NULL,
                    y_coord float NOT NULL,

                    FOREIGN KEY (file_path, type, curve_id) REFERENCES curve (file_path, type, curve_id)
                    
                );
            """
        conn = self._create_connection(file_path)
        if conn is not None:
            self._execute_command(conn, sql_create_curve_table)
            self._execute_command(conn, sql_create_coords_table)
            conn.close()
        else:
            print("Error creating database.")
        
    # def insert_curve(self, fp: str, type: str, curve_id: int,
    
    def _create_connection(self, file_path):
        conn = None
        try:
            conn = sqlite3.connect(file_path)
        except Error as e:
            print(e)
        return conn
    
    def _execute_command(self, conn, command):
        try:
            c = conn.cursor()
            c.execute(command)
            conn.commit()
            return c.fetchall()
        except Error as e:
            print(e)
        return None

    def _save(self, container: line_container, file_path: str):
        conn = self._create_connection(file_path)
        if conn is not None:
            curves_list = container.get_curves_list()
            for i in curves_list:
                pass
            # self._execute_command(conn, sql_create_curve_table)
            # self._execute_command(conn, sql_create_coords_table)
            conn.close()
        else:
            print("Error creating database.")

    def save(self, container: line_container, file_path: str) -> None:
        self._create_db(file_path)
        self._save(container, file_path)
        # print(container.get_curves_list())

if __name__ == '__main__':
    pass