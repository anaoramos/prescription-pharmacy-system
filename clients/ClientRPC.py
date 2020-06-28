# -*- coding: utf-8 -*-
import xmlrpc.client
import sys, os

server = xmlrpc.client.ServerProxy('http://localhost:12345/', encoding=None)
# Print list of available methods
print(server.system.listMethods())


def printTable(myDict, colList=None):
   """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
   If column names (colList) aren't specified, they will show in random order.
   Author: Thierry Husson
   """
   if not colList: colList = list(myDict[0].keys() if myDict else [])
   myList = [colList] # 1st row = header
   for item in myDict: myList.append([str(item[col] or '') for col in colList])
   colSize = [max(map(len,col)) for col in zip(*myList)]
   formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
   myList.insert(1, ['-' * i for i in colSize]) # Seperating line
   for item in myList: print(formatStr.format(*item))


def print_Menu_Principal():
    print(30 * "-" , "MENU Principal" , 30 * "-")
    print()
    print("")
    print("\t1. Administração")
    print("\t2. Funcionários")
    print("")
    print("\t0. Sair")
    print("")
    print(67 * "-")

def print_Menu_Admin():
    print(30 * "-" , "MENU Administração" , 30 * "-")
    print()
    print("")
    print("\t1. Lista farmácias")
    print("\t2. Adicionar Farmácia ao Sistema")
    print("\t3. Utentes")
    print("\t4. Médicos")
    print("\t5. Medicamentos")
    print("")
    print("\t0. Sair")
    print("")
    print(67 * "-")


def print_Menu_Func():
    print(30 * "-" , "MENU" , 30 * "-")
    print()
    print("")
    print("\t1. Receitas")
    print("")
    print("\t0. Sair")
    print("")
    print(67 * "-")


def print_MenuReceitas():    
    print(30 * "-" , "MENU Receitas" , 30 * "-")
    print("")   
    print("1. Adicionar Receita")
    print("2. Listar Receitas de uma Farmácia")
    print("")   
    print("9. Retroceder")
    print("0. Sair")
    print("")   
    print(67 * "-")
    
def print_MenuUtentes():    
    print(30 * "-" , "MENU Utentes" , 30 * "-")
    print("")   
    print("1. Adicionar Utente")
    print("2. Atualizar Ficha de Utente")
    print("3. Apagar Utente")
    print("4. Lista de Utentes")
    print("5. Utentes com mais receitas")
    print("6. Utentes mais gastadores")
    print("7. Média de receitas por Utente")
    print("8. Selecionar Utente")
    print("")      
    print("9. Retroceder")
    print("0. Sair")
    print("")   
    print(67 * "-")
    
def print_MenuMedicos():    
    print(30 * "-" , "MENU Utentes" , 30 * "-")
    print("")
    print("1. Adicionar Médico")
    print("2. Altualizar Ficha de Médico")
    print("3. Apagar Médico da Base de dados")
    print("4. Lista de Médicos")
    print("5. Médicos com mais receitas")
    print("6. Média de receitas por médico")
    print("7. Selecionar Médico")
    print("")
    print("9. Retroceder")
    print("0. Sair")
    print("")
    print(67 * "-") 
    
def print_MenuMedicamentos():    
    print(30 * "-" , "MENU Medicamentos" , 30 * "-")
    print("")
    print("1. Lista dos Medicamentos na Base de Dados")
    print("2. Adicionar Medicamento à Base de dados")
    print("3. Adicionar Medicamento ao Stock de uma Farmácia")
    print("4. Lista Medicamento em Stock de uma Farmácia")
    print("5. Lista Medicamento em Alarme de uma Farmácia")
    print("6. Verificar medicamentos em Alarme de uma Farmácia")
    print("7. Medicamentos mais vendidos")
    print("")   
    print("9. Retroceder")
    print("0. Sair")
    print("")
    print(67 * "-")

