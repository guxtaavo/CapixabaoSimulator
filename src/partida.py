class Partida:
    def __init__(self, time_casa, time_fora):
        self.time_casa = time_casa
        self.time_fora = time_fora
        self._gols_casa = 0
        self._gols_fora = 0

    def registrar_placar(self, gols_casa, gols_fora):
        self._gols_casa = gols_casa
        self._gols_fora = gols_fora