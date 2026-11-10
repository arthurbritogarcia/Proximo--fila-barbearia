# Proximo! - Fila virtual para barbearias (versao com janelas)
# Trabalho de Engenharia de Software
#
# Abre duas janelas: o "celular do cliente" e o "celular do barbeiro".
# As duas usam as MESMAS listas, entao o que acontece em uma
# aparece na outra na hora.
#
# Usa o tkinter, que ja vem com o Python.

import tkinter as tk

# ---------------- DADOS (iguais ao proximo.py) ----------------

servicos = [
    {"nome": "Corte", "tempo": 30, "preco": 45},
    {"nome": "Barba", "tempo": 20, "preco": 30},
    {"nome": "Sobrancelha", "tempo": 10, "preco": 15},
    {"nome": "Corte + barba", "tempo": 45, "preco": 70},
    {"nome": "Corte + sobrancelha", "tempo": 35, "preco": 55},
    {"nome": "Corte + barba + sobrancelha", "tempo": 55, "preco": 80},
]

fila = [
    {"nome": "Rafael", "servico": 0, "origem": "app"},
    {"nome": "Seu Antonio", "servico": 1, "origem": "balcao"},
    {"nome": "Lucas", "servico": 5, "origem": "app"},
    {"nome": "Pedro", "servico": 4, "origem": "app"},
]

na_cadeira = {"nome": "Marcos", "servico": 3, "origem": "app"}
atendidos_hoje = 7
faturamento = 385

# nome de quem esta usando o "celular do cliente" ("" = ninguem entrou ainda)
meu_nome = ""

# lista so com os nomes dos servicos, para mostrar nas opcoes
nomes_servicos = []
for s in servicos:
    nomes_servicos.append(s["nome"] + " - R$ " + str(s["preco"]))


# ---------------- FUNCOES DA FILA (iguais ao proximo.py) ----------------

def tempo_de_espera(posicao):
    total = 0
    if na_cadeira != None:
        total = total + servicos[na_cadeira["servico"]]["tempo"]
    for i in range(posicao):
        total = total + servicos[fila[i]["servico"]]["tempo"]
    return total


def procurar_cliente(nome):
    for i in range(len(fila)):
        if fila[i]["nome"].lower() == nome.lower():
            return i
    return -1


def numero_do_servico(texto):
    # recebe o texto escolhido na tela e devolve a posicao do servico
    for i in range(len(nomes_servicos)):
        if nomes_servicos[i] == texto:
            return i
    return 0


# ---------------- ACOES DO CLIENTE ----------------

def entrar_na_fila():
    global meu_nome
    nome = campo_nome_cliente.get()
    if nome == "":
        notificar("Digite seu nome para entrar na fila.")
        return
    if procurar_cliente(nome) != -1:
        notificar("Esse nome ja esta na fila.")
        return
    servico = numero_do_servico(servico_cliente.get())
    fila.append({"nome": nome, "servico": servico, "origem": "app"})
    meu_nome = nome
    campo_nome_cliente.delete(0, tk.END)
    notificar("Voce entrou na fila!")
    atualizar_telas()


def sair_da_fila():
    global meu_nome
    posicao = procurar_cliente(meu_nome)
    if posicao != -1:
        fila.pop(posicao)
        notificar("Voce saiu da fila.")
    meu_nome = ""
    atualizar_telas()


def notificar(texto):
    # mostra a "notificacao" no topo do celular do cliente
    aviso_cliente.config(text=texto)
    # depois de 4 segundos, apaga a notificacao
    janela_cliente.after(4000, apagar_notificacao)


def apagar_notificacao():
    aviso_cliente.config(text="")


# ---------------- ACOES DO BARBEIRO ----------------

