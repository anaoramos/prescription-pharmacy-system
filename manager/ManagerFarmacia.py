# -*- coding: utf-8 -*-
import os
import threading
import pickle 
from model.Receita import *
from model.Farmacia import *
import threading
from db.DataBase import *
from manager.ManagerUtentes import *
from manager.ManagerMedicos import *
from manager.ManagerMedicamentos import *
from model.Stock import *
from exceptions.IDJaExisteException import *
import threading

class ManagerFarmacia():

    def __init__(self):
        self.lock = threading.RLock()
        self.DB = DataBase()
        self.managerUtentes = ManagerUtentes(self.DB)
        self.managerMedicos = ManagerMedicos(self.DB)
        self.managerMedicamentos = ManagerMedicamentos(self.DB)
        
        if not self.LoadDataBase():           
            self.loadDataBase()  
            #self.SaveDataBase(self.DB)

    def SaveDataBase(self,db):         
        with self.lock:
            fp=open('database.obj', 'wb')
            pickle.dump(self.DB, fp, pickle.HIGHEST_PROTOCOL) 
            
    def SaveDataBaseOut(self):         
        self.SaveDataBase(self.DB)         

    def LoadDataBase(self):
        if os.path.exists('database.obj'):
            if os.path.getsize('database.obj') > 0 :
                with self.lock:
                    fp=open('database.obj', 'rb')
                    self.DB = pickle.load(fp)
                return True
            else:
                print("")
        return False

#------------------------------------------Medicamentos-----------------------------------------------------------

    def AddMedicamento(self, nome, dosagem):
        with self.lock:
            self.managerMedicamentos.Add(nome,dosagem)
        #self.SaveDataBase(self.DB)

    def GetMedicamentos(self):
        try:
            content = self.managerMedicamentos.GetAll()
            return content
        except Exception as ex:
            raise Exception(ex)

#--------------------------------------------------Medicos--------------------------------------------------------

    def AddMedico(self, nomeMedico, morada, nif, cc, tel, especialidade):
        with self.lock:
            self.managerMedicos.Add(nomeMedico, morada, nif, cc, tel, especialidade)
        #self.SaveDataBase(self.DB)

    def UpdateMedico(self, nomeMedico, morada, nif, cc, tel, especialidade):
        with self.lock:
            self.managerMedicos.Update(nomeMedico, morada, nif, cc, tel, especialidade)
        #self.SaveDataBase(self.DB)

    def DeleteMedico(self, nomeMedico):
        with self.lock:
            self.managerMedicos.Delete(nomeMedico)
        #self.SaveDataBase(self.DB)

    def SelectMedico(self, nomeMedico):
        return self.managerMedicos.Get(nomeMedico)

    def GetMedicos(self):
        try:
            content = self.managerMedicos.GetAll()
            return content
        except Exception as ex:
            raise Exception(ex)

    def GetMedico(self, nomeMedico):
        try:
            content = self.managerMedicos.Get(nomeMedico)
            return content
        except Exception as ex:
            raise Exception(ex)

    def MedicosMaisReceitas(self):
        return self.managerMedicos.MedMaisReceitas()

    def MediaReceitaPorMedico(self, nomeMedico):
        return self.managerMedicos.MediaReceitasMedico(nomeMedico)


#-----------------------------------------------Utentes---------------------------------------------------------

    def AddUtente(self, idUtente, nomeUtente, morada, nif, cc, tel):
        with self.lock:
            self.managerUtentes.AddUtente(idUtente, nomeUtente, morada, nif, cc, tel)
        #self.SaveDataBase(self.DB)

    def UpdateUtente(self, idUtente, nomeUtente, morada, nif, cc, tel):
        with self.lock:
            self.managerUtentes.UpdateUtente(idUtente, nomeUtente, morada, nif, cc, tel)
        #self.SaveDataBase(self.DB)

    def DeleteUtente(self, idUtente):
        with self.lock:
            self.managerUtentes.DeleteUtente(idUtente)
        #self.SaveDataBase(self.DB)

    def selectUtente(self, idUtente):
        return self.managerUtentes.GetUtente(idUtente)

    def GetUtentes(self):
        try:
            content = self.managerUtentes.GetUtentes()
            return content
        except Exception as ex:
            raise Exception(ex)

    def GetUtente(self,idUtente):
        try:
            content = self.managerUtentes.GetUtente(idUtente)
            return content
        except Exception as ex:
            raise Exception(ex)

    def UtentesMaisReceitas(self):
        return self.managerUtentes.UtenteMaisReceitas()

    def MediaReceitaPorUtente(self,idUtente):
        return self.managerUtentes.MediaReceitasporUtente(idUtente)

    def UtentesGastadores(self):
        return self.managerUtentes.UtentesGastadores()


