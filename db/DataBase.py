# -*- coding: utf-8 -*-
from model.Medicamento import *
from model.Utente import *
from model.Medico import *
from model.Farmacia import *
from model.Stock import *

class DataBase():

    def __init__(self):
        self.TReceitas = dict()  # dict<key,value> when key is idFarm and value list<Receitas>
        self.TStocks = dict()    # dict<key,value> when key is idFarm and value list<Stocks>
        self.TAlarmes = dict()
        self.TFarmacias = dict()
        self.TMedicamentos = dict()
        self.TMedicos = dict()
        self.TUtentes = dict()

    #Farmacias
    
    def SelectAllFarmacias(self):
        try:
            return self.TFarmacias.values()
        except Exception as ex:
            return list()
   
    def InsertFarmacias(self,farmacia):        
        try:
            self.TFarmacias[farmacia.idFarm]= farmacia
        except Exception :
            raise Exception("Error insert farmacia in system...")

    def SelectFarmacia(self, idFarm):
        return self.TFarmacias[idFarm]
        
        
    #Stocks
    
    def InsertStock(self, idFarm, stock):
        listRec = self.TStocks[idFarm]
        listRec.append(stock)
        self.TStocks[idFarm] = listRec

    def SelectStock(self,idFarm):
        return self.TStocks[idFarm]
    
    def SelectAllStock(self,idFarm):
        return self.TStocks[idFarm] 

    def InsertAlarme(self, idFarm, stock):
        listRec = self.TAlarmes[idFarm]
        listRec.append(stock)
        self.TAlarmes[idFarm] = listRec

    def SelectAlarme(self, idFarm):
        return self.TAlarmes[idFarm]

    def DeleteAlarme(self,idfarm,nomeMedic):
        lmedicamentos = self.SelectAlarme(idfarm)
        for s in lmedicamentos:
            if s["nome"] == nomeMedic:
                del s



    #Receitas
    
    def InsertReceita(self,receita):
        try:
            lista = list()
            if receita.idFarmacia in self.TReceitas.keys():
                lista = self.TReceitas[receita.idFarmacia]
                lista.append(receita)
            else:
                lista.append(receita)
                self.TReceitas[receita.idFarmacia] = lista

        except Exception as ex:
            return 0

        return 1


    def SelectReceita(self,idFarm, idReceita):
        farm=self.SelectAllReceita(idFarm)
        for val in farm:
            if val.idReceita == idReceita:
                return val            
        return None

    def SelectAllReceita(self,idFarm):
        return self.TReceitas[idFarm]
    
    def DeleteReceita(self,receita):
        del self.TMedicamentos[receita.idReceita]   
        
    def UpdateReceita(self,receita):
        self.TMedicamentos[receita.idReceita]=receita  
        
    def SelectAllReceitaInSystem(self):
        return self.TReceitas.values()
    

    #Medicamentos
    
    def InsertMedicamento(self,medicamento):
        try:
            self.TMedicamentos[medicamento.nome] = medicamento
        except Exception as ex:
            return 0
        return 1

        
    def SelectMedicamento(self,nomeMedic):
        try:
            return self.TMedicamentos[nomeMedic]
        except Exception as ex:
            return None
    
    def SelectAllMedicamentos(self):
        return self.TMedicamentos.values() 
    
    def DeleteMedicamento(self,nomeMedic):
        try:
            del self.TMedicamentos[nomeMedic]
        except Exception as ex:
            return 0

        return 1

    def UpdateMedicamento(self, medicamento):
        try:
            self.TMedicamentos[medicamento.nome] = medicamento
        except Exception as ex:
            return 0
        return 1

      
    #Medicos
     
    def InsertMedico(self,medico):
        try:
            self.TMedicos[medico.Nome] = medico
        except Exception as ex:
            return 0
        return 1
    
    def SelectMedico(self,nomeMedico):
        try:
            return self.TMedicos[nomeMedico]
        except Exception as ex:
            return None

    def SelectAllMedicos(self):
        try:
            return self.TMedicos.values()
        except Exception as ex:
            return list()
    
    def DeleteMedico(self,nomeMedico):
        try:
            del self.TMedicos[nomeMedico]
        except Exception as ex:
            return 0
        return 1

    def UpdateMedico(self,medico):
        try:
            self.TMedicos[medico.Nome] = medico
        except Exception as ex:
            return 0
        return 1
        
    #Utentes
     
    def InsertUtente(self,utente):
        try:
            self.TUtentes[utente.idUtente] = utente
        except Exception as ex:
            return 0
        return 1
        
    def SelectUtente(self,idUtente):
        try:
            return self.TUtentes[idUtente]
        except Exception as ex:
            return None

    def DeleteUtente(self,idUtente):
        try:
            del self.TUtentes[idUtente]
        except Exception as ex:
            return 0
        return 1
        
    def UpdateUtente(self,utente):
        try:
            self.TUtentes[utente.idUtente] = utente
        except Exception as ex:
            return 0
        return 1

    def SelectAllUtentes(self):
        try:
            return self.TUtentes.values()
        except Exception as ex:
            return list()










