#Definimos las constantes
kbd0 = 0.1
ka = 0.01
ko2 = 1.4
DBOe = 20
ODe = 2
ODs = 9 
Vi = 110.9*(10**6) #Pasamos el volumen iniciar a m**3


def calcular_volumen_euler_explicito(Vi:float,h:int,cant_de_iter:int,lista_Qe:list,lista_Qs:list):
    lista = [] 
    j = 0
    contador = 0 


    V_i_mas_1 = Vi + h*(lista_Qe[j]-lista_Qs[j])
    lista.append(V_i_mas_1)


    for i in range(cant_de_iter):
        Vi = V_i_mas_1
        V_i_mas_1 = Vi + h*(lista_Qe[j]-lista_Qs[j])

        lista.append(V_i_mas_1)
        contador = contador + 1

        if contador == 31 :
            j = j + 1
            contador = 0 


    return lista


def calcular_DBO_OD_euler_explicito(lista_de_volumen:list, h:int,lista_Qe:list, lista_Qs:list):
    DBO_i = DBOe
    OD_i = ODe
    lista_DBO = []
    lista_OD = []
    j =  0 
    contador = 0

    for i in range(len(lista_de_volumen)):
        V = lista_de_volumen[i]
        DBO_i_mas_uno = DBO_i + h*( ((lista_Qe[j]*DBOe) / V ) - ( (lista_Qs[j]*DBO_i) / V) -kbd0*DBO_i*( (OD_i**2 ) / (OD_i**2 + ko2) ) ) #Quitamos G ya que solo aplica en OD
        
        OD_i_mas_uno = OD_i + h*( (( (lista_Qe[j]*ODe)/V ) - ((lista_Qs[j]* OD_i)/V ) )  - kbd0 * ( ( ((OD_i)**2) *(DBO_i) ) / ( (OD_i)**2 + ko2 ) )  + ka*(ODs- OD_i) ) #Volvemos a escribir G
    
        lista_DBO.append(DBO_i_mas_uno)
        lista_OD.append(OD_i_mas_uno)

        DBO_i = DBO_i_mas_uno
        OD_i = OD_i_mas_uno

        contador = contador + 1

        if contador == 31:
            j = j + 1

            contador = 0 


    return lista_DBO, lista_OD

def calcular_error(lista_Dbo_sol_exacta:list, lista_Od_sol_exacta:list , lista_Dbo_h:list, lista_Od_h:list):
    lista_e_od = []
    lista_e_dbo = []

    for i in range(len(lista_Od_sol_exacta)):
        e_od = abs(lista_Od_sol_exacta[i] - lista_Od_h[i])
        e_dbo = abs(lista_Dbo_sol_exacta[i] - lista_Dbo_h[i])

        lista_e_od.append(e_od)
        lista_e_dbo.append(e_dbo)

    return lista_e_dbo, lista_e_od

def main() -> None:
    lista_Qe = [518400,777600,1036800,1296000,1641600,2160000,2160000,1555200,1209600,864000,604800,518400] #Pasamos el caudal a dias M**3/ Dia
    lista_Qs = [0,0,1036800,1296000,1641600,3801600,2937600,1555200,1209600,864000,0,0]
    lista_volumen = calcular_volumen_euler_explicito(Vi,1,365,lista_Qe,lista_Qs)
    lista_DBO_h,lista_OD_h = calcular_DBO_OD_euler_explicito(lista_volumen,0.5,lista_Qe,lista_Qs)
    lista_dbo_sol_exacta ,lista_od_sol_exacta= calcular_DBO_OD_euler_explicito(lista_volumen,0.001,lista_Qe,lista_Qs)

    lista_e_dbo , lista_e_od = calcular_error(lista_dbo_sol_exacta,lista_od_sol_exacta,lista_DBO_h,lista_OD_h)

    print(lista_e_dbo)
main()