import sqlite3
import utils
import pandas as pd
import re
import numpy as np


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
        "Attack Victims Sector":"""
            CREATE TABLE IF NOT EXISTS Attack_sectors(
                id_att INTEGER,
                id_sec INTEGER,
                FOREIGN KEY (id_att) REFERENCES Attacks (id_attack)
                FOREIGN KEY (id_sec) REFERENCES Sectors (id_sector)
             );
            """,
        "Attacks":"""
            CREATE TABLE IF NOT EXISTS Attacks(
                id_attack INTEGER PRIMARY KEY,
                date TEXT,
                title TEXT,
                source_information TEXT,
                attackers_confirmed TEXT,
                group_attackers TEXT,
                sponsored TEXT,
                type_response TEXT,
                source_info TEXT,
                victim TEXT,
                username_agent TEXT,
                FOREIGN KEY (username_agent) REFERENCES Agent(username)
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
    df = pd.read_csv(csv_file_name)
    
    df_sector_vict = df.loc[:, ["Category"]].drop_duplicates().dropna().values.tolist()
    list_sector_vict = pd.unique([cat for liste in df_sector_vict for cat in liste[0].split(", ")])
    pd.DataFrame(list_sector_vict).iloc[:, 0].to_sql("Sectors", con=conn, if_exists="replace")
    
    jointure_cat = df.loc[:, "Category"].apply(lambda x: [np.where(list_sector_vict == vic.strip())[0].item() if np.where(list_sector_vict == vic)[0].size > 0 else -1 for vic in str(x).split(", ")])
    
    for i, row in jointure_cat.items():
        for sector in row:
            cursor.execute(f"""INSERT INTO Attack_sectors VALUES ({i}, {sector})""")
    

    df[["username_agents"]] = pd.NA
    df.loc[:, "sources"] = df["Sources_1"].fillna("None") + " ___ " + df["Sources_2"].fillna("None") + " ___ " + df["Sources_3"].fillna("None")

    df.loc[:, ["Date", "Title", "sources", "Attackers confirmed", "Affiliations", "Sponsor", "type of response", "source of response", "Victims", "username_agents"]].to_sql("Attacks", con=conn, if_exists="replace")


def init_database():
    """Initialise the database by creating the database
    and populating it.
    """
    try:
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
