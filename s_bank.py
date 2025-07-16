import json
import os

# Caminho do arquivo JSON onde os dados dos usuários serão armazenados
CAMINHO_ARQUIVO = "usuarios.json"

# Variáveis globais de controle e configuração
usuarios = {}  # Dicionário para armazenar usuários na memória (não usado neste trecho)
contas = []    # Lista para armazenar contas (não usada neste trecho)
AGENCIA = "0001"  # Número fixo da agência
conta_logada = None  # Variável para guardar o usuário logado no momento
LIMITE_SAQUE_VALOR = 1000  # Limite máximo permitido por saque

# Função para carregar a lista de usuários do arquivo JSON
def carregar_usuarios():
    # Caso o arquivo não exista, cria um arquivo vazio com lista vazia
    if not os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump([], f)

    # Lê e retorna a lista de usuários armazenada no arquivo JSON
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

# Função para salvar a lista atualizada de usuários no arquivo JSON
def salvar_usuarios(usuarios):
    # Salva os dados com indentação para facilitar leitura manual
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

# Atualiza os dados de um usuário específico na lista armazenada
def atualizar_usuario_atualizado(usuario_atualizado):
    lista_usuarios = carregar_usuarios()

    # Percorre a lista para encontrar o usuário pelo CPF e substituí-lo
    for i, u in enumerate(lista_usuarios):
        if u["cpf"] == usuario_atualizado["cpf"]:
            lista_usuarios[i] = usuario_atualizado
            break

    # Salva a lista atualizada no arquivo JSON
    salvar_usuarios(lista_usuarios)

# Função para criar uma nova conta de usuário
def criar_conta():
    print("\n~~ Criar conta ~~")

    # Solicita dados pessoais e endereço para cadastro
    cpf = input("Digite seu CPF (Apenas números. Sem pontos ou traços): ")
    nome_pessoa = input("Digite seu nome: ")
    logradouro = input("Digite o nome da rua: ")
    num_casa = input("Digite o número da casa: ")
    cep = input("Digite o CEP (Apenas números. Sem pontos ou traços): ")
    uf = input("Digite o UF: ")

    # Solicita criação de senha simples para autenticação
    print("\n~~ Agora crie uma senha ~~")
    senha = input("Crie uma senha com 4 caracteres (Apenas números são permitidos): ")

    # Monta o dicionário do novo usuário com dados e saldo inicial zerado
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

    # Verifica se o CPF já existe para evitar duplicidade de cadastro
    if any(usuario["cpf"] == cpf for usuario in lista_usuarios):
        print("⚠️ CPF já cadastrado!")
        return

    # Adiciona novo usuário à lista e salva no arquivo
    lista_usuarios.append(novo_usuario)
    salvar_usuarios(lista_usuarios)
    print("✅ Conta criada com sucesso!")

# Função para autenticar o usuário pelo CPF e senha
def acessar_conta():
    print(f"""
    ~~ Por favor, entre com o seu CPF e senha ~~
          """)
    cpf = input("Digite seu CPF (Apenas números. Sem pontos ou traços): ")
    senha = input("Digite sua senha: ")

    usuarios = carregar_usuarios()

    # Busca o usuário que tenha CPF e senha correspondentes
    for usuario in usuarios:
        if usuario["cpf"] == cpf and usuario["senha"] == senha:
            print(f"\n✅ Login bem-sucedido! Bem-vindo, {usuario['nome_pessoa']}.")
            return usuario

    # Se não encontrar, retorna None para sinalizar falha
    print("❌ CPF ou senha incorretos.")
    return None

usuario_logado = None

# Loop principal que exibe menus conforme o estado do login
while True:
    if not usuario_logado:
        # Menu inicial para login, cadastro ou sair
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
    
    else:
        # Menu exibido para usuário já logado
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
                # Atualiza saldo e adiciona registro no extrato
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
                # Subtrai valor do saldo e registra no extrato
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

# OPÇÃO DESLOGAR #
        elif opcao_logado == "0":
            print(f"\nDeslogando {usuario_logado['nome_pessoa']}...")
            usuario_logado = None

        else:
            print("❌ Opção inválida.")
