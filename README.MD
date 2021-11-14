## L'emploie du temps synchronisé sur Discord !
En cours de development ! Ce bot Discord est configuré uniquement pour le groupe B1

### À quoi peut-il bien servir ?
Ce bot permet de synchroniser l'emploie du temps des BUT INFO vers Discord ! Il permet d'êtres notifier 30min a l'avance des cours qui vont suivre et permet de mieux s'organiser.
De plus, dans les jours a venir, il aura la possibilité de faire des rappels sur des contrôles ou bien des devoirs à faire sur les jours qui viennent

### Je veux le tester ! Je suis dans le groupe B1 !
Malheureusement, il n'est pas encore configurer pour du multi-guild car il est en cours de development mais si vous insistez, vous pouvez le démarrer.
Il vous suffit tous d'abord de crée un fichier `settings.json` et de mettre a l'interieur:
```json
{
  "TOKEN": "Votre_Token_Du_Bot_Discord",
  "USERNAME": "Votre_nom_d'utilisateur",
  "PASSWORD": "Votre_mot_de_passe"
}
```
Pour l'username et le password, ce n'est pas n'importe lesquels, c'est celui de l'ENT de l'IUT de Montreuil fournis par le département informatique !

Ensuite, une fois que votre fichier `settings.json` est créé, vous devez le lancer grâce à cette commande qui est la suivante:
```commandline
python3 ./bot.py
```
Si vous avez une erreur, essayez celui-ci:
```commandline
python ./bot.py
```
