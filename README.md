# Mini-projet : Propagation radio urbaine sous l'effet de l'humidité et de la pluie
**Réaliser par :** ETTAKI Salma & ELBADRI Adam  
**Encadrer par :** Mr.ELMAMOUNI
**Formation :** Cycle Ingénieur, Génie des Télécommunications (GSR1)  
**Établissement :** ENSA Tanger  
**Module :** Propagation des ondes électromagnétiques  

---
## 1.Contexte et objectif

Ce mini-projet étudie l'influence de la fréquence, de la distance, de la pluie et de l'humidité sur une liaison radio en environnement urbain. Le dépôt fournit un simulateur interactif autonome en HTML et JavaScript. Il permet de distinguer les pertes du trajet de propagation des atténuations météorologiques, puis d'observer leurs effets sur la puissance reçue et le rapport signal sur bruit (SNR).

L'objectif est d'évaluer quantitativement dans quelles situations les effets météorologiques peuvent devenir importants, en particulier aux fréquences millimétriques, sans les confondre avec les pertes urbaines liées aux obstacles et au modèle de propagation choisi.
## 2. Scénarios et Paramètres de Simulation

Le simulateur permet de configurer et d'analyser les paramètres suivants :

- **Fréquence :** Entre 1 et 100 GHz, avec des préréglages à 2,4, 5, 10, 28 et 60 GHz.
- **Distance :** Entre 0,1 et 5 km.
- **Pluie :** Intensité comprise entre 0 et 100 mm/h, avec choix de la polarisation (horizontale, verticale ou circulaire).
- **Humidité et Température :** Humidité relative de 0 à 100 % et température de -20 à 40 °C (la pression atmosphérique étant fixée par défaut).
- **Modèle de trajet :** Espace libre (Friis) ou scénarios urbains simplifiés LOS/NLOS.
- **Paramètres RF :** Puissance d'émission, gains d'antennes, bande passante (20 MHz) et facteur de bruit.

## 3. Modèles Physiques et Implémentation

### A. Modélisation théorique (Recommandations UIT-R)
- **Espace libre :** Calcul de l'affaiblissement de propagation selon le modèle de Friis.
- **Pluie (UIT-R P.838-3) :** Calcul de l'atténuation spécifique $\gamma_R = k \cdot R^\alpha$ en fonction de la fréquence, de la polarisation et de l'intensité de la pluie supposée uniforme sur le trajet.
- **Gaz atmosphériques (UIT-R P.676-13) :** Estimation pédagogique des contributions de l'oxygène et de la vapeur d'eau, mettant en évidence les pics d'absorption (vapeur d'eau autour de 22 GHz et oxygène autour de 60 GHz).
- **Propagation urbaine (UIT-R P.1411-13) :** Scénarios LOS et NLOS combinés aux pertes en espace libre.

  Les pertes du trajet, de la pluie et des gaz sont cumulées pour calculer la puissance reçue. Le SNR est ensuite calculé  à partir du bruit thermique, de la bande passante et du facteur de bruit. L'interface affiche également la contribution des différentes pertes et un seuil indicatif de SNR de 10 dB.

### B. Architecture Logicielle Python
Afin de compléter l'application web interactive par un code exécutable et modulaire sur le dépôt GitHub, les scripts suivants ont été implémentés :
- **`config.py` :** Centralise l'ensemble des constantes physiques et des paramètres de simulation.
- **`propagation_models.py` :** Regroupe les fonctions mathématiques des modèles de propagation (FSPL, UIT-R P.838, bruit thermique).
- **`main.py` :** Script principal d'exécution et de génération des courbes de performance.
  
## 4. Hypothèses et Validation Numérique

Avant d'analyser l'impact global de la propagation, les hypothèses et la rigueur de l'implémentation numérique ont été validées selon les points suivants :

