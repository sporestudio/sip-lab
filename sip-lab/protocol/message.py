#!/usr/bin/env python3

"""
SIP Message Module
-------------------

This module defines the SIPMessage class, which represents a SIP (Session Initiation Protocol) message.
"""

from typing import Optional

class SIPMessage:
    def __init__(
            self,
            headers: dict[str, str],
            body: Optional[str] = None
    ) -> None:
        """
        Initialize a SIPMessage instance.

        Args:
            headers (dict[str, str]): A dictionary of SIP headers.
            body (Optional[str]): The body of the SIP message, if any.
        
        Returns:
            None
        """
        self._headers = headers
        self._body = body or ""

    def get_headers(self, name: str) -> Optional[str]:
        """
        Retrieve the value of a specific header.

        Args:
            name (str): The name of the header to retrieve.
        
        Returns:
            Optional[str]: The value of the header if it exists, otherwise None.
        """
        return self._headers.get(name.lower())
    
class SIPRequest(SIPMessage):
    def __init__(
            self,
            method: str,
            uri: str,
            version: str,
            headers: dict[str, str],
            body: Optional[str] = None
    ) -> None:
        """
        Initialize a SIPRequest instance.

        Args:
            method (str): The SIP method (e.g., INVITE, ACK).
            uri (str): The Request-URI.
            headers (dict[str, str]): A dictionary of SIP headers.
            body (Optional[str]): The body of the SIP message, if any.
        
        Returns:
            None
        """
        super().__init__(headers, body)
        self._method = method
        self._uri = uri
        self._version = version

        def __repr__(self) -> str:
            return f"SIPRequest(method={self._method}, uri={self._uri})"
        
class SIPResponse(SIPMessage):
    def __init__(
            self,
            version: str,
            status_code: int,
            reason_phrase: str,
            headers: dict[str, str],
            body: Optional[str] = None
    ) -> None:
        """
        Initialize a SIPResponse instance.

        Args:
            version (str): The SIP version (e.g., SIP/2.0).
            status_code (int): The status code of the response.
            reason_phrase (str): The reason phrase associated with the status code.
            headers (dict[str, str]): A dictionary of SIP headers.
            body (Optional[str]): The body of the SIP message, if any.
        
        Returns:
            None
        """
        super().__init__(headers, body)
        self._version = version
        self._status_code = status_code
        self._reason_phrase = reason_phrase

        def __repr__(self) -> str:
            return f"SIPResponse(status_code={self._status_code}, reason_phrase={self._reason_phrase})"