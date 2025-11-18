#region generated meta
import typing
class Inputs(typing.TypedDict):
    imageURL: str
    sourceLang: typing.Literal["zh", "en", "ko", "ja", "ru", "es", "fr", "pt", "it"]
    targetLang: typing.Literal["zh", "en", "ko", "ja", "ru", "es", "fr", "pt", "it"]
class Outputs(typing.TypedDict):
    taskId: typing.NotRequired[str]
#endregion

from oocana import Context
import requests

async def main(params: Inputs, context: Context) -> Outputs:
    """
    Submit an image translation request to the Qwen MT Image service.

    Args:
        params: Input parameters containing imageURL, sourceLang, and targetLang
        context: OOMOL context for accessing system features

    Returns:
        Dictionary containing the taskId for polling the result
    """
    url = "https://fusion-api.oomol.com/v1/qwen-mt-image/submit"

    # Get OOMOL token for authentication
    token = await context.oomol_token()

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    payload = {
        "imageURL": params["imageURL"],
        "sourceLang": params["sourceLang"],
        "targetLang": params["targetLang"]
    }

    response = requests.post(url, headers=headers, json=payload)

    # Raise exception if request failed
    response.raise_for_status()

    result = response.json()

    # Extract session ID from response (API returns sessionID instead of taskId)
    task_id = result.get("sessionID") or result.get("taskId")

    if not task_id:
        raise ValueError(f"No sessionID or taskId found in response: {result}")

    return {"taskId": task_id}
