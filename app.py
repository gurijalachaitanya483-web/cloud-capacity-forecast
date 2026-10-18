"""Hourly demand forecasting and capacity planning on synthetic data."""
import math
import random


def generate(hours=24 * 35, seed=7):
    rng = random.Random(seed)
    demand = []
    for hour in range(hours):
        day, clock = divmod(hour, 24)
        daily = 35 * math.sin(2 * math.pi * (clock - 7) / 24)
        weekend = -25 if day % 7 in (5, 6) else 0
        demand.append(max(1, round(120 + daily + weekend + 0.08 * hour + rng.gauss(0, 5))))
    return demand


def forecast(demand, hour):
    """Same hour last week, adjusted by recent weekly mean change."""
    if hour < 24 * 14 or hour > len(demand):
        raise ValueError("forecast needs two complete prior weeks")
    week = 24 * 7
    recent = sum(demand[hour - week:hour]) / week
    previous = sum(demand[hour - 2 * week:hour - week]) / week
    return max(0, demand[hour - week] + recent - previous)


def instances(predicted_requests, requests_per_instance=50, target_utilization=0.7):
    if requests_per_instance <= 0 or not 0 < target_utilization <= 1:
        raise ValueError("capacity and utilization must be positive")
    return math.ceil(predicted_requests / (requests_per_instance * target_utilization))


def evaluate(actual, predicted):
    if len(actual) != len(predicted) or not actual:
        raise ValueError("equal nonempty inputs required")
    mae = sum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual)
    mape = sum(abs(a - p) / a for a, p in zip(actual, predicted) if a > 0) / sum(a > 0 for a in actual) * 100
    return mae, mape


def main():
    demand = generate()
    start = 24 * 28
    predictions = [forecast(demand, hour) for hour in range(start, len(demand))]
    mae, mape = evaluate(demand[start:], predictions)
    next_hour = forecast(demand, len(demand))
    print(f"Chronological test: MAE={mae:.2f} requests/hour; MAPE={mape:.2f}%")
    print(f"Next hour forecast={next_hour:.1f}; recommended instances={instances(next_hour)}")


if __name__ == "__main__":
    main()
