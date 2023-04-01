#!/usr/bin/env python
# coding: utf-8

# - Author: **Hatem Bou Hjar**
# - Date: **30/03/2022**

# - Ennonce
# 
# 1. Installer une base de données Mongodb
# 2. Iinsérer les données du fichier joint (tu peux t'aider du code ci-dessus).
# 3. Répondre aux exercices suivants en écrivant le code python :
#        a. Compter le nombre de femmes / d'hommes.
#        b. Écrire une fonction qui renvoie les entreprises de plus de N personnes.
#        c. Écrire une fonction qui prend en paramètre un métier et qui renvoie la pyramide des âges pour ce métier."

# # Importation des bibliotheques

# In[13]:


import json 
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import date
import plotly.graph_objects as gp


# # Fonction collection 

# In[3]:


def collection(uri):
    client = MongoClient(uri)
    database = client["rhobs"]
    collection = database["people"]
    return collection 


# # Fonction load

# In[4]:


def load (uri, datapath):
    coll = collection(uri = uri)
    with open(datapath,"r") as fp:
        data = json.load(fp)
        
        for person in data:
            coll.insert_one(person)        


# # Integration des donnees

# In[5]:


load(uri="mongodb://localhost:27017/", datapath="C:/Users/hatem/OneDrive/Desktop/Entretient stage rhodes/data.json")


# # Affichage du nombre des femmes

# In[6]:


nb_femmes = collection("mongodb://localhost:27017/").count_documents({"sex": "F"})
print("Nombre de femmes :", nb_femmes)


# # Affichage du nombre des hommes

# In[7]:


nb_hommes = collection("mongodb://localhost:27017/").count_documents({"sex": "M"})
print("Nombre de hommes :", nb_hommes)


# # Connection a la base des donnees

# In[8]:


mycollection = collection("mongodb://localhost:27017/")


# # Fonction trouver_entreprise

# In[9]:


def trouver_entreprise():  

    while True:
        try:
            nb_personne = int(input("Entrez le nombre de personne: "))
            break

        except ValueError:
            print("Entrez seulement des entiers")
            
    big_companies = mycollection.aggregate([
        {"$group": {"_id": "$company", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gte": nb_personne}}}
    ])
    resultat = list(big_companies)
    if  not resultat:
        print("Pas de company avec ce nombre de personne")
    else:
        return ["entrprise: " + company["_id"] for company in resultat]
    
trouver_entreprise()


# # Fonction pyramide_age

# In[14]:


def pyramide_age(travail):
    
    entreprise = mycollection.find({"job": travail})

    male_ages = []
    female_ages = []
    for person in entreprise:
        birthdate = date.fromisoformat(person["birthdate"])
        age = relativedelta(date.today(), birthdate).years
        if person["sex"] == "M":
            male_ages.append(age)
        elif person["sex"] == "F":
            female_ages.append(age)

    x_M = [-age for age in male_ages]
    x_F = female_ages
    y_age = [f"{i*10}-{(i+1)*10-1}" for i in range(10)]

    fig = gp.Figure()

    fig.add_trace(gp.Bar(y=y_age, x=x_M, 
                         name='Male', 
                         orientation='h'))

    fig.add_trace(gp.Bar(y=y_age, x=x_F,
                         name='Female', 
                         orientation='h'))

    fig.update_layout(title=f"Pyramide age {travail}",
                      title_font_size=22, 
                      barmode='relative',
                      bargap=0.0, 
                      bargroupgap=0,
                      xaxis=dict(tickvals=[-80, -60, -40, -20, 0, 20, 40, 60, 80],
                                 ticktext=['80+', '70-79', '60-69', '50-59', '40-49', '30-39', '20-29', '10-19', '0-9'],
                                 title='Age',
                                 title_font_size=14),
                      yaxis=dict(title='Number of people',
                                 title_font_size=14)
                      )

    fig.show()


# In[15]:


pyramide_age("aérodynamicien")

