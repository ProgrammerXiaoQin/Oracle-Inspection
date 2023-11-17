import cx_Oracle

class OracleDBConnector:
    def __init__(self, driver_path,connstr):
        cx_Oracle.init_oracle_client(lib_dir=driver_path)
        self.connection = cx_Oracle.connect(
            connstr, encoding='utf-8'
        )
        self.cursor = self.connection.cursor()

    def execute_query_and_fetch_all(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
