import pyfiglet
def banner():
    copyright_notice = """╔══════════════════════════════════════════════════╗
║  © 2025 Mohamed eraki                            ║
║  mohamed-ibrahim2021@outlook.com                 ║
║  Version: 1.0.0                                  ║
║  eraXplor - AWS Cost exporter Tool               ║
╚══════════════════════════════════════════════════╝
    """
    banner = pyfiglet.figlet_format("eraXplor", font='slant')
    return banner, copyright_notice