def chamar_proximo():
    global na_cadeira, atendidos_hoje, faturamento

    if na_cadeira != None:
        atendidos_hoje = atendidos_hoje + 1
        faturamento = faturamento + servicos[na_cadeira["servico"]]["preco"]

    if len(fila) > 0:
        na_cadeira = fila.pop(0)
    else:
        na_cadeira = None

    # notificacoes para o cliente do celular
    if meu_nome != "":
        posicao = procurar_cliente(meu_nome)
        if na_cadeira != None and na_cadeira["nome"] == meu_nome:
            notificar("E a sua vez! Pode sentar na cadeira.")
        elif posicao == 0:
            notificar("Voce e o proximo! Venha para a barbearia.")
        elif posicao == 1:
            notificar("Faltam 2 pessoas. Ja pode ir saindo.")

    atualizar_telas()


def adicionar_balcao():
    nome = campo_nome_barbeiro.get()
    if nome == "":
        return
    servico = numero_do_servico(servico_barbeiro.get())
    fila.append({"nome": nome, "servico": servico, "origem": "balcao"})
    campo_nome_barbeiro.delete(0, tk.END)
    atualizar_telas()


def remover_selecionado():
    global meu_nome
    selecionado = lista_fila.curselection()
    if len(selecionado) == 0:
        return
    posicao = selecionado[0]
    if fila[posicao]["nome"] == meu_nome:
        meu_nome = ""
    fila.pop(posicao)
    atualizar_telas()


# ---------------- ATUALIZAR AS DUAS TELAS ----------------

def atualizar_telas():
    # ----- celular do barbeiro -----
    texto_resumo = "Na fila: " + str(len(fila))
    texto_resumo = texto_resumo + "   |   Atendidos: " + str(atendidos_hoje)
    texto_resumo = texto_resumo + "   |   Faturado: R$ " + str(faturamento)
    resumo_barbeiro.config(text=texto_resumo)

    if na_cadeira != None:
        cadeira_barbeiro.config(text="Na cadeira: " + na_cadeira["nome"] + " - " + servicos[na_cadeira["servico"]]["nome"])
    else:
        cadeira_barbeiro.config(text="Cadeira livre")

    # apaga a lista e escreve de novo
    lista_fila.delete(0, tk.END)
    for i in range(len(fila)):
        c = fila[i]
        linha = str(i + 1) + "o  " + c["nome"] + "  (" + c["origem"] + ")  -  "
        linha = linha + servicos[c["servico"]]["nome"] + "  -  " + str(tempo_de_espera(i)) + " min"
        lista_fila.insert(tk.END, linha)

    # ----- celular do cliente -----
    info_cliente.config(text="Pessoas na fila: " + str(len(fila)) + "   |   Espera: " + str(tempo_de_espera(len(fila))) + " min")

    posicao = procurar_cliente(meu_nome)

    if meu_nome != "" and na_cadeira != None and na_cadeira["nome"] == meu_nome:
        # chegou a vez: fica verde
        quadro_posicao.config(text="Chegou a sua vez!", bg="#27AE60")
        detalhe_posicao.config(text="Pode sentar na cadeira, " + meu_nome + ".", bg="#27AE60")
    elif posicao != -1:
        texto = str(posicao + 1) + "o da fila"
        espera = "Espera de " + str(tempo_de_espera(posicao)) + " min"
        if posicao <= 1:
            # perto da vez: fica laranja
            quadro_posicao.config(text=texto, bg="#E8A33D")
            detalhe_posicao.config(text=espera + " - ja pode ir!", bg="#E8A33D")
        else:
            quadro_posicao.config(text=texto, bg="#1A1A18")
            detalhe_posicao.config(text=espera, bg="#1A1A18")
    else:
        quadro_posicao.config(text="Voce nao esta na fila", bg="#888888")
        detalhe_posicao.config(text="Digite seu nome e escolha o servico", bg="#888888")


# ================================================================
# JANELA 1: CELULAR DO CLIENTE
# ================================================================

janela_cliente = tk.Tk()
janela_cliente.title("Celular do cliente - Proximo!")
janela_cliente.geometry("380x560+50+50")
janela_cliente.config(bg="white")

aviso_cliente = tk.Label(janela_cliente, text="", bg="#333333", fg="white", font=("Arial", 11, "bold"), height=2)
aviso_cliente.pack(fill="x")