#--------------------------------------------------Farmacias-------------------------------------------------
    
    def CreateFarmacia(self, idFarm, nome, morada):
        with self.lock:
            listRec = self.DB.SelectAllFarmacias()
            if listRec == None:
                return 0
            for farmRec in listRec:
                if farmRec == idFarm:
                    raise IDJaExisteException ("Já existe essa identificação da Farmácia no Sistema")
            farmaciaRec = Farmacia(idFarm, nome, morada)
            self.DB.InsertFarmacias(farmaciaRec)
            self.DB.TStocks[idFarm]=list()
            self.DB.TAlarmes[idFarm] = list()
        #self.SaveDataBase(self.DB)
        return 1

    def GetFarmacias(self):
        content = []
        for val in self.DB.SelectAllFarmacias():            
            info = {}
            info["Farmacia Id"] = val.idFarm
            info["Nome"] = val.nome
            info["Morada"] = val.morada
            content.append(info)
        return content


#------------------------------------------------Receitas---------------------------------------------------------
    
    def InsertReceita(self,idFarmacia,idReceita, idUtente, nomeMedico, listMedicamentos):
        recMed = self.DB.SelectMedico(nomeMedico)
        if recMed == None:
            recMedic = Medico(nomeMedico, None, None, None, None, None)
            self.DB.InsertMedico(recMedic)
        recUt = self.DB.SelectUtente(idUtente)
        if recUt == None:
            recU = Utente(idUtente,None, None, None, None, None)
            self.DB.InsertUtente(recU)
        inStock= self.ValidarMedicamentos(listMedicamentos)
        if len(inStock) != 0:
            for stockRec in inStock:
                nomeMedicamento = stockRec["Nome"]
                medicamento = self.DB.SelectMedicamento(nomeMedicamento)
                if medicamento != None:
                    stock = self.SearchMedicamentoInStock(idFarmacia,nomeMedicamento)
                    if stock != None:
                        self.Pendente(stock, int(str(stockRec["Qt"])))
            rec = Receita(idFarmacia, idReceita, idUtente, nomeMedico, inStock)
            self.DB.InsertReceita(rec)
        else:
            return 0
        #self.SaveDataBase(self.DB)
            

    def Pendente(self, stock,qt):
        quantidade = stock.quantidade
        stock.condition.acquire()
        if int(qt) < quantidade:
            stock.quantidade -= qt
        else:
            stock.condition.wait()
            stock.quantidade -= qt
        stock.condition.release()
        return True
     
     
    def SearchMedicamentoInStock(self,idFarmacia,nomeMedicamento):
        try:
            listStock = self.DB.SelectStock(idFarmacia)
        except Exception as ex:
            listStock = list()
            print(ex)
        for item in listStock:
            stock = item
            if stock.nome == nomeMedicamento:
                return stock
        return None
        
    def ListarReceitas (self,idFarmacia):
        content = []
        listRec = self.DB.SelectAllReceita(idFarmacia)
        for r in listRec:
            info = {}
            info["Identificação da Receita"] = r.idReceita
            info["Identificação do Utente"] = r.idUtente
            info["Nome do Médico"] = r.nomeMedico
            info["Lista de Medicamentos"] = r.Medicamentos
            content.append(info)
        return content

