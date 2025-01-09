import sqlite3
from pathlib import Path
from clube import Clube

# Configuração do caminho do banco de dados
ROOT_DIR = Path(__file__).parent
DB_NAME = "db.sqlite3"
DB_FILE = ROOT_DIR / DB_NAME
TABLE_NAME = "Capixabao"

class ManagerDB:
    rodadas = []

    @classmethod
    def create_table(cls):
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_do_time TEXT,
                pontos INTEGER,
                jogos INTEGER,
                vitorias INTEGER,
                empates INTEGER,
                derrotas INTEGER,
                gols_pro INTEGER,
                gols_contra INTEGER,
                saldo_de_gols INTEGER,
                aproveitamento INTEGER,
                posicao INTEGER
            )
            """
        )
        con.commit()
        con.close()

    @classmethod
    def visualizar_tabela(cls):
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute(f'SELECT nome_do_time, pontos, jogos, vitorias, empates, derrotas, gols_pro, gols_contra, saldo_de_gols, aproveitamento, posicao FROM {TABLE_NAME}')
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
            f"INSERT INTO {TABLE_NAME} (nome_do_time, pontos, jogos, vitorias, empates, derrotas, gols_pro, gols_contra, saldo_de_gols, aproveitamento, posicao) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        cursor.execute(sql, (clube.nome, clube.pontos, clube.jogos, clube.vitorias, clube.empates, clube.derrotas, clube.gols_pro, clube.gols_contra, clube.saldo_gols, clube.aproveitamento, posicao))
        con.commit()
        con.close()

    @classmethod
    def adicionar_rodada(cls, numero_rodada):
        rodada = []
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS Rodada_{numero_rodada} (id INTEGER PRIMARY KEY AUTOINCREMENT, time1_id INTEGER, time1_nome TEXT, time2_id INTEGER, time2_nome TEXT, placar_time1 INTEGER, placar_time2 INTEGER)")
        con.commit()

        for i in range(5):
            while True:
                time1 = input(f"Digite o nome do primeiro time do jogo {i+1}: ")
                cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE nome_do_time = ?", (time1,))
                row1 = cursor.fetchone()
                if row1 is None:
                    print(f"Time '{time1}' não encontrado. Tente novamente.")
                    continue

                time2 = input(f"Digite o nome do segundo time do jogo {i+1}: ")
                cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE nome_do_time = ?", (time2,))
                row2 = cursor.fetchone()
                if row2 is None:
                    print(f"Time '{time2}' não encontrado. Tente novamente.")
                    continue

                if time1 == time2:
                    print("Os times não podem ser iguais. Tente novamente.")
                    continue
                break

            clube1 = Clube.from_db_row(row1)
            clube2 = Clube.from_db_row(row2)

            rodada.append([clube1.nome, clube2.nome])
            cursor.execute(f"INSERT INTO Rodada_{numero_rodada} (time1_id, time1_nome, time2_id, time2_nome, placar_time1, placar_time2) VALUES (?, ?, ?, ?, ?, ?)", (row1[0], clube1.nome, None, row2[0], clube2.nome, None))
            con.commit()

        cls.rodadas.append(rodada)
        print(f"Rodada {numero_rodada} adicionada: {rodada}")
        con.close()

    @classmethod
    def criar_rodadas(cls):
        NUMERO_DE_RODADAS = 10
        for i in range(1, NUMERO_DE_RODADAS + 1):
            cls.adicionar_rodada(i)

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
    ManagerDB.adicionar_time(Clube("Vilavelhense"))
    ManagerDB.adicionar_time(Clube("Vitória"))
    ManagerDB.criar_rodadas()
    ManagerDB.visualizar_tabela()