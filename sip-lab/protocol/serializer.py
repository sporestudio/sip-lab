#!/usr/bin/env python3

"""
SIP Serializer Module
----------------------

This module defines the SIPSerializer class, which is responsible for 
serializing SIP (Session Initiation Protocol) messages.
"""

from .message import SIPMessage, SIPRequest, SIPResponse

CRLF = "\r\n"

def serailize_message(msg: SIPMessage) -> str:
    """
    Serialize a SIPMessage instance into a SIP message string.

    Args:
        msg (SIPMessage): The SIPMessage instance to serialize.

    Returns:
        str: The serialized SIP message as a string.
    """
    if not isinstance(msg, (SIPRequest, SIPResponse)):
        raise TypeError("msg must be an instance of SIPRequest or SIPResponse")
    
    # Start line
    lines = [msg.start_line()]

    # Headers
    lines.extend(_serialize_headers(msg._headers))

    # Content-Length
    body = msg._body or ""
    lines.append(f"Content-Length: {len(body)}")

    # Separator headers/body
    lines.append("")
    lines.append(body)

    return CRLF.join(lines)

def _serialize_headers(headers: dict[str, str]) -> list[str]:
    """
    Serialize SIP headers into a list of strings.

    Args:
        headers (dict[str, str]): The headers to serialize.

    Returns:
        list[str]: The serialized headers as a list of strings.
    """
    return [
        f"{_format_header_name(name)}: {value}"
        for name, value in headers.items()
    ]

def _format_header_name(name: str) -> str:
    """
    Format a SIP header name to standard capitalization.

    Args:
        name (str): The header name to format.

    Returns:
        str: The formatted header name.
    """
    return "-".join(part.capitalize() for part in name.split("-"))