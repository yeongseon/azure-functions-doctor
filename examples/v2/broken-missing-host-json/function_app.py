import azure.functions as func

app = func.FunctionApp()


@app.route(route="MissingHostJson", auth_level=func.AuthLevel.Anonymous)
def MissingHostJson(req: func.HttpRequest) -> func.HttpResponse:  # noqa: N802 (Azure style name retained)
    return func.HttpResponse("This fixture is intentionally missing host.json.", status_code=200)
