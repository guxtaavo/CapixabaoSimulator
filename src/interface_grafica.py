import tkinter as tk
from tkinter import messagebox, Listbox, PhotoImage
from tkinter import ttk
from pathlib import Path
from campeonato import Campeonato
from manager_db import ManagerDB
import sys
import math

# Detecta se está rodando como .exe (PyInstaller) ou como script
if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys._MEIPASS)
else:
    ROOT_DIR = Path(__file__).parent.parent

class InterfaceGrafica:
    def __init__(self):
        self.manager_db = None
        self.largura = 1980
        self.altura = 1080

        self.ICON_SIZE_JOGOS = 26
        self.ICON_SIZE_CLASS = 36
        self.ICON_SIZE_MATA = 80

        self.janela = tk.Tk()
        self.janela.title("Capixabão Simulator 2026")
        ico_path = ROOT_DIR / "images/icone.ico"
        png_path = ROOT_DIR / "images/Capixaba.png"
        self._icon_img = None

        # Usa .ico no Windows e PhotoImage (png) como fallback para Linux/macOS
        if sys.platform == "win32" and ico_path.exists():
            try:
                self.janela.iconbitmap(default=str(ico_path))
            except tk.TclError:
                pass

        if png_path.exists():
            try:
                self._icon_img = PhotoImage(file=str(png_path))
                self.janela.iconphoto(True, self._icon_img)
            except tk.TclError:
                pass

        # maximizada (não fullscreen). Nem todos sistemas suportam "zoomed".
        maximized = False
        try:
            # Windows suporta state("zoomed")
            self.janela.state("zoomed")
            maximized = True
        except tk.TclError:
            pass

        if not maximized:
            try:
                # Algumas builds Tk no Linux aceitam attribute -zoomed
                self.janela.attributes("-zoomed", True)
                maximized = True
            except tk.TclError:
                pass

        if not maximized:
            # fallback: ajusta tamanho para a resolução disponível
            self.janela.update_idletasks()
            sw = self.janela.winfo_screenwidth()
            sh = self.janela.winfo_screenheight()
            self.janela.geometry(f"{sw}x{sh}")

        self.janela.configure(bg="#2c3e50")
        self.canvas = tk.Canvas(self.janela, bg="#2c3e50", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # ícones começam vazios
        self.icones_jogos = {}
        self.icones_class = {}
        self.icones_mata = {}

        self.menu()

        # força desenhar a tela ANTES de começar a carregar
        self.janela.update_idletasks()

        # inicia carregamento
        self._start_icon_loader()

    def _start_icon_loader(self):
        """Prepara a fila de carregamento de ícones e começa incrementalmente."""
        pasta = ROOT_DIR / "images"
        self._mapa_icones = {
            "Capixaba": "Capixaba.png",
            "Desportiva": "Desportiva.png",
            "Forte": "Forte.png",
            "Porto Vitória": "Porto_Vitoria.png",
            "Real Noroeste": "Real_Noroeste.png",
            "Rio Branco": "Rio_Branco.png",
            "Rio Branco VNI": "Rio_Branco_VNI.png",
            "Serra": "Serra.png",
            "Vilavelhense": "Vilavelhense.png",
            "Vitória": "Vitoria.png",
        }
        self._pasta_icones = pasta
        self._icon_queue = list(self._mapa_icones.items())  # [(time, arquivo), ...]
        self.janela.after(1, self._load_next_icon)


    def _load_next_icon(self):
        """Carrega ícones de 1 time por tick (não trava a UI)."""
        if not self._icon_queue:
            # terminou
            if hasattr(self, "_loading_text_id"):
                self.canvas.delete(self._loading_text_id)
            return

        time, arquivo = self._icon_queue.pop(0)
        caminho = self._pasta_icones / arquivo

        if caminho.exists():
            self.icones_jogos[time] = self._carregar_redimensionado(caminho, self.ICON_SIZE_JOGOS)
            self.icones_class[time] = self._carregar_redimensionado(caminho, self.ICON_SIZE_CLASS)
            self.icones_mata[time]  = self._carregar_redimensionado(caminho, self.ICON_SIZE_MATA)
        else:
            self.icones_jogos[time] = None
            self.icones_class[time] = None
            self.icones_mata[time]  = None

        # agenda o próximo sem travar
        self.janela.after(1, self._load_next_icon)


    def _carregar_redimensionado(self, path_img: Path, alvo_px: int):
        """Redimensiona via subsample."""
        img = PhotoImage(file=str(path_img))
        w, h = img.width(), img.height()
        fator = max(w / alvo_px, h / alvo_px)
        fator_int = max(1, int(math.ceil(fator)))
        return img.subsample(fator_int, fator_int)

    def iniciar(self):
        self.janela.mainloop()

    def menu(self):
        self.canvas.delete("all")

        # pega tamanho real do canvas/janela
        self.janela.update_idletasks()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        # fallback se ainda não calculou (primeiro frame)
        if w <= 1 or h <= 1:
            w = self.janela.winfo_width()
            h = self.janela.winfo_height()

        self.canvas.create_text(
            w // 2, h // 4,
            text="Campeonato Capixaba 2026",
            font=("Lato", 32, "bold"),
            fill="#ecf0f1"
        )

        botao_criar = tk.Button(
            self.janela,
            text="Criar Nova Simulação",
            width=22,
            font=("Lato", 14, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.criar_simulacao
        )
        self.canvas.create_window(w // 2, h // 2 - 30, window=botao_criar)

        botao_carregar = tk.Button(
            self.janela,
            text="Carregar Simulação",
            width=22,
            font=("Lato", 14, "bold"),
            bg="#9b59b6",
            fg="white",
            activebackground="#8e44ad",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.abrir_seletor_de_db
        )
        self.canvas.create_window(w // 2, h // 2 + 50, window=botao_carregar)

        # AGORA o © sempre fica visível porque usa "h real"
        self.canvas.create_text(
            w // 2, h - 40,
            text="© 2026 Capixabão Simulator",
            font=("Lato", 10),
            fill="#bdc3c7"
        )

    def criar_simulacao(self):
        campeonato = Campeonato()
        self.manager_db = ManagerDB(campeonato)
        self.manager_db.setup_database()
        self.mostrar_tela_simulacao()

    def abrir_seletor_de_db(self):
        arquivos_salvos = sorted(list(ROOT_DIR.glob('Campeonato_Capixaba_2026*.sqlite3')))
        if not arquivos_salvos:
            messagebox.showinfo("Nenhum Arquivo Encontrado", "Não há simulações salvas para carregar.")
            return

        seletor_janela = tk.Toplevel(self.janela)
        seletor_janela.title("Carregar Simulação")
        seletor_janela.geometry("400x350")
        seletor_janela.configure(bg="#34495e")
        seletor_janela.transient(self.janela)
        seletor_janela.grab_set()
        seletor_janela.resizable(False, False)

        tk.Label(
            seletor_janela,
            text="Selecione uma simulação:",
            bg="#34495e",
            fg="white",
            font=("Lato", 12)
        ).pack(pady=10)

        listbox = Listbox(
            seletor_janela,
            bg="#2c3e50",
            fg="white",
            selectbackground="#3498db",
            font=("Lato", 11),
            relief="flat"
        )
        listbox.pack(fill="both", expand=True, padx=10, pady=5)

        for arquivo in arquivos_salvos:
            listbox.insert(tk.END, arquivo.name)

        def carregar_selecionado():
            indices = listbox.curselection()
            if not indices:
                messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione um arquivo para carregar.")
                return

            nome_arquivo = listbox.get(indices[0])
            caminho_completo = ROOT_DIR / nome_arquivo
            seletor_janela.destroy()

            campeonato = Campeonato()
            self.manager_db = ManagerDB(campeonato, db_file_path=caminho_completo)
            self.mostrar_tela_simulacao()

        btn_frame = tk.Frame(seletor_janela, bg="#34495e")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Carregar",
            command=carregar_selecionado,
            bg="#27ae60",
            fg="white",
            relief="flat",
            font=("Lato", 10)
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Cancelar",
            command=seletor_janela.destroy,
            bg="#c0392b",
            fg="white",
            relief="flat",
            font=("Lato", 10)
        ).pack(side="left", padx=10)

    def mostrar_tela_simulacao(self):
        self.janela.withdraw()

        sim_janela = tk.Toplevel(self.janela)
        sim_janela.title(f"Simulação - {self.manager_db.db_file.name}")
        maximized = False
        try:
            sim_janela.state("zoomed")
            maximized = True
        except tk.TclError:
            pass

        if not maximized:
            try:
                sim_janela.attributes("-zoomed", True)
                maximized = True
            except tk.TclError:
                pass

        if not maximized:
            sim_janela.update_idletasks()
            sw = sim_janela.winfo_screenwidth()
            sh = sim_janela.winfo_screenheight()
            sim_janela.geometry(f"{sw}x{sh}")

        sim_janela.configure(bg="#34495e")

        def ao_fechar():
            try:
                self.manager_db._close()
            except:
                pass

            sim_janela.destroy()
            self.janela.destroy()

        sim_janela.protocol("WM_DELETE_WINDOW", ao_fechar)

        # Estrutura principal da janela
        frame_esquerda = tk.Frame(sim_janela, bg="#2c3e50", padx=10, pady=10)
        frame_esquerda.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        frame_direita = tk.Frame(sim_janela, bg="#2c3e50", padx=10, pady=10)
        frame_direita.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        # Classificação
        tk.Label(
            frame_esquerda,
            text="CLASSIFICAÇÃO",
            font=("Lato", 18, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack(pady=10)

        frame_class = tk.Frame(frame_esquerda, bg="#2c3e50")
        frame_class.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Classificacao.Treeview",
            background="#34495e",
            fieldbackground="#34495e",
            foreground="white",
            rowheight=self.ICON_SIZE_CLASS + 12,
            borderwidth=0,
            font=("Lato", 10)
        )
        style.configure(
            "Classificacao.Treeview.Heading",
            background="#2c3e50",
            foreground="#ecf0f1",
            font=("Lato", 10, "bold")
        )
        style.map(
            "Classificacao.Treeview",
            background=[("selected", "#2d8cff")],
            foreground=[("selected", "white")]
        )

        cols = ("pos", "time", "p", "j", "v", "e", "d", "gp", "gc", "sg", "aprov")
        tree = ttk.Treeview(
            frame_class,
            columns=cols,
            show="tree headings",
            style="Classificacao.Treeview"
        )

        tree.heading("#0", text="")  # escudo
        tree.column("#0", width=self.ICON_SIZE_CLASS + 18, stretch=False, anchor="center")

        tree.heading("pos", text="")
        tree.heading("time", text="Time")
        tree.heading("p", text="P")
        tree.heading("j", text="J")
        tree.heading("v", text="V")
        tree.heading("e", text="E")
        tree.heading("d", text="D")
        tree.heading("gp", text="GP")
        tree.heading("gc", text="GC")
        tree.heading("sg", text="SG")
        tree.heading("aprov", text="Aprov.")

        tree.column("pos", width=40, anchor="center", stretch=False)
        tree.column("time", width=260, anchor="w", stretch=True)
        for c in ("p", "j", "v", "e", "d", "gp", "gc", "sg"):
            tree.column(c, width=55, anchor="center", stretch=False)
        tree.column("aprov", width=80, anchor="center", stretch=False)

        sb = ttk.Scrollbar(frame_class, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Cores das linhas da tabela (G4 G8 E Z2)
        tree.tag_configure("top4", background="#1f4e79", foreground="white")
        tree.tag_configure("mid58", background="#1f552d", foreground="white")
        tree.tag_configure("z2", background="#7a1f1f", foreground="white")

        # fallback alternado (para quando não entra em nenhuma faixa)
        tree.tag_configure("odd", background="#31465a")
        tree.tag_configure("even", background="#34495e")

        def _parse_classificacao_from_string(tabela_str: str):
            rows = []
            for line in tabela_str.splitlines():
                line = line.strip()
                if not line.startswith("|"):
                    continue
                if "Escudo" in line or "Time" in line:
                    continue
                parts = [p.strip() for p in line.strip("|").split("|")]
                if len(parts) < 12:
                    continue
                try:
                    int(parts[0])
                except ValueError:
                    continue

                pos = parts[0]
                time_nome = parts[2]
                p = parts[3]
                j = parts[4]
                v = parts[5]
                e = parts[6]
                d = parts[7]
                gp = parts[8]
                gc = parts[9]
                sg = parts[10]
                aprov = parts[11]
                rows.append((pos, time_nome, p, j, v, e, d, gp, gc, sg, aprov))
            return rows

        def atualizar_classificacao_gui():
            tabela_str = self.manager_db.get_classificacao_formatada()
            dados = _parse_classificacao_from_string(tabela_str)

            # limpa
            for item in tree.get_children():
                tree.delete(item)

            total = len(dados)

            for idx, (pos, time_nome, p, j, v, e, d, gp, gc, sg, aprov) in enumerate(dados):
                pos_int = int(pos)

                # Regras para colorir a linha
                if 1 <= pos_int <= 4:
                    tag = "top4"
                elif 5 <= pos_int <= 8:
                    tag = "mid58"
                elif pos_int >= max(1, total - 1):   # dois últimos
                    tag = "z2"
                else:
                    tag = "even" if idx % 2 == 0 else "odd"

                iid = tree.insert(
                    "",
                    "end",
                    values=(pos, time_nome, p, j, v, e, d, gp, gc, sg, aprov),
                    tags=(tag,)
                )

                ic = self.icones_class.get(time_nome)
                if ic is not None:
                    tree.item(iid, image=ic)

        # Editor de Rodadas
        tk.Label(
            frame_direita,
            text="EDITOR DE RODADAS",
            font=("Lato", 18, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack(pady=10)

        frame_lista_rodadas = tk.Frame(frame_direita, bg="#2c3e50")
        frame_lista_rodadas.pack(fill="x", pady=5)

        frame_jogos_rodada = tk.Frame(frame_direita, bg="#34495e")
        frame_jogos_rodada.pack(fill="both", expand=True, pady=10)

         # Botão para entrar no mata-mata
        def abrir_mata_mata():
            top8 = self.manager_db.get_top8_times()  # [1º..8º]

            win = tk.Toplevel(sim_janela)
            win.title("Mata-Mata - Quartas / Semi / Final")
            win.configure(bg="#2c3e50")

            # abre como janela maximizada (não fullscreen)
            maximized = False
            try:
                win.state("zoomed")
                maximized = True
            except tk.TclError:
                pass

            if not maximized:
                try:
                    win.attributes("-zoomed", True)
                    maximized = True
                except tk.TclError:
                    pass

            if not maximized:
                win.update_idletasks()
                sw = win.winfo_screenwidth()
                sh = win.winfo_screenheight()
                win.geometry(f"{sw}x{sh}")

            # garante que a janela fique na frente
            win.transient(sim_janela)
            win.lift()
            win.focus_force()

            from mata_mata import MataMataCanvas

            bracket = MataMataCanvas(
                win,
                icones=self.icones_mata,
                times_top8=top8,
                on_campeao=None
            )
            bracket.pack(fill="both", expand=True)

            # força o Tk a calcular tamanhos antes do primeiro desenho
            win.update_idletasks()

            # redesenha após a janela estar dimensionada de verdade
            win.after(50, bracket.redesenhar)

        # Botão no topo do painel direito
        btn_mata = tk.Button(
            frame_direita,
            text="Mata-Mata",
            command=abrir_mata_mata,
            cursor="hand2",
            bg="#f39c12",
            fg="white",
            activebackground="#d68910",
            activeforeground="white",
            relief="flat",
            font=("Lato", 11, "bold"),
            padx=14,
            pady=6
        )
        btn_mata.pack(pady=(0, 10), anchor="e")

        def mostrar_jogos(num_rodada):
            for widget in frame_jogos_rodada.winfo_children():
                widget.destroy()

            tk.Label(
                frame_jogos_rodada,
                text=f"Jogos da Rodada {num_rodada}",
                font=("Lato", 14, "bold"),
                bg="#34495e",
                fg="#ecf0f1"
            ).pack(pady=(5, 15))

            jogos = self.manager_db.get_jogos_da_rodada(num_rodada)
            for id_jogo, mandante, visitante, pm, pv in jogos:
                frame_jogo = tk.Frame(frame_jogos_rodada, bg="#2c3e50", pady=8)
                frame_jogo.pack(fill="x", pady=3, padx=10)

                frame_jogo.grid_columnconfigure(0, weight=3)
                frame_jogo.grid_columnconfigure(1, weight=1)
                frame_jogo.grid_columnconfigure(2, weight=0)
                frame_jogo.grid_columnconfigure(3, weight=1)
                frame_jogo.grid_columnconfigure(4, weight=3)
                frame_jogo.grid_columnconfigure(5, weight=2)

                # Mandante (Escudo + Nome)
                frame_mandante = tk.Frame(frame_jogo, bg="#2c3e50")
                frame_mandante.grid(row=0, column=0, sticky="e", padx=(0, 10))

                icone_m = self.icones_jogos.get(mandante)
                if icone_m is not None:
                    tk.Label(frame_mandante, image=icone_m, bg="#2c3e50").pack(side="left", padx=(0, 6))

                tk.Label(
                    frame_mandante,
                    text=mandante,
                    font=("Lato", 12),
                    bg="#2c3e50",
                    fg="white"
                ).pack(side="left")

                # Placar (Entradas)
                pm_var = tk.StringVar(value=pm if pm is not None else "")
                entry_pm = tk.Entry(
                    frame_jogo,
                    textvariable=pm_var,
                    width=3,
                    font=("Lato", 12, "bold"),
                    justify="center",
                    relief="flat"
                )
                entry_pm.grid(row=0, column=1)

                tk.Label(
                    frame_jogo,
                    text="X",
                    font=("Lato", 12, "bold"),
                    bg="#2c3e50",
                    fg="white"
                ).grid(row=0, column=2, padx=5)

                pv_var = tk.StringVar(value=pv if pv is not None else "")
                entry_pv = tk.Entry(
                    frame_jogo,
                    textvariable=pv_var,
                    width=3,
                    font=("Lato", 12, "bold"),
                    justify="center",
                    relief="flat"
                )
                entry_pv.grid(row=0, column=3)

                # Visitante (Nome + Escudo)
                frame_visitante = tk.Frame(frame_jogo, bg="#2c3e50")
                frame_visitante.grid(row=0, column=4, sticky="w", padx=(10, 0))

                tk.Label(
                    frame_visitante,
                    text=visitante,
                    font=("Lato", 12),
                    bg="#2c3e50",
                    fg="white"
                ).pack(side="left")

                icone_v = self.icones_jogos.get(visitante)
                if icone_v is not None:
                    tk.Label(frame_visitante, image=icone_v, bg="#2c3e50").pack(side="left", padx=(6, 0))

                # Salvar botão
                def salvar(id_j=id_jogo, pm_v=pm_var, pv_v=pv_var, rodada=num_rodada):
                    try:
                        novo_pm = int(pm_v.get()) if pm_v.get() else 0
                        novo_pv = int(pv_v.get()) if pv_v.get() else 0
                        self.manager_db.atualizar_placar(rodada, id_j, novo_pm, novo_pv)
                        atualizar_classificacao_gui()
                    except ValueError:
                        messagebox.showerror("Erro de Entrada", "Placar inválido. Por favor, insira apenas números.")

                btn_salvar = tk.Button(
                    frame_jogo,
                    text="Salvar",
                    command=salvar,
                    cursor="hand2",
                    bg="#27ae60",
                    fg="white",
                    relief="flat",
                    font=("Lato", 9, "bold")
                )
                btn_salvar.grid(row=0, column=5, padx=(20, 0))

        # Botões de rodadas
        for i in range(len(self.manager_db.campeonato._rodadas)):
            num_rodada = i + 1
            btn = tk.Button(
                frame_lista_rodadas,
                text=f"{num_rodada}",
                cursor="hand2",
                command=lambda r=num_rodada: mostrar_jogos(r),
                relief="flat",
                font=("Lato", 10),
                bg="#34495e",
                fg="white"
            )
            btn.pack(side="left", expand=True, fill="x", padx=2, pady=2)

        atualizar_classificacao_gui()
        mostrar_jogos(1)

    # Ícones
    def _carregar_icones_em_tres_tamanhos(self):
        """
        Carrega os escudos e devolve três dicionários:
        - icones_jogos
        - icones_class
        - icones_mata

        Cada dicionário mapeia nome do time para PhotoImage redimensionada.
        """
        pasta = ROOT_DIR / "images"
        mapa = {
            "Capixaba": "Capixaba.png",
            "Desportiva": "Desportiva.png",
            "Forte": "Forte.png",
            "Porto Vitória": "Porto_Vitoria.png",
            "Real Noroeste": "Real_Noroeste.png",
            "Rio Branco": "Rio_Branco.png",
            "Rio Branco VNI": "Rio_Branco_VNI.png",
            "Serra": "Serra.png",
            "Vilavelhense": "Vilavelhense.png",
            "Vitória": "Vitoria.png",
        }

        def carregar_redimensionado(path_img: Path, alvo_px: int):
            img = PhotoImage(file=str(path_img))
            w, h = img.width(), img.height()
            fator = max(w / alvo_px, h / alvo_px)
            fator_int = max(1, int(math.ceil(fator)))
            return img.subsample(fator_int, fator_int)

        icones_jogos = {}
        icones_class = {}
        icones_mata = {}

        for time, arquivo in mapa.items():
            caminho = pasta / arquivo
            if caminho.exists():
                icones_jogos[time] = carregar_redimensionado(caminho, self.ICON_SIZE_JOGOS)
                icones_class[time] = carregar_redimensionado(caminho, self.ICON_SIZE_CLASS)
                icones_mata[time] = carregar_redimensionado(caminho, self.ICON_SIZE_MATA)  # novo
            else:
                icones_jogos[time] = None
                icones_class[time] = None
                icones_mata[time] = None

        return icones_jogos, icones_class, icones_mata

def main():
    interface = InterfaceGrafica()
    interface.iniciar()


if __name__ == "__main__":
    main()