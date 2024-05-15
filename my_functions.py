from qgis.PyQt.QtCore import QSettings
from qgis.core import QgsProject, QgsDataSourceUri
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery


# create the "create_project_structure()" callback function
# then add it as a parameter to "get_connections()"
# def create_project(self):

#     # get schema name from user
#     user_schema_name = self.dlg.GnsProjectNameInput.text()
#     geom = "geom"

#     # get database uri
#     db_uri = QgsDataSourceUri()  # create an empty instance
#     db_uri.setConnection()  # host_name, port, db_name, owner, password

#     # create groups:
#     layer_panel = QgsProject.instance().layerTreeRoot()
#     node_group = layer_panel.addGroup("Node")
#     arc_group = layer_panel.addGroup("Arc")

#     ftth_db_layers = ["dp", "mfg", "duct", "drop_cable"]

#     print("create_project function !")


# TODO: create "get_schema()" function:
# TODO: create "get_db_config()" function:


# get QSettings PostgreSQL/connections group
def get_connections(self):
    db_connection_key_names = [
        "authcfg",
        "database",
        "host",
        "password",
        "port",
        "service",
        "sslmode",
        "username",
        "connection_name",
    ]

    conn_name = {}
    # get postgres db connections
    settings = QSettings()
    pgsql_grp = "PostgreSQL/connections"
    settings.beginGroup(pgsql_grp)
    dbs = settings.childGroups()  # dbs connected to QGIS (list)
    for db in dbs:
        temp_dict = {}
        pgsql_grp = "PostgreSQL/connections"
        settings.beginGroup(f"{pgsql_grp}/ {db}")
        db_info = settings.childKeys()  # db parameters (e.g.: port, hostname,..)
        for db_params in db_connection_key_names:
            if db_params in db_info:
                temp_dict[db_params] = settings.values(db_params)
            elif db_params == "connection_name":
                temp_dict[db_params] = db
                # print(temp_dict)
                conn_name[db] = temp_dict
            # print(conn_name)
    self.dlg.DBcomboBox.clear()
    self.dlg.DBcomboBox.addItems(list(conn_name))
    # print(self.conn_name)


# from PyQt5.QtSql import QSqlDatabase, QSqlQuery

# def get_schema_names(host, port, user, password, database):
#     # Initialize the database connection
#     db = QSqlDatabase.addDatabase("QPSQL")
#     db.setHostName(host)
#     db.setPort(port)
#     db.setUserName(user)
#     db.setPassword(password)
#     db.setDatabaseName(database)

#     # Open the database connection
#     if not db.open():
#         print("Error:", db.lastError().text())
#         return []

#     # Execute SQL query to fetch schema names
#     query = QSqlQuery()
#     query.exec_("SELECT schema_name FROM information_schema.schemata;")

#     # Extract schema names from the result set
#     schema_names = []
#     while query.next():
#         schema_names.append(query.value(0))

#     # Close the database connection
#     db.close()

#     return schema_names

# # Example usage:
# host = 'your_host'
# port = 'your_port'
# user = 'your_username'
# password = 'your_password'
# database = 'your_database'

# schema_names = get_schema_names(host, port, user, password, database)
# print("Schema Names:", schema_names)


def get_schema_list(self):

    db = QSqlDatabase.addDatabase("QPSQL")
    db.setDatabaseName("ftth_db")
    db.setHostName("localhost")
    db.setPort(5432)
    db.setPassword("0000")
    db.setUserName("postgres")

    # if not db.isOpen():
    #     print("something is wrong ")
    #     return []

    db.open()
    query = QSqlQuery()
    query.exec_(
        """SELECT schema_name FROM information_schema.schemata WHERE schema_name != 'information_schema' """
    )

    schema_list = []
    while query.next():
        schema_list.append(query.value(0))

    db.close()

    print("function is working !")

    self.dlg.SchemacomboBox.addItems(schema_list)
