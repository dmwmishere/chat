#!/usr/bin/python
import logging, hashlib, ChatServerLogic as csl, GenerateDBStruct;
from twisted.internet import protocol, reactor;
from time import ctime;
from chatData_pb2 import CMD, MSG, RSPS;

system_name = 'ChatServer'
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

PORT = 6666


def makeResponse(code, message):
    response = RSPS()
    response.response_code = code
    if message != None:
        response.message = message
    return response


class ChatServerProtocol(protocol.Protocol):
    def connectionMade(self):
        clnt = self.clnt = self.transport.getPeer().host
        log.info('%s connected', clnt)

    def process_command(self, cmd):
        log.info('Command = %d', cmd.code)
        if cmd.code == CMD.LOGIN:
            result = csl.login(cmd.data.login, cmd.data.pswd)
        elif cmd.code == CMD.REGISTER:
            result = csl.register_new(cmd.data.login, cmd.data.pswd, cmd.data.name)

        if result == True:
            return makeResponse(RSPS.SUCCESS, None)
        else:
            return makeResponse(RSPS.SERVER_ERROR, "Failed to execute command!")

    def process_chat(self, chat):
        log.error('not implemented!')
        return makeResponse(RSPS.SERVER_ERROR, "Chats not yet implemented!")

    def dataReceived(self, data):
        log.debug('Received: ' + data)
        msg = MSG()
        msg.ParseFromString(data)
        if msg.HasField("cmd"):
            log.debug('this is COMMAND message')
            response = self.process_command(msg.cmd)
        else:
            log.debug('this is CHAT message');
            response = self.process_chat(msg.chat)

        self.transport.write(response.SerializeToString())


if __name__ == '__main__':
    # GenerateDBStruct.makeStructure('chats');
    factory = protocol.Factory()
    factory.protocol = ChatServerProtocol
    log.info('Waiting for client...')
    reactor.listenTCP(PORT, factory)
    reactor.run()
