"""
Modulo di configurazione per il Quiz a scelta multipla.

Contiene la mappatura dei livelli di difficoltà verso i relativi parametri
operativi del quiz, come il numero di domande da presentare e il tempo
massimo consentito per rispondere a ciascuna domanda.

Questo modulo viene importato da:
- ui.py → per offrire la selezione della difficoltà all’utente;
- main.py → per impostare la sessione iniziale del quiz.

:author: Tuo Nome
:created: 2025-06-12
"""

from typing import Dict, Tuple

#: Dizionario che associa ciascun livello di difficoltà a una coppia di parametri.
#:
#: La chiave è un intero compreso tra 1 e 3:
#: - 1 → Facile
#: - 2 → Medio
#: - 3 → Difficile
#:
#: Ogni valore è una tupla formata da:
#: - numero_domande (int): quante domande includere nella sessione
#: - timeout (int): tempo massimo per risposta, in secondi
#:
#: Esempio:
#:     DIFFICULTY_SETTINGS[2] == (10, 10)  # 10 domande, 10 secondi ciascuna
DIFFICULTY_SETTINGS: Dict[int, Tuple[int, int]] = {
    1: (5, 15),    # Facile: meno domande, più tempo
    2: (10, 10),   # Medio: equilibrio tra tempo e quantità
    3: (15, 5)     # Difficile: più domande, meno tempo
}

#: Livello di difficoltà predefinito (medio), usato in caso di input errato
#: o dopo un numero massimo di tentativi falliti nella selezione della difficoltà.
DEFAULT_DIFFICULTY: int = 2
