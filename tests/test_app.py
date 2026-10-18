import unittest
from app import evaluate, forecast, generate, instances


class CapacityTests(unittest.TestCase):
    def test_forecast_beats_flat_baseline(self):
        demand = generate()
        start = 24 * 28
        actual = demand[start:]
        predictions = [forecast(demand, i) for i in range(start, len(demand))]
        self.assertLess(evaluate(actual, predictions)[0], evaluate(actual, [sum(demand[:start]) / start] * len(actual))[0])

    def test_capacity_boundary(self):
        self.assertEqual(instances(70), 2)
        self.assertEqual(instances(71), 3)


if __name__ == '__main__':
    unittest.main()
