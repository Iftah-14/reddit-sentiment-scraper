#!/bin/bash

# Install certs if using Debian-based container (not Alpine)
apt-get update && apt-get install -y ca-certificates

# Explicitly export cert path
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

# Run Flask app
python main.py