### A. Hypothèses de Calcul et Paramètres Fixes
- **Uniformité du milieu :** La pluie et l'humidité sont considérées comme homogènes le long du trajet de propagation pour chaque simulation ponctuelle.
- **Conditions de référence :** Les calculs comparent un état de référence (temps sec, $RH = 50\,\%$ sans précipitation) à des scénarios dégradés (pluie intense jusqu'à $100\text{ mm/h}$).
- **Bande passante et Bruit :** Le bruit thermique de référence est calculé sur une bande passante fixe (ex: $20\text{ MHz}$) avec un récepteur étalonné.

### B. Validation Numérique et Comportement des Modèles
- **Cohérence des fonctions Python :** Les scripts modulaires (`propagation_models.py`) ont été testés par validation croisée des fonctions mathématiques (notamment la vérification que l'atténuation de Friis tend vers les valeurs théoriques attendues en espace libre lorsque $R = 0$).
- **Stabilité des calculs de l'UIT-R :** Les approximations numériques des recommandations P.838 et P.676 montrent une continuité correcte sur toute la plage de fréquences de $1$ à $100\text{ GHz}$, confirmant l'absence d'aberrations numériques aux pics d'absorption.
## 5. Visualisations du Tableau de Bord

Afin d'offrir une lecture intuitive et graphique des simulations, l'application interactive intègre un tableau de bord structuré comprenant :

- **Évolution du SNR en fonction de la distance :** Comparaison en temps réel entre le temps sec et les conditions météorologiques sélectionnées, avec affichage clair du seuil de coupure minimal (fixé à $10\text{ dB}$).
- **Atténuation spécifique de la pluie :** Courbes de l'atténuation spécifique $\gamma_R$ ($\text{dB/km}$) en fonction de l'intensité des précipitations ($0$ à $100\text{ mm/h}$) pour les différentes bandes de fréquences étudiées ($2{,}4$, $5$, $10$, $28$ et $60\text{ GHz}$).
- **Spectre de l'atténuation atmosphérique :** Balayage fréquentiel de $1$ à $100\text{ GHz}$ mettant en évidence les contributions des gaz et les pics d'absorption caractéristiques (vapeur d'eau autour de $22\text{ GHz}$ et oxygène autour de $60\text{ GHz}$).
- **Indicateurs et bilan de liaison :** Répartition quantitative des pertes globales (trajet, pluie, gaz) et calcul instantané de la puissance reçue $P_r$ au point de fonctionnement courant.

  
  ## 6. Résultats et Analyse des Performances

Les simulations menées via le script Python et l'interface interactive permettent d'évaluer concrètement l'impact combiné de la distance, de la fréquence et des conditions météorologiques sur le bilan de liaison :

- **Atténuation en espace libre (FSPL) :** Les courbes de puissance reçue ($P_r$) en fonction de la distance traduisent la décroissance logarithmique usuelle, d'autant plus prononcée que la fréquence de la porteuse est élevée.
- **Impact de la pluie et des intempéries :** 
  - Aux basses fréquences ($2{,}4\text{ GHz}$ et $5\text{ GHz}$), l'atténuation additionnelle liée à la pluie (même intense, de l'ordre de $50$ à $100\text{ mm/h}$) reste très faible sur une courte liaison urbaine.
  - Aux fréquences millimétriques ($28\text{ GHz}$ et $60\text{ GHz}$), l'atténuation spécifique devient en revanche critique et provoque une chute abrupte de la puissance reçue.
- **Évolution du Rapport Signal sur Bruit (SNR) :** En confrontant le SNR au seuil minimal de réception fixé (par exemple $10\text{ dB}$), on observe une réduction drastique de la portée maximale de la liaison en présence de fortes précipitations, en particulier pour les bandes 5G et au-delà.
  

  ## 7. Interprétation Physique :

###  Précision scientifique et distinction des effets
Une conclusion physique fondamentale de cette étude réside dans la séparation stricte entre les différentes sources d'atténuation sur une liaison radio urbaine :
- **Aux fréquences usuelles ($2{,}4\text{ GHz}$ et $5\text{ GHz}$) :** Sur des distances urbaines courtes (de l'ordre du kilomètre), l'atténuation directement imputable à l'humidité de l'air ou aux précipitations reste extrêmement faible, voire négligeable. Il est donc crucial de ne pas confondre les pertes météorologiques avec les dégradations majeures subies par le signal, qui découlent en réalité des masquages par les bâtiments, des réflexions sur les parois et des phénomènes de trajets multiples.
- **Aux fréquences élevées et millimétriques ($28\text{ GHz}$ et $60\text{ GHz}$) :** L'interaction entre l'onde électromagnétique et les gouttes d'eau ou les molécules gazeuses devient très forte. Les pertes météorologiques s'additionnent alors lourdement aux pertes de propagation urbaine.

## 8. Analyse des Limites du Modèle

Bien que le simulateur et les scripts fournissent des tendances quantitatives très exploitables, l'étude présente certaines limites théoriques :
- **Approximation des Recommandations UIT-R :** Les algorithmes s'inspirent des recommandations P.676-13, P.838-3 et P.1411-13 sans constituer une implémentation normative complète raie par raie.
- **Hypothèse de pluie uniforme :** Le calcul de l'atténuation suppose une précipitation homogène sur tout le trajet de liaison, ce qui peut tendre à surestimer les pertes sur de plus longues distances.
- **Paramètres environnementaux :** La pression atmosphérique et d'autres variables annexes restent fixées dans cette version ; les comparaisons doivent donc être interprédiées à conditions constantes.
## 9. Conclusion et Perspectives

Ce mini-projet a permis de concevoir une solution complète — combinant une application web interactive et une architecture logicielle Python modulaire — pour modéliser et analyser la propagation des ondes radio en milieu urbain. 

L'étude des modèles inspirés de l'UIT-R a démontré la robustesse des bandes de fréquences traditionnelles face aux intempéries, tout en soulignant la nécessité d'une marge de liaison renforcée pour l'exploitation des bandes millimétriques. 

Au-delà des résultats techniques, ce travail a revêtu un fort intérêt pédagogique pour notre formation d'ingénieur. 
Il nous a permis d'adopter une démarche d'évaluation quantitative rigoureuse, en évitant de supposer systématiquement qu'une augmentation de l'humidité ou de la pluie entraîne une forte dégradation du signal, et en apprenant à isoler précisément chaque facteur limitant du rapport signal sur bruit (SNR). 

En perspectives, l'intégration de données pluviométriques réelles et de profils de relief topographiques permettraient d'affiner encore davantage la précision de ces bilans de liaison.


## Exécution

Ouvrir le [simulateur de propagation radio](https://elbadriadam-bit.github.io/Projets-ondes-radio/simulateur_de_propagation_radio_uit_r%20(1).html) dans un navigateur. 
