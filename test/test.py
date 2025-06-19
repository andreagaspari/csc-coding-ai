import unittest

from calcola_media import calcola_media  # Sostituisci 'tuo_modulo' con il nome del file se stai testando da un file separato

class TestCalcolaMedia(unittest.TestCase):
    
    def test_lista_numeri_interi(self):
        self.assertEqual(calcola_media([1, 2, 3, 4]), 2.5)

    def test_lista_numeri_float(self):
        self.assertAlmostEqual(calcola_media([1.5, 2.5, 3.0]), 2.3333333333, places=6)

    def test_lista_stringhe_numeriche(self):
        self.assertEqual(calcola_media(["1", "2.5", "3"]), 2.1666666666666665)

    def test_lista_mista_numeri_e_stringhe(self):
        self.assertEqual(calcola_media([1, "2", "abc", None, 4.0]), 2.3333333333333335)

    def test_lista_con_valori_non_convertibili(self):
        self.assertEqual(calcola_media(["abc", None, [], {}]), 0.0)

    def test_lista_vuota(self):
        self.assertEqual(calcola_media([]), 0.0)

    def test_lista_con_zero_esplicito(self):
        self.assertEqual(calcola_media(["0", 0, 0.0]), 0.0)

if __name__ == '__main__':
    unittest.main()
