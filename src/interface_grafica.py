import tkinter as tk

class InterfaceGrafica:
    def __init__(self):
        self.largura = 1280
        self.altura = 720
        self.janela = tk.Tk()
        self.janela.title("Campeonato Capixaba 2026")
        self.janela.iconbitmap("images/icone.ico")
        self.janela.geometry(f"{self.largura}x{self.altura}")
        self.janela.configure(bg="#000000")  # fundo neutro e moderno

        # Canvas principal
        self.canvas = tk.Canvas(
            self.janela,
            width=self.largura,
            height=self.altura,
            bg="#948E8E",
            highlightthickness=0  # remove borda do canvas
        )
        self.canvas.pack(fill="both", expand=True)

        self.menu()  # exibe o menu assim que inicia

    def iniciar(self):
        self.janela.mainloop()

    def menu(self):
        self.canvas.delete("all")  # limpa o canvas antes de desenhar o menu

        # ---------- Título ----------
        self.canvas.create_text(
            self.largura // 2,
            self.altura // 4,
            text="Campeonato Capixaba 2026",
            font=("Lato", 32, "bold"),
            fill="#000000"
        )

        # ---------- Botão Criar ----------
        botao_criar = tk.Button(
            self.janela,
            text="Criar nova simulação",
            font=("Lato", 14, "bold"),
            bg="#00a8ff",
            fg="white",
            activebackground="#0097e6",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.criar_simulacao
        )
        self._estilizar_botao(botao_criar)
        self.canvas.create_window(
            self.largura // 2,
            self.altura // 2 - 30,
            window=botao_criar
        )

        # ---------- Botão Carregar ----------
        botao_carregar = tk.Button(
            self.janela,
            text="Carregar simulação",
            font=("Lato", 14, "bold"),
            bg="#9c88ff",
            fg="white",
            activebackground="#8c7ae6",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.carregar_simulacao
        )
        self._estilizar_botao(botao_carregar)
        self.canvas.create_window(
            self.largura // 2,
            self.altura // 2 + 50,
            window=botao_carregar
        )

        # ---------- Rodapé ----------
        self.canvas.create_text(
            self.largura // 2,
            self.altura - 40,
            text="© 2025 Capixabão Simulator",
            font=("Lato", 10),
            fill="#FFFFFF"
        )

    def _estilizar_botao(self, botao):
        # Animação leve de hover
        def on_enter(e):
            botao.config(bg="#273c75")

        def on_leave(e):
            if "Criar" in botao.cget("text"):
                botao.config(bg="#00a8ff")
            else:
                botao.config(bg="#9c88ff")

        botao.bind("<Enter>", on_enter)
        botao.bind("<Leave>", on_leave)

    def criar_simulacao(self):
        print("🆕 Criando nova simulação...")

    def carregar_simulacao(self):
        print("📂 Carregando simulação existente...")

def main():
    interface = InterfaceGrafica()
    interface.iniciar()

if __name__ == "__main__":
    main()
