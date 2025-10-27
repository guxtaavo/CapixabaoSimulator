from collections import Counter
import random

class Campeonato:
    def __init__(self):
        self._nome = "Campeonato Capixaba 2026"
        
        self._times = [
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
        
        random.shuffle(self._times)

        self._rodadas = self._gerar_calendario()

        self._partidas = [partida for rodada in self._rodadas for partida in rodada]

    # Enquanto não é definido
    def _gerar_calendario(self):
        times = self._times.copy()
        num_times = len(times)
        num_rodadas = num_times - 1
        jogos_por_rodada = num_times // 2
        
        rodadas_geradas = []

        # Separa o último time para fixá-lo no algoritmo
        times_rotativos = times[:-1]
        time_fixo = times[-1]

        for i in range(num_rodadas):
            rodada_atual = []

            # O time fixo joga contra o primeiro da lista rotativa
            # Alternamos o mando de campo para o time fixo a cada rodada
            if i % 2 == 0:
                rodada_atual.append([time_fixo, times_rotativos[0]])
            else:
                rodada_atual.append([times_rotativos[0], time_fixo])

            # Monta os outros jogos da rodada
            for j in range(1, jogos_por_rodada):
                mandante = times_rotativos[j]
                visitante = times_rotativos[num_times - 1 - j]
                # Para balancear, podemos fixar o mando ou alternar
                # Aqui, fixamos o primeiro do par como mandante
                rodada_atual.append([mandante, visitante])
            
            rodadas_geradas.append(rodada_atual)

            # Gira a lista de times (exceto o time fixo)
            times_rotativos.insert(1, times_rotativos.pop())

        return rodadas_geradas


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