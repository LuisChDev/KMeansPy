import unittest
from main import normalize, euclid, voronoi, vals, centroid


class TestKMeansMethods(unittest.TestCase):
    def test_normalize(self):
        # falla si alguno de los rangos es 0
        with self.assertRaises(ZeroDivisionError):
            normalize([(0, 0)])
            normalize([(11, 11)])

        # normaliza correctamente cuatro valores
        norms = normalize([(1, 1),
                           (1, -1),
                           (-1, -1),
                           (-1, 1)])
        self.assertEqual(norms, [(0.5, 0.5),
                                 (0.5, -0.5),
                                 (-0.5, -0.5),
                                 (-0.5, 0.5)])

    def test_euclid(self):
        # 0 si los puntos están en el mismo lugar
        self.assertEqual(0, euclid((1, 1), (1, 1)))

        # 5 si las distancias en X y Y son 3 y 4
        self.assertAlmostEqual(5.0, euclid((0, 0), (3, 4)), 5)

    def test_voronoi(self):
        points = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        # si se pasa un solo centroide, la lista debería contener sólo ceros
        self.assertEqual([0, 0, 0, 0], voronoi(points, [(0, 0)]))

        # si se pasan dos centroides sobre el eje X, los puntos deberían
        # quedar clasificados en dos y dos
        self.assertEqual([0, 0, 1, 1], voronoi(points, [(1, 0), (-1, 0)]))

    def test_centroid(self):
        points = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        # el centroide de cuatro puntos en un cuadrado sobre el origen
        # es 0, 0
        self.assertEqual(centroid(points), (0, 0))

        # el centroide del triángulo formado por los tres primeros
        # puntos anteriores es (1/3, -1/3)
        self.assertEqual(centroid(points[:-1]), (1/3, -1/3))

        # el centroide de un solo punto, es el mismo punto.
        self.assertEqual(centroid(points[:1]), points[0])

        # el centroide de una lista vacía retorna un error.
        with self.assertRaises(ZeroDivisionError):
            normalize([])


class TestKMeansValues(unittest.TestCase):
    def test_readfile(self):
        # 200 entradas
        self.assertEqual(200, len(vals))


if __name__ == "__main__":
    unittest.main()
