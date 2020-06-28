# -*- coding: utf-8 -*-

class Receita():
    
    def __init__(self, idFarmacia, idReceita, idUtente, nomeMedico, listMedicamentos):
        self.idFarmacia=idFarmacia
        self.idReceita = idReceita
        self.idUtente=idUtente
        self.nomeMedico = nomeMedico
        self.Medicamentos=listMedicamentos 