#socketserver_threaded.py
import threading
import socketserver
import struct
import argparse
import sys


class ThreadedEchoRequestHandler(
        socketserver.BaseRequestHandler,
):

    '''def serve_forever(self, poll_interval=0.5):
        print('waiting for request')
        print(
            'Handling requests, press <Ctrl-C> to quit'
        )
        try:
            socketserver.TCPServer.serve_forever(self, poll_interval)
        except KeyboardInterrupt as e:
            print("shutdown requested")
            return
        return'''

    def handle(self):
        # Echo the back to the client
        data = self.request.recv(4)
        messageSize =  struct.unpack('>I', data)[0]

        received = b''
        dataRemaining = messageSize
        while dataRemaining != 0:
            received += self.request.recv(dataRemaining)
            dataRemaining = messageSize - len(received)


        #data = self.request.recv(messageSize)

        cur_thread = threading.currentThread()
        response = b'%s: %s' % (cur_thread.getName().encode(),
                                received)
        replysize = struct.pack('>I', len(response))
        self.request.sendall(replysize)
        self.request.sendall(response)
        return


class ThreadedEchoServer(socketserver.ThreadingMixIn,
                         socketserver.TCPServer,
                         ):
    pass



def serverHandler(args):

    address = (args.host, args.port)  # let the kernel assign a port
    server = ThreadedEchoServer(address,
                                ThreadedEchoRequestHandler)
    server.allow_reuse_address = True
    ip, port = server.server_address  # what port was assigned?
    print("Server started on %s port %s <CTRL-C to end> " %(ip,port))
    #while True:
    t = threading.Thread(target=server.serve_forever)
    print('Server loop running in thread:', t.getName())
    t.setDaemon(False)  # don't hang on exit
    t.start()
    try:
        t.join()
    except KeyboardInterrupt:
        print("\nShutdown requested")


    # Clean up
    server.shutdown()
    #s.close()
    server.socket.close()


def main ():
    parser = argparse.ArgumentParser(prog='testserver')
    parser.add_argument("--version", action="version",
                        help="Prints version information.",
                        version='%(prog)s 0.1.0')
    subparsers = parser.add_subparsers(title="options")

    server_parser = subparsers.add_parser("server", description="Server",
                                          help="Connect to a given address and port.")
    server_parser.add_argument("host", type=str, help="The remote endpoint IP (or localhost).")
    server_parser.add_argument("port", type=int, help="The remote endpoint port.")
    server_parser.set_defaults(func=serverHandler)

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()