import log_server


def rtp_pkt_log_server_creator(stat_queue, rtp_pkt_queue, decoder_class, source_id):
    return log_server.RTPPacketLogServer(
        "RTP packet log server (for client source id #%d)" % source_id,
        stat_queue, rtp_pkt_queue, decoder_class, source_id)
