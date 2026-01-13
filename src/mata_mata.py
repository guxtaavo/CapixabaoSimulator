import tkinter as tk

class MataMataCanvas(tk.Frame):
    """
    Mata-mata em Canvas:
    - Quartas: 1x8, 4x5 (chave A) | 2x7, 3x6 (chave B)
    - Semis: vencedores sobem
    - Final: clique no vencedor da Semi esquerda (SF1W) ou Semi direita (SF2W) para definir o campeão
    """

    def __init__(self, master, icones, times_top8, on_campeao=None, **kwargs):
        """
        icones: dict { "Nome Time": PhotoImage } (tamanho já ajustado)
        times_top8: lista de 8 nomes na ordem [1º,2º,3º,4º,5º,6º,7º,8º]
        on_campeao: callback(campeao_nome) opcional
        """
        super().__init__(master, bg="#2c3e50", **kwargs)
        self.icones = icones
        self.times = times_top8
        self.on_campeao = on_campeao

        # Estado do bracket
        self.qf = {
            "QF1": {"a": self.times[0], "b": self.times[7], "w": None},  # 1x8
            "QF2": {"a": self.times[3], "b": self.times[4], "w": None},  # 4x5
            "QF3": {"a": self.times[1], "b": self.times[6], "w": None},  # 2x7
            "QF4": {"a": self.times[2], "b": self.times[5], "w": None},  # 3x6
        }

        self.sf = {
            "SF1": {"a": None, "b": None, "w": None},  # vencedor QF1 vs QF2
            "SF2": {"a": None, "b": None, "w": None},  # vencedor QF3 vs QF4
        }

        self.f = {"F": {"a": None, "b": None, "w": None}}  # final (campeão em w)

        # Canvas
        self.canvas = tk.Canvas(self, bg="#2c3e50", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Slots
        self.slot = {}

        # Ajustes
        self.icon_r = 36
        self.pad_y = 120
        self.pad_x = 800

        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, _):
        self.redesenhar()

    def redesenhar(self):
        self.canvas.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()

        cx = w // 2
        left_x1 = cx - self.pad_x
        left_x2 = cx - (self.pad_x // 2)
        right_x2 = cx + (self.pad_x // 2)
        right_x1 = cx + self.pad_x

        top = h // 2 - 2 * self.pad_y
        mid = h // 2

        # posições dos vencedores das semis (meio)
        sfw_y = h // 2 - self.pad_y

        # posição do campeão (embaixo)
        champ_y = h // 2 + int(self.pad_y * 1.2)

        # ---- Slots ----
        self.slot = {
            # Quartas esquerda
            "QF1A": (left_x1, top - self.pad_y // 2),
            "QF1B": (left_x1, top + self.pad_y // 2),
            "QF2A": (left_x1, mid - self.pad_y // 2),
            "QF2B": (left_x1, mid + self.pad_y // 2),

            # Semi esquerda
            "SF1A": (left_x2, top),
            "SF1B": (left_x2, mid),
            "SF1W": (cx - 160, sfw_y),

            # Quartas direita
            "QF3A": (right_x1, top - self.pad_y // 2),
            "QF3B": (right_x1, top + self.pad_y // 2),
            "QF4A": (right_x1, mid - self.pad_y // 2),
            "QF4B": (right_x1, mid + self.pad_y // 2),

            # Semi direita
            "SF2A": (right_x2, top),
            "SF2B": (right_x2, mid),
            "SF2W": (cx + 160, sfw_y),

            # Campeão
            "FW": (cx, champ_y),
        }

        # ---- Linhas ----
        line = "#2ecc71"
        thick = 4

        def connect(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            mx = (x1 + x2) // 2
            self.canvas.create_line(x1, y1, mx, y1, fill=line, width=thick)
            self.canvas.create_line(mx, y1, mx, y2, fill=line, width=thick)
            self.canvas.create_line(mx, y2, x2, y2, fill=line, width=thick)

        # Quartas -> Semis (esquerda)
        connect(self.slot["QF1A"], self.slot["SF1A"])
        connect(self.slot["QF1B"], self.slot["SF1A"])
        connect(self.slot["QF2A"], self.slot["SF1B"])
        connect(self.slot["QF2B"], self.slot["SF1B"])
        connect(self.slot["SF1A"], self.slot["SF1W"])
        connect(self.slot["SF1B"], self.slot["SF1W"])

        # Quartas -> Semis (direita)
        connect(self.slot["QF3A"], self.slot["SF2A"])
        connect(self.slot["QF3B"], self.slot["SF2A"])
        connect(self.slot["QF4A"], self.slot["SF2B"])
        connect(self.slot["QF4B"], self.slot["SF2B"])
        connect(self.slot["SF2A"], self.slot["SF2W"])
        connect(self.slot["SF2B"], self.slot["SF2W"])

        # Final (SEM repetir finalistas embaixo):
        # conecta SF1W e SF2W direto ao campeão
        connect(self.slot["SF1W"], self.slot["FW"])
        connect(self.slot["SF2W"], self.slot["FW"])

        # ---- Desenha quartas ----
        self._draw_team_slot("QF1A", self.qf["QF1"]["a"], click=("QF1", "a"))
        self._draw_team_slot("QF1B", self.qf["QF1"]["b"], click=("QF1", "b"))

        self._draw_team_slot("QF2A", self.qf["QF2"]["a"], click=("QF2", "a"))
        self._draw_team_slot("QF2B", self.qf["QF2"]["b"], click=("QF2", "b"))

        self._draw_team_slot("QF3A", self.qf["QF3"]["a"], click=("QF3", "a"))
        self._draw_team_slot("QF3B", self.qf["QF3"]["b"], click=("QF3", "b"))

        self._draw_team_slot("QF4A", self.qf["QF4"]["a"], click=("QF4", "a"))
        self._draw_team_slot("QF4B", self.qf["QF4"]["b"], click=("QF4", "b"))

        # ---- Semis ----
        self._sync_semis()
        self._draw_team_slot("SF1A", self.sf["SF1"]["a"], click=("SF1", "a"), faint=True)
        self._draw_team_slot("SF1B", self.sf["SF1"]["b"], click=("SF1", "b"), faint=True)

        self._draw_team_slot("SF2A", self.sf["SF2"]["a"], click=("SF2", "a"), faint=True)
        self._draw_team_slot("SF2B", self.sf["SF2"]["b"], click=("SF2", "b"), faint=True)

        # vencedores das semis (no meio)
        self._draw_team_slot("SF1W", self.sf["SF1"]["w"], winner=True)
        self._draw_team_slot("SF2W", self.sf["SF2"]["w"], winner=True)

        # ---- Final (campeão) ----
        self._sync_final()

        # Se ainda não tem campeão e ambos finalistas existem,
        # clique no SF1W ou SF2W define campeão
        if self.f["F"]["w"] is None and self.f["F"]["a"] and self.f["F"]["b"]:
            # torna SF1W e SF2W clicáveis para definir o campeão
            self._draw_team_slot("SF1W", self.sf["SF1"]["w"], click=("F", "a"), winner=True)
            self._draw_team_slot("SF2W", self.sf["SF2"]["w"], click=("F", "b"), winner=True)

        # Campeão (desenha só se tiver)
        if self.f["F"]["w"]:
            self._draw_team_slot("FW", self.f["F"]["w"], winner=True, crown=True)
        else:
            # slot vazio do campeão (só placeholder discreto)
            self._draw_team_slot("FW", None, winner=True, crown=True)

    def _draw_team_slot(self, slot_id, team_name, click=None, faint=False, winner=False, crown=False):
        # se o slot não existir (segurança)
        if slot_id not in self.slot:
            return

        x, y = self.slot[slot_id]

        # se não há time, não desenha NADA
        if not team_name:
            return

        img = self.icones.get(team_name)
        if img is None:
            return

        tag = f"{slot_id}_TEAM"
        self.canvas.create_image(x, y, image=img, tags=(tag,))

        # texto de campeão (única coisa extra que fica)
        if crown:
            self.canvas.create_text(
                x,
                y + self.icon_r + 14,
                text="CAMPEÃO",
                fill="#f1c40f",
                font=("Lato", 12, "bold")
            )

        if click:
            self.canvas.tag_bind(
                tag,
                "<Button-1>",
                lambda e, g=click[0], t=team_name: self._pick_winner(g, t)
            )
            self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))


    def _pick_winner(self, game_id, team_name):
        if game_id.startswith("QF"):
            self.qf[game_id]["w"] = team_name
        elif game_id.startswith("SF"):
            self.sf[game_id]["w"] = team_name
        elif game_id == "F":
            self.f["F"]["w"] = team_name
            if self.on_campeao:
                self.on_campeao(team_name)

        self._sync_semis()
        self._sync_final()
        self.redesenhar()

    def _sync_semis(self):
        self.sf["SF1"]["a"] = self.qf["QF1"]["w"]
        self.sf["SF1"]["b"] = self.qf["QF2"]["w"]
        if self.sf["SF1"]["w"] not in (self.sf["SF1"]["a"], self.sf["SF1"]["b"]):
            self.sf["SF1"]["w"] = None

        self.sf["SF2"]["a"] = self.qf["QF3"]["w"]
        self.sf["SF2"]["b"] = self.qf["QF4"]["w"]
        if self.sf["SF2"]["w"] not in (self.sf["SF2"]["a"], self.sf["SF2"]["b"]):
            self.sf["SF2"]["w"] = None

    def _sync_final(self):
        self.f["F"]["a"] = self.sf["SF1"]["w"]
        self.f["F"]["b"] = self.sf["SF2"]["w"]
        if self.f["F"]["w"] not in (self.f["F"]["a"], self.f["F"]["b"]):
            self.f["F"]["w"] = None