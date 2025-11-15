# PDF Generation Setup Guide

## Installing GTK+ for Windows (Required for PDF Generation)

The health app uses WeasyPrint to generate beautiful PDF reports. WeasyPrint requires GTK+ runtime on Windows.

### Step 1: Download GTK+ Runtime

1. Visit the releases page: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
2. Download the latest installer (e.g., `gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe`)

### Step 2: Install GTK+ Runtime

1. Run the downloaded installer
2. Follow the installation wizard
3. Use the default installation directory (recommended)
4. Complete the installation

### Step 3: Verify Installation

After installation, restart any open terminals and try running the backend server.

### Alternative: Using Windows Subsystem for Linux (WSL)

If you encounter issues with GTK+ on Windows, you can run the backend in WSL:

```bash
# In WSL terminal
sudo apt-get update
sudo apt-get install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
pip install -r requirements.txt
python main.py
```

## Troubleshooting

### Issue: "OSError: cannot load library 'gobject-2.0-0'"

**Solution:** GTK+ is not properly installed. Reinstall GTK+ runtime and restart your terminal.

### Issue: "ImportError: DLL load failed"

**Solution:** 
1. Make sure you installed the correct version (64-bit vs 32-bit) matching your Python installation
2. Restart your computer after installing GTK+
3. Check if GTK+ bin directory is in your system PATH

### Issue: PDF generation is slow

**Solution:** This is normal for the first PDF generation. Subsequent generations will be faster as libraries are cached.

## Testing PDF Generation

After setup, you can test PDF generation:

1. Start the backend server
2. Complete a health assessment in the frontend
3. Click "Download PDF Report" button
4. A beautifully formatted PDF should download automatically

## Features of Generated PDF

- ✅ Professional header with gradient design
- ✅ Color-coded health metrics
- ✅ Visual BMI category badges
- ✅ Formatted workout schedule table
- ✅ Meal suggestions with calorie information
- ✅ Lifestyle tips and recommendations
- ✅ Weekly goals breakdown
- ✅ Important disclaimer section
- ✅ Clean, print-ready formatting

## Support

If you continue to experience issues with PDF generation:
1. Check the backend console for detailed error messages
2. Ensure all Python dependencies are installed: `pip install -r requirements.txt`
3. Try using a virtual environment to isolate dependencies
4. Consider using Docker for consistent environment setup
