# Qwen MT Image Translation

A powerful OOMOL package for translating text in images using the Qwen Multi-modal Translation API. This package provides both URL-based and file-based workflows to seamlessly integrate image translation into your processing pipelines.

## Features

- Translate text in images via URL
- Translate text in local image files
- Support for 9 languages (Chinese, English, Korean, Japanese, Russian, Spanish, French, Portuguese, Italian)
- Automatic cloud upload and download
- Configurable polling for translation completion
- Easy-to-use subflow blocks

## Subflows

This package includes two main subflows for different use cases:

### 1. URL Image Translation

Translate text in an image URL from source to target language and return the translated image URL.

**Inputs:**
- `imageURL` (string, required): The URL of the image to be translated
- `sourceLang` (string, required): Source language code (default: "en")
  - Options: zh, en, ko, ja, ru, es, fr, pt, it
- `targetLang` (string, required): Target language code (default: "zh")
  - Options: zh, en, ko, ja, ru, es, fr, pt, it

**Outputs:**
- `translatedImageURL` (string): URL of the translated image

**Use Case:** Perfect for processing web-hosted images or when you want to keep images in the cloud.

### 2. Local Image Translation

Translate text in a local image file from source to target language and save the result.

**Inputs:**
- `image_file` (file, required): Local image file to translate
- `sourceLang` (string, required): Source language code (default: "en")
- `targetLang` (string, required): Target language code (default: "zh")
- `saved_path` (string, optional): Path to save the translated image

**Outputs:**
- `saved_path` (string): Path of the successfully downloaded translated image

**Use Case:** Ideal for batch processing local images or integrating translation into file-based workflows.

## Supported Languages

The package supports translation between the following languages:

| Language | Code |
|----------|------|
| Chinese (简体中文) | zh |
| English (英文) | en |
| Korean (韩语) | ko |
| Japanese (日语) | ja |
| Russian (俄语) | ru |
| Spanish (西班牙语) | es |
| French (法语) | fr |
| Portuguese (葡萄牙语) | pt |
| Italian (意大利语) | it |

## Basic Usage

### Using URL Image Translation

1. Add the `url-image-translation` subflow to your workflow
2. Connect an image URL to the `imageURL` input
3. Select source and target languages
4. The translated image URL will be available in the `translatedImageURL` output

### Using Local Image Translation

1. Add the `local-image-translation` subflow to your workflow
2. Select a local image file using the `image_file` input
3. Choose source and target languages
4. Optionally specify where to save the result in `saved_path`
5. The translated image will be saved and its path returned in the output

## Task Blocks

This package includes two core task blocks:

### Submit Image Translation

Submit an image translation request to the Qwen MT Image service and receive a task ID for result polling.

**Inputs:**
- `imageURL` (string): The URL of the image to be translated
- `sourceLang` (string): Source language code
- `targetLang` (string): Target language code

**Outputs:**
- `taskId` (string): Task ID for polling the translation result

### Get Image Translation Result

Poll the Qwen MT Image service for translation results using the task ID. Automatically retries until the task is complete or max retries is reached.

**Inputs:**
- `taskId` (string): The task ID from submit request
- `maxRetries` (number, optional): Maximum polling attempts (default: 60)
- `retryInterval` (number, optional): Seconds between polls (default: 2)

**Outputs:**
- `translatedImageURL` (string): URL of the translated image
- `status` (string): Final status of the translation

## Dependencies

This package requires the following OOMOL packages:
- `upload-to-cloud` (v0.0.5): For uploading local files to cloud storage
- `downloader` (v0.1.1): For downloading translated images

## Installation

This package can be installed through the OOMOL package manager:

```bash
# Install the package
oomol install qwen-mt-image

# Add to your workspace dependencies
oomol use qwen-mt-image
```

## Configuration

The translation service uses the OOMOL Fusion API. No additional API key configuration is required - the package automatically uses your OOMOL token for authentication.

## Technical Details

### Workflow Architecture

Both subflows follow a similar pattern:

1. **Submit Phase**: Submit the image (URL or uploaded file) to the Qwen MT API
2. **Poll Phase**: Continuously check the translation status until completion
3. **Retrieve Phase**: Return or download the translated image

### Polling Mechanism

The polling system includes:
- Configurable retry attempts to handle long translation times
- Adjustable retry intervals to balance responsiveness and API load
- Automatic error handling and status reporting
- Default configuration: 60 retries with 2-second intervals (up to 2 minutes)

### API Integration

The package integrates with the Qwen Multi-modal Translation API through OOMOL's Fusion API endpoint:
- Base URL: `https://fusion-api.oomol.com/v1`
- Authentication: Automatic via OOMOL token
- Endpoints: `/image/translation` for submission and result retrieval

### Translation Process

1. **Image Analysis**: The AI analyzes the image to detect and extract text
2. **Text Translation**: Detected text is translated from source to target language
3. **Image Rendering**: The translated text is rendered back onto the image maintaining original layout and styling

## Error Handling

The package includes robust error handling:
- Connection failures are reported with clear error messages
- Timeout scenarios are handled gracefully with retry logic
- Translation status is tracked and reported throughout the process
- Invalid language codes are validated before submission

## Use Cases

- **E-commerce**: Translate product images for international markets
- **Documentation**: Localize technical diagrams and screenshots
- **Social Media**: Adapt visual content for different regions
- **Marketing**: Convert promotional materials for global campaigns
- **Education**: Translate instructional materials and infographics

## Version

Current version: 0.0.1

## License

This package is provided as part of the OOMOL ecosystem.
