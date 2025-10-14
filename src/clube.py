# src/clube.py

class Clube:
    def __init__(self, nome, pontos=0, jogos=0, vitorias=0, empates=0, derrotas=0, gols_pro=0, gols_contra=0):
        self.nome = nome
        self.pontos = pontos
        self.jogos = jogos
        self.vitorias = vitorias
        self.empates = empates
        self.derrotas = derrotas
        self.gols_pro = gols_pro
        self.gols_contra = gols_contra

    @property
    def saldo_gols(self):
        return self.gols_pro - self.gols_contra

    @property
    def aproveitamento(self):
        if self.jogos == 0:
            return 0
        return round((self.pontos / (self.jogos * 3)) * 100)