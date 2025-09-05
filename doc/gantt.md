---
config:
  theme: neo
---
gantt
    dateFormat  YYYY-MM-DD
    axisFormat  %d %b
    title       Diagramme de Gantt
    section Suivi
    Practical 1 et Follow-up 1   :milestone, 2025-08-29,
    Practical 2 et Follow-up 2   :milestone, 2025-09-05,
    Practical 3 et Follow-up 3   :milestone, 2025-09-12,
    TP4                          :milestone, 2025-09-19,
    Suivi 4                      :milestone, 2025-10-03,
    3j immersion                 :active,    2025-11-04, 3d
    Suivi 7                      :milestone, 2025-11-14,
    section Rendu
    Dossier Analyse              :milestone, 2025-09-27,
    Rapport + Code               :milestone, 2025-11-22,
    Soutenance                   :milestone, 2025-12-10,
    section Vac
    Toussaint                    :crit,      2025-10-25, 9d

    section Analyse
    analyse sujet                :done,      2025-08-29, 29d
    rédaction                    :active,    2025-09-15, 12d

    section Modélisation
    diagramme de cas d'utilisation :active,    2025-09-05, 7d
    diagramme d'activité           :active, 2025-09-14, 13d
    diagramme de classe           :active, 2025-09-14, 13d

    section Code
    coder une v0                 :active,    2025-09-29, 14d
    filtres                      :active,    2025-10-13, 7d
    recherche sémantique         :active,    2025-10-20, 21d
    API                          :active,    2025-11-10, 7d

    section Rapport
    rédaction                    :active,    2025-11-03, 19d
