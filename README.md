# FlyForce – Capteur de force 3-DOF à guidages flexibles

Projet réalisé dans le cadre du cours **Conception de mécanismes** à l’**EPFL** (Mai 2025) – **Groupe 28**

## 🎯 Objectif du projet

FlyForce est un **capteur de force tri-axial** basé sur un **mécanisme à guidages flexibles**. Il permet la mesure précise de forces de contact dans les trois directions de l’espace (\(x, y, z\)) à l’aide de **capteurs capacitifs**. Ce capteur est conçu pour équiper un stylet sphérique utilisé dans des machines de mesure tridimensionnelle (CMM), afin de contrôler la qualité géométrique des pièces mécaniques.

Le système doit respecter des contraintes strictes :
- Mesure de force dans une plage de ±5 N
- Résolution inférieure à 1.5 mN
- Insensibilité aux effets de la gravité et aux accélérations de la base
- Fonctionnement uniquement en translation (3 DOF)
- Durabilité (> 57 millions de cycles)

## 🧠 Principe de fonctionnement

Le cœur du système repose sur :
- **Un bloc central mobile** qui porte le stylet.
- **Trois soufflets** qui autorisent uniquement les 3 translations du bloc, en bloquant toutes les rotations.
- **Six membranes flexibles et rotules guidées** assurant l’équilibrage dynamique (force et moment).

### Guidage

Les soufflets sont des assemblages de deux lames flexibles inversées, permettant uniquement la translation du bloc central. Leur disposition empêche les rotations tout en autorisant des mouvements égaux dans chaque direction. Cela assure **une isotropie cinématique parfaite**.

### Équilibrage

Le mécanisme est :
- **Équilibré en force** : masse répartie pour que les quantités de mouvement se compensent (aucune force résultante transmise à la base).
- **Équilibré en moment** : pas de moment cinétique global.
- **Quasi-équilibré inertiellement** : au repos, le système est parfaitement équilibré ; pendant un déplacement, les erreurs inertiales sont faibles et contenues.

### Mesure

Les **capteurs capacitifs** sont montés entre le bâti et les faces du bloc central. Le déplacement de celui-ci est mesuré directement, sans pièces intermédiaires, garantissant une **mesure directe et précise** de la force appliquée.

## ⚙️ Architecture mécanique

Le système est conçu en **guidages flexibles**, avec :
- **Rotules à doigt guidée** (1 lame flexion/torsion) ;
- **Membranes flexibles** (3 lames parallèles modélisées comme 4 lames équivalentes) ;
- **Soufflets** (2 lames inversées) ;

Les pièces sont principalement usinées :
- Par **électroérosion** (pour les pièces flexibles) ;
- Par **fraisage** (pour les blocs rigides) ;
- Assemblées mécaniquement (vis, interfaces sandwich pour les membranes).

## 🧮 Fichiers du dépôt

Ce dépôt contient :
- tous les fichiers o
