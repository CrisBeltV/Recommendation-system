from main import RecommendationSystem
import random
import re
import pandas as pd


from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar

class ConverterApp(MDApp):

#Creamos nuevos valroes no existentes para los nuevos registros
    def newValue(self,a,rank=1000):
        newVal= random.randint(0, rank)
        while newVal in a:
            newVal = random.randint(0, rank)
        return newVal
#Creamos nuevos ids de usuarios no existentes para los nuevos registros, los antiguos crean +
#un nuevo registro pero no un nuevo usuario ni id de usuario logicamente.
    def newUserID(self, list,Name):
        if not Name in list.UserName.values:
            return self.newValue(list.ID_user.values, rank=100)
        else:
          return int(list[list['UserName']==Name].ID_user.head(1))

#Nuevo registrro y actualización de la BD
    def NewRegis(self, Name, FoodList, rank):

        df_platos = pd.read_excel("data.xlsx", sheet_name='Platos')
        df_rankingUsers = pd.read_excel("data.xlsx", sheet_name='ranking')

        newId_plato = self.newValue(df_platos.ID.values)
        temp_string = str(df_platos.Nombre.values)
        PlateListNum = [float(s) for s in re.findall(r'-?\d+\.?\d*', temp_string)]
        newNamePlate = "Plato"+str(self.newValue(PlateListNum))

        df_platos = df_platos.append({'ID':newId_plato, 'Nombre':newNamePlate, 'Lista_de_alimentos':FoodList}, ignore_index=True)
        ID_user = self.newUserID(df_rankingUsers ,Name)


        df_rankingUsers= df_rankingUsers.append({'ID_Plato':newId_plato, 'ID_user':ID_user, 'UserName':Name, 'Ranking': rank}, ignore_index=True)

        with pd.ExcelWriter("data.xlsx") as writer:
            df_platos.to_excel(writer, sheet_name="Platos", index=False)  
            df_rankingUsers.to_excel(writer, sheet_name="ranking",index=False) 



    def flip(self):
        # Cambio de estado de la App
        if self.state == 0:
            self.state = 1
            self.toolbar.title = "Ordenar"
            self.inputName.text = "Nombre de usuario existente/nuevo"
            
            #Mostramos los input de lista y calificación

            self.inputFoodList.height= 1
            self.inputFoodList.size_hint_y= 0.1
            self.inputFoodList.opacity= 1
            self.inputFoodList.disabled= False

            self.inputRank.height= 1
            self.inputRank.size_hint_y= 0.1
            self.inputRank.opacity= 1
            self.inputRank.disabled= False
            

        else:
            self.state = 0
            self.toolbar.title = "Recomiendame"
            self.inputName.text = "Nombre de usuario"
            #Escondemos los input de lista y calificación
            self.inputFoodList.height= 0
            self.inputFoodList.size_hint_y= None
            self.inputFoodList.opacity= 0
            self.inputFoodList.disabled= True

            self.inputRank.height= 0
            self.inputRank.size_hint_y= None
            self.inputRank.opacity= 0
            self.inputRank.disabled= True

        self.responseList.text = ""
        self.labelName.text = ""

    def process_fun(self, args):
        # la función encutra Ordenar/recomendar por igual
        if self.state == 0:
            # <Ordenar> comida pasa a <recomendar> comida
            User = self.inputName.text
            dataUser_ = RecommendationSystem(User)
            self.labelName.text = 'Le recomendamos el '+ str(dataUser_['Nombre'].iloc[0])
            val = str(dataUser_['Lista_de_alimentos'].iloc[0])
            
        else:
            # <Recomendar> comida pasa a <ordenar> comida
            val =   self.inputFoodList.text 
            self.labelName.text = "Para Nombre: "+ self.inputName.text
            self.responseRanking.text= ":)#"+self.inputRank.text
            self.NewRegis(self.inputName.text, val, self.inputRank.text)
            

        self.responseList.text = val

    def build(self):
        self.state = 0 #Estado inicial
        #self.theme_cls.primary_palette = "DeepOrange"
        screen = MDScreen()

        # top toolbar
        self.toolbar = MDToolbar(title="Recomiendame :)")
        self.toolbar.pos_hint = {"top": 1}
        self.toolbar.right_action_items = [
            ["rotate-3d-variant", lambda x: self.flip()]]
        screen.add_widget(self.toolbar)

        # logo
        screen.add_widget(Image(
            source="logo.png",
            pos_hint = {"center_x": 0.5, "center_y":0.75}
            ))

        # first in run
        self.inputName = MDTextField(
            text="Nombre de usuario: ",
            halign="center",
            size_hint = (0.8,1),
            pos_hint = {"center_x": 0.5, "center_y":0.60},
            font_size = 22
        )


        
        self.inputFoodList = MDTextField(
            text="Lista de ingredientes: ",
            halign="center",
            size_hint = (0.5,1),
            pos_hint = {"center_x": 0.5, "center_y":0.5},                
            font_size = 22
            )

        self.inputRank = MDTextField(
            text="Calificación: ",
            halign="center",
            size_hint = (0.5,1),
            pos_hint = {"center_x": 0.5, "center_y":0.40},                
            font_size = 22
            )

        screen.add_widget(self.inputFoodList)

        screen.add_widget(self.inputName)
        
        screen.add_widget(self.inputRank)

        self.inputFoodList.height,self.inputRank.height= 0,0
        self.inputFoodList.size_hint_y,self.inputRank.hesize_hint_yight= None,None
        self.inputFoodList.opacity, self.inputRank.opacity= 0,0
        self.inputFoodList.disabled, self.inputRank.disabled= True, True



        #secondary + primary labels
        self.labelName = MDLabel(
            halign="center",
            pos_hint = {"center_x": 0.5, "center_y":0.3},
            theme_text_color = "Primary"
        )

        self.responseList = MDLabel(
            halign="center",
            pos_hint = {"center_x": 0.5, "center_y":0.25},
            theme_text_color = "Primary",
            font_style = "H5"
        )

        self.responseRanking = MDLabel(
            halign="center",
            pos_hint = {"center_x": 0.5, "center_y":0.2},
            theme_text_color = "Secondary",
            font_style = "H5"
        )
        
        screen.add_widget(self.labelName)
        screen.add_widget(self.responseList)
        screen.add_widget(self.responseRanking)


        # "Procesar" button
        screen.add_widget(MDFillRoundFlatButton(
            text="PROCESAR",
            font_size = 17,
            pos_hint = {"center_x": 0.5, "center_y":0.10},
            on_press = self.process_fun
        ))

        return screen

if __name__ == '__main__':
    ConverterApp().run()