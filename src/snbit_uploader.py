#!/usr/bin/env python3
"""
SNBit Uploader - A secure and modern file upload server
Author: nabie
Description: A Python-based HTTP file upload server with QR code generation,
             mobile-friendly UI, and comprehensive security features.
"""

import os
import socket
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import qrcode
from io import BytesIO
import base64
import logging
from urllib.parse import unquote
import mimetypes
import json
import sys
from pathlib import Path

# Configuration
DEFAULT_UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uploads")
UPLOAD_DIR = os.environ.get('SNBIT_UPLOAD_DIR', DEFAULT_UPLOAD_DIR)
MAX_FILE_SIZE = int(os.environ.get('SNBIT_MAX_FILE_SIZE', 100 * 1024 * 1024))  # 100MB default
ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.zip', '.docx', '.mp4', '.mp3'}
PORT = int(os.environ.get('SNBIT_PORT', 8080))

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('snbit_uploader.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def generate_qr(ip_port):
    """Generate QR code with IP URL"""
    try:
        qr = qrcode.make(f"http://{ip_port}")
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{qr_base64}"
    except Exception as e:
        logging.error(f"Error generating QR code: {e}")
        return None

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote address to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def is_allowed_file(filename):
    """Check if the file extension is allowed"""
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

class SNBitRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logging.info(f"{self.client_address[0]} - {format % args}")

    def do_GET(self):
        try:
            if self.path == '/':
                self.serve_main_page()
            elif self.path.startswith('/download/'):
                self.serve_file_download()
            elif self.path.startswith('/delete/'):
                self.delete_file()
            elif self.path == '/health':
                self.serve_health_check()
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            logging.error(f"Error in GET request: {e}")
            self.send_error(500, "Internal Server Error")

    def serve_health_check(self):
        """Health check endpoint"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        health_data = {
            'status': 'healthy',
            'upload_dir': UPLOAD_DIR,
            'max_file_size': MAX_FILE_SIZE,
            'allowed_extensions': list(ALLOWED_EXTENSIONS)
        }
        self.wfile.write(json.dumps(health_data).encode('utf-8'))

    def serve_main_page(self):
        """Serve the main upload page"""
        try:
            files = []
            for filename in os.listdir(UPLOAD_DIR):
                filepath = os.path.join(UPLOAD_DIR, filename)
                if os.path.isfile(filepath):
                    file_size = os.path.getsize(filepath)
                    files.append({
                        'name': filename,
                        'size': format_file_size(file_size),
                        'size_bytes': file_size
                    })
            
            # Sort files by name
            files.sort(key=lambda x: x['name'].lower())
            
            files_html = ""
            if files:
                files_html = "<ul>"
                for file_info in files:
                    files_html += f'''
                    <li style="margin-bottom: 10px; padding: 10px; background: #2a2a2a; border-radius: 5px;">
                        <span style="font-weight: bold;">{file_info['name']}</span> 
                        <span style="color: #aaa;">({file_info['size']})</span>
                        <div style="margin-top: 5px;">
                            <a href="/download/{file_info['name']}" 
                               style="color: #00ffff; text-decoration: none; margin-right: 10px;">Download</a>
                            <a href="/delete/{file_info['name']}" 
                               onclick="return confirm('Are you sure you want to delete this file?')"
                               style="color: #ff4444; text-decoration: none;">Delete</a>
                        </div>
                    </li>
                    '''
                files_html += "</ul>"
            else:
                files_html = "<p style='color: #aaa;'>No files uploaded yet.</p>"

            local_ip = get_local_ip()
            ip_port = f"{local_ip}:{PORT}"
            qr_data = generate_qr(ip_port)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>SNBit Uploader</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        body {{
                            background-color: #121212;
                            color: #fff;
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            justify-content: center;
                            padding: 20px;
                            margin: 0;
                            min-height: 100vh;
                        }}
                        .container {{
                            max-width: 800px;
                            width: 100%;
                        }}
                        h1 {{
                            color: #00ffff;
                            text-align: center;
                            margin-bottom: 30px;
                            font-size: 2.5em;
                        }}
                        h2 {{
                            color: #00ffff;
                            margin-bottom: 15px;
                        }}
                        .upload-section {{
                            background: #1e1e1e;
                            padding: 30px;
                            border-radius: 12px;
                            box-shadow: 0 0 20px rgba(0,255,255,0.2);
                            margin-bottom: 30px;
                            border: 1px solid #333;
                        }}
                        input[type="file"] {{
                            display: block;
                            margin-bottom: 20px;
                            color: #ccc;
                            background: #2a2a2a;
                            padding: 10px;
                            border-radius: 5px;
                            border: 1px solid #444;
                            width: 100%;
                            box-sizing: border-box;
                        }}
                        input[type="submit"] {{
                            padding: 12px 30px;
                            border: none;
                            border-radius: 8px;
                            background-color: #00ffff;
                            color: #000;
                            font-weight: bold;
                            cursor: pointer;
                            font-size: 16px;
                            transition: background-color 0.3s;
                        }}
                        input[type="submit"]:hover {{
                            background-color: #00cccc;
                        }}
                        input[type="submit"]:disabled {{
                            background-color: #555;
                            cursor: not-allowed;
                        }}
                        progress {{
                            width: 100%;
                            height: 25px;
                            margin-top: 15px;
                            border-radius: 12px;
                        }}
                        .files-section {{
                            background: #1e1e1e;
                            padding: 20px;
                            border-radius: 12px;
                            margin-bottom: 30px;
                            border: 1px solid #333;
                        }}
                        .files-section ul {{
                            list-style: none;
                            padding: 0;
                            margin: 0;
                        }}
                        .qr-section {{
                            background: #1e1e1e;
                            padding: 20px;
                            border-radius: 12px;
                            text-align: center;
                            border: 1px solid #333;
                        }}
                        .qr-section img {{
                            border-radius: 8px;
                            margin: 10px 0;
                        }}
                        .info {{
                            background: #2a2a2a;
                            padding: 15px;
                            border-radius: 8px;
                            margin-bottom: 20px;
                            border-left: 4px solid #00ffff;
                        }}
                        .status {{
                            margin-top: 15px;
                            padding: 10px;
                            border-radius: 5px;
                            display: none;
                        }}
                        .status.success {{
                            background-color: #1a4a3a;
                            color: #4ade80;
                            border: 1px solid #4ade80;
                        }}
                        .status.error {{
                            background-color: #4a1a1a;
                            color: #f87171;
                            border: 1px solid #f87171;
                        }}
                        @media (max-width: 768px) {{
                            body {{
                                padding: 10px;
                            }}
                            .upload-section, .files-section, .qr-section {{
                                padding: 15px;
                            }}
                            h1 {{
                                font-size: 2em;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>SNBit Uploader</h1>
                        
                        <div class="info">
                            <strong>Server Address:</strong> http://{ip_port}<br>
                            <strong>Max File Size:</strong> {format_file_size(MAX_FILE_SIZE)}<br>
                            <strong>Allowed Extensions:</strong> {', '.join(sorted(ALLOWED_EXTENSIONS))}
                        </div>

                        <div class="upload-section">
                            <h2>Upload Files</h2>
                            <form id="uploadForm" enctype="multipart/form-data" method="post">
                                <input name="files" type="file" multiple accept="{','.join(ALLOWED_EXTENSIONS)}" />
                                <input type="submit" value="Upload Files" id="uploadButton" />
                                <progress id="progressBar" value="0" max="100" style="display:none;"></progress>
                                <div id="status" class="status"></div>
                            </form>
                        </div>

                        <div class="files-section">
                            <h2>Uploaded Files ({len(files)} files)</h2>
                            {files_html}
                        </div>

                        <div class="qr-section">
                            <h2>QR Code for Mobile Access</h2>
                            <p>Scan this QR code with your mobile device to access the uploader:</p>
                            {f'<img src="{qr_data}" width="200" />' if qr_data else '<p style="color: #ff4444;">QR code generation failed</p>'}
                            <p style="color: #aaa; font-size: 14px;">http://{ip_port}</p>
                        </div>
                    </div>

                    <script>
                        const form = document.getElementById("uploadForm");
                        const progress = document.getElementById("progressBar");
                        const button = document.getElementById("uploadButton");
                        const status = document.getElementById("status");

                        function showStatus(message, type) {{
                            status.textContent = message;
                            status.className = `status ${{type}}`;
                            status.style.display = 'block';
                            setTimeout(() => {{
                                status.style.display = 'none';
                            }}, 5000);
                        }}

                        form.onsubmit = async (e) => {{
                            e.preventDefault();
                            
                            const fileInput = form.querySelector('input[type="file"]');
                            if (!fileInput.files.length) {{
                                showStatus('Please select files to upload', 'error');
                                return;
                            }}

                            const formData = new FormData(form);
                            const xhr = new XMLHttpRequest();
                            
                            button.disabled = true;
                            button.value = 'Uploading...';
                            progress.style.display = 'block';

                            xhr.open("POST", "/", true);

                            xhr.upload.onprogress = (event) => {{
                                if (event.lengthComputable) {{
                                    const percent = (event.loaded / event.total) * 100;
                                    progress.value = percent;
                                }}
                            }};

                            xhr.onload = () => {{
                                button.disabled = false;
                                button.value = 'Upload Files';
                                progress.style.display = 'none';
                                
                                if (xhr.status === 200) {{
                                    showStatus('Files uploaded successfully!', 'success');
                                    setTimeout(() => location.reload(), 1000);
                                }} else {{
                                    showStatus(`Upload failed: ${{xhr.responseText}}`, 'error');
                                }}
                            }};

                            xhr.onerror = () => {{
                                button.disabled = false;
                                button.value = 'Upload Files';
                                progress.style.display = 'none';
                                showStatus('Upload failed: Network error', 'error');
                            }};

                            xhr.send(formData);
                        }};

                        // File input validation
                        const fileInput = form.querySelector('input[type="file"]');
                        fileInput.onchange = () => {{
                            const files = Array.from(fileInput.files);
                            const allowedExtensions = [{','.join([f"'{ext}'" for ext in ALLOWED_EXTENSIONS])}];
                            const maxSize = {MAX_FILE_SIZE};
                            
                            let hasError = false;
                            
                            for (const file of files) {{
                                const ext = '.' + file.name.split('.').pop().toLowerCase();
                                if (!allowedExtensions.includes(ext)) {{
                                    showStatus(`File type not allowed: ${{file.name}}`, 'error');
                                    hasError = true;
                                    break;
                                }}
                                if (file.size > maxSize) {{
                                    showStatus(`File too large: ${{file.name}} (${{(file.size / 1024 / 1024).toFixed(1)}}MB)`, 'error');
                                    hasError = true;
                                    break;
                                }}
                            }}
                            
                            if (hasError) {{
                                fileInput.value = '';
                            }}
                        }};
                    </script>
                </body>
                </html>
            '''
            
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            logging.error(f"Error serving main page: {e}")
            self.send_error(500, "Internal Server Error")

    def serve_file_download(self):
        """Serve file downloads"""
        try:
            filename = unquote(self.path[10:])  # Remove '/download/'
            filepath = os.path.join(UPLOAD_DIR, filename)
            
            if not os.path.exists(filepath) or not os.path.isfile(filepath):
                self.send_error(404, "File not found")
                return
            
            # Security check: ensure file is within upload directory
            if not os.path.abspath(filepath).startswith(os.path.abspath(UPLOAD_DIR)):
                self.send_error(403, "Access denied")
                return
            
            file_size = os.path.getsize(filepath)
            mime_type, _ = mimetypes.guess_type(filepath)
            if not mime_type:
                mime_type = 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', str(file_size))
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.end_headers()
            
            with open(filepath, 'rb') as f:
                while True:
                    data = f.read(8192)
                    if not data:
                        break
                    self.wfile.write(data)
                    
        except Exception as e:
            logging.error(f"Error serving file download: {e}")
            self.send_error(500, "Internal Server Error")

    def delete_file(self):
        """Delete a file"""
        try:
            filename = unquote(self.path[8:])  # Remove '/delete/'
            filepath = os.path.join(UPLOAD_DIR, filename)
            
            if not os.path.exists(filepath) or not os.path.isfile(filepath):
                self.send_error(404, "File not found")
                return
            
            # Security check: ensure file is within upload directory
            if not os.path.abspath(filepath).startswith(os.path.abspath(UPLOAD_DIR)):
                self.send_error(403, "Access denied")
                return
            
            os.remove(filepath)
            logging.info(f"File deleted: {filename}")
            
            # Redirect back to main page
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
            
        except Exception as e:
            logging.error(f"Error deleting file: {e}")
            self.send_error(500, "Internal Server Error")

    def do_POST(self):
        """Handle file uploads with validation and error handling"""
        try:
            content_type = self.headers.get('Content-Type', '')
            if not content_type.startswith('multipart/form-data'):
                self.send_error(400, "Invalid content type")
                return
            
            # Get boundary from content type
            boundary = None
            for part in content_type.split(';'):
                part = part.strip()
                if part.startswith('boundary='):
                    boundary = part[9:].strip('"')
                    break
            
            if not boundary:
                self.send_error(400, "No boundary found")
                return
            
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, "No content")
                return
            
            # Read the entire request body
            body = self.rfile.read(content_length)
            
            # Parse multipart data manually
            uploaded_files = []
            errors = []
            
            # Split by boundary
            boundary_bytes = ('--' + boundary).encode()
            parts = body.split(boundary_bytes)
            
            for part in parts[1:-1]:  # Skip first empty part and last closing part
                if not part.strip():
                    continue
                
                # Split headers and body
                try:
                    header_end = part.find(b'\r\n\r\n')
                    if header_end == -1:
                        continue
                    
                    headers_section = part[:header_end].decode('utf-8', errors='ignore')
                    file_data = part[header_end + 4:].rstrip(b'\r\n')
                    
                    # Parse headers
                    filename = None
                    for line in headers_section.split('\r\n'):
                        if line.startswith('Content-Disposition:'):
                            # Extract filename
                            parts = line.split(';')
                            for p in parts:
                                p = p.strip()
                                if p.startswith('filename='):
                                    filename = p[9:].strip('"')
                                    break
                    
                    if not filename or not file_data:
                        continue
                    
                    filename = os.path.basename(filename)
                    
                    # Validate file extension
                    if not is_allowed_file(filename):
                        errors.append(f"File type not allowed: {filename}")
                        continue
                    
                    # Check file size
                    if len(file_data) > MAX_FILE_SIZE:
                        errors.append(f"File too large: {filename} ({format_file_size(len(file_data))})")
                        continue
                    
                    # Prevent filename conflicts
                    filepath = os.path.join(UPLOAD_DIR, filename)
                    counter = 1
                    original_filename = filename
                    while os.path.exists(filepath):
                        name, ext = os.path.splitext(original_filename)
                        filename = f"{name}_{counter}{ext}"
                        filepath = os.path.join(UPLOAD_DIR, filename)
                        counter += 1
                    
                    # Save file
                    try:
                        with open(filepath, 'wb') as f:
                            f.write(file_data)
                        uploaded_files.append(filename)
                        logging.info(f"File uploaded: {filename} ({format_file_size(len(file_data))})")
                    except Exception as e:
                        errors.append(f"Error saving {filename}: {str(e)}")
                        
                except Exception as e:
                    logging.error(f"Error processing file part: {e}")
                    continue

            # Send response
            self.send_response(200 if not errors else 207)  # 207 = Multi-Status
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                'success': len(uploaded_files) > 0,
                'uploaded': uploaded_files,
                'errors': errors,
                'message': f"Uploaded {len(uploaded_files)} files" + (f", {len(errors)} errors" if errors else "")
            }
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            logging.error(f"Error in POST request: {e}")
            self.send_error(500, f"Internal Server Error: {str(e)}")

def main():
    """Main function to start the server"""
    try:
        local_ip = get_local_ip()
        httpd = HTTPServer(('', PORT), SNBitRequestHandler)
        
        print(f"🚀 SNBit Uploader starting...")
        print(f"📍 Local access: http://localhost:{PORT}")
        print(f"🌐 Network access: http://{local_ip}:{PORT}")
        print(f"📁 Upload directory: {os.path.abspath(UPLOAD_DIR)}")
        print(f"📏 Max file size: {format_file_size(MAX_FILE_SIZE)}")
        print(f"📋 Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}")
        print("⛔ Press Ctrl+C to stop the server")
        
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        logging.error(f"Server error: {e}")

if __name__ == "__main__":
    main()
