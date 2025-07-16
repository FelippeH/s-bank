import json
import os

CAMINHO_ARQUIVO = "usuarios.json"

usuarios = {}
contas = []
AGENCIA = "0001"
conta_logada = None
LIMITE_SAQUE_VALOR = 1000

# DADOS ARMAZENADOS #
def carregar_usuarios():
    if not os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
        
def atualizar_usuario_atualizado(usuario_atualizado):
    lista_usuarios = carregar_usuarios()

    for i, u in enumerate(lista_usuarios):
        if u["cpf"] == usuario_atualizado["cpf"]:
            lista_usuarios[i] = usuario_atualizado
            break

    salvar_usuarios(lista_usuarios)

# CRIAR CONTA #
def criar_conta():
    print("\n~~ Criar conta ~~")

    cpf = input("Digite seu CPF (Apenas números. Sem pontos ou traços): ")
    nome_pessoa = input("Digite seu nome: ")
    logradouro = input("Digite o nome da rua: ")
    num_casa = input("Digite o número da casa: ")
    cep = input("Digite o CEP (Apenas números. Sem pontos ou traços): ")
    uf = input("Digite o UF: ")

    print("\n~~ Agora crie uma senha ~~")
    senha = input("Crie uma senha com 4 caracteres (Apenas números são permitidos): ")

    novo_usuario = {
        "cpf": cpf,
        "nome_pessoa": nome_pessoa,
        "endereco": {
            "logradouro": logradouro,
            "num_casa": num_casa,
            "cep": cep,
            "uf": uf
        },
        "senha": senha,
        "saldo": 0.0,
        "extrato": []
    }

    lista_usuarios = carregar_usuarios()

    if any(usuario["cpf"] == cpf for usuario in lista_usuarios):
        print("⚠️ CPF já cadastrado!")
        return

    lista_usuarios.append(novo_usuario)
    salvar_usuarios(lista_usuarios)
    print("✅ Conta criada com sucesso!")

# ACESSAR CONTA #
def acessar_conta():
    print(f"""
    ~~ Por favor, entre com o seu CPF e senha ~~
          """)
    cpf = input("Digite seu CPF (Apenas números. Sem pontos ou traços): ")
    senha = input("Digite sua senha: ")

    usuarios = carregar_usuarios()

    for usuario in usuarios:
        if usuario["cpf"] == cpf and usuario["senha"] == senha:
            print(f"\n✅ Login bem-sucedido! Bem-vindo, {usuario['nome_pessoa']}.")
            return usuario

    print("❌ CPF ou senha incorretos.")
    return None

usuario_logado = None

# MENU PRINCIPAL #
while True:
    if not usuario_logado:
        menu = """
    ~~ Seja Bem-vindo ao S-Bank ~~
    [1] Acessar conta
    [2] Criar conta
    [0] Sair
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    => """
        opcao = input(menu)

        if opcao == "1":
            usuario_logado = acessar_conta()

        elif opcao == "2":
            criar_conta()

        elif opcao == "0":
            print("\nEncerrando o sistema...")
            break

        else:
            print("❌ Opção inválida.")
    
# MENU LOGADO #
    else:
        menu_logado = f"""
    ~~ Olá {usuario_logado['nome_pessoa']}! Selecione uma opção: ~~
    Saldo atual: R$ {usuario_logado['saldo']:.2f}
    [1] Depósito
    [2] Saque
    [3] Extrato
    [0] Voltar
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    => """
    
        opcao_logado = input(menu_logado)

# OPÇÃO DEPÓSITO #
        if opcao_logado == "1":
            valor = float(input("Valor do depósito: R$ "))
            if valor <= 0:
                print("❌ Valor inválido.")
            else:
                usuario_logado["saldo"] += valor
                usuario_logado["extrato"].append(f"Depósito: +R$ {valor:.2f}")
                atualizar_usuario_atualizado(usuario_logado)
                print(f"✅ Depósito de R$ {valor:.2f} realizado.")

# OPÇÃO SAQUE #
        elif opcao_logado == "2":
            valor = float(input("Valor do saque: R$ "))
            if valor <= 0:
                print("❌ Valor inválido.")
            elif valor > usuario_logado["saldo"]:
                print("❌ Saldo insuficiente.")
            elif valor > LIMITE_SAQUE_VALOR:
                print(f"❌ O valor máximo por saque é de R${LIMITE_SAQUE_VALOR:.2f}.")
                print(f"Saques acima desse valor, favor, dirigir à agência.")
            else:
                usuario_logado["saldo"] -= valor
                usuario_logado["extrato"].append(f"Saque: -R$ {valor:.2f}")
                atualizar_usuario_atualizado(usuario_logado)
                print(f"✅ Saque de R$ {valor:.2f} realizado.")

# OPÇÃO EXTRATO #
        elif opcao_logado == "3":
            print("\n📜 Extrato:")
            if not usuario_logado["extrato"]:
                print("Nenhuma movimentação.")
            else:
                for item in usuario_logado["extrato"]:
                    print(item)
            print(f"Saldo atual: R$ {usuario_logado['saldo']:.2f}")

        elif opcao_logado == "0":
            print(f"\nDeslogando {usuario_logado['nome_pessoa']}...")
            usuario_logado = None

        else:
            print("❌ Opção inválida.")