#-----------------------------------------------------Stocks-------------------------------------------------------

    def UpdateStock(self,idFarmacia, nomeMedic, quantidade):
        stockRec = self.SearchMedicamentoInStock(idFarmacia,nomeMedic)
        if stockRec == None:
            rec = Stock(idFarmacia, nomeMedic, quantidade)
            self.DB.InsertStock(idFarmacia,rec)
        else:
            stockRec.condition.acquire()
            stockRec.quantidade += quantidade
            stockRec.condition.notify_all()
            stockRec.condition.release()
        
        return 1

    def ExisteFarmacia(self, idFarm):
        return self.DB.SelectFarmacia(idFarm)

    def ValidarMedicamentos(self, listMedicamentos):
        results = list()
        for item in listMedicamentos:
            r = item["Nome"]
            rec = self.DB.SelectMedicamento(r)
            if rec != None:
                results.append(item)
        return results
    
    def ListMedicamentoStock(self,idFarmacia):
        content = []
        listStock = self.DB.SelectStock(idFarmacia)
        for s in listStock:
            info = {}
            info["nome"] = s.nome
            info["quantidade"]= s.quantidade
            content.append(info)
        return content

    def AlarmeMedicamentos(self,idFarmacia):
        with self.lock:
            listStock = self.DB.SelectStock(idFarmacia)
            for s in listStock:
                if s.quantidade < 4:
                    rec = Stock(s.idFarm,s.nome,s.quantidade)
                    self.DB.InsertAlarme(idFarmacia,rec)
        #self.SaveDataBase(self.DB)

    def MedicamentosAlarme(self,idFarmacia):
        content = []
        listStock = self.DB.SelectAlarme(idFarmacia)
        for s in listStock:
            info = {}
            info["nome"] = s.nome
            info["quantidade"] = s.quantidade
            content.append(info)
        return content

    def MedicamentVendidos(self,idFarmacia):
        with self.lock:
            dic = dict()
            n = 0
            listReceitas = self.DB.SelectAllReceita(idFarmacia)
            for rec in listReceitas:
                for list in rec.Medicamentos:
                    n = list["Qt"]
                    if list["Nome"] in dic.keys():
                        dic[list["Nome"]] = int(dic[list["Nome"]]) + int(n)
                    else:
                        dic[list["Nome"]] = int(n)
            t = 0
            nome = []
            for i, j in dic.items():
                if int(j) < t:
                    nome = nome
                    t = t
                elif int(j) == t:
                    nome.append(i)
                    t = int(j)
                elif int(j) > t:
                    nome = []
                    nome.append(i)
                    t = int(j)
            return nome

    def loadDataBase(self):
        self.CreateFarmacia(1,"Oliveira","braga")
        self.CreateFarmacia(2, "Santos", "barcelos")
        self.CreateFarmacia(3, "Praça", "viladoconde")
        self.UpdateStock(1,"aspirina", 50)
        self.UpdateStock(1, "brufen", 34)
        self.UpdateStock(1, "benuron", 15)
        self.UpdateStock(2, "vitamina", 10)
        self.UpdateStock(2, "aspirina", 50)
        self.UpdateStock(2, "brufen", 20)
        self.UpdateStock(1,"medic1",2)
        self.AddMedicamento("aspirina",2)
        self.AddMedicamento("brufen", 1)
        self.AddMedicamento("benuron", 2)
        self.AddMedicamento("vitamina", 4)
        self.AddMedicamento("medic1", 1)
        qtMedic = 2
        count = 0
        listMedicamentos = []
        while (count < qtMedic):
            medicamento = "aspirina"
            qt = 2
            info = {}
            info['Nome'] = medicamento
            info['Qt'] = qt
            listMedicamentos.append(info)
            count = count + 1
        self.InsertReceita(1, 1, 1, "medico1", listMedicamentos)
        qtMedic = 2
        count = 0
        listMedicamentos = []
        while (count < qtMedic):
            medicamento = "brufen"
            qt = 1
            info = {}
            info['Nome'] = medicamento
            info['Qt'] = qt
            listMedicamentos.append(info)
            count = count + 1
        self.InsertReceita(1, 3, 1, "medico1", listMedicamentos)
        qtMedic = 2
        count = 0
        listMedicamentos = []
        while (count < qtMedic):
            medicamento = "brufen"
            qt = 2
            info = {}
            info['Nome'] = medicamento
            info['Qt'] = qt
            listMedicamentos.append(info)
            count = count + 1
        self.InsertReceita(1, 2, 1, "medico1", listMedicamentos)