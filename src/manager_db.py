import sqlite3
from pathlib import Path
from tabulate import tabulate
from clube import Clube
from campeonato import Campeonato

# Define o diretório raiz do projeto para encontrar/salvar os arquivos .sqlite3
ROOT_DIR = Path(__file__).parent

class ManagerDB:
    def __init__(self, campeonato: Campeonato, db_file_path: Path = None):
        """
        Inicializa o gerenciador do banco de dados.

        Este construtor é flexível:
        - MODO CARREGAR: Se 'db_file_path' for um arquivo válido, ele se conecta a esse banco de dados.
        - MODO CRIAR: Se 'db_file_path' for None ou inválido, ele cria um novo banco de dados com
          um nome único para evitar sobrescrever simulações existentes.
        """
        self.campeonato = campeonato
        self.table_name = self.campeonato._nome.replace(" ", "_") # Ex: Campeonato_Capixaba_2026

        if db_file_path and db_file_path.exists():
            # MODO CARREGAR: Conecta ao arquivo existente fornecido.
            self.db_file = db_file_path
            print(f"INFO: Carregando banco de dados existente de '{self.db_file.name}'")
        else:
            # MODO CRIAR: Procura por um nome de arquivo que ainda não exista.
            base_db_name = f"{self.table_name}.sqlite3"
            db_file = ROOT_DIR / base_db_name
            counter = 1
            while db_file.exists():
                new_db_name = f"{self.table_name}_{counter}.sqlite3"
                db_file = ROOT_DIR / new_db_name
                counter += 1
            self.db_file = db_file
            print(f"INFO: O banco de dados para esta nova simulação será salvo em '{self.db_file.name}'")

        # Conecta ao arquivo de banco de dados definido pela lógica acima
        self.con = sqlite3.connect(self.db_file)
        self.cursor = self.con.cursor()

    def _close(self):
        """Fecha a conexão com o banco de dados de forma segura."""
        self.con.close()
        print(f"INFO: Conexão com '{self.db_file.name}' fechada.")

    def setup_database(self):
        """
        Cria e popula todas as tabelas necessárias para uma nova simulação.
        Esta função é destrutiva e deve ser usada apenas ao criar um novo campeonato.
        """
        print(f"Configurando estrutura inicial no banco de dados '{self.db_file.name}'...")

        # 1. Cria a tabela principal de classificação
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                posicao INTEGER DEFAULT 0,
                nome_do_time TEXT UNIQUE,
                pontos INTEGER DEFAULT 0,
                jogos INTEGER DEFAULT 0,
                vitorias INTEGER DEFAULT 0,
                empates INTEGER DEFAULT 0,
                derrotas INTEGER DEFAULT 0,
                gols_pro INTEGER DEFAULT 0,
                gols_contra INTEGER DEFAULT 0,
                saldo_de_gols INTEGER DEFAULT 0,
                aproveitamento REAL DEFAULT 0.0
            )
            """
        )
        
        # 2. Insere os times na tabela de classificação
        for time_nome in self.campeonato._times:
            self.cursor.execute(f"INSERT INTO {self.table_name} (nome_do_time) VALUES (?)", (time_nome,))
        
        # 3. Cria uma tabela para cada rodada e insere os jogos pré-definidos
        for i, rodada_partidas in enumerate(self.campeonato._rodadas, start=1):
            tabela_rodada = f"Rodada_{i}_{self.table_name}"
            self.cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {tabela_rodada} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mandante TEXT,
                    visitante TEXT,
                    placar_mandante INTEGER,
                    placar_visitante INTEGER
                )
                """
            )
            for mandante, visitante in rodada_partidas:
                self.cursor.execute(f"INSERT INTO {tabela_rodada} (mandante, visitante) VALUES (?, ?)", (mandante, visitante))
        
        self.con.commit()
        print("Estrutura do campeonato criada com sucesso!")

    def get_classificacao_formatada(self) -> str:
        """
        Busca os dados da classificação, atualiza as estatísticas e retorna
        a tabela formatada como uma string, ideal para GUIs com fontes monoespaçadas.
        """
        self.atualizar_estatisticas_gerais()
        self.cursor.execute(f'SELECT * FROM {self.table_name} ORDER BY pontos DESC, vitorias DESC, saldo_de_gols DESC, gols_pro DESC')
        rows = self.cursor.fetchall()
        
        dados = [
            [row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], f'{row[11]:.1f}%']
            for row in rows
        ]
        cabecalho = ["#", "Time", "P", "J", "V", "E", "D", "GP", "GC", "SG", "Aprov."]
        # 'psql' ou 'grid' funcionam bem em fontes como Courier
        return tabulate(dados, headers=cabecalho, tablefmt="psql")

    def get_jogos_da_rodada(self, num_rodada: int) -> list:
        """Retorna uma lista de tuplas com os jogos da rodada especificada."""
        tabela_rodada = f"Rodada_{num_rodada}_{self.table_name}"
        self.cursor.execute(f"SELECT id, mandante, visitante, placar_mandante, placar_visitante FROM {tabela_rodada}")
        return self.cursor.fetchall()

    def atualizar_placar(self, num_rodada: int, id_jogo: int, placar_mandante: int, placar_visitante: int):
        """Atualiza o placar de um jogo específico no banco de dados."""
        tabela_rodada = f"Rodada_{num_rodada}_{self.table_name}"
        self.cursor.execute(
            f"UPDATE {tabela_rodada} SET placar_mandante = ?, placar_visitante = ? WHERE id = ?",
            (placar_mandante, placar_visitante, id_jogo)
        )
        self.con.commit()

    def atualizar_estatisticas_gerais(self):
        """
        (Método interno) Recalcula todas as estatísticas de todos os times
        com base nos placares salvos nas tabelas de rodadas.
        """
        self.cursor.execute(f"SELECT nome_do_time FROM {self.table_name}")
        todos_os_times = self.cursor.fetchall()

        for (time_nome,) in todos_os_times:
            stats = {'p': 0, 'j': 0, 'v': 0, 'e': 0, 'd': 0, 'gp': 0, 'gc': 0}
            
            for i in range(len(self.campeonato._rodadas)):
                tabela_rodada = f"Rodada_{i+1}_{self.table_name}"
                
                # Jogos como mandante com placar definido
                self.cursor.execute(f"SELECT placar_mandante, placar_visitante FROM {tabela_rodada} WHERE mandante = ? AND placar_mandante IS NOT NULL", (time_nome,))
                for pm, pv in self.cursor.fetchall():
                    stats['j'] += 1; stats['gp'] += pm; stats['gc'] += pv
                    if pm > pv: stats['v'] += 1; stats['p'] += 3
                    elif pm == pv: stats['e'] += 1; stats['p'] += 1
                    else: stats['d'] += 1
                
                # Jogos como visitante com placar definido
                self.cursor.execute(f"SELECT placar_mandante, placar_visitante FROM {tabela_rodada} WHERE visitante = ? AND placar_mandante IS NOT NULL", (time_nome,))
                for pm, pv in self.cursor.fetchall():
                    stats['j'] += 1; stats['gp'] += pv; stats['gc'] += pm
                    if pv > pm: stats['v'] += 1; stats['p'] += 3
                    elif pv == pm: stats['e'] += 1; stats['p'] += 1
                    else: stats['d'] += 1
            
            saldo_gols = stats['gp'] - stats['gc']
            aprov = (stats['p'] / (stats['j'] * 3) * 100) if stats['j'] > 0 else 0

            self.cursor.execute(f"""
                UPDATE {self.table_name} SET 
                pontos = ?, jogos = ?, vitorias = ?, empates = ?, derrotas = ?, 
                gols_pro = ?, gols_contra = ?, saldo_de_gols = ?, aproveitamento = ?
                WHERE nome_do_time = ?""",
                (stats['p'], stats['j'], stats['v'], stats['e'], stats['d'], 
                 stats['gp'], stats['gc'], saldo_gols, aprov, time_nome))
        
        self.con.commit()
        self.atualizar_posicoes()

    def atualizar_posicoes(self):
        """(Método interno) Atualiza a coluna 'posicao' com base na ordenação de critérios."""
        self.cursor.execute(f'SELECT id FROM {self.table_name} ORDER BY pontos DESC, vitorias DESC, saldo_de_gols DESC, gols_pro DESC')
        rows = self.cursor.fetchall()
        for posicao, (id_time,) in enumerate(rows, start=1):
            self.cursor.execute(f"UPDATE {self.table_name} SET posicao = ? WHERE id = ?", (posicao, id_time))
        self.con.commit()