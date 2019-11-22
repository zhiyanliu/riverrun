import constants
import video_publisher
from video_reader import horizon_x2
import video_sender


def create_reader():
    shm_filename = constants.get_shm_filename()
    if "" == shm_filename:
        print("Invalid environment variables provided for video packet sender")
        print("Variable %s is necessary, exit" % constants.VIDEO_RTP_PACKET_SHM_FILENAME)
        reader = None
    else:
        reader = horizon_x2.VideoPacketHoBotX2SDKReader()
    return reader


def create_udp_sender():
    receiver_ip, receiver_port = constants.get_server_ip_port()
    if "" == receiver_ip:
        sender = None
    else:
        sender = video_sender.RTPPacketUDPSender(receiver_ip, port=receiver_port)
    return sender


def create_requester():
    receiver_ip, receiver_port = constants.get_server_ip_port()
    if "" == receiver_ip:
        sender = None
    else:
        sender = video_sender.RTPPacketTCPSender(receiver_ip, port=receiver_port)
    return sender


def create_publisher():
    subscriber_ip, subscriber_port = constants.get_server_ip_port()
    topic = constants.get_publish_topic()
    if "" == subscriber_ip:
        publisher = None
    elif "" == topic:
        publisher = video_publisher.RTPPacketPublisher(subscriber_ip, port=subscriber_port)
    else:
        publisher = video_publisher.RTPPacketPublisher(subscriber_ip, port=subscriber_port, topic=topic)
    return publisher


def create_emitter():
    emitter = None
    emit_type = constants.get_client_emit_type()
    if constants.EMIT_TYPE_PUBLISH == emit_type:
        emitter = create_publisher()
    elif constants.EMIT_TYPE_REQUEST == emit_type:
        emitter = create_requester()
    elif constants.EMIT_TYPE_UDP == emit_type:
        emitter = create_udp_sender()

    if emitter is None:
        print("Invalid environment variables provided for video packet sender")
        print("Variable %s is necessary, exit" % constants.SERVER_IP_ENV_VAR_NAME)
        print("Variable %s must be %s %s or %s, exit" %
              (constants.EMIT_TYPE_ENV_VAR_NAME, constants.EMIT_TYPE_UDP,
               constants.EMIT_TYPE_REQUEST, constants.EMIT_TYPE_PUBLISH))
    return emitter
