from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.lista_meteo = []

    def trova_umidita_media(self, mese):
        if len(self.lista_meteo) == 0:
            self.lista_meteo = MeteoDao.get_all_situazioni()
        lista_meteo_mensile = []
        for sit in self.lista_meteo:
            if sit.data.month == int(mese):
                lista_meteo_mensile.append(sit)
        lista_meteo_mensile_genova = []
        lista_meteo_mensile_milano = []
        lista_meteo_mensile_torino = []
        um_ge = 0
        um_to = 0
        um_mi = 0
        for sit in lista_meteo_mensile:
            if sit.localita == "Genova":
                lista_meteo_mensile_genova.append(sit)
            if sit.localita == "Milano":
                lista_meteo_mensile_milano.append(sit)
            if sit.localita == "Torino":
                lista_meteo_mensile_torino.append(sit)
        for sit in lista_meteo_mensile_genova:
            umidita = sit.umidita
            um_ge += umidita
        um_ge = um_ge / len(lista_meteo_mensile_genova)
        for sit in lista_meteo_mensile_milano:
            umidita = sit.umidita
            um_mi += umidita
        um_mi = um_mi / len(lista_meteo_mensile_milano)
        for sit in lista_meteo_mensile_torino:
            umidita = sit.umidita
            um_to += umidita
        um_to = um_to / len(lista_meteo_mensile_torino)
        return um_ge, um_mi, um_to

    def trova_umidita_primi_15(self, mese):
        if len(self.lista_meteo) == 0:
            self.lista_meteo = MeteoDao.get_all_situazioni()
        diz_meteo_mensile_by_city = {}
        for sit in self.lista_meteo:
            if sit.data.month == int(mese) and sit.data.day <= 15:
                city = sit.localita
                if city not in diz_meteo_mensile_by_city:
                    diz_meteo_mensile_by_city[city] = []
                diz_meteo_mensile_by_city[city].append(sit)

        for city in diz_meteo_mensile_by_city:  # Itera direttamente sulle chiavi del dizionario
            diz_meteo_mensile_by_city[city] = sorted(diz_meteo_mensile_by_city[city], key=lambda x: x.data.day)

        return diz_meteo_mensile_by_city