def MenuMain():
    loop=True
    while loop:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_Menu_Principal()
        choice = int(input("Diga a opção : "))
        if choice==1:
            MenuAdmin()
        elif choice==2:
            MenuFunc()
        elif choice==0:
            os.system('cls' if os.name == 'nt' else 'clear')
            close = int(input("Fechar aplicacao ? [1:0] : "))
            if close==1:
                server.SaveInfoDataBase()
                loop=False
        else:
            input("Opção errada. Clique numa tecla para voltar atrás...")

def MenuAdmin():
    loop=True
    while loop:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_Menu_Admin()
        choice = int(input("Diga a opção : "))
        if choice==1:
            os.system('cls' if os.name == 'nt' else 'clear')
            result = server.listaFarmacias()
            printTable(result)
            input("\nContinuar...")

        elif choice==2:
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                id = input("Introduza a identificação da farmácia: ")
                nome=input("Introduza o nome da Farmácia: ")
                morada=input("Introduza a morada da Framácia: ")
                server.adicionarFarmacia(id,nome,morada)
                input("\nContinuar....")

            except Exception as ex:
                print(ex)

        elif choice == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            MenuUtentes()

        elif choice == 4:
            os.system('cls' if os.name == 'nt' else 'clear')
            MenuMedicos()

        elif choice == 5:
            os.system('cls' if os.name == 'nt' else 'clear')
            MenuMedicamentos()

        elif choice==0:
            os.system('cls' if os.name == 'nt' else 'clear')            
            loop=False
        else:           
            input("Opção errada. Clique numa tecla para voltar atrás...")

def MenuReceitas():
    loop=True
    while loop:         
        os.system('cls' if os.name == 'nt' else 'clear')
        print_MenuReceitas()   
        choice = int(input("Enter your choice [1-5]: "))         
        if choice==1:
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                idReceita=input("Adicionar identificador da receita: ")
                idUtente= input("Adicionar identificação do Utente: ")
                nomeMedico=input("Nome do Médico que registou a receita: ")
                qtMedic = int(input("Quantos medicamentos vai introduzir: "))
                count = 0
                listMedicamentos = []

                while (count < qtMedic):
                    medicamento = input("Nome do Medicamento : ")
                    qt = input("Quantidade : ")
                    info = {}
                    info['Nome'] = medicamento
                    info['Qt'] = qt
                    listMedicamentos.append(info)
                    count = count + 1

                idFarmacia=int(input("Identificação da farmacia: "))
                server.RegistarReceita(idFarmacia,idReceita,idUtente,nomeMedico,listMedicamentos)
                print("Receita registada com Sucesso")

            except Exception as ex:
                print(ex)
            input("\nContinuar...")

        elif choice==2:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("------RECEITAS-------")
            idFarmacia = int(input("Identificação da farmacia: "))
            result = server.listarReceitas(idFarmacia)
            printTable(result)
            input("\nContinuar...")


        elif choice==9:
            os.system('cls' if os.name == 'nt' else 'clear')
            loop=False

        elif choice==0:
            os.system('cls' if os.name == 'nt' else 'clear')
            MenuMain()
        else:            
            input("Opção errada. Clique numa tecla para voltar atrás..")
            
            
