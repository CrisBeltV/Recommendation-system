
#Función principal que dado un nombre de usuario dentreo de la BD identifica sus preferencias en 
# relación a la data presente de dicho usuarioe en la BD.
import pandas as pd


def RecommendationSystem(User):
    #Importamos datos de nuestra bd
    df_platos = pd.read_excel("data.xlsx", sheet_name='Platos')
    df_rankingUsers = pd.read_excel("data.xlsx", sheet_name='ranking')
    #Alistamos los datos para tratarlos
    df_platos['Lista_de_alimentos'] = df_platos.Lista_de_alimentos.str.split(' ')
    PlateswithFood_df = df_platos.copy()
    #Separamos cada alimentos y hacemos variables onehot/dummy
    PlateswithFood_df = SeparateFood(df_platos, PlateswithFood_df)
    print("PlateswithFood_df")
    print(PlateswithFood_df)
    #Indetificamos las preferencias del usuario 'User'
    UserPref = UserPreferences(df_platos,df_rankingUsers, User)#platosuser1
    print("UserPref")
    print(UserPref)
    #Perfilamos al usuario
    userProf = userProfile(UserPref, PlateswithFood_df) #recommendationTable_df
    print('userProf')
    print(userProf)
    #sacamos la lista ordenada de preferencias del usuario 'User'
    Top_ = Top_userPreferences(df_platos, userProf)
    print("Top_")
    print(Top_)
    return Top_


#Ordenamos los resultados
def Top_userPreferences(df_platos, recommendationTable_df):
    merged_inner = pd.merge(df_platos,recommendationTable_df.reset_index(), left_on='ID', right_on='ID')
    return merged_inner.sort_values(0, ascending=False)


def userProfile(platosuser1, PlateswithFood_df):
    
    userPlates = PlateswithFood_df[PlateswithFood_df['ID'].isin(platosuser1['ID_Plato'].tolist())]
    #Inicializando el índice para evitar problemas a futuro
    userPlates = userPlates.reset_index(drop=True)
    #Eliminar columna no utiles por el momento
    userGenreTable = userPlates.drop('ID', 1).drop('Nombre', 1).drop('Lista_de_alimentos', 1)
    userProfile = userGenreTable.transpose().dot(platosuser1['Ranking'])
    #Ahora llevemos los alimentos de cada plato al marco de datos original
    genreTable = PlateswithFood_df.set_index(PlateswithFood_df['ID'])
    #Y eliminemos información innecesaria
    genreTable = genreTable.drop('ID', 1).drop('Nombre', 1).drop('Lista_de_alimentos', 1)
    #Multiplicando alimentos por los pesos para luego calcular el peso promedio
    recommendationTable_df = ((genreTable*userProfile).sum(axis=1))/(userProfile.sum()) 
    return recommendationTable_df


#Hacemos oneHot/Dummy a la lista de alimentos
def SeparateFood(df_platos, PlateswithFood_df):

    for index, row in df_platos.iterrows():
         for genre in row['Lista_de_alimentos']:
            PlateswithFood_df.at[index, genre] = 1
    PlateswithFood_df = PlateswithFood_df.fillna(0)

    return PlateswithFood_df


def UserPreferences(df_platos,df_rankingUsers, User):

    id = int(df_rankingUsers[df_rankingUsers['UserName']==User].ID_user.head(1))
    platosuser1 = df_rankingUsers[df_rankingUsers['ID_user']==id].drop('UserName', 1).drop('frecuencia', 1).drop('ID_user', 1)
    #Filtrar los platos  por Id
    inputId = df_platos[df_platos['ID'].isin(platosuser1['ID_Plato'].tolist())]
    inputId=inputId.rename({'ID':'ID_Plato'}, axis=1)
    #Luego juntarlas para obtener el INPUT del usuario. Implícitamente, lo está uniendo por plato.
    platosuser1 = pd.merge(inputId, platosuser1)
    #Eliminando información que no utilizaremos del dataframe de entrada
    platosuser1 = platosuser1.drop('Lista_de_alimentos', 1)

    return platosuser1

