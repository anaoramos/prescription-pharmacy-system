# -*- coding: utf-8 -*-
import os 
import pickle
from db.DataBase import * 
from exceptions.NIFJaExisteException import *
from exceptions.CCJaExisteException import *
from exceptions.IDJaExisteException import *

class ManagerUtentes():
    def __init__(self,db):
        self.DB = db

    def AddUtente(self, idUtente, nomeUtente, morada, nif, cc, tel):
        utente = Utente(idUtente, nomeUtente, morada, nif, cc, tel)
        for rec in self.DB.SelectAllUtentes():
            if idUtente == rec.idUtente:
                raise IDJaExisteException("A identificação do utente que introduziu já existe no sistema")
            if nif == rec.NIF:
                raise NIFJaExisteException("O NIF do Utente que introduziu já existe no sistema")
            if cc == rec.CC:
                raise CCJaExisteException("O CC do Utente que introduziu já existe no sistema")
        self.DB.InsertUtente(utente)

    def GetUtente(self, idUtente):
        listRec = []
        recUtente = self.DB.SelectUtente(idUtente)
        if recUtente == None:
            raise Exception("Nao Encontrado")
        listRec.append(recUtente)
        return self.CreateInfoUtente(listRec)

    def UpdateUtente(self, idUtente, nomeUtente, morada, nif, cc, tel):
        utente = Utente(idUtente, nomeUtente, morada, nif, cc, tel)
        self.DB.UpdateUtente(utente)

    def GetUtentes(self):
        listRec= self.DB.SelectAllUtentes()
        return self.CreateInfoUtente(listRec)

    def DeleteUtente(self, idUtente):
        return self.DB.DeleteUtente(idUtente)

    def CreateInfoUtente(self,listRec):
        content = []
        for val in listRec:
                info = {}
                info["Identificação"] = val.idUtente
                info["Nome"] = val.Nome
                info["Morada"] = val.Morada
                info["NIF"] = val.NIF
                info["CC"] = val.CC
                info["Telemóvel"] = val.Tel
                content.append(info)
        return content

    def UtentesReceitas(self):
        UtentesReceitas = dict()
        for value in self.DB.TReceitas.values():
            for res in value:
                if res.idUtente in UtentesReceitas.keys():
                    UtentesReceitas[res.idUtente] += 1
                else:
                    UtentesReceitas[res.idUtente] = 1
        return UtentesReceitas

    def MediaReceitasporUtente(self, idUtente):
        sizeDic = 0
        listRec = self.DB.SelectAllReceitaInSystem()
        for val in listRec:
            size = len(val)
            sizeDic += size
        UtenteReceitas = self.UtentesReceitas()
        val = UtenteReceitas[idUtente]
        return (val / sizeDic)

    def UtenteMaisReceitas(self):
        UtenteReceitas = self.UtentesReceitas()
        t = 0
        idUtente = []
        for i, j in UtenteReceitas.items():
            if j < t:
                idUtente = idUtente
                t = t
            elif j == t:
                idUtente.append(i)
                t = j
            elif j > t:
                idUtente = []
                idUtente.append(i)
                t = j
        return idUtente

    def UtentesGastadores(self):
        dic = dict()
        n = 0
        for r in self.DB.SelectAllReceitaInSystem():
            for m in r:
                for i in m.Medicamentos:
                    n = i["Qt"]
                    if m.idUtente in dic.keys():
                        dic[m.idUtente] = int(dic[m.idUtente]) + int(n)
                    else:
                        dic[m.idUtente] = int(n)
        t = 0
        idUtente = []
        for i, j in dic.items():
            if int(j) < t:
                idUtente = idUtente
                t = t
            elif int(j) == t:
                idUtente.append(i)
                t = int(j)
            elif int(j) > t:
                idUtente = []
                idUtente.append(i)
                t = int(j)
        return idUtente


    def loadUtente(self):
        self.AddUtente(1, "utente1", "braga", 1, 1, 1111111)
        self.AddUtente(2, "utente2", "barcelos", 2, 2, 2222222)
        self.AddUtente(3, "utente3", "porto", 3, 3, 3333333)
        self.AddUtente(4, "utente4", "viladoconde", 4, 4, 4444444)
        self.AddUtente(5, "utente5", "braga", 5, 5, 5555555)
