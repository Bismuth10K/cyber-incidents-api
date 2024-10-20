import sqlite3
import utils
import pandas as pd
import re
import numpy as np
import os


def get_db_connexion():
    # Loads the app config into the dictionary app_config.
    app_config = utils.load_config()
    if not app_config:
        print("Error: while loading the app configuration")
        return None

    # From the configuration, gets the path to the database file.
    db_file = app_config["db"]

    # Open a connection to the database.
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row

    return conn


def close_db_connexion(cursor, conn):
    """Close a database connexion and the cursor.

    Parameters
    ----------
    cursor
        The object used to query the database.
    conn
        The object used to manage the database connection.
    """
    cursor.close()
    conn.close()


def transform_csv(old_csv_file_name, new_csv_file_name):
    """Write a new CSV file based on the input CSV file by adding
    new columns to obtain a CSV file that is easier to read.

    Parameters
    ----------
    csv_file_name
        Name of the CSV file to transform
    new_csv_file_name
        Name of the new CSV file
    """
    df = pd.read_csv(old_csv_file_name)
    df[["type of response", "source of response"]] = df["Response"].str.split("   ", n=1, expand=True)
    is_believed = np.any([df["Affiliations"].str.contains(r"[bB]elieved"), df["Affiliations"].str.contains(r"[sS]uspected"), df["Affiliations"].str.contains(r"[pP]ossibly")], axis=0)
    df["Attackers confirmed"] = np.invert(is_believed)
    df.to_csv(new_csv_file_name)


def create_database(cursor, conn):
    """Creates the incident database

    Parameters
    ----------
    cursor
        The object used to query the database.
    conn
        The object used to manage the database connection.

    Returns
    -------
    bool
        True if the database could be created, False otherwise.
    """

    # We open a transaction.
    # A transaction is a sequence of read/write statements that
    # have a permanent result in the database only if they all succeed.
    #
    # More concretely, in this function we create many tables in the database.
    # The transaction is therefore a sequence of CREATE TABLE statements such as :
    #
    # BEGIN
    # CREATE TABLE XXX
    # CREATE TABLE YYY
    # CREATE TABLE ZZZ
    # ....
    #
    # If no error occurs, all the tables are permanently created in the database.
    # If an error occurs while creating a table (for instance YYY), no table will be created, even those for which
    # the statement CREATE TABLE has already been executed (in this example, XXX).
    #
    # When we start a transaction with the statement BEGIN, we must end it with either COMMIT
    # or ROLLBACK.
    #
    # * COMMIT is called when no error occurs. After calling COMMIT, the result of all the statements in
    # the transaction is permanently written to the database. In our example, COMMIT results in actually creating all the tables
    # (XXX, YYY, ZZZ, ....)
    #
    # * ROLLBACK is called when any error occurs in the transaction. Calling ROLLBACK means that
    # the database is not modified (in our example, no table is created).
    #
    #
    cursor.execute("BEGIN")

    # Create the tables.
    tables = {
        "Agent": """
            CREATE TABLE IF NOT EXISTS Agent(
                username TEXT PRIMARY KEY,
                password BINARY(256)
            );
            """,

        "Victims":"""
            CREATE TABLE IF NOT EXISTS Victims(
                id_victim INTEGER PRIMARY KEY,
                name_victim TEXT,
                name_sector TEXT
             );
            """,

        "Sources":"""
            CREATE TABLE IF NOT EXISTS Sources(
                id_source INTEGER PRIMARY KEY,
                name_source TEXT
             );
            """,
        "Attack Source":"""
            CREATE TABLE IF NOT EXISTS Attack_sources(
                id_att INTEGER,
                id_src INTEGER,
                FOREIGN KEY (id_att) REFERENCES Attacks (id_attack)
                FOREIGN KEY (id_src) REFERENCES Sources (id_source)
             );
            """,

        "Response":"""
            CREATE TABLE IF NOT EXISTS Response(
                id_resp INTEGER PRIMARY KEY,
                name_type TEXT,
                name_src TEXT
             );
            """,

        "Group Attackers":"""
            CREATE TABLE IF NOT EXISTS grp_attackers(
                id_grp_att INTEGER PRIMARY KEY,
                name_grp_att TEXT,
                name_sponsor TEXT
             );
            """,

        "Attacks":"""
            CREATE TABLE IF NOT EXISTS Attacks(
                id_attack INTEGER PRIMARY KEY,
                date TEXT,
                title TEXT,
                type TEXT,
                attackers_confirmed TEXT,
                group_attackers INTEGER,
                username_agent TEXT,
                response INTEGER,
                victims INTEGER,
                FOREIGN KEY (username_agent) REFERENCES Agent(username)
                FOREIGN KEY (group_attackers) REFERENCES grp_attackers(id_grp_att)
                FOREIGN KEY (response) REFERENCES Response(id_resp)
                FOREIGN KEY (victims) REFERENCES Victims(id_victim)
             );
            """}
    
    try:
        # To create the tables, we call the function cursor.execute() and we pass it the
        # CREATE TABLE statement as a parameter.
        # The function cursor.execute() can raise an exception sqlite3.Error.
        # That's why we write the code for creating the tables in a try...except block.
        for tablename in tables:
            print(f"Creating table {tablename}...", end=" ")
            cursor.execute(tables[tablename])
            print("OK")

    ###################################################################

    # Exception raised when something goes wrong while creating the tables.
    except sqlite3.Error as error:
        print("An error occurred while creating the tables: {}".format(error))
        # IMPORTANT : we rollback the transaction! No table is created in the database.
        conn.rollback()
        # Return False to indicate that something went wrong.
        return False

    # If we arrive here, that means that no error occurred.
    # IMPORTANT : we must COMMIT the transaction, so that all tables are actually created in the database.
    conn.commit()
    print("Database created successfully")
    # Returns True to indicate that everything went well!
    return True


