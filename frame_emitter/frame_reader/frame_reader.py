class FrameReader:
    def read(self):
        """Returns:
            1. if any smart frame is read.
            2. the timestamp of the smart frame.
            3. the smart frame buffer.
            """
        return False, -1, None

    def release(self):
        """Release the resource of this reader instance."""
        pass
