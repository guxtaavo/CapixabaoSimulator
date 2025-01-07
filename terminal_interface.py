from clube import Clube
import sys

class TerminalInterface():
    def __init__(self):
        self.menu()

    def menu(self):
        while True:
            print("Bem-vindo ao sistema de controle de campeonato!")
            print("Escolha uma opção:")
            print("1 - Cadastrar clube")
            print("2 - Listar clubes")
            print("3 - Cadastrar rodada")
            print("4 - Listar rodadas")
            print("5 - Sair")
            opcao = input("Digite o número da opção desejada: ")
            match opcao:
                case "1":
                    self.cadastrar_clube()
                case "2":
                    self.listar_clubes()
                case "3":
                    self.cadastrar_rodada()
                case "4":
                    self.listar_rodadas()
                case "5":
                    print("Obrigado por utilizar o sistema!")
                    sys.exit()
                case _:
                    print("Opção inválida!")

    def cadastrar_clube(self):
        while True:
            nome = input("Digite o nome do clube: ")
            apelido = input("Digite o apelido do clube: ")
            clube = Clube(nome, apelido)
            print(clube)
            resposta = input("Deseja cadastrar mais um clube? (s/n) ")
            if resposta.lower() == 'n':
                break

    def listar_clubes(self):
        sys.quit()

    def cadastrar_rodada(self):
        sys.quit()
        # while True:
        #     rodada = []
        #     i = 0
        #     print("Cadastrando rodada")
        #     for clube in clubes:
        #         i+=1
        #         print(f"{i}. {clube}")
        #     while True:
        #         indice_clube_casa = int(input("Digite o número do clube da casa: "))
        #         if indice_clube_casa < 1 or indice_clube_casa > len(clubes):
        #             print("Clube inválido!")
        #         else:
        #             clube_casa = clubes[indice_clube_casa-1]
        #             break
        #     while True:
        #         indice_clube_visitante = int(input("Digite o número do clube visitante: "))
        #         if indice_clube_visitante < 1 or indice_clube_visitante > len(clubes) or indice_clube_visitante == indice_clube_casa:
        #             print("Clube inválido!")
        #         else:
        #             clube_visitante = clubes[indice_clube_visitante-1]
        #             break
        #     rodada.append([clube_casa, clube_visitante])


    def listar_rodadas(self):
        sys.quit()

if __name__ == '__main__':
    terminal = TerminalInterface()