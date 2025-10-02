from fastapi import FastAPI, Query
import pandas as pd

df = pd.read_csv("sneediest.csv")

app = FastAPI(title="Termolecular Reaction Database API")

@app.get("/")
def root():
    return {"message": "does this work?"}

@app.get("/reactions/")
def search_reactions(
    reactant: str = Query(None, description="Filter by reactant"),
    temperature_min: float = Query(None, description="Minimum temperature (K)"),
    temperature_max: float = Query(None, description="Maximum temperature (K)")
):
    results = df.copy()

    if reactant:
        results = results[results["Reactant(s)"].str.contains(reactant, case=False, na=False)]

    if temperature_min is not None:
        results = results[results["Temp./K"] >= temperature_min]

    if temperature_max is not None:
        results = results[results["Temp./K"] <= temperature_max]

    return results.to_dict(orient="records")
