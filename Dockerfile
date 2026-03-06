FROM python:3.11-slim
WORKDIR /app
COPY *.py .
RUN pip install --no-cache-dir fastmcp requests python-dotenv
LABEL io.docker.server.metadata='{"name":"tme","description":"TME electronic components — search, pricing, stock, datasheets","command":["python","tme_mcp_server.py"],"secrets":[{"name":"tme.TME_APP_TOKEN","env":"TME_APP_TOKEN"},{"name":"tme.TME_APP_SECRET","env":"TME_APP_SECRET"}],"env":[{"name":"TME_COUNTRY","value":"PL"},{"name":"TME_LANGUAGE","value":"EN"},{"name":"TME_CURRENCY","value":"PLN"}]}'
CMD ["python", "tme_mcp_server.py"]
