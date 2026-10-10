# quickpic-image-tool
# QuickPic: High-Performance Batch Image Resizer & Format Converter

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

A lightweight, multi-threaded command-line utility to batch resize, crop, and convert images (PNG, JPG, WEBP, TIFF, BMP) in seconds. Optimized for content creators, e-commerce sellers, and developers who need instant asset pipelines.

Developed by [Autofroge-code](https://github.com/Autofroge-code).

---

## ✨ Features (Open-Source CLI Edition)

- **Blazing Fast**: Multi-threaded processing powered by Pillow and SIMD optimizations.
- **Smart Resizing**: Scale by percentage, target width/height, or fit within bounding boxes while strictly preserving aspect ratio.
- **Format Conversion**: Convert between `.jpg`, `.png`, `.webp`, `.tiff`, and `.bmp`.
- **Quality Preservation & Compression**: Smart WebP/JPEG quantization to slash file sizes without noticeable visual degradation.
- **Exif Handling**: Optional stripping of GPS and metadata to protect privacy and shave extra kilobytes.

---

> ### 🚀 Need a Zero-Setup Desktop App?
> Don't want to install Python, manage dependencies, or type terminal commands?
> 
> Check out **QuickPic Pro (Desktop GUI Edition)**:
> - 🖥️ **Native Windows GUI**: Clean drag-and-drop interface, zero configuration required.
> - ⚡ **Visual Live Preview**: Side-by-side compression comparison and instant zoom.
> - 📦 **Standalone Executable**: Runs immediately without installing Python or third-party libraries.
> - 🔑 **Lifetime License (\$19.00)**: Free lifetime updates and priority customer support.
>
> 👉 **[Get QuickPic Pro Lifetime License on Creem.io →](https://creem.io/store/autoforge/quickpic-pro)**

---

## 📦 Quick Start

### 1. Installation

Clone the repository and install the dependencies:

```bash
git clone [https://github.com/Autofroge-code/quickpic-image-tool.git](https://github.com/Autofroge-code/quickpic-image-tool.git)
cd quickpic-image-tool
pip install -r requirements.txt
