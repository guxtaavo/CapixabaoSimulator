class Clube:
    def __init__(self, nome, vitorias=0, empates=0, derrotas=0, gols_pro=0, gols_contra=0):
        self.nome = nome
        self.jogos = vitorias + derrotas + empates
        self.vitorias = vitorias
        self.empates = empates
        self.derrotas = derrotas
        self.gols_pro = gols_pro
        self.gols_contra = gols_contra
        self.saldo_gols = gols_pro - gols_contra
        self.pontos = vitorias * 3 + empates
        self.aproveitamento = self.calcular_aproveitamento()

    def calcular_aproveitamento(self):
        if self.jogos == 0:
            return 0
        return round((self.pontos / (self.jogos * 3)) * 100)

    @classmethod
    def from_db_row(cls, row):
        nome = row[2]
        vitorias = row[4]
        empates = row[5]
        derrotas = row[6]
        gols_pro = row[7]
        gols_contra = row[8]
        return cls(nome, vitorias, empates, derrotas, gols_pro, gols_contra)

    def __str__(self):
        return (f"{self.nome} - Pontos: {self.pontos}, Jogos: {self.jogos}, Vitórias: {self.vitorias}, "
                f"Empates: {self.empates}, Derrotas: {self.derrotas}, Gols Pró: {self.gols_pro}, "
                f"Gols Contra: {self.gols_contra}, Saldo de Gols: {self.saldo_gols}, Aproveitamento: {self.aproveitamento}%")

if __name__ == "__main__":
    # Exemplo de uso
    row = [1, 1, "Rio Branco SAF", 10, 5, 3, 2, 20, 10]
    clube = Clube.from_db_row(row)
    print(clube)