import json
import cutie
from datetime import datetime
import os

def is_date_string(value):
    try:
        datetime.strptime(value, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def custom_deserializer(obj):
    for key, value in obj.items():
        if isinstance(value, str) and is_date_string(value):
            try:
                # Tentar converter a string para um objeto datetime
                obj[key] = datetime.strptime(value, "%d/%m/%Y")
            except ValueError:
                # Se não for possível converter, manter o valor original
                pass
    return obj

def load_data(filename):
    try:
        # Obtenha o diretório atual do script
        diretorio_atual = os.path.dirname(__file__)
        # Combine o caminho do diretório com o nome do arquivo desejado
        caminho_arquivo = os.path.join(diretorio_atual, filename)
        with open(caminho_arquivo, "r") as f:
            data = json.load(f, object_hook=custom_deserializer)
        return data
    except FileNotFoundError:
        # Se o arquivo não existe, retorna uma lista vazia
        return []
    except Exception as e:
        print(f"\nErro ao carregar dados do arquivo {filename}:", str(e))
        return []

listAutomovel = load_data("listautomovel.json")
listCliente = load_data("listcliente.json")
listBooking = load_data("listbooking.json")
###    *********************************** ################  

def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%d/%m/%Y")
    return obj

def save_data(filename, data):
    try:
        # Obtenha o diretório atual do script
        diretorio_atual = os.path.dirname(__file__)
        # Combine o caminho do diretório com o nome do arquivo desejado
        caminho_arquivo = os.path.join(diretorio_atual, filename)
        # Salva os dados no arquivo na mesma pasta do script
        with open(caminho_arquivo, "w") as f:
            json.dump(data, f, default=custom_serializer, indent=4)
    except Exception as e:
        print(f"\nErro ao salvar dados em {filename}: {e}")

def save_all_data():
    save_data("listautomovel.json", listAutomovel)
    save_data("listcliente.json", listCliente)
    save_data("listbooking.json", listBooking)

def adicionar_automovel():
    print("\nAdicionar Automóvel:")
    matricula = input("Matrícula: ")
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    cor = input("Cor: ")
    portas = int(input("Número de Portas: "))
    preco_diario = float(input("Preço Diário: "))
    cilindrada = int(input("Cilindrada: "))
    potencia = int(input("Potência: "))

    novo_automovel = {
    'id': len(listAutomovel) + 1,
    'matricula': matricula,
    'marca': marca,
    'modelo': modelo,
    'cor': cor,
    'portas': portas,
    'precoDiario': preco_diario,
    'cilindrada': cilindrada,
    'potencia': potencia
}
    listAutomovel.append(novo_automovel)
    save_data("listautomovel.json", listAutomovel)
    print("Novo automóvel adicionado com sucesso!")

def calcular_preco(numero_dias):
    preco = float(input("Preço Reserva: "))
    if(numero_dias <= 4):
        return preco
    elif(numero_dias > 4 and numero_dias <= 8):
        print("Desconto de 15% aplicado")
        return preco - (preco * 15 / 100)
    elif(numero_dias > 8):
        print("Desconto de 25% aplicado")
        return preco - (preco * 25 / 100)

def adicionar_reserva():
    print("\nAdicionar Reserva:")
    cliente_id = int(input("ID do cliente: "))
    automovel_id = int(input("ID do automóvel: "))
    while True:
        try:
            # Solicitar datas como strings
            data_inicio_str = input("Data de Início (dd/mm/yyyy): ")
            data_fim_str = input("Data de Fim (dd/mm/yyyy): ")
            # Converter strings de data para objetos datetime
            data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")
            data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")
            break  # Se a conversão for bem-sucedida, sai do loop
        except ValueError:
            print("Formato de data incorreto. Por favor, insira a data no formato dd/mm/yyyy (utilize a /).")
    numeroDias = (data_fim - data_inicio).days
    precoReserva = calcular_preco(numeroDias)
    nova_reserva = {
        'id': len(listBooking) + 1,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'cliente_id': cliente_id,
        'automovel_id': automovel_id,
        'precoReserva': precoReserva,
        'numeroDias': numeroDias
    }
    listBooking.append(nova_reserva)
    save_data("listbooking.json", listBooking)
    print("Reserva efetuada com sucesso!")
    print(f"Preço a pagar: {precoReserva}")

def cliente_existe(telefone, email):
    for cliente in listCliente:
        if cliente['telefone'] == telefone or cliente['email'] == email:
            return True
    return False

def adicionar_cliente():
    print("Entra com os dados do Cliente:")
    nome = input("Nome: ")
    nif = int(input("NIF: "))
    while True:
        try:
            # Solicitar a data de nascimento como string
            data_nascimento_str = input("Data de Nascimento (dd/mm/yyyy): ")
            # Converter a string de data para um objeto datetime
            data_nascimento = datetime.strptime(data_nascimento_str, "%d/%m/%Y")
            break  # Se a conversão for bem-sucedida, sai do loop
        except ValueError:
            print("Formato de data incorreto. Por favor, insira a data no formato dd/mm/yyyy (utilize a /).")
    telefone = int(input("Telefone: "))
    email = input("Email: ")
    if cliente_existe(telefone, email):
        print("Telefone ou email já existem na lista. Não é possível adicionar cliente.")
        return
    
    novo_cliente = {
        'id': len(listCliente) + 1,
        'nome': nome,
        'nif': nif,
        'dataNascimento': data_nascimento,
        'telefone': telefone,
        'email': email
    }
    listCliente.append(novo_cliente)
    save_data("listcliente.json", listCliente)
    print("Novo cliente adicionado com sucesso!")

def removerCliente(): 
    id = int(input("Digite o id do cliente a ser removido: "))
    cliente_encontrado = False
    for pessoa in listCliente: 
        if pessoa['id'] == id: 
            listCliente.remove(pessoa) 
            print(f"Cliente {id} removido com sucesso!") 
            cliente_encontrado = True
            break  # Uma vez que o cliente foi encontrado e removido, podemos sair do loop
    if not cliente_encontrado: 
        print(f"Cliente {id} não encontrado na lista.")

def removerAutomovel(): 
    id = int(input("Digite o id do automóvel a ser removido: "))
    automovel_encontrado = False
    for automovel in listAutomovel: 
        if automovel['id'] == id: 
            listAutomovel.remove(automovel) 
            print(f"Automóvel {id} removido com sucesso!") 
            automovel_encontrado = True
            break  # Uma vez que o automóvel foi encontrado e removido, podemos sair do loop
    if not automovel_encontrado: 
        print(f"Automóvel {id} não encontrado na lista.")

def removerReserva(): 
    id = int(input("Digite o id da reserva a ser removida: "))
    reserva_encontrada = False
    for reserva in listBooking: 
        if reserva['id'] == id: 
            listBooking.remove(reserva) 
            print(f"Reserva {id} removida com sucesso!") 
            reserva_encontrada = True
            break  # Uma vez que a reserva foi encontrada e removida, podemos sair do loop
    if not reserva_encontrada: 
        print(f"Reserva {id} não encontrada na lista.")

def listar_automoveis():
    print("\nLista de Automóveis:")
    for automovel in listAutomovel:
        print("\n=== Dados do Automóvel ===")
        print(f"ID: {automovel['id']}")
        print(f"Matrícula: {automovel['matricula']}")
        print(f"Marca: {automovel['marca']}")
        print(f"Modelo: {automovel['modelo']}")
        print(f"Cor: {automovel['cor']}")
        print(f"Número de Portas: {automovel['portas']}")
        print(f"Preço Diário: {automovel['precoDiario']}")
        print(f"Cilindrada: {automovel['cilindrada']}")
        print(f"Potência: {automovel['potencia']}")
        print("============================")


def listar_clientes():
    print("\nLista de Clientes:")
    for cliente in listCliente:
        print("\n=== Dados do Cliente ===")
        print(f"ID: {cliente['id']}")
        print(f"Nome: {cliente['nome']}")
        print(f"NIF: {cliente['nif']}")
        print(f"Data de Nascimento: {cliente['dataNascimento'].strftime('%d/%m/%Y')}")
        print(f"Telefone: {cliente['telefone']}")
        print(f"Email: {cliente['email']}")
        print("=========================")


def listar_reservas():
    print("\nLista de Reservas:")
    for reserva in listBooking:
        print("\n=== Dados da Reserva ===")
        print(f"ID: {reserva['id']}")
        print(f"Data de Início: {reserva['data_inicio'].strftime('%d/%m/%Y')}")
        print(f"Data de Fim: {reserva['data_fim'].strftime('%d/%m/%Y')}")
        print(f"Cliente ID: {reserva['cliente_id']}")
        print(f"Automóvel ID: {reserva['automovel_id']}")
        print(f"Preço Reserva: {reserva['precoReserva']}")
        print(f"Número de Dias: {reserva['numeroDias']}")
        print("==========================")


def obter_nova_data_nascimento():
    while True:
        try:
            nova_data_nascimento_str = input("Nova data de nascimento (dd/mm/yyyy): ")
            if nova_data_nascimento_str:
                return datetime.strptime(nova_data_nascimento_str, "%d/%m/%Y")
            else:
                return None
        except ValueError:
            print("Formato de data incorreto. Por favor, insira a data no formato dd/mm/yyyy (utilize a /).")

def atualizar_cliente():
    print("\nAtualizar Cliente:")
    if not listCliente:  # Verifica se a lista está vazia
        print("Não há clientes")
        return
    cliente_id = int(input("ID do cliente a ser atualizado: "))
    print("Escolha o dado que deseja atualizar:")
    options = [
        "Nome",
        "Nif",
        "Data de Nascimento",
        "Telefone",
        "Email",
        "Cancelar"
    ]
    selected_option = cutie.select(options)
    cliente_encontrado = False
    for pessoa in listCliente: 
        if pessoa['id'] == cliente_id:
            cliente_encontrado = True
            if selected_option == 0:
                pessoa['nome'] = input("Novo nome: ")
            elif selected_option == 1:
                pessoa['nif'] = input("Novo nif: ") 
            elif selected_option == 2:
                pessoa['data_nascimento'] = obter_nova_data_nascimento()
            elif selected_option == 3:
                novo_telefone = int(input("Novo telefone: "))
                if cliente_existe(novo_telefone, None):
                    print("Telefone já está associado a outro cliente. Não é possível atualizar.")
                else:
                    pessoa['telefone'] = novo_telefone
            elif selected_option == 4:
                novo_email = input("Novo email: ")
                if cliente_existe(None, novo_email):
                    print("Email já está associado a outro cliente. Não é possível atualizar.")
                else:
                    pessoa['email'] = novo_email
            else:
                print("Pedido cancelado!")
    if not cliente_encontrado:
        print(f"Cliente {cliente_id} não encontrado.")

def atualizar_automovel():
    print("\nAtualizar Automóvel:")
    if not listAutomovel:  # Verifica se a lista está vazia
        print("Não há automóveis")
        return
    automovel_id = int(input("ID do automóvel a ser atualizado: "))
    print("Escolha o dado que deseja atualizar:")
    options = [
        "Matrícula",
        "Marca",
        "Modelo",
        "Cor",
        "Número de Portas",
        "Preço Diário",
        "Cilindrada",
        "Potência",
        "Cancelar"
    ]
    selected_option = cutie.select(options)
    automovel_encontrado = False
    for automovel in listAutomovel: 
        if automovel['id'] == automovel_id:
            automovel_encontrado = True
            if selected_option == 0:
                automovel['matricula'] = input("Nova matrícula: ")
            elif selected_option == 1:
                automovel['marca'] = input("Nova marca: ") 
            elif selected_option == 2:
                automovel['modelo'] = input("Novo modelo: ")
            elif selected_option == 3:
                automovel['cor'] = input("Nova cor: ")
            elif selected_option == 4:
                automovel['portas'] = int(input("Novo número de portas: ")) 
            elif selected_option == 5:
                automovel['precoDiario'] = float(input("Novo preço diário: "))
            elif selected_option == 6:
                automovel['cilindrada'] = int(input("Nova Cilindrada: "))
            elif selected_option == 7:
                automovel['potencia'] = int(input("Nova Potência: ")) 
            else:
                print("Pedido cancelado!")
    if not automovel_encontrado:
        print(f"Automóvel {automovel_id} não encontrado.")

def obter_nova_data_inicio():
    while True:
        try:
            nova_data_inicio_str = input("Nova Data de Início (dd/mm/yyyy): ")
            return datetime.strptime(nova_data_inicio_str, "%d/%m/%Y")
        except ValueError:
            print("Formato de data incorreto. Por favor, insira a data no formato dd/mm/yyyy.")

def obter_nova_data_fim():
    while True:
        try:
            nova_data_fim_str = input("Nova Data de Fim (dd/mm/yyyy): ")
            return datetime.strptime(nova_data_fim_str, "%d/%m/%Y")
        except ValueError:
            print("Formato de data incorreto. Por favor, insira a data no formato dd/mm/yyyy.")

def atualizar_reserva():
    print("\nAtualizar Reserva:")
    if not listBooking:  # Verifica se a lista está vazia
        print("Não há reservas")
        return
    reserva_id = int(input("ID da reserva a ser atualizada: "))
    print("Escolha o dado que deseja atualizar:")
    options = [
        "Data de Início",
        "Data de Fim",
        "Cliente ID",
        "Automóvel ID",
        "Preço Reserva",
        "Cancelar"
    ]
    selected_option = cutie.select(options)
    reserva_encontrada = False
    for reserva in listBooking:
        if reserva['id'] == reserva_id:
            reserva_encontrada = True
            if selected_option == 0:
                reserva['data_inicio'] = obter_nova_data_inicio()
                reserva['numeroDias'] = (reserva['data_fim'] - reserva['data_inicio']).days
            elif selected_option == 1:
                reserva['data_fim'] = obter_nova_data_fim()
                reserva['numeroDias'] = (reserva['data_fim'] - reserva['data_inicio']).days
            elif selected_option == 2:
                reserva['cliente_id'] = int(input("Novo Cliente ID: "))
            elif selected_option == 3:
                reserva['automovel_id'] = int(input("Novo Automóvel ID: "))
            elif selected_option == 4:
                reserva['precoReserva'] = calcular_preco(reserva['numeroDias'])
            elif selected_option == 5:
                print("Pedido cancelado!")
    if not reserva_encontrada:
        print(f"Reserva {reserva_id} não encontrada.")

def pesquisar_cliente():
    nif = input("Inserir NIF do cliente para pesquisa: ")
    flag = 0
    for cliente in listCliente:
        if cliente['nif'] == nif:
            flag = 1
            id_cliente = cliente['id']
            print(f"\n=== Dados Cliente {cliente['nome']}: ===")
            for chave, valor in cliente.items():
                print(f"{chave}: {valor}")
            print(f"=============================")
            break
    if(flag == 0):
        print("Cliente não encontrado.")
        return
    i = 1
    for cliente in listBooking:
        if cliente['cliente_id'] == id_cliente:
            print(f"\n=== Cliente {id_cliente} - Booking {i}: ===")
            for chave, valor in cliente.items():
                print(f"{chave}: {valor}")
            print(f"=============================")
            i += 1
            if i == 6:
                break

def pesquisar_automovel():
    matricula = input("Inserir matrícula do cliente para pesquisa: ")
    flag = 0
    for automovel in listAutomovel:
        if automovel['matricula'] == matricula:
            flag = 1
            id_automovel = automovel['id']
            print(f"\n=== Dados Automóvel {matricula}: ===")
            for chave, valor in automovel.items():
                print(f"{chave}: {valor}")
            print(f"=============================")
            break
    if(flag == 0):
        print("Automóvel não encontrado.")
        return
    i = 1
    for automovel in listBooking:
        if automovel['automovel_id'] == id_automovel:
            print(f"\n=== Automóvel {id_automovel} - Booking {i}: ===")
            for chave, valor in automovel.items():
                print(f"{chave}: {valor}")
            print(f"=============================")
            i += 1
            if i == 6:
                break
def achar_nome(id_cliente):
   for cliente in listCliente:
        if cliente['id'] == id_cliente:
            return cliente['nome']
        
def achar_automovel(id_automovel):
   for automovel in listAutomovel:
        if automovel['id'] == id_automovel:
            return automovel['matricula'],automovel['marca']

def listar_reservas_futuras():
    print("\nReservas Futuras:")
    hoje = datetime.now()
    flag = 0
    for booking in listBooking:
        if booking['data_fim'] > hoje:
            flag = 1
            data_inicio_str = booking['data_inicio'].strftime('%d/%m/%Y')
            data_fim_str = booking['data_fim'].strftime('%d/%m/%Y')
            nome = achar_nome(booking['cliente_id'])
            matricula, marca = achar_automovel(booking['automovel_id'])
            print(f"\n=== Detalhes Reserva ID {booking['id']} ===")
            print(f"Data de Início: {data_inicio_str}")
            print(f"Data de Fim: {data_fim_str}")
            print(f"Cliente: {nome}")
            print(f"Automóvel: {marca} - {matricula}")
            print(f"Total: {booking['precoReserva']}€")
            print("===============================")
    if(flag == 0):
        print("Não há reservas futuras.")

def menu():
    print("===== Rent-a-Car - Bem-vindo =====")
    print("Explore as opções abaixo e gerencie facilmente sua frota de automóveis e reservas:")
    options = [
        "Listar Clientes",
        "Listar Automóveis",
        "Listar Reservas",
        "Adicionar Novo Cliente",
        "Adicionar Novo Automóvel",
        "Adicionar Nova Reserva",
        "Remover Automóvel",
        "Remover Cliente",
        "Remover Reserva",
        "Atualizar Automóvel",
        "Atualizar Cliente",
        "Atualizar Reserva",
        "Pesquisar por Automóvel",
        "Pesquisar por Cliente",
        "Listar Reservas Futuras",
        "Sair",
    ]
    selected_option = cutie.select(options)
    if(selected_option == 0):
        listar_clientes()
    elif(selected_option == 1):
        listar_automoveis() 
    elif(selected_option == 2):
        listar_reservas()
    elif(selected_option == 3):
        adicionar_cliente()
    elif(selected_option == 4):
        adicionar_automovel()
    elif(selected_option == 5):
        adicionar_reserva()
    elif(selected_option == 6):
        removerAutomovel()
    elif(selected_option == 7):
        removerCliente()
    elif(selected_option == 8):
        removerReserva()
    elif(selected_option == 9):
        atualizar_automovel()
    elif(selected_option == 10):
        atualizar_cliente()
    elif(selected_option == 11):
        atualizar_reserva()
    elif(selected_option == 12):
        pesquisar_automovel()
    elif(selected_option == 13):
        pesquisar_cliente()
    elif(selected_option == 14):
        listar_reservas_futuras()
    else:
        print("Até a próxima!")
     
def main():
    menu()
    # Salvando todas as listas com os novos dados de volta nos arquivos JSON
    save_all_data()


if __name__ == "__main__":
    main()
