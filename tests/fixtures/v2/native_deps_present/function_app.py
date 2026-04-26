from collections.abc import Callable
from typing import TypeVar

F = TypeVar("F", bound=Callable[..., object])


class FakeFunctionApp:
    def route(self, route: str, auth_level: str) -> Callable[[F], F]:
        _ = (route, auth_level)

        def decorator(func: F) -> F:
            return func

        return decorator


app = FakeFunctionApp()


@app.route(route="native-deps", auth_level="anonymous")
def native_deps() -> str:
    return "ok"
