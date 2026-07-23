#!/usr/bin/env python3

"""
Validation config.txt
 format KEY=VALUE
 ignore les commentaire
 donnee obligatoire : WIDTH: int, HEIGHT: int, ENTRY: tuple[int, int], EXIT: tuple[int, int], OUTPUT_FILE, PERFECT: bool
 
Condition maze:
 entry != exit
 entry, exit dans le maze
 tou les case doivent etre connecte
 sans case isole
 coherence entre voisin: le meme mur = meme etat
 pas de zone trop ouverte (max 2 cases de large)
 PERFECT; un seul chemin

Fichier de sortie:
 1 chiffre hexa par case, une ligne par rangée
   FFFFFFFFFFFF
 coordonnee; entry, exit
 le chemin le plus court

Affichage visuel
 ASCII
 Doit montrer : murs, entrée, sortie, chemin solution
 Interactions : régénérer, montrer/cacher le chemin, changer les couleurs

"""