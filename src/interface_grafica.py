import tkinter

class InterfaceGrafica:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.janela = tkinter.Tk()
        self.janela.title("Campeonato Capixaba 2026")
        self.janela.iconbitmap("images/icone.ico")
        self.janela.geometry(f"{self.largura}x{self.altura}")
        self.canvas = tkinter.Canvas(self.janela, width=self.largura, 
        height=self.altura)
        self.canvas.pack()

    def iniciar(self):
        self.janela.mainloop()

    def menu(self):
        self.canvas.delete("all") # Limpa o canvas antes de desenhar o menu
        self.canvas.create_text(self.largura // 2, self.altura // 4, 
                                text="Campeonato Capixaba 2026", 
                                font=("Arial", 24, "bold"))
        self.canvas.create_text(self.largura // 2, self.altura // 2, 
                                text="Bem-vindo ao simulador do Campeonato Capixaba de Futebol!", 
                                font=("Arial", 16))
        botao_iniciar = tkinter.Button(self.janela, text="Iniciar Simulação")
        botao_iniciar_window = self.canvas.create_window(self.largura // 2, 
                                                         (self.altura // 4) * 3, 
                                                         window=botao_iniciar)

def main():
    interface = InterfaceGrafica(1280, 720)
    interface.menu()
    interface.iniciar()

if __name__ == "__main__":
    main()