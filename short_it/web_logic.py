"""Module for the app object, and all handlers."""
import fastapi.responses

import short_it.parse_config as parse_config

app = fastapi.FastAPI()


@app.get("/{project_name}/{link_type}")
async def find_and_redirect_to_the_link(project_name: str, link_type: str) -> fastapi.responses.RedirectResponse:
    """The ``View`` in MVC in this program."""
    result = parse_config.ParseConfigToMachineData().get_url(project_name, link_type)

    if result is None:
        raise fastapi.HTTPException(status_code=404)

    return fastapi.responses.RedirectResponse(url=result)
