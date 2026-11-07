---
title: "FastAPI: from a Python function to a web API"
summary: See how another application can call your Python code, then turn the example into a short reel.
tags: [AI for Students, Teaching]
---
A Python function can make a prediction inside your notebook. A website or mobile app needs a way to ask for that prediction and receive the result. An API gives it a predictable address and a format for the input and output.

## Try one endpoint

Save the following as `main.py`. The rule in this example stands in for a trained model.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class PredictionInput(BaseModel):
    study_hours: float


@app.post("/predict")
def predict(data: PredictionInput):
    return {"ready_for_practice_test": data.study_hours >= 10}
```

Install with `python -m pip install "fastapi[standard]"` and run `fastapi dev main.py`. Open [the local interactive docs](http://127.0.0.1:8000/docs), select `POST /predict`, and try two different values. The development server runs locally. A deployed API needs a hosting environment that runs Python.

- [FastAPI first steps](https://fastapi.tiangolo.com/tutorial/first-steps/)

## Short reel script

> You've built an AI model. Now what? If it only runs on your laptop, a website can't ask it for a prediction. FastAPI lets you give your Python code an API that a website or mobile app can call. Start with one endpoint and test it yourself.
