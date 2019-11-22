import os


SERVER_IP_ENV_VAR_NAME = "METADATA_FRAME_SERVER_IP"
SERVER_PORT_ENV_VAR_NAME = "METADATA_FRAME_SERVER_PORT"
PUBLISH_TOPIC_ENV_VAR_NAME = "METADATA_FRAME_PUBLISH_TOPIC"
EMIT_TYPE_ENV_VAR_NAME = "METADATA_FRAME_EMIT_TYPE"

EMIT_TYPE_PUBLISH = "PUB"
EMIT_TYPE_REQUEST = "REQ"

REQUEST_RELY_TIMEOUT_MS_ENV_VAR_NAME = "METADATA_FRAME_REQUEST_RELY_TIMEOUT_MS"


def get_server_ip_port(default_server_port=9528):
    os.environ.setdefault(SERVER_IP_ENV_VAR_NAME, "")  # prevent KeyError error
    os.environ.setdefault(SERVER_PORT_ENV_VAR_NAME, str(default_server_port))

    try:
        port = int(os.environ[SERVER_PORT_ENV_VAR_NAME].strip())
    except ValueError:
        port = default_server_port

    return os.environ[SERVER_IP_ENV_VAR_NAME].strip(), port


def get_publish_topic(default_topic="md"):
    os.environ.setdefault(PUBLISH_TOPIC_ENV_VAR_NAME, str(default_topic))
    return os.environ[PUBLISH_TOPIC_ENV_VAR_NAME].strip()


def get_client_emit_type(default_type=EMIT_TYPE_PUBLISH):
    os.environ.setdefault(EMIT_TYPE_ENV_VAR_NAME, default_type)
    return os.environ[EMIT_TYPE_ENV_VAR_NAME].strip()


def get_request_rely_timeout(default_timeout_ms=500):
    os.environ.setdefault(REQUEST_RELY_TIMEOUT_MS_ENV_VAR_NAME, str(default_timeout_ms))

    try:
        timeout = int(os.environ[REQUEST_RELY_TIMEOUT_MS_ENV_VAR_NAME].strip())
    except ValueError:
        timeout = default_timeout_ms

    return timeout
