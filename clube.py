class Clube:
    def __init__(self, nome, apelido, vitorias=0, empates=0, derrotas=0, gols_pro=0, gols_contra=0):
        self.nome = nome
        self.jogos = vitorias + derrotas + empates
        self.apelido = apelido
        self.vitorias = vitorias
        self.empates = empates
        self.derrotas = derrotas
        self.gols_pro = gols_pro
        self.gols_contra = gols_contra
        self.saldo_gols = gols_pro - gols_contra

    def __str__(self):
        return f"{self.nome} - ({self.apelido})"

if __name__ == "__main__":
    ...