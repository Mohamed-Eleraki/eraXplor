"""Module to display a banner and copyright notice."""

import pyfiglet
def banner():
    """Generates a banner and copyright notice for the application."""

    copyright_notice = """╔══════════════════════════════════════════════════╗
║  © 2025 Mohamed eraki                            ║
║  mohamed-ibrahim2021@outlook.com                 ║
║  Version: 1.0.0                                  ║
║  eraXplor - Azure Cost exporter Tool             ║
╚══════════════════════════════════════════════════╝
    """
    banner_format = pyfiglet.figlet_format("eraXplor", font='slant')
    return banner_format, copyright_notice
