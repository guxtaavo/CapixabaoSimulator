class Campeonato:
    def __init__(self):
        self.nome = "Campeonato Capixaba 2026"
        self.times = [
            "Capixaba",
            "Desportiva",
            "Forte",
            "Porto Vitória",
            "Real Noroeste",
            "Rio Branco",
            "Rio Branco VNI",
            "Serra",
            "Vilavelhense",
            "Vitória"
        ]
        self.partidas = []

    def adicionar_time(self, time):
        self.times.append(time)

    def agendar_partida(self, partida):
        self.partidas.append(partida)