#region generated meta
import typing
class Inputs(typing.TypedDict):
    taskId: str
    maxRetries: float | None
    retryInterval: float | None
class Outputs(typing.TypedDict):
    translatedImageURL: typing.NotRequired[str]
    status: typing.NotRequired[str]
#endregion

from oocana import Context
import requests
import asyncio
import time

async def main(params: Inputs, context: Context) -> Outputs:
    """
    Poll the Qwen MT Image service for translation results.

    Args:
        params: Input parameters containing taskId and optional polling configuration
        context: OOMOL context for accessing system features

    Returns:
        Dictionary containing the translated image URL and status
    """
    task_id = params["taskId"]
    max_retries = params.get("maxRetries", 60)
    retry_interval = params.get("retryInterval", 2)

    url = f"https://fusion-api.oomol.com/v1/qwen-mt-image/result/{task_id}"

    # Get OOMOL token for authentication
    token = await context.oomol_token()

    headers = {
        "Authorization": token
    }

    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            result = response.json()

            # Print the response for analysis
            print(f"[Polling attempt {retries + 1}] API Response: {result}")

            # Report progress based on retries
            progress = min(int((retries / max_retries) * 100), 99)
            context.report_progress(progress)

            # Check if we have the translated image data
            # When data is ready, the response should contain the image URL or data
            if "data" in result:
                # Data is ready, stop polling
                data = result["data"]
                # Extract image_url from the data object
                if isinstance(data, dict):
                    translated_url = data.get("image_url", "")
                else:
                    translated_url = str(data)

                print(f"[Success] Translation completed, URL: {translated_url}")

                context.report_progress(100)

                return {
                    "translatedImageURL": translated_url,
                    "status": "completed"
                }

            # Check for explicit status field
            status = result.get("status", "").lower()

            if status == "completed" or status == "success":
                translated_url = result.get("translatedImageURL") or result.get("outputURL") or result.get("result") or result.get("data")

                if not translated_url:
                    raise ValueError(f"Translation completed but no image URL found in response: {result}")

                print(f"[Success] Translation completed with status, URL: {translated_url}")
                context.report_progress(100)

                return {
                    "translatedImageURL": translated_url,
                    "status": status
                }

            elif status == "failed" or status == "error":
                error_msg = result.get("error") or result.get("message") or "Translation failed"
                print(f"[Error] Translation failed: {error_msg}")
                raise RuntimeError(f"Translation task failed: {error_msg}")

            # Task is still processing, wait and retry
            print(f"[Processing] Still waiting for result, retrying in {retry_interval} seconds...")
            await asyncio.sleep(retry_interval)
            retries += 1

        except requests.exceptions.RequestException as e:
            print(f"[Network Error] Request failed: {str(e)}")
            # Network error, wait and retry
            if retries >= max_retries - 1:
                raise RuntimeError(f"Failed to get translation result after {max_retries} attempts: {str(e)}")

            await asyncio.sleep(retry_interval)
            retries += 1

    # Max retries reached without completion
    raise TimeoutError(f"Translation task did not complete after {max_retries} polling attempts ({max_retries * retry_interval} seconds)")
