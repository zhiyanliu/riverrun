import constants
import frame_publisher
from frame_reader import horizon_x2
import frame_sender


def create_reader():
    # reader = horizon_x2.FrameNoneReader()  # eat all frames, for test
    reader = horizon_x2.FrameHoBotX2SDKReader()
    return reader


def create_sender():
    receiver_ip, receiver_port = constants.get_server_ip_port()
    if "" == receiver_ip:
        sender = None
    else:
        sender = frame_sender.FrameSender(receiver_ip, port=receiver_port)
    return sender


def create_publisher():
    subscriber_ip, subscriber_port = constants.get_server_ip_port()
    topic = constants.get_publish_topic()
    if "" == subscriber_ip:
        publisher = None
    elif "" == topic:
        publisher = frame_publisher.FramePublisher(subscriber_ip, port=subscriber_port)
    else:
        publisher = frame_publisher.FramePublisher(subscriber_ip, port=subscriber_port, topic=topic)
    return publisher


def create_emitter():
    emitter = None
    emit_type = constants.get_client_emit_type()
    if constants.EMIT_TYPE_PUBLISH == emit_type:
        emitter = create_publisher()
    elif constants.EMIT_TYPE_REQUEST == emit_type:
        emitter = create_sender()

    if emitter is None:
        print("Invalid environment variables provided for metadata frame sender")
        print("Variable %s is necessary, exit" % constants.SERVER_IP_ENV_VAR_NAME)
        print("Variable %s must be %s or %s, exit" %
              (constants.EMIT_TYPE_ENV_VAR_NAME, constants.EMIT_TYPE_REQUEST, constants.EMIT_TYPE_PUBLISH))
    return emitter
