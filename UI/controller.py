import copy

import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0
        self.costo_min = float("inf")
        self.sequenza_migliore = []

    def handle_umidita_media(self, e):
        mese = self._view.dd_mese.value
        (um_ge, um_mi, um_to) = self._model.trova_umidita_media(mese)
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel mese selezionato è: \n Genova: {um_ge} \n Milano: {um_mi} \n Torino: {um_to}"))
        self._view.update_page()

    def handle_sequenza(self, e):
        mese = self._view.dd_mese.value
        diz_citta = self._model.trova_umidita_primi_15(mese)

        def calculate_cost(lista):
            c = 0
            for i in range(len(lista) - 1):
                if i != 0:
                    if lista[i].localita != lista[i + 1].localita:
                        c += 1
            cc = 0
            for i in lista:
                cc += i.umidita
            costo_temp = cc + c * 100 + 200
            return costo_temp

        def controllo_citta(lista):
            citta = []
            for i in lista:
                citta.append(i.localita)
            for i in lista:
                if citta.count(i.localita) > 6:
                    return False
            return True

        def controllo_costo(lista, costo_min):
            c = 0
            for i in range(len(lista) - 1):
                if i != 0:
                    if lista[i].localita != lista[i + 1].localita:
                        c += 1
            cc = 0
            for i in lista:
                cc += i.umidita
            costo_temp = cc + c * 100 + 200
            if costo_temp > costo_min:
                return False
            else:
                return True

        def controllo_staz_min(lista, citta):
            if len(lista) == 1:
                if lista[-1].localita == citta:
                    return True
                else:
                    return False
            else:
                if lista[-1].localita == lista[-2].localita == citta:
                    return True
                else:
                    if len(lista) >= 4 and lista[-2].localita == lista[-3].localita == lista[-4].localita:
                        return True
                    else:
                        return False

        def recursive_optimize(days, current_sequence, diz_giorni_citta):
            # Provo tutte le possibili combinazioni e vedo quella di costo minore
            # Pago solo per i primi due giorni di stazionamento

            if days > 15:
                if calculate_cost(current_sequence) < self.costo_min:
                    self.costo_min = calculate_cost(current_sequence)
                    self.sequenza_migliore = copy.deepcopy(current_sequence)
                return

            for c in diz_giorni_citta:
                for giorno in range(len(diz_giorni_citta[c])):
                    if int(diz_giorni_citta[c][giorno].data.day) == int(days):
                        current_sequence.append(copy.deepcopy(diz_giorni_citta[c][giorno]))
                        if (controllo_citta(current_sequence) and controllo_costo(current_sequence, self.costo_min)
                                and controllo_staz_min(current_sequence, c)):
                            recursive_optimize(days+1, current_sequence, diz_giorni_citta)
                        current_sequence.pop()

        recursive_optimize(1, [], diz_citta)
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ha costo ottimo {self.costo_min} ed è:"))
        for seq in self.sequenza_migliore:
            self._view.lst_result.controls.append(ft.Text(f"    [{seq.localita} - {seq.data}] Umidità = {seq.umidita}"))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)


