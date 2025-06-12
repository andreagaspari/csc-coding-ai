"""
Modulo per il calcolo del punteggio nel quiz.

Contiene funzioni che determinano il bonus basato sulla rapidità
e il punteggio finale da assegnare per ogni risposta, in base
alla correttezza e al tempo impiegato.

:author: Tuo Nome
:created: 2025-06-12
"""

from math import floor


def calculate_bonus(tempo: float, timeout: int) -> int:
    """
    Calcola il bonus in punti in base alla velocità di risposta.

    :param tempo: tempo impiegato per rispondere (secondi)
    :param timeout: tempo massimo consentito per la risposta
    :return: numero di punti bonus (0 se risposta lenta o oltre il timeout)
    """
    bonus = max(0, timeout - floor(tempo))
    return bonus


def calculate_score(is_correct: bool, tempo: float, timeout: int) -> int:
    """
    Calcola il punteggio da assegnare per una risposta.

    Se la risposta è corretta, si somma un punteggio base e il bonus.
    Se è errata o nulla, si sottrae una penalità base e un malus proporzionale al tempo residuo.

    :param is_correct: True se la risposta è corretta, False altrimenti
    :param tempo: tempo impiegato per rispondere (secondi)
    :param timeout: tempo massimo disponibile
    :return: punteggio (positivo o negativo)
    """
    base_score = 10       # punti per risposta corretta
    base_penalty = 5      # penalità minima per errore
    bonus = calculate_bonus(tempo, timeout)

    if is_correct:
        return base_score + bonus
    else:
        return -(base_penalty + bonus)