def MenuUtentes():
    loop=True
    while loop:         
        os.system('cls' if os.name == 'nt' else 'clear')
        print_MenuUtentes() 
        choice = int(input("Escolha a opção [1-5]: "))
        if choice==1:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                idUtente=input("Introduza a identificação do Utente: ")
                nomeUtente=input(("Introduza o nome do Utente: "))
                morada = input("Introduza a morada do Utente: ")
                nif = int(input("Introduza o nif do Utente: "))
                cc = int(input("Introduza o CC do Utente: "))
                tel= input("Introduza o número de telemóvel do Utente:")
                server.adicionarUtente(idUtente,nomeUtente, morada, nif, cc, tel)
                print("Utente foi dicionado com sucesso")

            except Exception as ex:
                print(ex)

            input("\nContinuar....")

        elif choice==2:
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                idUtente = input("Introduza a identificação do Utente: ")
                nomeUtente = input(("Introduza o nome do Utente: "))
                morada = input("Introduza a morada do Utente: ")
                nif = input("Introduza o nif do Utente: ")
                cc = input("Introduza o CC do Utente: ")
                tel = input("Introduza o número de telemóvel do Utente:")
                server.updateUtente(idUtente,nomeUtente, morada, nif, cc, tel)
                print("Utente adicionado com sucesso.")

            except Exception as ex:
                print(ex)
            input("\nContinuar...")

        elif choice==3:
            os.system('cls' if os.name == 'nt' else 'clear')
            idUtente=input("Introduza a identificação do utente que pretende eliminar da base de dados: ")
            server.apagarUtente (idUtente)
            print("Utente",idUtente," foi eliminado do sistema")
            input("\nContinuar...")

        elif choice==4:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("-----Utentes------")
            result=server.listUtentes()
            if len(result) > 0:
                printTable(result)
            else:
                print("Não há utentes no sistema..")

            input("\nContinuar....")

        elif choice==5:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("---Lista de utentes com mais receitas----------")
            result = server.UtentesMaisReceitas()
            print(result)
            input("\nContinuar...")

        elif choice==6:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("---Lista de utentes mais gastadores----------")
            result=server.UtentesGastadores()
            print(result)
            input("\nContinuar...")

        elif choice==7:
            os.system('cls' if os.name == 'nt' else 'clear')
            idUtente=int(input("Introduza a identificação do utente: "))
            result=server.MediaReceitaPorUtente(idUtente)
            print(result)
            input("\nContinuar...")

        elif choice==8:
            os.system('cls' if os.name == 'nt' else 'clear')
            idUtente=int(input("Introduza a identificação do Utente: "))
            result=server.selectUtente(idUtente)
            printTable(result)
            input("\nContinuar...")

        elif choice == 9:
            os.system('cls' if os.name == 'nt' else 'clear')
            loop = False

        elif choice == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            MenuMain()
        else:            
            input("Opção errada. Clique numa tecla para voltar atrás..")


def MenuMedicos():
     loop = True
     while loop:
         os.system('cls' if os.name == 'nt' else 'clear')
         print_MenuMedicos()
         choice = int(input("Escolha a opção [1-5]: "))
         if choice == 1:
             os.system('cls' if os.name == 'nt' else 'clear')
             try:
                 nomeMedico = input(("Introduza o nome do Médico: "))
                 morada = input("Introduza a morada do Médico: ")
                 nif = input("Introduza o nif do Médico: ")
                 cc = input("Introduza o CC do Médico: ")
                 tel = input("Introduza o número de telemóvel do Médico:")
                 especialidade = input("Introduza a especialidade:")
                 server.AddMedico(nomeMedico, morada, nif, cc, tel,especialidade)
                 print ("Médico adicionado com sucesso")
             except Exception as ex:
                 print(ex)

             input("\nContinuar...")

         elif choice == 2:
             os.system('cls' if os.name == 'nt' else 'clear')
             print("Volte a colocar as informações todas do Utente pretendido")
             nomeMedico = input(("Introduza o nome do Médico: "))
             morada = input("Introduza a morada do Médico: ")
             nif = input("Introduza o nif do Médico: ")
             cc = input("Introduza o CC do Médico: ")
             tel = input("Introduza o número de telemóvel do Médico:")
             especialidade = input("Introduza a especialidade:")
             server.updateMedico(nomeMedico, morada, nif, cc, tel,especialidade)
             print("Médico atualizado com sucesso.")
             input("\nContinuar...")

         elif choice == 3:
             os.system('cls' if os.name == 'nt' else 'clear')
             nomeMedico = input("Introduza o nome do médico que pretende eliminar da base de dados: ")
             server.apagarMedico (nomeMedico)
             input("\nContinuar...")

         elif choice == 4:
             os.system('cls' if os.name == 'nt' else 'clear')
             print("-----Médicos------")
             result=server.listMedico()
             printTable(result)
             input("\nContinuar...")

         elif choice == 5:
             os.system('cls' if os.name == 'nt' else 'clear')
             print("---Lista de Médicos com mais receitas----------")
             result = server.MedicosMaisReceitas()
             print(result)
             input("\nContinuar...")

         elif choice == 6:
             os.system('cls' if os.name == 'nt' else 'clear')
             nomeMedico = input("Introduza o nome do médico: ")
             result=server.MediaReceitaPorMedico(nomeMedico)
             print(result)
             input("\nContinuar...")

         elif choice == 7:
             os.system('cls' if os.name == 'nt' else 'clear')
             nomeMedico = input("Introduza o nome do Médico: ")
             result=server.SelectMedico(nomeMedico)
             printTable(result)
             input("\nContinuar...")

         elif choice == 9:
             os.system('cls' if os.name == 'nt' else 'clear')
             loop = False

         elif choice == 0:
             os.system('cls' if os.name == 'nt' else 'clear')
             MenuMain()
         else:
             input("Opção errada. Clique numa tecla para voltar atrás..")


