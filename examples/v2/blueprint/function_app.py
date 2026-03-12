import azure.functions as func

from http_blueprint import bp

app = func.FunctionApp()
app.register_functions(bp)
