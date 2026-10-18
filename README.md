# Cloud Capacity Forecast

A dependency-free Python demo that forecasts hourly service demand from synthetic traffic and turns the forecast into a simple capacity recommendation. It reflects capacity pipeline work described in the resume without using internal Google Cloud data or code.

## Run

```bash
python app.py
python -m unittest discover -s tests
```

## Method

The generator combines daily seasonality, a weekend effect, gentle growth, and noise. For each test hour, the baseline predicts from the same hour in the preceding week, adjusted by the recent week-over-week trend. Evaluation uses a chronological split and reports mean absolute error (MAE) and mean absolute percentage error (MAPE). Required instances are `ceil(forecast / target_utilization / requests_per_instance)`. This is an educational baseline, not a production autoscaler.

## Resume description

Created a synthetic service-demand forecasting demo with chronological evaluation and transparent capacity recommendations in Python.
