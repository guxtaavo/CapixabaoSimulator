import unicodedata

class Clube:
    def __init__(self, nome, pontos=0, jogos=0, vitorias=0, empates=0,
                 derrotas=0, gols_pro=0, gols_contra=0):
        self.nome = nome
        self.escudo = self.formatar_nome_para_arquivo(nome)
        self.pontos = pontos
        self.jogos = jogos
        self.vitorias = vitorias
        self.empates = empates
        self.derrotas = derrotas
        self.gols_pro = gols_pro
        self.gols_contra = gols_contra

    @staticmethod
    def formatar_nome_para_arquivo(nome: str) -> str:
        """
        Converte o nome do clube em um formato seguro para nome de arquivo:
        - Remove acentos
        - Substitui espaços por "_"
        - Deixa tudo em minúsculas
        - Adiciona extensão ".png"
        """
        # Normaliza e remove acentos (ex: "São Paulo" → "Sao Paulo")
        nome_sem_acentos = ''.join(
            c for c in unicodedata.normalize('NFD', nome)
            if unicodedata.category(c) != 'Mn'
        )
        # Substitui espaços e deixa em minúsculas
        nome_formatado = nome_sem_acentos.lower().replace(' ', '_')
        return f"{nome_formatado}.png"

    @property
    def saldo_gols(self):
        return self.gols_pro - self.gols_contra

    @property
    def aproveitamento(self):
        if self.jogos == 0:
            return 0
        return round((self.pontos / (self.jogos * 3)) * 100)
