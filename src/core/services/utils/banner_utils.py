"""
Module to display the eraXplor application banner and copyright notice.

This module provides the visual branding elements for the eraXplor Azure cost export tool.
It uses pyfiglet to generate an ASCII art banner and includes version and copyright
information for display in the CLI interface.

The banner is displayed at the start of the main() function to provide visual feedback
to users and establish the application's identity.

Dependencies:
    - pyfiglet: For generating ASCII art text banners

Example:
    >>> from eraXplor_azure.utils.banner_utils import banner
    >>> banner_format, copyright_notice = banner()
    >>> print(banner_format)
"""

import pyfiglet  # Pylint: disable=import-error


def banner():
    """
    Generates a banner and copyright notice for the eraXplor application.

    Creates an ASCII art banner using the 'slant' font with the application name,
    along with a formatted copyright notice containing version information and
    contact details.

    Returns:
        tuple: A tuple containing two strings:
            - banner_format (str): ASCII art banner with the text "eraXplor"
            - copyright_notice (str): Formatted copyright and version information

    Example:
        >>> banner_format, copyright_notice = banner()
        >>> print(banner_format)
        >>> print(copyright_notice)

    Note:
        The copyright year is currently set to 2025 and should be updated
        annually. The version number reflects the current release version
        of the eraXplor package.
    """

    copyright_notice = """╔══════════════════════════════════════════════════╗
║  © 2026 Mohamed Eraki                            ║
║  mohamed-ibrahim2021@outlook.com                 ║
║  Version: 4.0.0                                  ║
║  eraXplor - FinOps Cost exporter Tool            ║
╚══════════════════════════════════════════════════╝
    """
    banner_format = pyfiglet.figlet_format("eraXplor", font='slant')
    return banner_format, copyright_notice
