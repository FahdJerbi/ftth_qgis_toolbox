from qgis.PyQt.QtCore import QSettings


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
