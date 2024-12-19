<p align="center">
  <h1>projet ecommerce</h1>
  <strong>Analyse des ventes d'un site de ecommerce</strong>
</p>

## Introduction

Bonjour à tous, aujourd’hui, nous allons vous présenter le backend d’un projet d’analyse et de visualisation de données pour un site e-commerce. L’objectif de ce projet était de gérer les données efficacement, de calculer des KPIs et de les présenter de manière claire et interactive grâce aux technologies MongoDB, FastAPI et Streamlit.

---

### 1. Pourquoi MongoDB ?

MongoDB est une base de données NoSQL, ce qui signifie qu'elle est parfaitement adaptée pour gérer des données semi-structurées, comme celles d’un site e-commerce. Dans ce projet, les données des produits, des clients et des commandes sont variées et peuvent évoluer avec le temps, ce qui fait de MongoDB un choix idéal.

De plus, MongoDB permet d’effectuer des jointures complexes directement dans la base de données grâce à ses pipelines d’agrégation. Cela nous a permis de relier des informations, comme les commandes aux produits ou les clients à leurs commandes, afin de calculer des KPIs tels que les ventes par client ou par région, directement dans la base. Ce traitement de données est rapide et efficace.

Enfin, MongoDB est conçu pour être hautement scalable, c’est-à-dire qu’il peut facilement gérer un volume croissant de données. Cela est particulièrement important pour un projet comme le nôtre, qui peut évoluer et nécessiter le traitement de grandes quantités de données à mesure que le site se développe.

---

### 2. Pourquoi FastAPI ?

FastAPI est un framework web moderne et très performant pour créer des APIs. Il est particulièrement adapté aux projets nécessitant des performances élevées, car son architecture asynchrone permet de gérer plusieurs requêtes simultanées sans ralentir le système.

Une des grandes forces de FastAPI, c’est sa documentation automatique générée via Swagger. Cela permet à tout développeur de tester et d’interagir facilement avec l’API sans avoir à écrire de documentation supplémentaire, ce qui simplifie le développement et l'intégration.

FastAPI est aussi très efficace pour exposer des KPIs sous forme d'endpoints. Par exemple, nous avons utilisé FastAPI pour calculer et exposer des KPIs comme les ventes par client ou par produit, en utilisant des pipelines d'agrégation MongoDB pour effectuer des calculs sur les données avant de les envoyer via l'API.

---

### 3. Pourquoi Streamlit ?

Streamlit est un outil incroyable pour créer rapidement des tableaux de bord interactifs sans avoir besoin de connaissances poussées en développement frontend. Il permet de transformer des données brutes en visualisations claires et intuitives en quelques lignes de code.

Dans ce projet, Streamlit est utilisé pour afficher les KPIs calculés via l’API FastAPI. Grâce à des widgets interactifs, les utilisateurs peuvent filtrer et explorer les données en temps réel, ce qui facilite l'analyse des tendances et des performances. De plus, l’intégration avec FastAPI est très simple : Streamlit récupère les données de l'API via des appels HTTP pour les afficher sur l'interface utilisateur.

Streamlit est donc un excellent choix pour rendre les données et les KPIs accessibles, tout en offrant une expérience utilisateur fluide et interactive.

---

### 4. Pourquoi ce stack est optimal ?

Le choix de MongoDB, FastAPI et Streamlit n’est pas anodin. Ces technologies sont modernes, performantes et parfaitement adaptées à l’analyse et la visualisation de données dans un contexte e-commerce.

MongoDB nous permet de gérer les données de manière flexible et évolutive. FastAPI, quant à lui, nous donne une API rapide et facile à maintenir, avec une documentation automatique. Enfin, Streamlit nous permet de créer des tableaux de bord interactifs de manière simple, sans nécessiter un développement frontend complexe.

En combinant ces technologies, on obtient une solution complète, fluide et évolutive, capable de gérer des volumes de données importants tout en offrant une expérience utilisateur optimale. Ce stack est idéal pour un projet qui doit évoluer, être facile à maintenir et offrir une expérience utilisateur interactive et performante.

---

## Conclusion

En résumé, nous avons choisi MongoDB pour sa flexibilité et sa scalabilité, FastAPI pour sa rapidité et sa documentation automatique, et Streamlit pour sa simplicité et son interactivité. Ces technologies se complètent parfaitement pour créer une solution moderne d’analyse et de visualisation de données, idéale pour un projet e-commerce.

Nous vous remercions pour votre attention et nous sommes maintenant disponibles pour répondre à vos questions.


![image](https://github.com/user-attachments/assets/bb7a3842-3187-4f1b-ba6c-cfe69ccb4e1a)

