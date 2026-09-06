Someicho - An python RPG game.

## En
This is a Python text-based RPG I've been building from the ground up to both practice and demonstrate my Python skills, along with the languages I speak. It's written entirely in base Python for its core game logic — no pygame or other game engine — as a deliberate exercise in building a full game loop, combat engine, and data-driven content system without leaning on a framework.

The game is fully playable in **three languages**: English, Portuguese, and French. Every player-facing string lives in `languages.json`, so the game logic itself never needs to know which language is active.

### Features
- **Turn-based combat** with speed-based initiative, elemental weaknesses/resistances, status effects (bleed, stun, defense buffs, taunt), and fleeing.
- **A job/class system** — nine base classes plus **Dragon**, a prestige class unlocked through story encounters, with switchable combat styles that change your available skillset mid-fight.
- **A 4-phase final boss fight**, with later phases dynamically escalating in power and callbacks to earlier bosses you've faced.
- **A full economy**: shops, a crafting system with material-based recipes, weighted loot tables, and sellable inventory.
- **A recruit and mission system** — party members join through branching story dialogue and side missions, not random encounters.
- **Save/load** with automatic backward-compatible field migration, so older saves don't break when new stats or systems are added.
- **The Tanban**, a minigame hub with:
  - A dice high-low betting game
  - A slot machine
  - A karaoke minigame with lyrics that light up as you hit the beat

### Running it
Requires only the Python standard library.
```
python Main.py
```

## Pt
Este é um RPG de texto em Python que venho desenvolvendo do zero para praticar e demonstrar minhas habilidades em Python, além dos idiomas que falo. Toda a lógica principal do jogo é escrita em Python puro — sem pygame ou qualquer motor de jogo — como um exercício deliberado de construir um loop de jogo completo, um sistema de combate e um sistema de conteúdo orientado a dados sem depender de um framework.

O jogo é totalmente jogável em **três idiomas**: inglês, português e francês. Todo texto voltado ao jogador vive em `languages.json`, então a lógica do jogo nunca precisa saber qual idioma está ativo.

### Funcionalidades
- **Combate por turnos** com iniciativa baseada em velocidade, fraquezas/resistências elementais, efeitos de status (sangramento, atordoamento, bônus de defesa, provocação) e fuga.
- **Sistema de classes** — nove classes base mais **Dragon**, uma classe de prestígio desbloqueada através de encontros da história, com estilos de combate alternáveis que mudam suas habilidades disponíveis no meio da luta.
- **Uma luta de chefe final com 4 fases**, cujas fases mais avançadas escalam dinamicamente em poder e fazem referência a chefes anteriores que você enfrentou.
- **Uma economia completa**: lojas, sistema de crafting com receitas baseadas em materiais, tabelas de loot ponderadas e inventário vendável.
- **Sistema de recrutamento e missões** — membros do grupo se juntam através de diálogos ramificados da história e missões paralelas, não por encontros aleatórios.
- **Salvar/carregar** com migração automática de campos compatível com versões antigas, então saves antigos não quebram quando novos atributos ou sistemas são adicionados.
- **O Tanban**, um hub de minijogos com:
  - Um jogo de apostas de dados (maior ou menor)
  - Uma caça-níqueis
  - Um minijogo de karaokê com letras que acendem conforme você acerta o ritmo

### Executando
Requer apenas a biblioteca padrão do Python.
```
python Main.py
```

## Fr
Ceci est un RPG textuel en Python que je développe depuis le début pour à la fois m'exercer et démontrer mes compétences en Python, ainsi que les langues que je parle. Toute la logique principale du jeu est écrite en Python pur — sans pygame ni aucun moteur de jeu — comme un exercice délibéré consistant à construire une boucle de jeu complète, un moteur de combat et un système de contenu piloté par les données sans dépendre d'un framework.

Le jeu est entièrement jouable en **trois langues** : anglais, portugais et français. Tout le texte destiné au joueur se trouve dans `languages.json`, donc la logique du jeu n'a jamais besoin de savoir quelle langue est active.

### Fonctionnalités
- **Combat au tour par tour** avec initiative basée sur la vitesse, faiblesses/résistances élémentaires, effets de statut (saignement, étourdissement, bonus de défense, provocation) et fuite.
- **Un système de métiers/classes** — neuf classes de base plus **Dragon**, une classe de prestige débloquée via des rencontres liées à l'histoire, avec des styles de combat interchangeables qui changent les compétences disponibles en plein combat.
- **Un combat de boss final à 4 phases**, dont les phases avancées augmentent dynamiquement en puissance et font référence aux boss précédemment affrontés.
- **Une économie complète** : boutiques, système de fabrication avec recettes basées sur des matériaux, tables de butin pondérées, et inventaire revendable.
- **Un système de recrutement et de missions** — les membres du groupe rejoignent l'équipe via des dialogues d'histoire ramifiés et des missions annexes, pas par rencontres aléatoires.
- **Sauvegarde/chargement** avec migration automatique des champs rétrocompatible, afin que les anciennes sauvegardes ne cassent pas lorsque de nouvelles statistiques ou systèmes sont ajoutés.
- **Le Tanban**, un centre de mini-jeux avec :
  - Un jeu de dés à pari haut/bas
  - Une machine à sous
  - Un mini-jeu de karaoké dont les paroles s'illuminent au rythme

### Lancer le jeu
Ne nécessite que la bibliothèque standard de Python.
```
python Main.py
```

---
