import struct
import os


registro_formato = 'if8s'
registro_tamanho = struct.calcsize(registro_formato)


def criar_arquivo(nome_arquivo):
    with open(nome_arquivo, 'wb'):
        pass


def adicionar_venda(arquivo, codigo_vendedor, valor_venda, mes_ano):
    arquivo.seek(0, os.SEEK_END)
    data = struct.pack(registro_formato, codigo_vendedor, valor_venda, mes_ano.encode('utf-8'))
    arquivo.write(data)


def verificar_registro(arquivo, codigo_vendedor, mes_ano):
    arquivo.seek(0)
    while True:
        data = arquivo.read(registro_tamanho)
        if not data:
            break
        codigo, _, mes_ano_registro = struct.unpack(registro_formato, data)
        mes_ano_registro = mes_ano_registro.decode('utf-8').strip('\x00')
        if codigo == codigo_vendedor and mes_ano_registro == mes_ano:
            return True
    return False


def excluir_venda(arquivo, codigo_vendedor, mes_ano):
    temp = open('temp.bin', 'wb')
    arquivo.seek(0)
    while True:
        data = arquivo.read(registro_tamanho)
        if not data:
            break
        codigo, _, mes_ano_registro = struct.unpack(registro_formato, data)
        mes_ano_registro = mes_ano_registro.decode('utf-8').strip('\x00')
        if codigo != codigo_vendedor or mes_ano_registro != mes_ano:
            temp.write(data)
    temp.close()
    arquivo.close()
    os.remove(arquivo.name)
    os.rename('temp.bin', arquivo.name)
    arquivo = open(arquivo.name, 'rb+')  
    return arquivo 


def alterar_valor_venda(arquivo, codigo_vendedor, mes_ano, novo_valor):
    arquivo.seek(0)
    while True:
        posicao = arquivo.tell()
        data = arquivo.read(registro_tamanho)
        if not data:
            break
        codigo, valor, mes_ano_registro = struct.unpack(registro_formato, data)
        mes_ano_registro = mes_ano_registro.decode('utf-8').strip('\x00')
        if codigo == codigo_vendedor and mes_ano_registro == mes_ano:
            novo_registro = struct.pack(registro_formato, codigo, novo_valor, mes_ano_registro.encode('utf-8'))
            arquivo.seek(posicao)
            arquivo.write(novo_registro)
            break


def imprimir_registros(arquivo):
    arquivo.seek(0)
    while True:
        data = arquivo.read(registro_tamanho)
        if not data:
            break
        codigo, valor, mes_ano = struct.unpack(registro_formato, data)
        mes_ano = mes_ano.decode('utf-8').strip('\x00')
        print("Código do vendedor:", codigo)
        print("Valor da venda:", valor)
        print("Mês/Ano:", mes_ano)
        print()

def consultar_maior_vendedor(arquivo):
    maior_valor = 0
    maior_venda = None
    arquivo.seek(0)
    while True:
        data = arquivo.read(registro_tamanho)
        if not data:
            break
        codigo, valor, mes_ano = struct.unpack(registro_formato, data)
        if valor > maior_valor:
            maior_valor = valor
            maior_venda = (codigo, valor, mes_ano)
    if maior_venda is not None:
        codigo_vendedor, valor_venda, mes_ano = maior_venda
        print("O vendedor com maior valor de venda é o código:", codigo_vendedor)
        print("Valor da venda:", valor_venda)
        print("Mês/Ano:", mes_ano.decode('utf-8').strip('\x00'))
    else:
        print("Não há vendas registradas.")



def menu():
    nome_arquivo = 'vendas.bin'
    if not os.path.exists(nome_arquivo):
        criar_arquivo(nome_arquivo)
    
    arquivo = open(nome_arquivo, 'rb+')

    while True:
        print("\nMenu:")
        print("1. Incluir venda")
        print("2. Excluir venda")
        print("3. Alterar valor da venda")
        print("4. Imprimir registros")
        print("5. Consultar vendedor com maior valor de venda")
        print("6. Finalizar o programa")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            codigo = int(input("Digite o código do vendedor: "))
            valor = float(input("Digite o valor da venda: "))
            mes_ano = input("Digite o mês/ano (mm/aaaa): ")
            if not verificar_registro(arquivo, codigo, mes_ano):
                adicionar_venda(arquivo, codigo, valor, mes_ano)
            else:
                print("Já existe uma venda registrada para este vendedor neste mês.")
        elif opcao == '2':
            codigo = int(input("Digite o código do vendedor a ser excluído: "))
            mes_ano = input("Digite o mês/ano da venda a ser excluída (mm/aaaa): ")
            arquivo = excluir_venda(arquivo, codigo, mes_ano)  
        elif opcao == '3':
            codigo = int(input("Digite o código do vendedor: "))
            mes_ano = input("Digite o mês/ano da venda a ser alterada (mm/aaaa): ")
            novo_valor = float(input("Digite o novo valor da venda: "))
            alterar_valor_venda(arquivo, codigo, mes_ano, novo_valor)
        elif opcao == '4':
            print("\nRegistros de venda:")
            imprimir_registros(arquivo)
        elif opcao == '5':
            consultar_maior_vendedor(arquivo)
        elif opcao == '6':
            arquivo.close()
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
