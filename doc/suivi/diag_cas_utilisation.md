@startuml
' à coller ici pour visualiser : https://www.plantuml.com/plantuml/uml/SyfFKj2rKt3CoKnELR1Io4ZDoSa70000
' doc : https://plantuml.com/fr/use-case-diagram


left to right direction

actor "Utilisateur"      as user
actor "Administrateur"   as admin
actor "Joueur"           as joueur

rectangle {
  usecase "S'inscrire"        as inscription
  usecase "S'authentifier"    as authentification
  usecase "Quitter"           as quitter
  usecase "Lister joueurs"    as lister_joueurs
}

joueur --> quitter

user --> inscription
user --> authentification
user --> quitter

admin --> quitter
admin --> lister_joueurs

@enduml