def MenuMedicamentos():
    loop = True
    while loop:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_MenuMedicamentos()
        choice = int(input("Escolha a opção [1-5]: "))
        if choice == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("------------Base de Dados de Medicamentos----------")
            result = server.listMedicamentos()
            printTable(result)
            input("\nContinuar...")

        elif choice == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            nomeMedicamento = input("Introduzir o nome do Medicamento: ")
            dosagem = int(input("Introduzir a dosagem do Medicamento: "))
            server.AddMedicamento(nomeMedicamento, dosagem)
            print("Medicamento adicionado à Base de Dados. ")
            input("\nContinuar...")

        elif choice == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            idfarm=int(input("Introduza a identificação da Farmácia: "))
            nomeMedicamento = input("Introduzir o nome do Medicamento: ")
            quantidade = int(input("Introduzir a quantidade do Medicamento: "))
            server.UpdateStock(idfarm, nomeMedicamento, quantidade)
            input("\nContinuar...")

        elif choice == 4:
            os.system('cls' if os.name == 'nt' else 'clear')
            idfarm=int(input("Introduza a identificação da Farmácia: "))
            result = server.listMedicamentosStock(idfarm)
            printTable(result)
            input("\nContinuar...")

        elif choice == 5:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("------Medicamentos em Alarme------- ")
            idfarm = int(input("Introduza a identificação da Farmácia: "))
            result=server.MedicamentosAlarme(idfarm)
            printTable(result)
            input("\nContinuar...")

        elif choice == 6:
            os.system('cls' if os.name == 'nt' else 'clear')
            idfarm = int(input("Introduza a identificação da Farmácia: "))
            server.VerificarAlarme(idfarm)
            print("Verificação de medicamentos em alarme realizada com sucesso")
            input("\nContinuar...")

        elif choice == 7:
            os.system('cls' if os.name == 'nt' else 'clear')
            idfarm = int(input("Introduza a identificação da Farmácia: "))
            result=server.MedicamentosMaisVendidos(idfarm)
            print (result)
            input ("\nContinuar...")

        elif choice == 9:
            os.system('cls' if os.name == 'nt' else 'clear')
            loop = False

        elif choice == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            MenuMain()
        else:
            input("Opção errada. Clique numa tecla para voltar atrás..")


def MenuFunc():
    loop = True
    while loop:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_Menu_Func()
        choice = int(input("Diga a opção : "))
        if choice == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            MenuReceitas()
        elif choice == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            loop = False
        else:
            input("Opção errada. Clique numa tecla para voltar atrás...")


if __name__ == '__main__':
    MenuMain()