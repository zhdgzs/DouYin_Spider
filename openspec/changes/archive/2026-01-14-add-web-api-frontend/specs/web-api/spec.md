## ADDED Requirements

### Requirement: Video Parse API
The system SHALL provide an HTTP API endpoint to parse Douyin video URLs and return video information with multiple quality download links including file sizes.

#### Scenario: Parse video URL successfully
- **WHEN** user sends POST request to `/api/video/parse` with valid Douyin video URL
- **THEN** system returns video metadata including title, author, statistics
- **AND** system returns multiple video URLs with different quality levels (720p, 540p, etc.)
- **AND** each video URL includes file size information (bytes and human-readable format)
- **AND** response format is JSON with `success: true`

#### Scenario: Parse invalid URL
- **WHEN** user sends POST request with invalid or non-Douyin URL
- **THEN** system returns error response with `success: false`
- **AND** error message indicates the URL is invalid

#### Scenario: Cookie expired or invalid
- **WHEN** system Cookie is expired or invalid
- **THEN** system returns error response with `success: false`
- **AND** error message indicates authentication failure

### Requirement: Health Check API
The system SHALL provide a health check endpoint for monitoring service status.

#### Scenario: Service healthy
- **WHEN** user sends GET request to `/api/health`
- **THEN** system returns `{"status": "ok", "version": "x.x.x"}`

### Requirement: Video Proxy API
The system SHALL provide a video proxy endpoint to bypass Referer restrictions for video preview.

#### Scenario: Proxy video stream
- **WHEN** frontend requests video through `/api/video/proxy?url=xxx`
- **THEN** system fetches video from original URL with proper headers
- **AND** system streams video content to frontend
- **AND** frontend can play video without CORS or Referer issues

### Requirement: CORS Support
The system SHALL support Cross-Origin Resource Sharing (CORS) for frontend integration.

#### Scenario: Frontend cross-origin request
- **WHEN** frontend sends request from different origin
- **THEN** system responds with appropriate CORS headers
- **AND** request is not blocked by browser

### Requirement: Video Preview Frontend
The system SHALL provide a web page for users to input Douyin video URL and preview video with download options.

#### Scenario: User inputs video URL
- **WHEN** user enters Douyin video URL in input field and clicks parse button
- **THEN** system displays loading indicator
- **AND** system calls backend API to parse video
- **AND** system displays video information and download links with file sizes

#### Scenario: Quality selection and preview linkage
- **WHEN** user clicks on a quality option in the list
- **THEN** system highlights the selected quality row
- **AND** video player switches to play the selected quality video
- **AND** player preserves current playback position if possible

#### Scenario: Default quality selection
- **WHEN** video is successfully parsed
- **THEN** system selects the highest quality by default
- **AND** video player loads and plays the highest quality video

#### Scenario: Copy download link
- **WHEN** user clicks copy button next to a quality option
- **THEN** system copies the download URL to clipboard
- **AND** system shows success notification

#### Scenario: Download video
- **WHEN** user clicks download button next to a quality option
- **THEN** browser initiates file download
- **OR** system opens download URL in new tab

### Requirement: Non-Invasive Integration
The system SHALL NOT modify any existing code files to ensure backward compatibility.

#### Scenario: Existing functionality preserved
- **WHEN** API service is added to the project
- **THEN** `main.py` remains unchanged
- **AND** `dy_apis/`, `builder/`, `utils/` modules remain unchanged
- **AND** original command-line functionality works as before
- **AND** API dependencies are managed in separate `requirements-api.txt`
