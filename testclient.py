'''
Created on 

@author: George
'''
#socketserver_threaded.py
import threading
import struct
import logging.handlers
from datetime import datetime
from timeit import default_timer as timer
import argparse
import socket
import sys
import time

# Set up a specific logger with our desired output level
LOG_FILENAME = 'IPclient.out'
log_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=4*(1024*1024), backupCount=5)

formatter = logging.Formatter('%(asctime)-15s [%(levelname)s] (%(threadName)-10s) %(message)s')
#formatter.converter = time.gmtime
log_handler.setFormatter(formatter)
my_logger = logging.getLogger("my_logger")
my_logger.addHandler(log_handler)
my_logger.setLevel(logging.DEBUG)


def xmit(address,iterations,textSize):
    # Connect to the server
    min = 1.0
    avg = 0.0
    max = 0.0
    old_max = 0.0
    x = 0.0
    j=1.0  # iterations for average

    nowStart = datetime.now()
    current_time = nowStart.strftime("%H:%M:%S")

    my_logger.debug('Starting - Data size (k) : %d, Iterations : %d' % (textSize, iterations))
    print('Starting %s - Data size : %d, Iterations : %d' % (current_time, textSize, iterations))

    cur_thread = threading.currentThread()
    threadName = cur_thread.getName().encode()

    for i in range(iterations):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(address)

            # for i in range(100):
            # Send the data
            #cur_thread = threading.currentThread()
            #threadName = cur_thread.getName().encode()

            message = threadName +  (b'-' * textSize)

            start = timer()

            len_sent = s.send(struct.pack('>I', len(message)))

            #print("sent %s bytes for Header" % len_sent)

            len_sent = s.send(message)
            #print("sent %s bytes for Body" % len_sent)

            try:
                # Receive a response
                response = s.recv(4)

                messageSize = struct.unpack('>I', response)[0]

                #response = s.recv(messageSize)
                received = b''
                dataRemaining = messageSize
                while dataRemaining != 0:
                    received += s.recv(dataRemaining)
                    dataRemaining = messageSize - len(received)


                assert (len_sent < len(received))

                j = j+1


            except ConnectionResetError as e:
                my_logger.info('Error %s Thread %s for Message Size %s Stopped %s iterations completed' % (e,threadName,textSize,j))

        except OSError as e:
            my_logger.info(
                'Error %s Thread %s for Message Size %s Stopped %s iterations completed' % (e, threadName, textSize, j))
            break



        end = timer()

        elapsed = (end - start)
        if elapsed < min:
            #my_logger.info('New minimum - was:%s:now:%s' % (min, elapsed))
            min = elapsed
        if elapsed > max:
            old_max = max
            #my_logger.info('New maximum - was:%s:now:%s' % (max, elapsed))
            max = elapsed

        x = x + elapsed
        avg = x / j
        ninetieth = old_max
        # my_logger.debug('Thread {} for data size {} stopped with time {}'.format(i, textSize, elapsed))

        s.close()
        #time.sleep(0.2)

    nowStop = datetime.now()
    runTime = nowStop - nowStart
    my_logger.debug('Stopping- dataSize:%d:Min:%s:Avg:%s:Max:%s:Nth:%s:Iterations:%s:Elapsed Runtime:%s' % (
        textSize, min, avg, max, ninetieth, j, str(runTime)))

def clientHandler(args):
    address = (args.host, args.port)  # let the kernel assign a port
    threadList = []
    i=1
    startMsgSize = 16
    while i <=args.threads:
        t2 = threading.Thread(name='xmit %s ' %i,target=xmit, args=((address),args.iterations,startMsgSize))
        threadList.append(t2)
        t2.start()
        startMsgSize = startMsgSize * 2
        i += 1

def main():
    parser = argparse.ArgumentParser(prog='IPclient')
    parser.add_argument("--version", action="version",
                        help="Prints version information.",
                        version='%(prog)s 0.1.0')
    subparsers = parser.add_subparsers(title="options")

    client_parser = subparsers.add_parser("client", description="Client",
                                          help="Connect to a given cid and port.")
    client_parser.add_argument("host", type=str, help="The remote endpoint IP (or localhost).")
    client_parser.add_argument("port", type=int, help="The remote endpoint port.")
    client_parser.add_argument("iterations", type=int, help="The number of iterations per thread.")
    client_parser.add_argument("threads", type=int, help="The number of threads to start.")
    client_parser.set_defaults(func=clientHandler)



    if len(sys.argv) < 4:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':

    main()
    '''import socket

    address = ('localhost', 5555)  # let the kernel assign a port
    threadList = []
    i=1
    startMsgSize = 32
    while i <=16:
        t2 = threading.Thread(name='xmit %s ' %i,target=xmit, args=((address),1000,startMsgSize))
        threadList.append(t2)
        t2.start()
        startMsgSize = startMsgSize * 2
        i += 1'''



