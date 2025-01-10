import sqlite3
from pathlib import Path
from tabulate import tabulate
from clube import Clube
import os

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
                posicao INTEGER,
                nome_do_time TEXT,
                pontos INTEGER,
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
        os.system('cls')
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute(f'SELECT * FROM {TABLE_NAME} ORDER BY pontos DESC, vitorias DESC, saldo_de_gols DESC, gols_pro DESC')
        rows = cursor.fetchall()

        dados = [
            [
                i + 1,  # Posição
                row[2],  # Nome do Time
                row[3],  # Pontos
                row[4],  # Jogos
                row[5],  # Vitórias
                row[6],  # Empates
                row[7],  # Derrotas
                row[8],  # Gols Pró
                row[9],  # Gols Contra
                row[10],  # Saldo de Gols
                f'{row[11]}%'  # Aproveitamento
            ]
            for i, row in enumerate(rows)
        ]

        cabecalho = [
            "Posição", "Nome do Time", "Pontos", "Jogos", "Vitórias",
            "Empates", "Derrotas", "Gols Pró", "Gols Contra", "Saldo de Gols", "Aproveitamento"
        ]

        tabela_formatada = tabulate(dados, headers=cabecalho, tablefmt="grid")
        print(tabela_formatada)

        con.close()

    @classmethod
    def atualizar_posicoes(cls):
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute(f'SELECT id FROM {TABLE_NAME} ORDER BY pontos DESC, vitorias DESC, saldo_de_gols DESC, gols_pro DESC')
        rows = cursor.fetchall()

        for nova_posicao, (time_id,) in enumerate(rows, start=1):
            cursor.execute(f"UPDATE {TABLE_NAME} SET posicao = ? WHERE id = ?", (nova_posicao, time_id))
        con.commit()
        con.close()

    @classmethod
    def adicionar_time(cls, clube: Clube):
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        count = cursor.fetchone()[0]
        posicao = count + 1
        sql = (
            f"INSERT INTO {TABLE_NAME} (posicao, nome_do_time, pontos, jogos, vitorias, empates, derrotas, gols_pro, gols_contra, saldo_de_gols, aproveitamento) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        cursor.execute(sql, (posicao, clube.nome, clube.pontos, clube.jogos, clube.vitorias, clube.empates, clube.derrotas, clube.gols_pro, clube.gols_contra, clube.saldo_gols, clube.aproveitamento))
        con.commit()
        con.close()

    @classmethod
    def adicionar_rodada(cls, numero_rodada):
        rodada = []
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS Rodada_{numero_rodada} (id INTEGER PRIMARY KEY AUTOINCREMENT, time1_id INTEGER, time1_nome TEXT, placar_time1 INTEGER, time2_id INTEGER, time2_nome TEXT, placar_time2 INTEGER)")
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
            cursor.execute(f"INSERT INTO Rodada_{numero_rodada} (time1_id, time1_nome, placar_time1, time2_id, time2_nome, placar_time2) VALUES (?, ?, ?, ?, ?, ?)", (row1[0], clube1.nome, None, row2[0], clube2.nome, None))
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
    def carregar_campeonato(cls):
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{TABLE_NAME}'")
        table_exists = cursor.fetchone()
        con.close()
        if table_exists:
            print("Campeonato carregado com sucesso.")
            return True
        else:
            print("Nenhum campeonato encontrado.")
            return None

    @classmethod
    def atualizar_rodada(cls, numero_rodada, jogo, placar_time1, placar_time2):
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute(f"UPDATE Rodada_{numero_rodada} SET placar_time1 = ?, placar_time2 = ? WHERE id = ?", (placar_time1, placar_time2, jogo))
        con.commit()
        con.close()
        cls.atualizar_estatisticas(numero_rodada)

    @classmethod
    def atualizar_estatisticas(cls):
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        times = cursor.fetchall()

        for time in times:
            time_id = time[0]
            cursor.execute(f"SELECT SUM(placar_time1), SUM(placar_time2) FROM Rodada WHERE time1_id = ? OR time2_id = ?", (time_id, time_id))
            gols_pro, gols_contra = cursor.fetchone()
            gols_pro = gols_pro if gols_pro is not None else 0
            gols_contra = gols_contra if gols_contra is not None else 0

            cursor.execute(f"SELECT COUNT(*) FROM Rodada WHERE (time1_id = ? AND placar_time1 > placar_time2) OR (time2_id = ? AND placar_time2 > placar_time1)", (time_id, time_id))
            vitorias = cursor.fetchone()[0]

            cursor.execute(f"SELECT COUNT(*) FROM Rodada WHERE (time1_id = ? AND placar_time1 < placar_time2) OR (time2_id = ? AND placar_time2 < placar_time1)", (time_id, time_id))
            derrotas = cursor.fetchone()[0]

            cursor.execute(f"SELECT COUNT(*) FROM Rodada WHERE (time1_id = ? OR time2_id = ?) AND placar_time1 = placar_time2", (time_id, time_id))
            empates = cursor.fetchone()[0]

            jogos = vitorias + derrotas + empates
            pontos = vitorias * 3 + empates
            saldo_de_gols = gols_pro - gols_contra
            aproveitamento = round((pontos / (jogos * 3)) * 100) if jogos > 0 else 0

            cursor.execute(f"UPDATE {TABLE_NAME} SET pontos = ?, jogos = ?, vitorias = ?, empates = ?, derrotas = ?, gols_pro = ?, gols_contra = ?, saldo_de_gols = ?, aproveitamento = ? WHERE id = ?", (pontos, jogos, vitorias, empates, derrotas, gols_pro, gols_contra, saldo_de_gols, aproveitamento, time_id))
            con.commit()

        con.close()

        cls.atualizar_posicoes()

if __name__ == "__main__":
    ...
    # ManagerDB.create_table()
    # ManagerDB.adicionar_time(Clube("Capixaba"))
    # ManagerDB.adicionar_time(Clube("Desportiva"))
    # ManagerDB.adicionar_time(Clube("Jaguaré"))
    # ManagerDB.adicionar_time(Clube("Nova Venécia"))
    # ManagerDB.adicionar_time(Clube("Porto Vitória"))
    # ManagerDB.adicionar_time(Clube("Real Noroeste"))
    # ManagerDB.adicionar_time(Clube("Rio Branco VN"))
    # ManagerDB.adicionar_time(Clube("Rio Branco SAF"))
    # ManagerDB.adicionar_time(Clube("Vilavelhense"))
    # ManagerDB.adicionar_time(Clube("Vitória"))
    # ManagerDB.criar_rodadas()
    # ManagerDB.visualizar_tabela()