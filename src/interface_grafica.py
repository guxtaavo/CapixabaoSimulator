import tkinter as tk
from tkinter import font, messagebox, Listbox
from pathlib import Path
from campeonato import Campeonato
from manager_db import ManagerDB
import sys

# Define o diretório raiz para encontrar os arquivos de banco de dados
# Bloco para detectar se está rodando como .exe ou script
if getattr(sys, 'frozen', False):
    # No modo .exe, os arquivos estão na pasta temp _MEIPASS
    ROOT_DIR = Path(sys._MEIPASS) 
else:
    # No modo script, a raiz é dois níveis acima (pasta 'CapixabaSimulator')
    ROOT_DIR = Path(__file__).parent.parent

class InterfaceGrafica:
    def __init__(self):
        self.manager_db = None
        self.largura = 1980
        self.altura = 1080

        self.janela = tk.Tk()
        self.janela.title("Capixabão Simulator 2026")
        self.janela.iconbitmap(ROOT_DIR / "images/icone.ico")

        # 👉 Tela cheia
        self.janela.attributes("-fullscreen", True)

        # 👉 ESC sai do fullscreen
        self.janela.bind("<Escape>", lambda e: self.janela.attributes("-fullscreen", False))

        self.janela.configure(bg="#2c3e50")

        self.canvas = tk.Canvas(
            self.janela,
            bg="#2c3e50",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.menu()


    def iniciar(self):
        """Inicia o loop principal da aplicação Tkinter."""
        self.janela.mainloop()

    def menu(self):
        """Desenha a tela do menu principal com as opções."""
        self.canvas.delete("all") # Limpa a tela antes de desenhar
        
        # Título do app
        self.canvas.create_text(self.largura // 2, self.altura // 4,
                                text="Campeonato Capixaba 2026", font=("Lato", 32, "bold"),
                                fill="#ecf0f1")
        
        # Botões de criar nova simulação
        botao_criar = tk.Button(self.janela, 
                                text="Criar Nova Simulação", font=("Lato", 14, "bold"),
                                bg="#3498db", fg="white", activebackground="#2980b9",
                                activeforeground="white", relief="flat", bd=0, padx=20, pady=10,
                                cursor="hand2", command=self.criar_simulacao)
        self.canvas.create_window(self.largura // 2, self.altura // 2 - 30, window=botao_criar)

        # Botões de carregar simulação existente
        botao_carregar = tk.Button(self.janela, text="Carregar Simulação",
                                   font=("Lato", 14, "bold"), bg="#9b59b6",
                                   fg="white", activebackground="#8e44ad", activeforeground="white", 
                                   relief="flat", bd=0, padx=20, pady=10, cursor="hand2", 
                                   command=self.abrir_seletor_de_db)
        self.canvas.create_window(self.largura // 2, self.altura // 2 + 50, window=botao_carregar)
        
        self.canvas.create_text(self.largura // 2, self.altura - 40,
                                text="© 2025 Capixabão Simulator",
                                font=("Lato", 10), fill="#bdc3c7")

    def criar_simulacao(self):
        """Cria uma nova instância de campeonato e configura o banco de dados."""
        campeonato = Campeonato()
        # Inicia ManagerDB sem um caminho de arquivo, ativando o modo de criação
        self.manager_db = ManagerDB(campeonato)
        # Cria as tabelas e a estrutura no novo arquivo de DB
        self.manager_db.setup_database()
        # Transiciona para a tela principal da simulação
        self.mostrar_tela_simulacao()

    def abrir_seletor_de_db(self):
        """Abre uma nova janela para o usuário selecionar um arquivo de DB salvo."""
        arquivos_salvos = sorted(list(ROOT_DIR.glob('Campeonato_Capixaba_2026*.sqlite3')))

        if not arquivos_salvos:
            messagebox.showinfo("Nenhum Arquivo Encontrado",
                                "Não há simulações salvas para carregar.")
            return

        seletor_janela = tk.Toplevel(self.janela)
        seletor_janela.title("Carregar Simulação")
        seletor_janela.geometry("400x350")
        seletor_janela.configure(bg="#34495e")
        seletor_janela.transient(self.janela)
        seletor_janela.grab_set()

        tk.Label(seletor_janela, text="Selecione uma simulação:", bg="#34495e", 
                 fg="white", font=("Lato", 12)).pack(pady=10)

        listbox = Listbox(seletor_janela, bg="#2c3e50", fg="white", 
                          selectbackground="#3498db", font=("Lato", 11), relief="flat")
        listbox.pack(fill="both", expand=True, padx=10, pady=5)

        for arquivo in arquivos_salvos:
            listbox.insert(tk.END, arquivo.name)

        def carregar_selecionado():
            indices = listbox.curselection()
            if not indices:
                messagebox.showwarning("Nenhuma Seleção",
                                       "Por favor, selecione um arquivo para carregar.")
                return
            
            nome_arquivo = listbox.get(indices[0])
            caminho_completo = ROOT_DIR / nome_arquivo
            seletor_janela.destroy()

            campeonato = Campeonato()
            # Inicia ManagerDB com o caminho do arquivo, ativando o modo de carregamento
            self.manager_db = ManagerDB(campeonato, db_file_path=caminho_completo)
            self.mostrar_tela_simulacao()

        btn_frame = tk.Frame(seletor_janela, bg="#34495e")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Carregar", command=carregar_selecionado,
                  bg="#27ae60", fg="white", 
                  relief="flat", font=("Lato", 10)).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancelar", command=seletor_janela.destroy,
                  bg="#c0392b", fg="white", 
                  relief="flat", font=("Lato", 10)).pack(side="left", padx=10)

    def mostrar_tela_simulacao(self):
        """Cria e exibe a tela principal da simulação com classificação e rodadas."""
        self.janela.withdraw() # Esconde a janela do menu

        sim_janela = tk.Toplevel(self.janela)
        sim_janela.title(f"Simulação - {self.manager_db.db_file.name}")
        sim_janela.geometry(f"{self.largura}x{self.altura}")
        sim_janela.configure(bg="#34495e")

        def ao_fechar():
            """Função chamada ao fechar a janela de simulação."""
            self.manager_db._close()
            sim_janela.destroy()
            self.janela.deiconify() # Reexibe a janela do menu
        sim_janela.protocol("WM_DELETE_WINDOW", ao_fechar)

        # ----- ESTRUTURA DA TELA DE SIMULAÇÃO -----
        frame_esquerda = tk.Frame(sim_janela, bg="#2c3e50", padx=10, pady=10)
        frame_esquerda.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        frame_direita = tk.Frame(sim_janela, bg="#2c3e50", padx=10, pady=10)
        frame_direita.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        # ----- CONTEÚDO DO FRAME ESQUERDO (CLASSIFICAÇÃO) -----
        tk.Label(frame_esquerda, text="CLASSIFICAÇÃO", font=("Lato", 18, "bold"),
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=10)
        
        fonte_mono = font.Font(family="Courier", size=10)
        texto_tabela = tk.Text(frame_esquerda, wrap="none", font=fonte_mono, 
                               bg="#34495e", fg="white", relief="flat", 
                               state="disabled", borderwidth=0)
        texto_tabela.pack(fill="both", expand=True)

        def atualizar_tabela_gui():
            tabela_str = self.manager_db.get_classificacao_formatada()
            texto_tabela.config(state="normal")
            texto_tabela.delete("1.0", "end")
            texto_tabela.insert("1.0", tabela_str)
            texto_tabela.config(state="disabled")

        # ----- CONTEÚDO DA PARTE DIREITA DA TELA (EDITOR DE RODADAS) -----
        tk.Label(frame_direita, text="EDITOR DE RODADAS", font=("Lato", 18, "bold"),
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=10)
        
        frame_lista_rodadas = tk.Frame(frame_direita, bg="#2c3e50")
        frame_lista_rodadas.pack(fill="x", pady=5)
        
        frame_jogos_rodada = tk.Frame(frame_direita, bg="#34495e")
        frame_jogos_rodada.pack(fill="both", expand=True, pady=10)
        
        def mostrar_jogos(num_rodada):
            for widget in frame_jogos_rodada.winfo_children():
                widget.destroy()

            tk.Label(frame_jogos_rodada, text=f"Jogos da Rodada {num_rodada}",
                     font=("Lato", 14, "bold"), bg="#34495e", fg="#ecf0f1").pack(pady=(5, 15))

            jogos = self.manager_db.get_jogos_da_rodada(num_rodada)
            for id_jogo, mandante, visitante, pm, pv in jogos:
                frame_jogo = tk.Frame(frame_jogos_rodada, bg="#2c3e50", pady=8)
                frame_jogo.pack(fill="x", pady=3, padx=10)

                # --- Configuração do Grid para alinhar tudo em colunas ---
                frame_jogo.grid_columnconfigure(0, weight=3) # Coluna time mandante
                frame_jogo.grid_columnconfigure(1, weight=1) # Coluna placar mandante
                frame_jogo.grid_columnconfigure(2, weight=0) # Coluna do "X"
                frame_jogo.grid_columnconfigure(3, weight=1) # Coluna placar visitante
                frame_jogo.grid_columnconfigure(4, weight=3) # Coluna time visitante
                frame_jogo.grid_columnconfigure(5, weight=2) # Coluna botão salvar

                # --- Widgets posicionados com .grid() para alinhamento perfeito ---
                tk.Label(frame_jogo, text=mandante, font=("Lato", 12), bg="#2c3e50",
                         fg="white", anchor='e').grid(row=0, column=0, sticky="ew", padx=(0, 10))
                
                pm_var = tk.StringVar(value=pm if pm is not None else "")
                entry_pm = tk.Entry(frame_jogo, textvariable=pm_var, width=3,
                                    font=("Lato", 12, "bold"), justify='center', relief="flat")
                entry_pm.grid(row=0, column=1)

                tk.Label(frame_jogo, text="X", font=("Lato", 12, "bold"),
                         bg="#2c3e50", fg="white").grid(row=0, column=2, padx=5)
                
                pv_var = tk.StringVar(value=pv if pv is not None else "")
                entry_pv = tk.Entry(frame_jogo, textvariable=pv_var, width=3,
                                    font=("Lato", 12, "bold"), justify='center', relief="flat")
                entry_pv.grid(row=0, column=3)

                tk.Label(frame_jogo, text=visitante, font=("Lato", 12), bg="#2c3e50",
                         fg="white", anchor='w').grid(row=0, column=4, sticky="ew", padx=(10, 0))

                def salvar(id_j=id_jogo, pm_v=pm_var, pv_v=pv_var, rodada=num_rodada):
                    try:
                        novo_pm = int(pm_v.get()) if pm_v.get() else 0
                        novo_pv = int(pv_v.get()) if pv_v.get() else 0
                        self.manager_db.atualizar_placar(rodada, id_j, novo_pm, novo_pv)
                        atualizar_tabela_gui() # ATUALIZA A TABELA NA ESQUERDA!
                    except ValueError:
                        messagebox.showerror("Erro de Entrada",
                                             "Placar inválido. Por favor, insira apenas números.")

                btn_salvar = tk.Button(frame_jogo, text="Salvar", command=salvar,
                                       cursor="hand2", bg="#27ae60", fg="white",
                                       relief="flat", font=("Lato", 9, "bold"))
                btn_salvar.grid(row=0, column=5, padx=(20, 0))

        # Cria os botões para navegação entre as rodadas
        for i in range(len(self.manager_db.campeonato._rodadas)):
            num_rodada = i + 1
            btn = tk.Button(frame_lista_rodadas, text=f"{num_rodada}", cursor="hand2",
                            command=lambda r=num_rodada: mostrar_jogos(r),
                            relief="flat", font=("Lato", 10), bg="#34495e", fg="white")
            btn.pack(side="left", expand=True, fill="x", padx=2, pady=2)

        # Carrega o estado inicial da tela
        atualizar_tabela_gui()
        mostrar_jogos(1) # Exibe a primeira rodada por padrão

def main():
    interface = InterfaceGrafica()
    interface.iniciar()

if __name__ == "__main__":
    main()