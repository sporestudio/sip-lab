#!/usr/bin/env python3

"""
Main Module
--------------

This module serves as the entry point for the SIP Lab application.
"""

from protocol.message import SIPRequest, SIPResponse
from protocol.parser import parse_message, SIPParserError

raw = (
    "OPTIONS sip:test@example.com SIP/2.0\r\n"
    "Via: SIP/2.0/UDP 127.0.0.1:5060\r\n"
    "From: <sip:a@test.com>\r\n"
    "To: <sip:b@test.com>\r\n"
    "Call-ID: 123\r\n"
    "CSeq: 1 OPTIONS\r\n"
    "Content-Length: 0\r\n\r\n"
)

msg = parse_message(raw)
print(msg)
print(msg.get_headers("via"))
