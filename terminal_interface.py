from clube import Clube
from manager_db import ManagerDB
import config
import sys, os

class TerminalInterface:
    def __init__(self):
        self.menu()

    def menu(self):
        while True:
            os.system('cls')
            print("Bem-vindo ao sistema de controle de campeonato!")
            print("Escolha uma opção:")
            print("1 - Criar campeonato")
            print("2 - Entrar em campeonato existente")
            print("3 - Sair")
            opcao = input("Digite o número da opção desejada: ")
            match opcao:
                case "1":
                    os.system('cls')
                    self.criar_campeonato()
                case "2":
                    os.system('cls')
                    self.entrar_campeonato()
                case "3":
                    os.system('cls')
                    print("Obrigado por utilizar o sistema!")
                    sys.exit()
                case _:
                    print("Opção inválida!")

    def criar_campeonato(self):
        ManagerDB.create_table()
        while True:
            print("Escolha uma opção:")
            print("1 - Cadastrar clube")
            print("2 - Listar clubes")
            print("3 - Cadastrar rodada")
            print("4 - Listar rodadas")
            print("5 - Voltar ao menu principal")
            opcao = input("Digite o número da opção desejada: ")
            match opcao:
                case "1":
                    os.system('cls')
                    self.cadastrar_clube()
                case "2":
                    os.system('cls')
                    self.visualizar_tabela()
                case "3":
                    os.system('cls')
                    self.cadastrar_rodada()
                case "4":
                    os.system('cls')
                    self.listar_rodadas()
                case "5":
                    return
                case _:
                    print("Opção inválida!")

    def entrar_campeonato(self):
        self.menu_campeonato()
        # print("Entrando em campeonato existente...")
        # nome_do_campeonato = input("Digite o nome do campeonato: ")
        # campeonato = ManagerDB.carregar_campeonato(nome_do_campeonato)
        # if campeonato is None:
        #     print("Nenhum campeonato encontrado!")
        #     return
        # elif campeonato is True: 
        #     self.menu_campeonato()
        # else:
        #     print("Erro inesperado!")
        #     sys.exit()

    def menu_campeonato(self):
        while True:
            print("Escolha uma opção:")
            print("1 - Mostrar classificação")
            print("2 - Mostrar rodadas")
            print("3 - Editar rodada")
            print("4 - Sair")
            opcao = input("Digite o número da opção desejada: ")
            match opcao:
                case "1":
                    os.system('cls')
                    self.visualizar_tabela()
                case "2":
                    os.system('cls')
                    ManagerDB.listar_rodadas()
                case "3":
                    os.system('cls')
                    ManagerDB.editar_rodada()
                case "4":
                    os.system('cls')
                    print("Obrigado por utilizar o sistema!")
                    sys.exit()
                case _:
                    print("Opção inválida!")

    def cadastrar_clube(self):
        os.system('cls')
        for _ in range(config.NUMERO_DE_TIMES):
            nome = input("Digite o nome do clube: ")
            clube = Clube(nome)
            ManagerDB.adicionar_time(clube)

    def visualizar_tabela(self):
        ManagerDB.visualizar_tabela()

    def cadastrar_rodada(self):
        numero_rodada = input("Digite o número da rodada: ")
        ManagerDB.adicionar_rodada(numero_rodada)

    def listar_rodadas(self):
        for i, rodada in enumerate(ManagerDB.rodadas, start=1):
            print(f"Rodada {i}: {rodada}")

if __name__ == "__main__":
    TerminalInterface()