# mypy: disable-error-code="untyped-decorator"

import azure.functions as func

app = func.FunctionApp()
bp = func.Blueprint()


@bp.route(route="hello")
def hello(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("ok")
