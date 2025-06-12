"""
Modelli principali del quiz: Domanda e QuizSession.

- Domanda: rappresenta una singola domanda a scelta multipla.
- QuizSession: gestisce lo stato della sessione corrente (domande, punteggio, statistiche).

Utilizzato da:
- main.py → per orchestrare il quiz
- ui.py → per mostrare domande e raccogliere risposte
- score_calculator.py → per calcolare i punteggi

:author: Tuo Nome
:created: 2025-06-12
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class Domanda:
    """
    Rappresenta una singola domanda del quiz.

    :param testo: testo della domanda
    :param opzioni: dizionario delle opzioni (es. {"A": "...", "B": "...", ...})
    :param corretta: chiave della risposta corretta (es. "C")
    """
    testo: str
    opzioni: Dict[str, str]
    corretta: str


@dataclass
class QuizSession:
    """
    Gestisce lo stato di una sessione quiz: domande, punteggio e statistiche.

    :param domande: lista delle domande da presentare
    :param timeout: secondi disponibili per ciascuna risposta
    :param punteggio: punteggio totale corrente
    :param stats: dizionario delle statistiche (corrette, errate, tempi, ecc.)
    """
    domande: List[Domanda]
    timeout: int
    punteggio: int = 0
    stats: Dict[str, any] = field(default_factory=lambda: {
        "corrette": 0,
        "errate": 0,
        "saltate": 0,
        "tempi": [],
    })

    _index: int = 0  # indice interno della domanda corrente

    def next_question(self) -> Optional[Domanda]:
        """
        Restituisce la prossima domanda, oppure None se terminate.

        :return: Domanda successiva o None
        """
        if self._index < len(self.domande):
            domanda = self.domande[self._index]
            self._index += 1
            return domanda
        return None

    def record_answer(self, domanda: Domanda, risposta: str, tempo: float) -> Tuple[int, bool, bool]:
        """
        Registra una risposta, calcola il punteggio e aggiorna le statistiche.

        :param domanda: oggetto Domanda
        :param risposta: stringa "A"–"D" o "" se nulla
        :param tempo: tempo impiegato per rispondere
        :return: (punti ottenuti, risposta corretta?, tempo scaduto?)
        """
        from score_calculator import calculate_score
        from timer import is_timeout

        scaduto = is_timeout(tempo, self.timeout)

        # Se il tempo è scaduto, la risposta è considerata nulla
        if scaduto:
            risposta = ""

        is_correct = risposta == domanda.corretta
        punti = calculate_score(is_correct, tempo, self.timeout)
        self.punteggio += punti
        self.stats["tempi"].append(tempo)

        if risposta == "":
            self.stats["saltate"] += 1
        elif is_correct:
            self.stats["corrette"] += 1
        else:
            self.stats["errate"] += 1

        return punti, is_correct, scaduto

