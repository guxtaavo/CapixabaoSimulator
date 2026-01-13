from collections import Counter
# import random

class Campeonato:
    def __init__(self):
        self._nome = "Campeonato Capixaba 2026"
        
        self._times = [        # ID dos times
            "Capixaba",        # 0 
            "Desportiva",      # 1
            "Forte",           # 2
            "Porto Vitória",   # 3
            "Real Noroeste",   # 4
            "Rio Branco",      # 5
            "Rio Branco VNI",  # 6
            "Serra",           # 7
            "Vilavelhense",    # 8
            "Vitória"          # 9
        ]
        
        # random.shuffle(self._times) -> Embaralha os times para gerar de forma
        # aleatória o calendário

        self._rodadas = self._gerar_calendario_oficial()

        self._partidas = [partida for rodada in self._rodadas for partida in rodada]

    # # Enquanto não é definido
    # def _gerar_calendario_random(self):
    #     times = self._times.copy()
    #     num_times = len(times)
    #     num_rodadas = num_times - 1
    #     jogos_por_rodada = num_times // 2
        
    #     rodadas_geradas = []

    #     # Separa o último time para fixá-lo no algoritmo
    #     times_rotativos = times[:-1]
    #     time_fixo = times[-1]

    #     for i in range(num_rodadas):
    #         rodada_atual = []

    #         # O time fixo joga contra o primeiro da lista rotativa
    #         # Alternamos o mando de campo para o time fixo a cada rodada
    #         if i % 2 == 0:
    #             rodada_atual.append([time_fixo, times_rotativos[0]])
    #         else:
    #             rodada_atual.append([times_rotativos[0], time_fixo])

    #         # Monta os outros jogos da rodada
    #         for j in range(1, jogos_por_rodada):
    #             mandante = times_rotativos[j]
    #             visitante = times_rotativos[num_times - 1 - j]
    #             # Para balancear, podemos fixar o mando ou alternar
    #             # Aqui, fixamos o primeiro do par como mandante
    #             rodada_atual.append([mandante, visitante])
            
    #         rodadas_geradas.append(rodada_atual)

    #         # Gira a lista de times (exceto o time fixo)
    #         times_rotativos.insert(1, times_rotativos.pop())

    #     return rodadas_geradas

    def _gerar_calendario_oficial(self):
        times = self._times

        rodadas = [
            # 1ª RODADA
            [
                (times[5], times[7]),  # Rio Branco x Serra
                (times[1], times[6]),  # Desportiva x Rio Branco VNI
                (times[9], times[8]),  # Vitória x Vilavelhense
                (times[3], times[0]),  # Porto Vitória x Capixaba
                (times[4], times[2]),  # Real Noroeste x Forte
            ],
            # 2ª RODADA
            [
                (times[7], times[1]),  # Serra x Desportiva
                (times[9], times[3]),  # Vitória x Porto Vitória
                (times[8], times[5]),  # Vilavelhense x Rio Branco
                (times[6], times[4]),  # Rio Branco VNI x Real Noroeste
                (times[2], times[0]),  # Forte x Capixaba
            ],
            # 3ª RODADA
            [
                (times[1], times[8]),  # Desportiva x Vilavelhense
                (times[3], times[2]),  # Porto Vitória x Forte
                (times[5], times[9]),  # Rio Branco x Vitória
                (times[4], times[7]),  # Real Noroeste x Serra
                (times[0], times[6]),  # Capixaba x Rio Branco VNI
            ],
            # 4ª RODADA
            [
                (times[5], times[3]),  # Rio Branco x Porto Vitória
                (times[9], times[1]),  # Vitória x Desportiva
                (times[6], times[2]),  # Rio Branco VNI x Forte
                (times[7], times[0]),  # Serra x Capixaba
                (times[8], times[4]),  # Vilavelhense x Real Noroeste
            ],
            # 5ª RODADA
            [
                (times[3], times[6]),  # Porto Vitória x Rio Branco VNI
                (times[1], times[5]),  # Desportiva x Rio Branco
                (times[2], times[7]),  # Forte x Serra
                (times[4], times[9]),  # Real Noroeste x Vitória
                (times[0], times[8]),  # Capixaba x Vilavelhense
            ],
            # 6ª RODADA
            [
                (times[1], times[3]),  # Desportiva x Porto Vitória
                (times[7], times[6]),  # Serra x Rio Branco VNI
                (times[5], times[4]),  # Rio Branco x Real Noroeste
                (times[8], times[2]),  # Vilavelhense x Forte
                (times[9], times[0]),  # Vitória x Capixaba
            ],
            # 7ª RODADA
            [
                (times[3], times[7]),  # Porto Vitória x Serra
                (times[4], times[1]),  # Real Noroeste x Desportiva
                (times[6], times[8]),  # Rio Branco VNI x Vilavelhense
                (times[0], times[5]),  # Capixaba x Rio Branco
                (times[2], times[9]),  # Forte x Vitória
            ],
            # 8ª RODADA
            [
                (times[4], times[3]),  # Real Noroeste x Porto Vitória
                (times[8], times[7]),  # Vilavelhense x Serra
                (times[1], times[0]),  # Desportiva x Capixaba
                (times[9], times[6]),  # Vitória x Rio Branco VNI
                (times[5], times[2]),  # Rio Branco x Forte
            ],
            # 9ª RODADA
            [
                (times[3], times[8]),  # Porto Vitória x Vilavelhense
                (times[0], times[4]),  # Capixaba x Real Noroeste
                (times[7], times[9]),  # Serra x Vitória
                (times[2], times[1]),  # Forte x Desportiva
                (times[6], times[5]),  # Rio Branco VNI x Rio Branco
            ],
        ]
        return rodadas

if __name__ == "__main__":
    campeonato = Campeonato()

    print(f"{campeonato._nome}\n")
    print("Times Participantes:")
    for time in sorted(campeonato._times):
        print(f"- {time}")

    print("\nRodadas Geradas:")
    for i, rodada in enumerate(campeonato._rodadas, start=1):
        print(f"\nRodada {i}:")
        for partida in rodada:
            print(f"   {partida[0]} x {partida[1]}")

    mandos = Counter([p[0] for p in campeonato._partidas])

    print("\n📊 Jogos em casa por time (Calendário Corrigido e Balanceado):")
    for time in sorted(campeonato._times):
        print(f"   {time}: {mandos[time]}")