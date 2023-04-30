import sqlite3
from sqlite3 import Error
import pathlib
import os

"""
    Useful Commands:
        PRAGMA table_info(table_name);
        .databases
        .tables
        .schema

"""

def create_connection(db_file):
    """_summary_

    Args:
        db_file (_type_): _description_

    Returns:
        _type_: _description_
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


# def create_table(conn: sqlite3.Connection, create_table_sql):
#     """ create a table from the create_table_sql statement
#     :param conn: Connection object
#     :param create_table_sql: a CREATE TABLE statement
#     :return:
#     """
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)

def execute_command(conn: sqlite3.Connection, create_table_sql):
    """_summary_

    Args:
        conn (sqlite3.Connection): _description_
        create_table_sql (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
        return c.fetchall()
    except Error as e:
        print(e)

def initialize():
    DB_PATH = pathlib.Path("tests/db/test.db")
    if DB_PATH.exists():
        os.remove(DB_PATH)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DB_PATH.touch()

    # sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
    #                                     id integer PRIMARY KEY,
    #                                     name text NOT NULL,
    #                                     begin_date text,
    #                                     end_date text
    #                                 ); """

    # sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
    #                                 id integer PRIMARY KEY,
    #                                 name text NOT NULL,
    #                                 priority integer,
    #                                 status_id integer NOT NULL,
    #                                 project_id integer NOT NULL,
    #                                 begin_date text NOT NULL,
    #                                 end_date text NOT NULL,
    #                                 FOREIGN KEY (project_id) REFERENCES projects (id)
    #                             );"""

    #CREATE TABLE IF NOT EXISTS curve
    #curve_id int IDENTIFY(1,1) PRIMARY KEY,
    # sql_create_db = \
    #     """
    #         DROP DATABASE IF EXISTS {};
    #         CREATE DATABASE cs122a_hackathon;
    #         USE cs122a_hackathon;
    #     """
    sql_create_curve_table = \
        """
            CREATE TABLE IF NOT EXISTS curve 
            (
                file_path text NOT NULL,
                type text NOT NULL CHECK (type='system' OR type='background' OR type='real'),
                curve_id int NOT NULL,

                pref_show_on_graph int NOT NULL CHECK (pref_show_on_graph=1 OR pref_show_on_graph=0),
                pref_line_color text NOT NULL,
                pref_line_size float NOT NULL,
                pref_marker_style text,
                pref_marker_size float NOT NULL,
                pref_marker_color text NOT NULL,
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
    # x_coords int NOT NULL,
    # y_coords int NOT NULL
    # create a database connection
    conn = create_connection(DB_PATH)

    # create tables
    if conn is not None:
        # # create projects table
        # create_table(conn, sql_create_projects_table)

        # # create tasks table
        # create_table(conn, sql_create_tasks_table)
        execute_command(conn, sql_create_curve_table)
        execute_command(conn, sql_create_coords_table)
        conn.close()
    else:
        print("Error! cannot create the database connection.")

#INSERT INTO curve VALUES ('some_addr','system',5,0,1,0,1,0,1);
#INSERT INTO coords VALUES ('some_addr','system',5,1,2);
#INSERT INTO coords VALUES ('some_addr','system',5,2,3);
#INSERT INTO coords VALUES ('some_addr','system',5,3,4);

#SELECT x_coord, y_coord FROM coords WHERE (file_path='some_addr' AND type='system' AND curve_id=5);

def main():
    initialize()
    # db_path = pathlib.Path("tests/db/test.db")
    # conn = create_connection(db_path)

    #     # """
    #     #     SELECT * FROM coords;
    #     # """


    # """
    #     INSERT INTO coords VALUES ('some_addr','system',1,3.12,9.234234);
    # """

    # if conn is not None:
    #     command = \
    #     """
    #         INSERT INTO curve VALUES ('some_addr','system',5,0,1,0,1,0,1);
    #     """
    #     print(execute_command(conn, command))
    #     command = \
    #     """
    #         INSERT INTO coords VALUES ('some_addr','system',5,1,2);
    #     """
    #     print(execute_command(conn, command))
    #     command = \
    #     """
    #         INSERT INTO coords VALUES ('some_addr','system',5,2,3);
    #     """
    #     print(execute_command(conn, command))
    #     command = \
    #     """
    #         INSERT INTO coords VALUES ('some_addr','system',5,3,4);
    #     """
    #     print(execute_command(conn, command))

    #     # conn.commit()
    #     conn.close()
    # else:
    #     print("Error! cannot create the database connection.")
    


if __name__ == '__main__':
    main()