FastAPI URL Shortener

A lightweight REST API built with FastAPI and Pydantic that generates short alphanumeric codes for HTTP/HTTPS URLs and redirects visitors to the original destination.

Features

URL Validation: Automatically validates incoming links using Pydantic's HttpUrl.

Collision-Safe Short Codes: Generates unique 6-character alphanumeric codes (a-z, A-Z, 0-9).

Fast Redirects: Redirects short links to their target URLs via HTTP 307 Temporary Redirect.

Health Check & Interactive Docs: Includes a root health endpoint (GET /) and built-in Swagger UI (/docs).

Container-Ready: Easily packaged and run via Docker.