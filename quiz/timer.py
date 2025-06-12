"""
Modulo per la gestione del tempo e dei timeout nel quiz.

Offre funzioni utili per:
- avviare un timer
- calcolare il tempo trascorso
- verificare se il tempo massimo è stato superato

:author: Tuo Nome
:created: 2025-06-12
"""

import time


def start_timer() -> float:
    """
    Restituisce il timestamp corrente di inizio.

    :return: tempo in secondi (float) dal riferimento dell’epoca (epoch)
    """
    return time.monotonic()


def elapsed_time(start: float) -> float:
    """
    Calcola il tempo trascorso dal momento di avvio.

    :param start: timestamp di inizio
    :return: tempo trascorso in secondi (float)
    """
    return time.monotonic() - start


def is_timeout(elapsed: float, timeout: int) -> bool:
    """
    Determina se è stato superato il limite massimo consentito.

    :param elapsed: tempo trascorso (secondi)
    :param timeout: tempo massimo concesso (intero, in secondi)
    :return: True se timeout superato, False altrimenti
    """
    return elapsed > timeout
