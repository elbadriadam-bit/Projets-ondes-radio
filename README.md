# Mini-projet : propagation radio urbaine sous l'effet de l'humidité et de la pluie

**Module :** Propagation des ondes électromagnétiques

**Formation :** Cycle ingénieur, Génie des télécommunications

## Contexte et objectif

Ce mini-projet étudie l'influence de la fréquence, de la distance, de la pluie et de l'humidité sur une liaison radio en environnement urbain. Le dépôt fournit un simulateur interactif autonome en HTML et JavaScript. Il permet de distinguer les pertes du trajet de propagation des atténuations météorologiques, puis d'observer leurs effets sur la puissance reçue et le rapport signal sur bruit (SNR).

L'objectif est d'évaluer quantitativement dans quelles situations les effets météorologiques peuvent devenir importants, en particulier aux fréquences millimétriques, sans les confondre avec les pertes urbaines liées aux obstacles et au modèle de propagation choisi.

## Scénarios et paramètres

Le simulateur permet de régler :

- la fréquence entre 1 et 100 GHz, avec des préréglages à 2,4, 5, 10, 28 et 60 GHz;
- la distance entre 0,1 et 5 km;
- l'intensité de pluie entre 0 et 100 mm/h et sa polarisation (horizontale, verticale ou circulaire);
- l'humidité relative entre 0 et 100 % et la température entre -20 et 40 °C;
- le modèle de trajet : espace libre (Friis), ou scénarios urbains LOS/NLOS simplifiés;
- les paramètres de liaison RF : puissance d'émission, gains d'antennes, bande passante et facteur de bruit.

La pression atmosphérique n'est pas réglable dans cette version. Les comparaisons d'humidité doivent donc être interprétées à température et paramètres de liaison fixés.

## Modèles et calculs

- **Espace libre :** calcul de la perte de propagation selon Friis.
- **Pluie, inspirée de l'UIT-R P.838-3 :** calcul de l'atténuation spécifique à partir des coefficients dépendant de la fréquence et de la polarisation, puis cumul sur la distance en supposant une pluie uniforme le long du trajet.
- **Gaz atmosphériques, inspiré de l'UIT-R P.676-13 :** estimation pédagogique des contributions de l'oxygène et de la vapeur d'eau. La densité de vapeur dépend de l'humidité relative et de la température. Le spectre est une approximation des bandes d'absorption, et non le calcul complet raie par raie de la recommandation.
- **Propagation urbaine, inspirée de l'UIT-R P.1411-13 :** scénarios LOS et NLOS simplifiés, ajoutés à la perte en espace libre. Ils ne couvrent pas l'ensemble des géométries, environnements et procédures de la recommandation.

Les pertes du trajet, de la pluie et des gaz sont cumulées pour calculer la puissance reçue. Le SNR est ensuite calculé à partir du bruit thermique, de la bande passante et du facteur de bruit. L'interface affiche également la contribution des différentes pertes et un seuil indicatif de SNR de 10 dB.

## Visualisations

Le tableau de bord comprend :

- l'évolution du SNR en fonction de la distance, avec comparaison entre temps sec et conditions météo sélectionnées;
- l'atténuation spécifique de la pluie en fonction de son intensité pour les bandes 2,4, 5, 10, 28 et 60 GHz;
- le spectre de l'atténuation spécifique des gaz et de la pluie entre 1 et 100 GHz;
- les indicateurs de pertes totales, puissance reçue, SNR et marge, ainsi qu'une répartition des pertes de propagation.

La puissance reçue est donnée sous forme d'indicateur pour le point courant; le graphe en fonction de la distance représente le SNR, pas la puissance reçue. La version actuelle ne produit pas de carte de chaleur.

## Lecture des résultats et limites

À 2,4 et 5 GHz, l'atténuation directe due aux gaz et à la pluie est généralement faible sur une liaison courte par rapport aux pertes de propagation. Elle peut devenir plus marquée à fréquence élevée; le modèle gazeux fait notamment apparaître les bandes d'absorption de l'eau autour de 22 GHz et de l'oxygène autour de 60 GHz. Les pertes urbaines LOS/NLOS sont calculées séparément des pertes météo.

Les recommandations UIT-R P.676-13, P.838-3 et P.1411-13 inspirent les modèles, mais l'interface ne constitue pas une implémentation complète ni une validation normative de ces trois recommandations. Le tableau de synthèse présente les contributions calculées; il ne compare pas encore les résultats à un jeu de valeurs de référence indépendant. Pour un rapport scientifique, les hypothèses, unités, paramètres maintenus fixes et limites ci-dessus doivent être indiqués, et les valeurs doivent être confrontées à des références UIT-R indépendantes avant de conclure à une conformité.

## Exécution

Ouvrir [`https://elbadriadam-bit.github.io/Projets-ondes-radio/simulateur_de_propagation_radio_uit_r%20(1).html`]([simulateur_de_propagation_radio_uit_r%20(1).html](https://elbadriadam-bit.github.io/Projets-ondes-radio/simulateur_de_propagation_radio_uit_r%20(1).html)) dans un navigateur. Le chargement des bibliothèques et des graphiques nécessite une connexion Internet.

Le livrable actuel est le simulateur HTML/JavaScript. Il ne comprend pas de programme MATLAB/Python distinct ni de rapport scientifique séparé; ceux-ci peuvent être produits à partir des scénarios et résultats du simulateur.
