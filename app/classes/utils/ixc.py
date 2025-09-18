from typing import List
from typing import Dict
from typing import cast

import os

import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.cursor import MySQLCursor
from classes.utils.types import Response

class IXC():

    @staticmethod
    def listLogin(contrato_id: int) -> Response[str] | Response[List[Dict[str,str]]]:
        try:
            conn: None | PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
                host=os.getenv("IXC_DB_ADDRESS"),
                user=os.getenv("IXC_DB_USER"),
                password=os.getenv("IXC_DB_PASSWORD"),
                database=os.getenv("IXC_DB_DATABASE"),
                port=os.getenv("IXC_DB_PORT")
            )
            cursor:MySQLCursor | None = None
            
            if conn is not None:
                cursor = conn.cursor(dictionary=True)

            query: str = """
                SELECT 
                    radusuarios.id,
                    radusuarios.login,
                    cliente.razao,
                    radusuarios.ip,
                    radusuarios.fixar_ip,
                    radusuarios.concentrador,
                    radusuarios.id_contrato
                FROM
                    radusuarios
                LEFT JOIN
                    cliente ON cliente.id = radusuarios.id_cliente
                WHERE 
                    radusuarios.id_contrato = %(contrato_id)s
            """

            if cursor is None:
                return Response(error=False, data="Nenhum resultado encontrado.")

            cursor.execute(query, {"contrato_id": contrato_id})
            results: List[Dict[str,str]] = cast(List[Dict[str,str]], cursor.fetchall())

            cursor.close()
            conn.close()

            if not results:
                return Response(error=False, data="Nenhum resultado encontrado.")
            
            return Response(error=False, data=results)

        except Exception as e:
            return Response(error=True, data=str(e))

    @staticmethod
    def getLogin(login_id: int) -> Response[str] | Response[List[Dict[str,str]]]:
        try:
            conn: None | PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
                host=os.getenv("IXC_DB_ADDRESS"),
                user=os.getenv("IXC_DB_USER"),
                password=os.getenv("IXC_DB_PASSWORD"),
                database=os.getenv("IXC_DB_DATABASE"),
                port=os.getenv("IXC_DB_PORT")
            )
            cursor:MySQLCursor | None = None
            
            if conn is not None:
                cursor = conn.cursor(dictionary=True)

            query: str = """
                SELECT 
                    radusuarios.id,
                    radusuarios.login,
                    cliente.razao,
                    radusuarios.ip,
                    radusuarios.fixar_ip,
                    radusuarios.concentrador
                FROM
                    radusuarios
                LEFT JOIN
                    cliente ON cliente.id = radusuarios.id_cliente
                WHERE 
                    radusuarios.id = %(login_id)s
            """

            if cursor is None:
                return Response(error=False, data="Nenhum resultado encontrado.")

            cursor.execute(query, {"login_id": login_id})
            results: List[Dict[str,str]] = cast(List[Dict[str,str]], cursor.fetchall())

            cursor.close()
            conn.close()

            if not results:
                return Response(error=False, data="Nenhum resultado encontrado.")
            
            return Response(error=False, data=results)

        except Exception as e:
            return Response(error=True, data=str(e))
