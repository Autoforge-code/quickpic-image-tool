# QuickPic: Batch Image Resizer & Optimizer

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

A lightweight, multi-threaded batch image processing tool designed for content creators, web designers, and e-commerce sellers. Effortlessly resize, optimize, and convert images into modern web formats (WebP, JPEG, PNG).

Developed by [Autofroge-code](https://github.com/Autofroge-code).

---

## ✨ Features (Community Edition)

- **Intuitive GUI**: Clean desktop interface built with Python & Tkinter—no complicated command flags needed.
- **Multi-Threaded Engine**: Concurrent batch processing powered by `ThreadPoolExecutor` and Pillow.
- **Smart Aspect Ratio Resizing**:
  - Keep original dimensions.
  - Constrain by max edge/pixel bounds.
  - Scale by percentage.
- **Format Conversion**: Convert bulk directories to `.webp`, `.jpg`, or `.png`.
- **Smart Transparency Handling**: Automatic white background composition for RGBA images converted to JPEG (no ugly black borders).
- **Progress Tracking**: Real-time progress bar and status feedback.

---

> ### 🚀 Looking for a Zero-Setup, Standalone App?
> Don't want to install Python, configure PIP dependencies, or see terminal prompts?
> 
> Check out **[QuickPic Pro (Standalone Desktop Build)](https://creem.io/store/autoforge/quickpic-pro)**:
> - ⚡ **Single-Click Executable (.exe)**: Zero dependencies. Just download and run.
> - 🚀 **Hardware-Accelerated Engine**: Enhanced SIMD & multi-process optimizations for processing thousands of RAW/DSLR assets in seconds.
> - 🔍 **Visual Live Preview**: Side-by-side quality comparison before batch export.
> - 🔑 **Lifetime License (\$29.00 USD)**: Perpetual access with lifetime updates and priority support.
>
> 👉 **[Get QuickPic Pro Lifetime License on Creem.io →](https://creem.io/store/autoforge/quickpic-pro)**

---

## 📦 Quick Start (Running from Source)

### 1. Clone the Repository

```bash
git clone [https://github.com/Autofroge-code/quickpic-image-tool.git](https://github.com/Autofroge-code/quickpic-image-tool.git)
cd quickpic-image-tool
