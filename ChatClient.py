#!/usr/bin/python
import logging, hashlib
from twisted.internet import protocol, reactor
from chatData_pb2 import MSG, CMD, RSPS

system_name = 'ChatClient'
logging_level = logging.DEBUG
log = logging.getLogger(system_name)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fh = logging.FileHandler(system_name + '.log')
fh.setFormatter(formatter)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(fh)
log.addHandler(ch)
log.setLevel(logging_level)

SERVER = 'localhost'
PORT = 6666


def process_response(response):
    rscode = response.response_code
    rsmsg = response.message
    log.info('Response code = %d, Message = %s', rscode, rsmsg)


class ChatClientProtocol(protocol.Protocol):
    def connectionMade(self):
        log.info('Connecting to server...')
        command = int(raw_input('''Select command:
		0 - Login,
		1 - Create new lobby,
		2 - Close owned lobby,
		3 - Enter existing lobby,
		4 - Quit existing lobby,
		5 - Register new user
		>'''))
        msg = MSG()
        if command == 0:
            login, pswd = raw_input('Enter login and password:').split(' ')
            log.debug('entering with %s and %s...', login, pswd)
            msg.cmd.code = CMD.LOGIN
            msg.cmd.data.login = login
            msg.cmd.data.pswd = hashlib.md5(pswd).hexdigest()

        elif command == 1:
            return;
        elif command == 5:
            login, pswd, name = raw_input('Enter login, password and full name:').split(' ')
            log.debug('registering %s, %s, %s', login, pswd, name)
            msg.cmd.code = CMD.REGISTER
            msg.cmd.data.login = login
            msg.cmd.data.pswd = hashlib.md5(pswd).hexdigest()
            msg.cmd.data.name = name
        log.debug('Ready 2 send: %r', msg.SerializeToString())
        self.transport.write(msg.SerializeToString())

    def dataReceived(self, data):
        response = RSPS()
        response.ParseFromString(data)
        process_response(response)


class ChatClientFactory(protocol.ClientFactory):
    protocol = ChatClientProtocol
    clientConnectionLost = clientConnectionLost = lambda self, connector, reason: reactor.stop()


if __name__ == '__main__':
    reactor.connectTCP(SERVER, PORT, ChatClientFactory())
    reactor.run()
