#!/usr/bin/env python3

"""
SIP Parser Module
-------------------

This module defines the SIPParser class, which is responsible for parsing SIP (Session Initiation Protocol) messages.
"""

from typing import Union
from .message import SIPRequest, SIPResponse

class SIPParserError(Exception):
    """
    Custom exception for SIP parsing errors.
    """
    pass

class SIPHeaderError(SIPParserError):
    """
    Custom exception for SIP header errors.
    """
    pass

class SIPBodyError(SIPParserError):
    """
    Custom exception for SIP body errors.
    """
    pass

class SIPMessageError(SIPParserError):
    """
    Custom exception for SIP message errors.
    """
    pass

def parser_headers(lines: list[str]) -> dict[str, str]:
    """
    Parse SIP headers from a list of lines.

    Args:
        lines (list[str]): A list of lines representing SIP headers.

    Returns:
        dict[str, str]: A dictionary of parsed SIP headers.
    """
    headers = {}

    for line in lines:
        if not line.strip():
            break

        if ":" not in line:
            raise SIPParserError(f"Malformed header line: {line}")
        
        name, value = line.split(":", 1)
        headers[name.strip().lower()] = value.strip()

    return headers


def _extract_body(raw: str, headers: dict[str, str]) -> str:
    """
    Extract the body from a SIP message based on the Content-Length header.

    Args:
        raw (str): The raw SIP message.
        headers (dict[str, str]): A dictionary of SIP headers.

    Returns:
        str: The extracted body of the SIP message.
    """
    content_length = int(headers.get("content-length", "0"))

    if content_length is None:
        raise SIPBodyError("Content-Length header is missing")

    try:
        length = int(content_length)
    
    except ValueError:
        raise SIPBodyError(f"Invalid Content-Length header value: {content_length}")

    body_start = raw.find("\r\n\r\n") + 4
    if body_start == 3:
        raise SIPBodyError("Malformed SIP message: missing header-body separator")

    body = raw[body_start:]

    if len(body) != length:
        raise SIPBodyError(f"Body length mismatch: expected {length}, got {len(body)}")

    return body

def _parse_request(start_line: str, lines: list[str], raw: str) -> SIPRequest:
    """
    Parse a SIP request message.

    Args:
        start_line (str): The start line of the SIP request.
        lines (list[str]): A list of lines representing SIP headers and body.
        raw (str): The raw SIP message.

    Returns:
        SIPRequest: The parsed SIP request object.
    """
    try:
        method, uri, version = start_line.split(" ", 2)
    
    except ValueError:
        raise SIPParserError(f"Malformed request start line: {start_line}")

    headers = parser_headers(lines[1:])
    body = _extract_body(raw, headers)

    return SIPRequest(
        method=method,
        uri=uri,
        version=version,
        headers=headers,
        body=body
    )

def _parse_response(start_line: str, lines: list[str], raw: str) -> SIPResponse:
    """
    Parse a SIP response message.

    Args:
        start_line (str): The start line of the SIP response.
        lines (list[str]): A list of lines representing SIP headers and body.
        raw (str): The raw SIP message.

    Returns:
        SIPResponse: The parsed SIP response object.
    """
    try:
        version, status_code_str, reason_phrase = start_line.split(" ", 2)
        status_code = int(status_code_str)
    
    except ValueError:
        raise SIPParserError(f"Malformed response start line: {start_line}")

    headers = parser_headers(lines[1:])
    body = _extract_body(raw, headers)

    return SIPResponse(
        version=version,
        status_code=status_code,
        reason_phrase=reason_phrase,
        headers=headers,
        body=body
    )

def parse_message(raw: str) -> Union[SIPRequest, SIPResponse]:
    """
    Parse a raw SIP mwssage into a SIPRequest or SIPResponse.

    Args:
        raw (str): The raw SIP message.

    Returns:
        Union[SIPRequest, SIPResponse]: The parsed SIP message object.
    """
    lines = raw.split("\r\n")

    if len(lines) < 1:
        raise SIPParserError("Empty SIP message")

    start_line = lines[0]

    if start_line.startswith(("INVITE", "REGISTER", "ACK", "BYE", "OPTIONS", "CANCEL")):
        return _parse_request(start_line, lines, raw)

    if start_line.startswith("SIP/"):
        return _parse_response(start_line, lines, raw)

    raise SIPMessageError("Unknown SIP message type")