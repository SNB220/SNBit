# SNBit Uploader - Instructions

This is a Python-based file upload server project with the following characteristics:

## Project Overview
- **Main Application**: `src/snbit_uploader.py` - A secure HTTP file upload server
- **Framework**: Pure Python using built-in `http.server` module
- **UI**: Modern dark theme with cyan accents, mobile-responsive design
- **Security**: File type validation, size limits, path traversal protection

## Code Style & Patterns
- Use Python 3.7+ features
- Follow PEP 8 style guidelines
- Comprehensive error handling with try-catch blocks
- Descriptive function and variable names
- Type hints where appropriate
- Detailed docstrings for functions and classes

## Security Considerations
- Always validate file extensions against ALLOWED_EXTENSIONS
- Implement path traversal protection using os.path.abspath
- Sanitize all user inputs
- Use proper HTTP status codes (200, 400, 403, 404, 500)
- Log security-related events

## Architecture Patterns
- Configuration via environment variables
- Modular function design
- Clean separation of concerns (HTML generation, file handling, security)
- Comprehensive logging for debugging and monitoring

## Dependencies
- `qrcode[pil]`: For QR code generation
- `Pillow`: Image processing for QR codes
- Standard library modules: `http.server`, `socket`, `logging`, `mimetypes`

## File Structure
- Keep main logic in `src/snbit_uploader.py`
- Use `uploads/` directory for file storage
- Maintain proper project structure with README, requirements.txt, LICENSE

## UI/UX Guidelines
- Dark theme (#121212 background, #00ffff accents)
- Mobile-first responsive design
- Clear status messages and progress indicators
- Accessibility considerations
- Professional, clean interface

When suggesting code improvements or new features, prioritize security, user experience, and maintainability.
