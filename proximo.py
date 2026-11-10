# Próximo! - Fila virtual para barbearias
# Trabalho de Engenharia de Software
#
# O programa simula o sistema de fila da Barbearia do Ze.
# Tem a parte do cliente (entrar na fila, ver posicao, sair)
# e a parte do barbeiro (chamar o proximo, adicionar cliente do balcao).

# Lista de servicos: nome, tempo em minutos e preco
servicos = [
    {"nome": "Corte", "tempo": 30, "preco": 45},
    {"nome": "Barba", "tempo": 20, "preco": 30},
    {"nome": "Sobrancelha", "tempo": 10, "preco": 15},
    {"nome": "Corte + barba", "tempo": 45, "preco": 70},
    {"nome": "Corte + sobrancelha", "tempo": 35, "preco": 55},
    {"nome": "Corte + barba + sobrancelha", "tempo": 55, "preco": 80},
]

# A fila comeca com alguns clientes de exemplo
fila = [
    {"nome": "Rafael", "servico": 0, "origem": "app"},
    {"nome": "Seu Antonio", "servico": 1, "origem": "balcao"},
    {"nome": "Lucas", "servico": 5, "origem": "app"},
    {"nome": "Pedro", "servico": 4, "origem": "app"},
]

# Cliente que esta sendo atendido agora (None = cadeira livre)
na_cadeira = {"nome": "Marcos", "servico": 3, "origem": "app"}

atendidos_hoje = 7
faturamento = 385


def mostrar_servicos():
    print("\nServicos:")
    for i in range(len(servicos)):
        s = servicos[i]
        print(i + 1, "-", s["nome"], "| R$", s["preco"], "|", s["tempo"], "min")


def escolher_servico():
    mostrar_servicos()
    opcao = input("Escolha o numero do servico: ")
    if opcao.isdigit() and 1 <= int(opcao) <= len(servicos):
        return int(opcao) - 1
    print("Opcao invalida, vou colocar Corte.")
    return 0


def tempo_de_espera(posicao):
    # soma o tempo de quem esta na cadeira + todo mundo na frente
    total = 0
    if na_cadeira != None:
        total = total + servicos[na_cadeira["servico"]]["tempo"]
    for i in range(posicao):
        total = total + servicos[fila[i]["servico"]]["tempo"]
    return total


def mostrar_fila():
    print("\n===== FILA =====")
    if na_cadeira != None:
        print("Na cadeira:", na_cadeira["nome"], "-", servicos[na_cadeira["servico"]]["nome"])
    else:
        print("Cadeira livre")

    if len(fila) == 0:
        print("Ninguem na fila.")
    for i in range(len(fila)):
        c = fila[i]
        print(str(i + 1) + "o", c["nome"], "-", servicos[c["servico"]]["nome"],
              "(" + c["origem"] + ")", "- espera de", tempo_de_espera(i), "min")


def procurar_cliente(nome):
    # devolve a posicao do cliente na fila, ou -1 se nao achar
    for i in range(len(fila)):
        if fila[i]["nome"].lower() == nome.lower():
            return i
    return -1


# ---------------- MENU DO CLIENTE ----------------
def menu_cliente():
    while True:
        print("\n--- APP DO CLIENTE ---")
        print("Barbearia do Ze - aberto das 8h as 18h")
        print("Pessoas na fila:", len(fila))
        print("1 - Entrar na fila")
        print("2 - Ver minha posicao")
        print("3 - Sair da fila")
        print("0 - Voltar")
        opcao = input("Opcao: ")

        if opcao == "1":
            nome = input("Seu nome: ")
            if nome == "":
                print("Precisa digitar um nome!")
            elif procurar_cliente(nome) != -1:
                print("Voce ja esta na fila!")
            else:
                servico = escolher_servico()
                fila.append({"nome": nome, "servico": servico, "origem": "app"})
                posicao = len(fila)
                print("\nPronto,", nome + "! Voce e o", str(posicao) + "o da fila.")
                print("Espera de mais ou menos", tempo_de_espera(posicao - 1), "minutos.")
                print("Valor: R$", servicos[servico]["preco"])

        elif opcao == "2":
            nome = input("Seu nome: ")
            posicao = procurar_cliente(nome)
            if posicao == -1:
                print("Voce nao esta na fila.")
            else:
                print("Voce e o", str(posicao + 1) + "o da fila.")
                print("Espera de mais ou menos", tempo_de_espera(posicao), "minutos.")
                if posicao <= 1:
                    print(">> Ja pode ir para a barbearia!")

        elif opcao == "3":
            nome = input("Seu nome: ")
            posicao = procurar_cliente(nome)
            if posicao == -1:
                print("Voce nao esta na fila.")
            else:
                fila.pop(posicao)
                print("Voce saiu da fila.")

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")


# ---------------- MENU DO BARBEIRO ----------------
def menu_barbeiro():
    global na_cadeira, atendidos_hoje, faturamento

    while True:
        print("\n--- APP DO BARBEIRO ---")
        print("Na fila:", len(fila), "| Atendidos hoje:", atendidos_hoje, "| Faturado: R$", faturamento)
        print("1 - Ver fila")
        print("2 - Finalizar e chamar proximo")
        print("3 - Adicionar cliente do balcao (sem app)")
        print("4 - Remover cliente da fila")
        print("0 - Voltar")
        opcao = input("Opcao: ")

        if opcao == "1":
            mostrar_fila()

        elif opcao == "2":
            # termina o atendimento de quem esta na cadeira
            if na_cadeira != None:
                atendidos_hoje = atendidos_hoje + 1
                faturamento = faturamento + servicos[na_cadeira["servico"]]["preco"]
                print("Atendimento de", na_cadeira["nome"], "finalizado.")

            # chama o primeiro da fila
            if len(fila) > 0:
                na_cadeira = fila.pop(0)
                print("Chamando", na_cadeira["nome"] + "!")
                print("[Notificacao para", na_cadeira["nome"] + ": E a sua vez!]")
                # avisa quem esta chegando perto
                if len(fila) >= 1:
                    print("[Notificacao para", fila[0]["nome"] + ": Voce e o proximo!]")
                if len(fila) >= 2:
                    print("[Notificacao para", fila[1]["nome"] + ": Faltam 2 pessoas]")
            else:
                na_cadeira = None
                print("A fila esta vazia.")

        elif opcao == "3":
            nome = input("Nome do cliente: ")
            if nome == "":
                print("Precisa digitar um nome!")
            else:
                servico = escolher_servico()
                fila.append({"nome": nome, "servico": servico, "origem": "balcao"})
                print(nome, "foi adicionado no fim da fila.")

        elif opcao == "4":
            mostrar_fila()
            nome = input("Nome de quem vai sair: ")
            posicao = procurar_cliente(nome)
            if posicao == -1:
                print("Cliente nao encontrado.")
            else:
                fila.pop(posicao)
                print(nome, "foi removido.")

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")


# ---------------- PROGRAMA PRINCIPAL ----------------
print("==============================")
print("   Próximo! - Barbearia do Ze")
print("==============================")

while True:
    print("\nQuem esta usando?")
    print("1 - Cliente")
    print("2 - Barbeiro")
    print("0 - Sair")
    opcao = input("Opcao: ")

    if opcao == "1":
        menu_cliente()
    elif opcao == "2":
        menu_barbeiro()
    elif opcao == "0":
        print("Ate mais!")
        break
    else:
        print("Opcao invalida.")
