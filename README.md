# 🚀 SNBit Uploader

A modern, secure, and user-friendly file upload server built with Python. Features a beautiful dark theme UI, QR code generation for mobile access, and comprehensive security measures.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey.svg)

## Features

### Security & Safety
- **File extension validation** - Only allows specified safe file types
- **File size limits** - Configurable maximum file size (default: 100MB)
- **Path traversal protection** - Prevents directory escape attacks
- **Dedicated uploads folder** - Isolated file storage
- **Automatic filename conflict resolution** - Prevents file overwrites

### Modern UI/UX
- **Professional dark theme** - Easy on the eyes with cyan accents
- **Custom logo support** - Add your own branding with SVG logos
- **Mobile-responsive design** - Works seamlessly on all devices
- **Real-time progress bar** - Visual upload progress feedback
- **File management interface** - Download and delete files directly
- **Status notifications** - Clear success/error messages
- **QR code generation** - Easy mobile access (web + terminal)
- **Terminal QR code** - ASCII QR code displayed in console for quick scanning

###  Technical Features
- **Multiple file uploads** - Select and upload multiple files at once
- **Health check endpoint** - Monitor server status at `/health`
- **Comprehensive logging** - Track all activities and errors
- **Environment configuration** - Easily configurable via environment variables
- **Cross-platform compatibility** - Works on Windows, macOS, and Linux

##  Supported File Types

By default, the following file types are allowed:
- **Documents**: `.txt`, `.pdf`, `.docx`
- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`
- **Media**: `.mp4`, `.mp3`
- **Archives**: `.zip`

##  Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SNB220/snbit-uploader.git
   cd snbit-uploader
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python src/snbit_uploader.py
   ```

4. **Access the interface:**
   - Open your browser and go to `http://localhost:8080`
   - Or scan the QR code with your mobile device

##  Configuration

Configure the server using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `SNBIT_PORT` | `8080` | Server port |
| `SNBIT_UPLOAD_DIR` | `./uploads` | Upload directory path |
| `SNBIT_MAX_FILE_SIZE` | `104857600` | Max file size in bytes (100MB) |

### Example Usage

```bash
# Run on port 3000 with custom upload directory
export SNBIT_PORT=3000
export SNBIT_UPLOAD_DIR=/path/to/uploads
python src/snbit_uploader.py
```

### Windows PowerShell
```powershell
$env:SNBIT_PORT=3000
$env:SNBIT_UPLOAD_DIR="C:\path\to\uploads"
python src/snbit_uploader.py
```

## 📁 Project Structure

```
snbit-uploader/
├── src/
│   └── snbit_uploader.py      # Main application
├── assets/
│   └── logo.svg              # Custom logo (SVG format)
├── uploads/                   # File upload directory (auto-created)
├── requirements.txt           # Python dependencies
├── run.py                    # Simple launcher script
├── README.md                 # Project documentation
├── LICENSE                   # MIT license
├── .gitignore               # Git ignore rules
└── .github/
    ├── workflows/
    │   └── ci.yml           # GitHub Actions CI
    └── copilot-instructions.md
```

## Development

### Running in Development Mode

```bash
# Clone and setup
git clone https://github.com/SNB220/snbit-uploader.git
cd snbit-uploader

# Install dependencies
pip install -r requirements.txt

# Run the server
python src/snbit_uploader.py
```

### Adding New Features

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main upload interface |
| `POST` | `/` | Upload files |
| `GET` | `/download/{filename}` | Download a file |
| `GET` | `/delete/{filename}` | Delete a file |
| `GET` | `/health` | Health check |

### Health Check Response
```json
{
    "status": "healthy",
    "upload_dir": "/path/to/uploads",
    "max_file_size": 104857600,
    "allowed_extensions": [".txt", ".pdf", ".png", ...]
}
```

## 🐳 Docker Support

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY uploads/ ./uploads/

EXPOSE 8080
CMD ["python", "src/snbit_uploader.py"]
```

Build and run:
```bash
docker build -t snbit-uploader .
docker run -p 8080:8080 snbit-uploader
```

## Security Considerations

- **File Type Validation**: Only whitelisted extensions are allowed
- **Size Limits**: Prevents DoS attacks via large files
- **Path Sanitization**: Prevents directory traversal attacks
- **Input Validation**: All user inputs are validated and sanitized
- **Error Handling**: Graceful error handling without information disclosure

##  Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Change the port
   export SNBIT_PORT=3000
   ```

2. **Permission denied on upload directory:**
   ```bash
   # Create directory with proper permissions
   mkdir uploads
   chmod 755 uploads
   ```

3. **QR code not generating:**
   ```bash
   # Reinstall qrcode with PIL support
   pip install qrcode[pil]
   ```

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

##  Acknowledgments

- Built with Python's built-in `http.server` module
- QR code generation powered by [qrcode](https://pypi.org/project/qrcode/)
- UI inspired by modern dark theme designs

---

**Made with ❤️ by [SNB](https://github.com/SNB220)**
