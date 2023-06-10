#Definimos las constantes
kbd0 = 0.1
ka = 0.01
ko2 = 1.4
DBOe = 20
ODe = 2
ODs = 9 
Qe = 518400 #Pasamos el caudal a dias M**3/ Dia
Qs = 0
Vi = 110.9 #Volumen inicial


def calcular_volumen_euler_explicito(Vi:float,h:int,cant_de_iter:int):
    lista = [] 
    V_i_mas_1 = Vi + h*(Qe-Qs)
    lista.append(V_i_mas_1)

    for i in range(cant_de_iter):
        Vi = V_i_mas_1

        V_i_mas_1 = Vi + h*(Qe-Qs)

        lista.append(V_i_mas_1)

    return lista


def calcular_dbo_euler_explicito(lista_de_volumen:list, h:int):
    DBO_i = DBOe
    OD_i = ODe
    lista_DBO = []
    lista_OD = []

    for i in range(len(lista_de_volumen)):
        V = lista_de_volumen[i]
        DBO_i_mas_uno = DBO_i + h*( ((Qe*DBOe) / V ) - ( (Qs*DBO_i) / V) -kbd0*DBO_i*( (OD_i**2 ) / (OD_i**2 + ko2) ) )
    
        OD_i_mas_uno = OD_i + h*( (( (Qe*ODe)/V ) - ((Qs* OD_i)/V ) ) - kbd0 * ( ( ((OD_i)**2) *(DBO_i) ) / ( (OD_i)**2 + ko2 ) )   )

        lista_DBO.append(DBO_i_mas_uno)
        lista_OD.append(OD_i_mas_uno)

        DBO_i = DBO_i_mas_uno
        OD_i = OD_i_mas_uno

    return lista_DBO, lista_OD



def main() -> None:
    lista_de_vol = calcular_volumen_euler_explicito(Vi, 1, 30)
    lista_DBO, lista_OD = calcular_dbo_euler_explicito(lista_de_vol,1)
    print(lista_OD)
main()