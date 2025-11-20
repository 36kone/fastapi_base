import logging

# import os
from app.core.config import settings
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

COLLECTOR = settings.OTEL_COLLECTOR_LOGS
SERVICE = settings.OTEL_SERVICE_NAME
# COLLECTOR = os.getenv("OTEL_COLLECTOR_LOGS", "http://localhost:4318/v1/logs")
# SERVICE = os.getenv("OTEL_SERVICE_NAME", "fastapi-app")

resource = Resource.create({"service.name": SERVICE})
provider = LoggerProvider(resource=resource)
set_logger_provider(provider)

exporter = OTLPLogExporter(endpoint=COLLECTOR)
provider.add_log_record_processor(BatchLogRecordProcessor(exporter))


def init_logging():
    """Attach OTLP logging handler without interfering with console handlers."""
    root = logging.getLogger()
    root.addHandler(LoggingHandler(level=logging.NOTSET, logger_provider=provider))
    root.info("Starting OTEL Logging Service")
    return None