tk.Label(janela_cliente, text="Proximo!", bg="white", fg="#E8A33D", font=("Arial", 22, "bold")).pack(pady=(10, 0))
tk.Label(janela_cliente, text="Barbearia do Ze - aberto das 8h as 18h", bg="white", font=("Arial", 10)).pack()

info_cliente = tk.Label(janela_cliente, text="", bg="white", font=("Arial", 10))
info_cliente.pack(pady=5)

quadro_posicao = tk.Label(janela_cliente, text="", fg="white", font=("Arial", 24, "bold"), height=2)
quadro_posicao.pack(fill="x", padx=15, pady=(10, 0))
detalhe_posicao = tk.Label(janela_cliente, text="", fg="white", font=("Arial", 11))
detalhe_posicao.pack(fill="x", padx=15, pady=(0, 10), ipady=6)

tk.Label(janela_cliente, text="Seu nome:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", padx=15)
campo_nome_cliente = tk.Entry(janela_cliente, font=("Arial", 12))
campo_nome_cliente.pack(fill="x", padx=15)

tk.Label(janela_cliente, text="Servico:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", padx=15, pady=(8, 0))
servico_cliente = tk.StringVar(value=nomes_servicos[0])
tk.OptionMenu(janela_cliente, servico_cliente, *nomes_servicos).pack(fill="x", padx=15)

tk.Button(janela_cliente, text="Entrar na fila", bg="#E8A33D", font=("Arial", 12, "bold"), command=entrar_na_fila).pack(fill="x", padx=15, pady=(12, 4), ipady=6)
tk.Button(janela_cliente, text="Sair da fila", font=("Arial", 11), command=sair_da_fila).pack(fill="x", padx=15, ipady=4)


# ================================================================
# JANELA 2: CELULAR DO BARBEIRO
# ================================================================

janela_barbeiro = tk.Toplevel(janela_cliente)
janela_barbeiro.title("Celular do barbeiro - Proximo! Pro")
janela_barbeiro.geometry("460x560+460+50")
janela_barbeiro.config(bg="#17171A")

tk.Label(janela_barbeiro, text="Painel do barbeiro", bg="#17171A", fg="white", font=("Arial", 18, "bold")).pack(pady=(12, 4))

resumo_barbeiro = tk.Label(janela_barbeiro, text="", bg="#17171A", fg="#E8A33D", font=("Arial", 11, "bold"))
resumo_barbeiro.pack()

cadeira_barbeiro = tk.Label(janela_barbeiro, text="", bg="#1F5B36", fg="white", font=("Arial", 12, "bold"))
cadeira_barbeiro.pack(fill="x", padx=15, pady=10, ipady=8)

tk.Button(janela_barbeiro, text="Finalizar e chamar proximo", bg="#E8A33D", font=("Arial", 12, "bold"), command=chamar_proximo).pack(fill="x", padx=15, ipady=6)

tk.Label(janela_barbeiro, text="Fila:", bg="#17171A", fg="white", font=("Arial", 10, "bold")).pack(anchor="w", padx=15, pady=(10, 0))
lista_fila = tk.Listbox(janela_barbeiro, font=("Arial", 10), height=8)
lista_fila.pack(fill="x", padx=15)
tk.Button(janela_barbeiro, text="Remover selecionado", font=("Arial", 10), command=remover_selecionado).pack(anchor="e", padx=15, pady=4)

tk.Label(janela_barbeiro, text="Cliente que chegou sem app:", bg="#17171A", fg="white", font=("Arial", 10, "bold")).pack(anchor="w", padx=15, pady=(6, 0))
campo_nome_barbeiro = tk.Entry(janela_barbeiro, font=("Arial", 12))
campo_nome_barbeiro.pack(fill="x", padx=15)
servico_barbeiro = tk.StringVar(value=nomes_servicos[0])
tk.OptionMenu(janela_barbeiro, servico_barbeiro, *nomes_servicos).pack(fill="x", padx=15, pady=4)
tk.Button(janela_barbeiro, text="+ Adicionar na fila", font=("Arial", 11), command=adicionar_balcao).pack(fill="x", padx=15, ipady=4)


# ---------------- COMECA O PROGRAMA ----------------
atualizar_telas()
janela_cliente.mainloop()
