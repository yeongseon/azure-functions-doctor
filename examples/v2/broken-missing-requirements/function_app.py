import azure.functions as func

app = func.FunctionApp()


@app.route(route="MissingRequirements", auth_level=func.AuthLevel.Anonymous)
def MissingRequirements(req: func.HttpRequest) -> func.HttpResponse:  # noqa: N802 (Azure style name retained)
    return func.HttpResponse(
        "This fixture is intentionally missing requirements.txt.", status_code=200
    )
