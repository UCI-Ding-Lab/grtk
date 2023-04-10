import sqlite3
from sqlite3 import Error
import pathlib

"""
    Useful Commands:
        PRAGMA table_info(table_name);
        .databases
        .tables
        .schema

"""

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn: sqlite3.Connection, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    DB_PATH = pathlib.Path("tests/db/grtk.db")
    if not DB_PATH.exists():
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

    #CREATE TABLE IF NOT EXISTS grtk
    sql_create_grtk_table = \
        """
            CREATE TABLE IF NOT EXISTS grtk 
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

                x_coords int NOT NULL,
                y_coords int NOT NULL
                
            );
        """

    # create a database connection
    conn = create_connection(DB_PATH)

    # create tables
    if conn is not None:
        # # create projects table
        # create_table(conn, sql_create_projects_table)

        # # create tasks table
        # create_table(conn, sql_create_tasks_table)
        create_table(conn, sql_create_grtk_table)
        conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()