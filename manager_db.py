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
                porcentagem INTEGER
            )
            """
        )
        con.commit()
        con.close()

    @classmethod
    def atualizar_tabela(cls):
        pass

    @classmethod
    def visualizar_tabela(cls):
        pass

    @classmethod
    def adicionar_time(cls, clube: Clube):
        pass

if __name__ == "__main__":
    ManagerDB.create_table()