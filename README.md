# les-francaises-et-francais-audiovisuel

Projet data d’analyse de l’information télévisée en France à partir de données ouvertes publiées par l’INA.

## Objectifs
- analyser la répartition thématique des journaux télévisés ;
- analyser la représentation femmes / hommes dans les contenus télévisés.

## Stack
Python, pandas, PostgreSQL, FastAPI, Streamlit

## Origine du projet

Ce projet s’inscrit dans le cadre du défi **« Les Françaises et Français face à l’information »**, proposé sur la plateforme **defis.data.gouv.fr** dans le programme **Open Data University**.

Le défi invite à explorer plusieurs dimensions du paysage informationnel français, notamment :
- l’évolution des thèmes diffusés à la télévision et à la radio ;
- la représentation des femmes dans les émissions ;
- le rapport des Françaises et des Français à l’information.

Dans ce projet, le périmètre a été volontairement resserré autour de deux axes principaux :
- l’analyse de l’offre d’information télévisée à travers les thématiques des JT ;
- l’analyse de la représentation femmes / hommes dans les contenus télévisés.

## Sources de données

Ce projet repose sur deux jeux de données principaux publiés par l’INA :

| Jeu de données | Période | Périmètre | Usage dans le projet |
|---|---|---|---|
| **Classement thématique des sujets de journaux télévisés** | 2000–2020 | JT du soir de TF1, France 2, France 3, Arte et M6 | Analyse de l’offre d’information et des thématiques |
| **Temps de parole des hommes et des femmes à la télévision et à la radio** | 1995–2019 | TV + radio dans la source, **TV uniquement** dans le projet | Analyse de la représentation femmes / hommes |