def populate_database(cursor, conn, csv_file_name):
    """Populate the database with data in a CSV file.

    Parameters
    ----------
    cursor
        The object used to query the database.
    conn
        The object used to manage the database connection.
    csv_file_name
        Name of the CSV file where the data are.

    Returns
    -------
    bool
        True if the database is correctly populated, False otherwise.
    """
    try:
        df = pd.read_csv(csv_file_name)

        df.loc[:, "Sources"] = df.loc[:, "Sources_1"].fillna("None") + " ___ " + df.loc[:, "Sources_2"].fillna("None") + " ___ " + df.loc[:, "Sources_3"].fillna("None")
        join_tables(cursor, conn, df, "Sources", "Sources", "Attack_sources")
        
        df[["username_agents"]] = pd.NA
        df[["group_attackers"]] = pd.NA
        df[["response"]] = pd.NA
        df[["victim"]] = pd.NA
        df = df.rename(columns={"Attackers confirmed": "attackers_confirmed"})

        df = populate_new_table(cursor, df, ["Affiliations", "Sponsor"], "group_attackers", "grp_attackers")
        df = populate_new_table(cursor, df, ["type of response", "source of response"], "response", "Response")
        df = populate_new_table(cursor, df, ["Victims", "Category"], "victim", "Victims")


        out = df.loc[:, ["Date", "Title", "Type", "attackers_confirmed", "group_attackers", "username_agents", "response", "victim"]].to_sql("Attacks", con=conn, if_exists="replace", index_label='id_attack')
        print(out)

        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False

def populate_new_table(cursor, df, columns, FK_column, table):
    """Populate a table with data coming from a CSV file.

    Parameters
    ----------
    cursor
        The object used to query the database.
    df
        The pandas dataframe of the datas coming from the csv.
    columns
        Tells which columns from df will go into the new table.
    FK_column
        Tells which column from df will act as the foreign key of the id in the new table.
    table
        Table where we add the datas in columns.

    Returns
    -------
    df
        Return the new dataframe as FK_column has been modified.
    """
    index_table = 0
    for index, row in df.loc[:, columns].iterrows():
        if not np.all(pd.isna(row)):
            part_query = ""
            for i in row:
                part_query += f', "{i}"'
            cursor.execute(f'Insert Into {table} Values ({index_table}{part_query})')
            df.at[index, FK_column] = index_table
            index_table += 1
        else:
            df.at[index, FK_column] = pd.NA
    return df

def join_tables(cursor, conn, df, column, table, table_joint):
    """Populate a table for one column of the dataframe, and make an association-table between the main table (attacks) and the new table.

    Parameters
    ----------
    cursor
        The object used to query the database.
    conn
        The object used to manage the database connection.
    df
        The pandas dataframe of the datas coming from the csv.
    column
        Tells which column from df will go into the new table.
    table
        Table where we add the datas in columns.
    table_joint
        The association-table.
    """
    df_col = df.loc[:, [column]].dropna().drop_duplicates().values.tolist()
    list_col = pd.unique([elem for liste in df_col for elem in liste[0].split(", ")])
    pd.DataFrame(list_col).to_sql(table, con=conn, if_exists="replace")
    cursor.execute(f"ALTER TABLE {table} RENAME COLUMN '0' TO name_source")

    jointure = df.loc[:, column].apply(lambda x: [np.where(list_col == elem)[0].item() if np.where(list_col == elem)[0].size > 0 else -1 for elem in str(x).split(", ")])
    for i, row in jointure.items():
        for elem in row:
            if elem != -1:
                cursor.execute(f"""INSERT INTO {table_joint} VALUES ({i}, {elem})""")

def init_database():
    """Initialise the database by creating the database
    and populating it.
    """
    try:
        try:
            os.remove("data/incidents.db")
        except:
            pass
        conn = get_db_connexion()

        # The cursor is used to execute queries to the database.
        cursor = conn.cursor()

        # Creates the database. THIS IS THE FUNCTION THAT YOU'LL NEED TO MODIFY
        create_database(cursor, conn)

        # Populates the database.
        populate_database(cursor, conn, "data/q3-cyber-operations-incidents.csv")

        # Closes the connection to the database
        close_db_connexion(cursor, conn)
    except Exception as e:
        print("Error: Database cannot be initialised:", e)
