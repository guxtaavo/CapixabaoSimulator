import sqlite3
from pathlib import Path
from clube import Clube

# Configuração do caminho do banco de dados
ROOT_DIR = Path(__file__).parent
DB_NAME = "db.sqlite3"
DB_FILE = ROOT_DIR / DB_NAME
TABLE_NAME = "Capixabao"

class ManagerDB:
    @classmethod
    def create_table(cls):
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                posicao INTEGER,
                nome_do_time TEXT,
                jogos INTEGER,
                vitorias INTEGER,
                empates INTEGER,
                derrotas INTEGER,
                gols_pro INTEGER,
                gols_contra INTEGER,
                saldo_de_gols INTEGER,
                aproveitamento INTEGER
            )
            """
        )
        con.commit()
        con.close()

    @classmethod
    def visualizar_tabela(cls):
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute(f'SELECT posicao, nome_do_time, jogos, vitorias, empates, derrotas, gols_pro, gols_contra, saldo_de_gols, aproveitamento FROM {TABLE_NAME}')
        rows = cursor.fetchall()

        for row in rows:
            print(row)
        
        con.close()

    @classmethod
    def adicionar_time(cls, clube: Clube):
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        count = cursor.fetchone()[0]
        posicao = count + 1
        sql = (
            f"INSERT INTO {TABLE_NAME} (posicao, nome_do_time, jogos, vitorias, empates, derrotas, gols_pro, gols_contra, saldo_de_gols, aproveitamento) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        cursor.execute(sql, (1, clube.nome, clube.jogos, clube.vitorias, clube.empates, clube.derrotas, clube.gols_pro, clube.gols_contra, clube.saldo_gols, 0))
        con.commit()
        con.close()

    @classmethod
    def adicionar_rodada(cls, time1: str, time2: str):
        pass

    @classmethod
    def atualizar_rodada(cls):
        pass

if __name__ == "__main__":
    ManagerDB.create_table()
    ManagerDB.adicionar_time(Clube("Capixaba"))
    ManagerDB.adicionar_time(Clube("Desportiva"))
    ManagerDB.adicionar_time(Clube("Jaguaré"))
    ManagerDB.adicionar_time(Clube("Nova Venécia"))
    ManagerDB.adicionar_time(Clube("Porto Vitória"))
    ManagerDB.adicionar_time(Clube("Real Noroeste"))
    ManagerDB.adicionar_time(Clube("Rio Branco VN"))
    ManagerDB.adicionar_time(Clube("Rio Branco SAF"))
    ManagerDB.adicionar_time(Clube("Vila Velhense"))
    ManagerDB.adicionar_time(Clube("Vitória"))
    ManagerDB.visualizar_tabela()