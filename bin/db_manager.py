import sqlite3
from sqlite3 import Error
import pathlib
import os 
# from bin.data_plot_new import line_container
class DBManager():
    
    def __init__(self, GUI=None):
        self.GUI = GUI
        
    def _create_db(self, db_path: str) -> None:
        fp = pathlib.Path(db_path)
        if fp.exists():
            os.remove(fp)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.touch()
        
        sql_optimizations = \
        [
            "PRAGMA journal_mode = WAL;", \
            "PRAGMA synchronous = EXTRA;", \
            # "PRAGMA cache_size = 1000000;", \
            "PRAGMA locking_mode = EXCLUSIVE;", \
            "PRAGMA temp_store = MEMORY;"
        ]


        sql_create_curve_table = \
            """
                CREATE TABLE IF NOT EXISTS curve 
                (
                    file_path text,
                    type text NOT NULL CHECK (type='system' OR type='background' OR type='data' OR type='Operations'),
                    curve_id text NOT NULL,

                    pref_show_on_graph int NOT NULL CHECK (pref_show_on_graph=1 OR pref_show_on_graph=0),
                    pref_line_color text,
                    pref_line_size float,
                    pref_marker_style text,
                    pref_marker_size float,
                    pref_marker_face_color text,
                    pref_marker_edge_color text,
                    
                    PRIMARY KEY (file_path, type, curve_id)

                );
            """
        
        sql_create_coords_table = \
            """
                CREATE TABLE IF NOT EXISTS coords 
                (
                    file_path text,
                    type text NOT NULL CHECK (type='system' OR type='background' OR type='data' OR type='Operations'),
                    curve_id text NOT NULL,

                    x_coord float NOT NULL,
                    y_coord float NOT NULL,

                    FOREIGN KEY (file_path, type, curve_id) REFERENCES curve (file_path, type, curve_id)
                    
                );
            """
        conn = self._create_connection(db_path)
        if conn is not None:
            for i in sql_optimizations:
                self._execute_command(conn, i)
            self._execute_command(conn, sql_create_curve_table)
            self._execute_command(conn, sql_create_coords_table)
            conn.close()
        else:
            print("Error creating database.")
        
    # def insert_curve(self, fp: str, type: str, curve_id: int,
    
    def _create_connection(self, db_path):
        conn = None
        try:
            conn = sqlite3.connect(db_path)
        except Error as e:
            print(e)
        return conn
    
    def _execute_command(self, conn, command, task=None, many=False):
        try:
            c = conn.cursor()
            if task == None:
                c.execute(command)
            else:
                if many == True:
                    c.executemany(command, task)
                else:
                    c.execute(command, task)
            conn.commit()
            return c.fetchall()
        except Error as e:
            print(e)
        return None

    def _save(self, container, db_path: str):
        conn = self._create_connection(db_path)
        if conn is not None:
            curves_list = container.get_curves_list()
            insert_curve_cmd = \
                """
                    INSERT INTO curve VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """
            insert_coords_cmd = \
                """
                    INSERT INTO coords VALUES (?, ?, ?, ?, ?);
                """
            for i in curves_list:
                self._execute_command(conn, insert_curve_cmd, i[:len(i)-1])

                coords = i[-1]
                zipped_coords = list(zip(coords[0], coords[1]))
                # temp = len(coords[0])
                # temp0 = [i[0] for j in range(temp)]
                # temp1 = [i[1] for j in range(temp)]
                # temp2 = [i[2] for j in range(temp)]
                rows = []
                for x, y in zipped_coords:
                    rows.append((i[0], i[1], i[2], x, y))
                self._execute_command(conn, insert_coords_cmd, \
                    rows, many=True)
                # for x, y in zipped_coords:
                #     self._execute_command(conn, insert_coords_cmd, (i[0], i[1], i[2], x, y))
                
            # self._execute_command(conn, sql_create_curve_table)
            # self._execute_command(conn, sql_create_coords_table)
            conn.close()
        else:
            print("Error saving database.")

    def save(self, container, db_path: str) -> None:
        self._create_db(db_path)
        self._save(container, db_path)
        # print(container.get_curves_list())
        
    def _fetch_curves(self, db_path: str) -> list:
        rows = []
        select_cmd = \
            """
                SELECT * FROM curve;
            """
        
        conn = self._create_connection(db_path)
        if conn is not None:
            rows = self._execute_command(conn, select_cmd)

            conn.close()
        else:
            print("Error fetching database table curve.")
        return rows

            
    def fetch_curves(self, db_path: str) -> list:
        return self._fetch_curves(db_path)
    
    def _fetch_coords(self, db_path: str, file_path: str, \
        type: str, curve_id: int) -> list:
        select_cmd = \
            """
                SELECT x_coord, y_coord FROM coords WHERE file_path=? AND type=? AND curve_id=?;
            """
        
        conn = self._create_connection(db_path)
        if conn is not None:
            rows = self._execute_command(conn, select_cmd, \
                (file_path, type, curve_id))

            conn.close()
        else:
            print("Error fetching database table coords.")
        return rows
    
    def fetch_coords(self, db_path: str, file_path: str, \
        type: str, curve_id: int) -> list:
        return self._fetch_coords(db_path, file_path, type, curve_id)
    
    
    
if __name__ == '__main__':
    pass