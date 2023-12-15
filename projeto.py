import json
import cutie
from datetime import datetime
import os

#Grupo: Clara Franco, Pedro Matos, Pedro Pinto, Temaco Mafumba

def is_date_string(value):
    #Verifica se uma string pode ser convertida para um objeto datetime no formato "dd/mm/yyyy".
    try:
        datetime.strptime(value, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def custom_deserializer(obj):
    #Converte strings de datas no formato "dd/mm/yyyy" para objetos datetime.
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
        # Obter o diretório atual
        diretorio_atual = os.path.dirname(__file__)
        # Combina o caminho do diretório com o nome do arquivo desejado
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

#Carrega os dados dos arquivos JSON para as listas ao iniciar o programa 
listAutomovel = load_data("listautomovel.json")
listCliente = load_data("listcliente.json")
listBooking = load_data("listbooking.json")
###    *********************************** ################  

#Converte objetos datetime para strings no formato "dd/mm/yyyy"
def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%d/%m/%Y")
    return obj

def save_data(filename, data):
    try:
        # Obter o diretório atual
        diretorio_atual = os.path.dirname(__file__)
        # Combina o caminho do diretório com o nome do arquivo desejado
        caminho_arquivo = os.path.join(diretorio_atual, filename)
        # Salva os dados no arquivo na mesma pasta
        with open(caminho_arquivo, "w") as f:
            json.dump(data, f, default=custom_serializer, indent=4)
    except Exception as e:
        print(f"\nErro ao salvar dados em {filename}: {e}")

#Salva todas as listas de dados em arquivos JSON correspondentes.
def save_all_data():
    save_data("listautomovel.json", listAutomovel)
    save_data("listcliente.json", listCliente)
    save_data("listbooking.json", listBooking)

def adicionar_automovel():
    print("\nAdicionar Automóvel:")
    #Solicita informações do usuário
    matricula = input("Matrícula: ")
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    cor = input("Cor: ")
    portas = int(input("Número de Portas: "))
    preco_diario = float(input("Preço Diário: "))
    cilindrada = int(input("Cilindrada: "))
    potencia = int(input("Potência: "))
    #Cria um novo dicionário representando o automóvel
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
    #Adiciona o novo automóvel a lista
    listAutomovel.append(novo_automovel)
    #Salva a lista atualizada no arquivo JSON
    save_data("listautomovel.json", listAutomovel)
    print("Novo automóvel adicionado com sucesso!")

#Calcula o preço da reserva com base no número de dias e aplica descontos, se aplicável.
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
    #Solicita informações do usuário
    cliente_id = int(input("ID do cliente: "))
    automovel_id = int(input("ID do automóvel: "))
    while True:
        try:
            #Solicita datas como strings
            data_inicio_str = input("Data de Início (dd/mm/yyyy): ")
            data_fim_str = input("Data de Fim (dd/mm/yyyy): ")
            #Converte strings de data para objetos datetime
            data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")
            data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")
            break  # Se a conversão for bem-sucedida, sai do loop
        except ValueError:
            print("Formato de data incorreto. Por favor, insira a data no formato dd/mm/yyyy (utilize a /).")
    numeroDias = (data_fim - data_inicio).days #Calcula o número de dias da reserva
    precoReserva = calcular_preco(numeroDias) #Calcula o preço da reserva 
    #Cria um dicionário da nova reserva
    nova_reserva = {
        'id': len(listBooking) + 1,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'cliente_id': cliente_id,
        'automovel_id': automovel_id,
        'precoReserva': precoReserva,
        'numeroDias': numeroDias
    }
    #Adicionar a nova reserva a lista de reservas
    listBooking.append(nova_reserva)
    #Salva a lista atualizada no arquivo JSON
    save_data("listbooking.json", listBooking)
    print("Reserva efetuada com sucesso!")
    print(f"Preço a pagar: {precoReserva}")

#Verifica se um cliente com o mesmo telefone ou e-mail já existe na lista de clientes.
def cliente_existe(telefone, email):
    for cliente in listCliente:
        if cliente['telefone'] == telefone or cliente['email'] == email:
            return True
    return False

def adicionar_cliente():
    print("Entra com os dados do Cliente:")
    #Solicita informações do usuário
    nome = input("Nome: ")
    nif = int(input("NIF: "))
    while True:
        try:
            #Solicita a data de nascimento como string
            data_nascimento_str = input("Data de Nascimento (dd/mm/yyyy): ")
            #Converte a string de data para um objeto datetime
            data_nascimento = datetime.strptime(data_nascimento_str, "%d/%m/%Y")
            break  #Se a conversão for bem-sucedida, sai do loop
        except ValueError:
            print("Formato de data incorreto. Por favor, insira a data no formato dd/mm/yyyy (utilize a /).")
    telefone = int(input("Telefone: "))
    email = input("Email: ")
    #Verifica se o cliente já existe
    if cliente_existe(telefone, email):
        print("Telefone ou email já existem na lista. Não é possível adicionar cliente.")
        return
    #Cria um dicionário do novo cliente
    novo_cliente = {
        'id': len(listCliente) + 1,
        'nome': nome,
        'nif': nif,
        'dataNascimento': data_nascimento,
        'telefone': telefone,
        'email': email
    }
    #Adicionar o novo cliente a lista de clientes
    listCliente.append(novo_cliente)
    #Salva a lista atualizada no arquivo JSON
    save_data("listcliente.json", listCliente)
    print("Novo cliente adicionado com sucesso!")

def removerCliente(): 
    id = int(input("Digite o id do cliente a ser removido: "))
    cliente_encontrado = False #Variável para verificar se o cliente foi encontrado
    for pessoa in listCliente: 
        if pessoa['id'] == id: 
            listCliente.remove(pessoa) #Remove o cliente da lista
            print(f"Cliente {id} removido com sucesso!") 
            cliente_encontrado = True
            break  #Uma vez que o cliente foi encontrado e removido, sai do loop
    if not cliente_encontrado: 
        print(f"Cliente {id} não encontrado na lista.")

def removerAutomovel(): 
    id = int(input("Digite o id do automóvel a ser removido: "))
    automovel_encontrado = False #Variável para verificar se o automovel foi encontrado
    for automovel in listAutomovel: 
        if automovel['id'] == id: 
            listAutomovel.remove(automovel) #Remove o automovel da lista
            print(f"Automóvel {id} removido com sucesso!") 
            automovel_encontrado = True
            break  #Uma vez que o automóvel foi encontrado e removido, sai do loop
    if not automovel_encontrado: 
        print(f"Automóvel {id} não encontrado na lista.")

def removerReserva(): 
    id = int(input("Digite o id da reserva a ser removida: "))
    reserva_encontrada = False #Variável para verificar se a reserva foi encontrada
    for reserva in listBooking: 
        if reserva['id'] == id: 
            listBooking.remove(reserva) #Remove a reserva da lista
            print(f"Reserva {id} removida com sucesso!") 
            reserva_encontrada = True
            break  #Uma vez que a reserva foi encontrada e removida, sai do loop
    if not reserva_encontrada: 
        print(f"Reserva {id} não encontrada na lista.")

def listar_automoveis():
    #Exibe na tela a lista de automóveis com seus respectivos dados.
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
    #Exibe na tela a lista de clientes com seus respectivos dados.
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
    #Exibe na tela a lista de reservas com seus respectivos dados.
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

#Solicita ao usuário uma nova data de nascimento e a converte para um objeto datetime.
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

#Permite ao usuário selecionar um cliente existente e escolher qual dado atualizar.
def atualizar_cliente():
    print("\nAtualizar Cliente:")
    if not listCliente:  #Verifica se a lista está vazia
        print("Não há clientes")
        return
    cliente_id = int(input("ID do cliente a ser atualizado: "))
    #Apresenta opções para o usuário
    print("Escolha o dado que deseja atualizar:")
    options = [
        "Nome",
        "Nif",
        "Data de Nascimento",
        "Telefone",
        "Email",
        "Cancelar"
    ]
    selected_option = cutie.select(options)  #Guarda a opção selecionada pelo usuário
    cliente_encontrado = False #Flag para verificar se o cliente foi encontrado
    for pessoa in listCliente: 
        if pessoa['id'] == cliente_id:
            cliente_encontrado = True
            if selected_option == 0:
                pessoa['nome'] = input("Novo nome: ")
            elif selected_option == 1:
                pessoa['nif'] = input("Novo nif: ") 
            elif selected_option == 2:
                pessoa['dataNascimento'] = obter_nova_data_nascimento()
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
    #Se o cliente não foi encontrado, exibe uma mensagem
    if not cliente_encontrado:
        print(f"Cliente {cliente_id} não encontrado.")

#Permite ao usuário selecionar um automovel existente e escolher qual dado atualizar.
def atualizar_automovel():
    print("\nAtualizar Automóvel:")
    if not listAutomovel:  #Verifica se a lista está vazia
        print("Não há automóveis")
        return
    automovel_id = int(input("ID do automóvel a ser atualizado: "))
    #Apresenta opções para o usuário
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
    selected_option = cutie.select(options) #Guarda a opção selecionada pelo usuário
    automovel_encontrado = False #Flag para verificar se o automovel foi encontrado
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
    #Se o automovel não foi encontrado, exibe uma mensagem
    if not automovel_encontrado:
        print(f"Automóvel {automovel_id} não encontrado.")

#Solicita ao usuário uma nova data de início e a converte para um objeto datetime.
def obter_nova_data_inicio():
    while True:
        try:
            nova_data_inicio_str = input("Nova Data de Início (dd/mm/yyyy): ")
            return datetime.strptime(nova_data_inicio_str, "%d/%m/%Y")
        except ValueError:
            print("Formato de data incorreto. Por favor, insira a data no formato dd/mm/yyyy.")

#Solicita ao usuário uma nova data de fim e a converte para um objeto datetime.
def obter_nova_data_fim():
    while True:
        try:
            nova_data_fim_str = input("Nova Data de Fim (dd/mm/yyyy): ")
            return datetime.strptime(nova_data_fim_str, "%d/%m/%Y")
        except ValueError:
            print("Formato de data incorreto. Por favor, insira a data no formato dd/mm/yyyy.")

#Permite ao usuário selecionar uma reserva existente e escolher qual dado atualizar.
def atualizar_reserva():
    print("\nAtualizar Reserva:")
    if not listBooking:  #Verifica se a lista está vazia
        print("Não há reservas")
        return
    reserva_id = int(input("ID da reserva a ser atualizada: "))
    #Apresenta opções para o usuário
    print("Escolha o dado que deseja atualizar:")
    options = [
        "Data de Início",
        "Data de Fim",
        "Cliente ID",
        "Automóvel ID",
        "Preço Reserva",
        "Cancelar"
    ]
    selected_option = cutie.select(options) #Guarda a opção selecionada pelo usuário
    reserva_encontrada = False #Flag para verificar se a reserva foi encontrada
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
    #Se a reserva não foi encontrada, exibe uma mensagem
    if not reserva_encontrada:
        print(f"Reserva {reserva_id} não encontrada.")

#Pesquisa um cliente pelo NIF e exibe seus dados, depois exibe as 5 primeiras reservas desse cliente.
def pesquisar_cliente():
    nif = int(input("Inserir NIF do cliente para pesquisa: "))
    flag = 0 #Flag para indicar se o cliente foi encontrado
    for cliente in listCliente:
        if cliente['nif'] == nif:
            flag = 1 #Atualiza a flag indicando que o cliente foi encontrado
            id_cliente = cliente['id'] #Obtém o ID do cliente para usar para encontrar as reservas
            print(f"\n=== Dados Cliente {cliente['nome']}: ===")
            for chave, valor in cliente.items():
                print(f"{chave}: {valor}")
            print(f"=============================")
            break
    #Se o cliente não foi encontrado, exibe uma mensagem
    if(flag == 0):
        print("Cliente não encontrado.")
        return
    i = 1 #Contador para limitar o número de reservas exibidas
    for cliente in listBooking:
        if cliente['cliente_id'] == id_cliente:
            print(f"\n=== Cliente {id_cliente} - Booking {i}: ===")
            for chave, valor in cliente.items():
                print(f"{chave}: {valor}")
            print(f"=============================")
            i += 1
            #Limita a exibição a 5 reservas
            if i == 6: 
                break

#Pesquisa um automóvel pela matrícula e exibe seus dados, depois exibe as 5 primeiras reservas desse automovel.
def pesquisar_automovel():
    matricula = input("Inserir matrícula do cliente para pesquisa: ")
    flag = 0 #Flag para indicar se o automóvel foi encontrado
    for automovel in listAutomovel:
        if automovel['matricula'] == matricula:
            flag = 1 #Atualiza a flag indicando que o automóvel foi encontrado
            id_automovel = automovel['id'] #Obtém o ID do automovel para usar para encontrar as reservas
            print(f"\n=== Dados Automóvel {matricula}: ===")
            for chave, valor in automovel.items():
                print(f"{chave}: {valor}")
            print(f"=============================")
            break #Uma vez que o automóvel foi encontrado, sai do loop
    #Se o automóvel não foi encontrado, exibe uma mensagem
    if(flag == 0):
        print("Automóvel não encontrado.")
        return
    i = 1 #Contador para limitar o número de reservas exibidas
    for automovel in listBooking:
        if automovel['automovel_id'] == id_automovel:
            print(f"\n=== Automóvel {id_automovel} - Booking {i}: ===")
            for chave, valor in automovel.items():
                print(f"{chave}: {valor}")
            print(f"=============================")
            i += 1
            #Limita a exibição a 5 reservas
            if i == 6:
                break

#Encontra o nome do cliente com base no ID do cliente
def achar_nome(id_cliente):
   for cliente in listCliente:
        if cliente['id'] == id_cliente:
            return cliente['nome']

#Encontra a matrícula e a marca do automóvel com base no ID do automóvel.    
def achar_automovel(id_automovel):
   for automovel in listAutomovel:
        if automovel['id'] == id_automovel:
            return automovel['matricula'],automovel['marca']

#Lista as reservas futuras, exibindo detalhes como data, cliente, automóvel e total.
def listar_reservas_futuras():
    print("\nReservas Futuras:")
    hoje = datetime.now() #Obtém a data atual
    flag = 0 #Flag para indicar se há reservas futuras
    for booking in listBooking:
        if booking['data_fim'] > hoje:
            flag = 1 #Atualiza a flag indicando que há reservas futuras
            #Formata as datas para exibição
            data_inicio_str = booking['data_inicio'].strftime('%d/%m/%Y')
            data_fim_str = booking['data_fim'].strftime('%d/%m/%Y')
            #Obtém o nome do cliente e as informações do automóvel
            nome = achar_nome(booking['cliente_id'])
            matricula, marca = achar_automovel(booking['automovel_id'])
            #Exibe os detalhes da reserva
            print(f"\n=== Detalhes Reserva ID {booking['id']} ===")
            print(f"Data de Início: {data_inicio_str}")
            print(f"Data de Fim: {data_fim_str}")
            print(f"Cliente: {nome}")
            print(f"Automóvel: {marca} - {matricula}")
            print(f"Total: {booking['precoReserva']}€")
            print("===============================")
    #Se não houver reservas futuras, exibe uma mensagem
    if(flag == 0):
        print("Não há reservas futuras.")

def menu():
    #Apresentação do menu principal
    print("===== Rent-a-Car - Bem-vindo =====")
    print("Explore as opções abaixo e gerencie facilmente sua frota de automóveis e reservas:")
    #Lista de opções disponíveis no menu
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
    selected_option = cutie.select(options) #Solicita ao usuário que escolha uma opção do menu e guarda
    #Executa a operação correspondente à opção escolhida
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
    #Se o usuário escolher uma opção inválida, sai o programa
    else:
        print("Até a próxima!")
     
def main():
    #Inicia o menu principal
    menu()
    #Salvando todas as listas com os novos dados de volta nos arquivos JSON
    save_all_data()

if __name__ == "__main__":
    main()
