class Clube:
    def __init__(self, nome, apelido, vitorias=0, derrotas=0, empates=0, gols_pro=0, gols_contra=0, saldo_gols=0):
        self.nome = nome
        self.apelido = apelido
        self.vitorias = vitorias
        self.derrotas = derrotas
        self.empates = empates
        self.gols_pro = gols_pro
        self.gols_contra = gols_contra
        self.saldo_gols = saldo_gols

    def __str__(self):
        return f"{self.nome} - ({self.apelido})"

def adicionar_clube(nome, apelido):
    clube = Clube(nome, apelido)
    clubes.append(clube)

# Lista global de clubes
clubes = []

if __name__ == "__main__":
    adicionar_clube("Rio Branco", "Capa Preta")
    adicionar_clube("Desportiva", "Diva")
    for clube in clubes:
        print(clube)