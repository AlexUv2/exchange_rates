import psycopg2


class Postgresql:

    def __init__(self, credentials: dict):

        try:
            self.__conn = psycopg2.connect(dbname=credentials['dbname'], user=credentials['user'],
                                           password=credentials['password'], host=credentials['host'])
        except Exception:
            self.__conn = None
            raise Exception('Connection failed')

    def __del__(self):
        if self.__conn:
            self.__conn.close()
            self.__conn = None

    def exec(self, sql: str):
        """
        For queries with no select statement
        :param sql: sql query
        :return: None or query result
        """

        query_result = None
        cursor = self.__conn.cursor()

        try:
            cursor.execute(sql)
            self.__conn.commit()

        except Exception:
            self.__conn.rollback()
            self.__del__()
            raise

        return query_result

    def get_rows(self, sql: str, as_dict: bool = False):
        """
        For queries with select statement
        :param as_dict:
        :param sql: sql query
        :return:
        """
        query_result = None

        cursor = self.__conn.cursor()

        try:
            cursor.execute(sql)

            values = cursor.fetchall()
            ################################ПЕРЕДЕЛАТЬ ЭТУ ДИЧЬ
            query_result = values
            if as_dict:
                cols_names = [column[0] for column in cursor.description]
                query_result = [dict(zip(cols_names, row)) for row in values]

        except Exception:
            self.__conn.rollback()
            self.__del__()
            raise

        return query_result

    def get_column(self, sql: str) -> list:
        """ Should return list of values for query with one column"""
        cursor = self.__conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        if not result:
            return []
        else:
            return [row[0] for row in result]

