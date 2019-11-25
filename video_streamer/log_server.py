import multiprocessing
import multiprocessing.queues

import base_server


class RTPPacketLogServer(base_server.Server):
    def __init__(self, name, stat_queue, rtp_pkt_queue, decoder_class, source_id):
        super(RTPPacketLogServer, self).__init__(name, stat_queue)
        if rtp_pkt_queue is None:
            raise Exception("RTP packet queue is None")
        if decoder_class is None:
            raise Exception("RTP packet decoder class is None")
        self._rtp_pkt_in_queue = rtp_pkt_queue
        self._source_id = source_id
        self._decoder = decoder_class(self._source_id)
        # logging indicator
        self._received_sync_pkt_count = 0
        self._latest_received_rtp_pkt = None
        self._latest_received_rtp_timestamp = None
        self._latest_received_meta_frame = None

    def _log_routine(self):
        if self._latest_received_rtp_pkt is not None and self._latest_received_meta_frame is not None:
            print("the number of received RTP packet from the source #%d in last 5 seconds: %d" %
                  (self._source_id, self._received_sync_pkt_count))
            print("latest RTP packet length = %d, timestamp = %d, metadata frame timestamp = %d" %
                  (len(self._latest_received_rtp_pkt), self._latest_received_rtp_timestamp,
                   self._latest_received_meta_frame.smart_msg_.timestamp_))
            # reset logging indicator
            self._received_sync_pkt_count = 0
            self._latest_received_rtp_pkt = None
            self._latest_received_rtp_timestamp = None
            self._latest_received_meta_frame = None

        self._start_log_routine()

    def serve(self):
        while True:
            try:
                while not self._stop_flag.is_set():
                    self._latest_received_meta_frame,\
                        self._latest_received_rtp_timestamp,\
                        self._latest_received_rtp_pkt = self._rtp_pkt_in_queue.get(timeout=1)
                    self._received_sync_pkt_count += 1

                    self._decoder.put(self._latest_received_rtp_pkt)

                break  # server stopped
            except multiprocessing.queues.Empty:
                pass  # timeout just for server stop checking, ignore safely

    def release(self):
        super(RTPPacketLogServer, self).release()
        if self._decoder is None:
            return  # to prevent re-entry

        self._decoder.release()
        self._decoder = None
