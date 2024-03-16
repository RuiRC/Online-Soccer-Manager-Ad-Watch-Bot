from OnlineSoccerManagerBot.controller import OnlineSoccerManagerController
import logging
import sys
import threading

class StreamToLoggerWithTerminalOutput:
    def __init__(self, logger, original_stdout, log_level=logging.INFO):
        self.logger = logger
        self.original_stdout = original_stdout
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
            # Also write to the original stdout
            self.original_stdout.write(line + '\n')

    def flush(self):
        # This flush method is required for file-like objects.
        # Flush the original stdout as well.
        self.original_stdout.flush()

def setup_logging():
    original_stdout = sys.stdout
    logging.basicConfig(filename="log.txt", level=logging.INFO,
                        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    sys.stdout = StreamToLoggerWithTerminalOutput(logging.getLogger("STDOUT"), original_stdout, logging.INFO)

def main():
    try:
        # Make threads daemon so they are killed when the main program exits
        setup_thread = threading.Thread(target=setup_logging, daemon=True)
        setup_thread.start()

        manager = OnlineSoccerManagerController()
        tokens_thread = threading.Thread(target=manager.getTokens, daemon=True)
        tokens_thread.start()

        # Wait for both threads to complete
        setup_thread.join()
        tokens_thread.join()
    except KeyboardInterrupt:
        print("\nInterrupt received, shutting down...")
        # Threads are daemonized, so they will terminate when the main program exits
        sys.exit(0)

if __name__ == "__main__":
    main()
