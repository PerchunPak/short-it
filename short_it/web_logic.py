"""Module for the app object, and all handlers."""
import fastapi.responses

import short_it.exc
import short_it.parse_config as parse_config

app = fastapi.FastAPI()


def find_and_redirect_to_the_link(
    project_name: str, link_type: str | None
) -> fastapi.responses.RedirectResponse | fastapi.responses.PlainTextResponse:
    """The logic in this module."""
    try:
        result = parse_config.ParseConfigToMachineData().get_url(project_name, link_type)
    except short_it.exc.ShortItException as exception:
        return fastapi.responses.PlainTextResponse(exception.message)
    else:
        if result is None:
            raise fastapi.HTTPException(status_code=404)

        return fastapi.responses.RedirectResponse(url=result)


@app.get("/{project_name}/{link_type}", response_model=None)
def route_project_link(
    project_name: str, link_type: str
) -> fastapi.responses.RedirectResponse | fastapi.responses.PlainTextResponse:
    """Route for the project link."""
    return find_and_redirect_to_the_link(project_name, link_type)


@app.get("/{link_type}", response_model=None)
def route_simple_link(link_type: str) -> fastapi.responses.RedirectResponse | fastapi.responses.PlainTextResponse:
    """Route for the simple link."""
    return find_and_redirect_to_the_link(link_type, None)
