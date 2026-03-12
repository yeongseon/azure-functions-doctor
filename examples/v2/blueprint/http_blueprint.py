import azure.functions as func

bp = func.Blueprint()


@bp.route(route="BlueprintExample", auth_level=func.AuthLevel.Anonymous)
def BlueprintExample(req: func.HttpRequest) -> func.HttpResponse:  # noqa: N802 (Azure style name retained)
    return func.HttpResponse("Blueprint-based v2 function executed successfully.", status_code=200)
