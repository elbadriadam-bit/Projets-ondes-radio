# Mini-projet : propagation radio urbaine sous pluie et humidité

## 1. Hypothèses et objectif

Ce mini-projet reproduit, sous une forme plus légère et exécutable, les modèles présentés dans le simulateur HTML du dépôt. L'objectif est d'évaluer l'impact de la fréquence, de la distance, de la pluie et de l'humidité relative sur une liaison radio en environnement urbain.

Les hypothèses principales sont les suivantes :
- la liaison est supposée en ligne de vue (LOS) ou en environnement urbain simplifié, ce qui justifie l'ajout d'une correction de type UIT-R P.1411 ;
- la perte géométrique de base est calculée par la formule de Friis ;
- l'atténuation due à la pluie est modélisée de manière pédagogique à partir d'une approximation de l'UIT-R P.838-3 : \(\gamma_R = k R^\alpha\) ;
- l'atténuation due aux gaz est estimée à partir d'une contribution combinée de l'oxygène et de la vapeur d'eau en s'appuyant sur les tendances de l'UIT-R P.676 ;
- les effets sont ajoutés linéairement en dB pour obtenir une estimation de la perte totale de propagation.

## 2. Modèles de calcul retenus

### 2.1 Perte de parcours

La perte de trajet en espace libre est donnée par :

\[
L_{FS} = 20\log_{10}(d) + 20\log_{10}(f) + 32.44
\]

avec :
- \(d\) en km,
- \(f\) en MHz.

Pour un environnement urbain simplifié, on ajoute une correction de type :

\[
L_{urban} = L_{FS} + \max(2,\ 6 + 10\log_{10}(d) + 0.5f)
\]

avec \(f\) en GHz.

### 2.2 Atténuation due à la pluie

L'atténuation spécifique est approximée par :

\[
\gamma_R = k R^\alpha
\]

et la perte sur la distance est :

\[
L_R = \gamma_R\, d
\]

où :
- \(R\) est l'intensité de pluie (mm/h),
- \(k\) et \(\alpha\) dépendent de la fréquence et de la polarisation.

### 2.3 Atténuation due aux gaz

On utilise une approximation pédagogique de la vapeur d'eau et de l'oxygène :

\[
\gamma_g = \gamma_{O_2} + \gamma_{H_2O}
\]

avec une densité de vapeur dépendant de l'humidité relative et de la température :

\[
\rho = \frac{216.7\, RH\, e_s(T)}{100(T+273.15)}
\]

et une contribution associée à la vapeur plus une absorption locale autour des bandes de résonance.

### 2.4 Rapport signal/bruit

Le bruit thermique au récepteur est estimé par :

\[
N = -174 + 10\log_{10}(B) + NF
\]

puis :

\[
SNR = P_r - N
\]

## 3. Hypothèses de validation numérique

Le script de calcul utilise des valeurs représentatives du projet :
- fréquence : 28 GHz ;
- distance : 1 km ;
- pluie : 25 mm/h ;
- humidité : 60 % ;
- température : 20 °C ;
- polarisation : circulaire, 45° ;
- puissance d'émission : 30 dBm ;
- gains d'antenne : 10 dBi (TX) et 5 dBi (RX) ;
- bande passante : 20 MHz ;
- facteur de bruit : 7 dB.

Les résultats numériques sont obtenus automatiquement par le programme Python, ce qui permet une validation rapide sans dépendre d'un navigateur.

## 4. Figures de simulation

Le script produit trois figures principales dans le dossier `figures/` :
1. `snr_vs_distance.png` : évolution du SNR en fonction de la distance pour des conditions sèches et humides ;
2. `rain_attenuation_curves.png` : atténuation spécifique due à la pluie pour plusieurs fréquences ;
3. `gas_and_rain_spectrum.png` : spectre d'absorption atmosphérique sur 1–100 GHz.

## 5. Interprétation physique des résultats

Les tendances attendues sont cohérentes avec la physique des ondes radio :
- la perte de trajet croît avec la distance et la fréquence ;
- la pluie devient déterminante aux fréquences millimétriques ;
- la vapeur d'eau et l'oxygène augmentent l'absorption atmosphérique, surtout autour des bandes de résonance ;
- la qualité du lien dépend fortement du compromis entre fréquence, distance et conditions météorologiques.

À 28 GHz, la pluie modérée ou forte peut devenir un facteur non négligeable, tandis que les pertes dues aux gaz restent généralement inférieures à celles dues au trajet et à la pluie sur des liaisons courtes à moyennes distances. En revanche, au-delà de quelques kilomètres, la contribution météorologique devient plus visible.

## 6. Limites du modèle

Le script est conçu comme un outil pédagogique et de validation numérique. Il ne remplace pas les recommandations complètes UIT-R P.676, P.838 et P.1411, qui intègrent des formulations plus détaillées et de nombreuses géométries de propagation. Le but est ici de reproduire les grands mécanismes physiques et de fournir une base de calcul exécutable et compréhensible.

## 7. Comment exécuter

```bash
pip install -r requirements.txt
python radio_propagation_simulation.py
```

Le programme affiche un résumé numérique dans le terminal et enregistre les figures dans le dossier `figures/`.

## 8. Conclusion

Le simulateur HTML contient déjà les éléments essentiels du projet ; le script Python fourni ici les rend exécutable, commenté et reproductible. Il constitue une base solide pour un rapport scientifique court, une validation numérique simple et une interprétation physique des mécanismes de propagation radio en milieu urbain.
