import azure.functions as func

app = func.FunctionApp()


@app.route(route="MissingAzureFunctionsPackage", auth_level=func.AuthLevel.Anonymous)
def MissingAzureFunctionsPackage(req: func.HttpRequest) -> func.HttpResponse:  # noqa: N802 (Azure style name retained)
    return func.HttpResponse(
        "This fixture is intentionally missing azure-functions in requirements.", status_code=200
    )
