# -*- coding: utf-8 -*-
import os 
import pickle 
from model.Receita import *
from model.Farmacia import *
from model.Stock import *
from db.DataBase import * 
from exceptions.NIFJaExisteException import *
from exceptions.NomeJaExisteException import *
from exceptions.CCJaExisteException import *
from exceptions.IDJaExisteException import *

class ManagerMedicos():
    def __init__(self,db):
        self.DB = db

    def Add(self, nomeMedico, morada, nif, cc, tel, especialidade):
        medico = Medico(nomeMedico, morada, nif, cc, tel, especialidade)
        for rec in self.DB.SelectAllMedicos():
            if nomeMedico == rec.Nome:
                raise IDJaExisteException("O nome do Médico que introduziu já existe no sistema")
            if nif == rec.NIF:
                raise NIFJaExisteException("O NIF do Medico que introduziu já existe no sistema")
            if cc == rec.CC:
                raise CCJaExisteException("O CC do Medico que introduziu já existe no sistema")
        self.DB.InsertMedico(medico)

    def Get(self, nomeMedico):
        listRec = []
        rec = self.DB.SelectMedico(nomeMedico)
        if rec == None:
            return listRec
        listRec.append(rec)
        return self.CreateInfoMedico(listRec)

    def Update(self, nomeMedico, morada, nif, cc, tel, especialidade):
        rec = Medico(nomeMedico, morada, nif, cc, tel, especialidade)
        self.DB.UpdateMedico(rec)

    def GetAll(self):
        listRec= self.DB.SelectAllMedicos()
        return self.CreateInfoMedico(listRec)

    def Delete(self, nomeMedico):
        return self.DB.DeleteMedico(nomeMedico)


    def CreateInfoMedico(self,listRec):
        content = []
        for val in listRec:
                info = {}
                info["Nome"] = val.Nome
                info["Morada"] = val.Morada
                info["NIF"] = val.NIF
                info["CC"] = val.CC
                info["Telemóvel"] = val.Tel
                info["Especialidade"] = val.especialidade
                content.append(info)
        return content

    def MedicoRceitas(self):
        MedicoReceitas = dict()
        for value in self.DB.SelectAllReceitaInSystem():
            for res in value:
                if res.nomeMedico in MedicoReceitas.keys():
                    MedicoReceitas[res.nomeMedico] += 1
                else:
                    MedicoReceitas[res.nomeMedico] = 1
        return MedicoReceitas

    def MediaReceitasMedico(self, nomeMedico):
        sizeDic = 0
        for val in self.DB.SelectAllReceitaInSystem():
            size=len(val)
            sizeDic+=size
        MedicoReceitas = self.MedicoRceitas()
        #if len (MedicoReceitas) > 0:
        val = MedicoReceitas[nomeMedico]
        return (val / sizeDic)
        #else:
            #return 0

    def MedMaisReceitas(self):
        medicoReceitas = self.MedicoRceitas()
        t = 0
        nomeMedico = list()
        for i, j in medicoReceitas.items():
            if j < t:
                nomeMedico = nomeMedico
                t = t
            elif j == t:
                nomeMedico.append(i)
                t = j
            elif j > t:
                nomeMedico = list()
                nomeMedico.append(i)
                t = j
        return (nomeMedico, t)

    def loadUtente(self):
        self.Add("medico1", "braga", 10, 10, 1111111,"Esp1")
        self.Add("medico2", "barcelos", 20, 20, 2222222,"Esp3")
        self.Add("medico3", "porto", 30, 30, 3333333,"Esp2")
        self.Add("medico4", "viladoconde", 40, 40, 4444444,"Esp1")
        self.Add("medico5", "braga", 50, 50, 5555555,"Esp2")