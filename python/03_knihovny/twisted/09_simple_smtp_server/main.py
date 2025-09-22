from os.path import join, dirname
from uuid import uuid4
from zope.interface import implementer
from twisted.internet import reactor, protocol, defer
from twisted.mail import smtp
from twisted.mail.imap4 import LOGINCredentials, PLAINCredentials
from twisted.cred.checkers import ICredentialsChecker
from twisted.cred.credentials import IUsernamePassword
from twisted.cred.portal import IRealm, Portal
from twisted.cred.error import UnauthorizedLogin

MESSAGES_DIR = join(dirname(__file__), "messages")

DOMAIN = "test.com"

class User:
  username: str
  password: str

  def __init__(self, username: str, password: str):
    self.username = username
    self.password = password

  def validateSender(self, senderAddress: str):
    name, domain = senderAddress.split("@")
    return name == self.username and domain == DOMAIN



USERS = [
  User("user1", "password1"),
  User("user2", "password2"),
]



@implementer(ICredentialsChecker)
class Checker:
  credentialInterfaces = (
    IUsernamePassword,
  )

  def requestAvatarId(self, credentials): # credentials implementuje IUsernamePassword
    username = credentials.username.decode()
    password = credentials.password.decode()
    print(f"Checking credentials: {username} {password}")
    for user in USERS:
      if user.username == username and user.password == password:
        return defer.succeed(user)
    return defer.fail(UnauthorizedLogin())



@implementer(IRealm)
class Realm:
  interface = smtp.IMessageDelivery

  def logout(self):
    pass

  def requestAvatar(self, avatarId, _, *interfaces):
    if not isinstance(avatarId, User):
      raise NotImplementedError()
    user = avatarId

    print(f"Requesting avatar: {user.username}")

    if self.interface in interfaces:
      account = Account(user)
      return self.interface, account, self.logout

    return NotImplementedError()



@implementer(smtp.IMessageDelivery)
class Account:
  def __init__(self, user: User):
    self.user = user
    self.senderAddress = None

  def receivedHeader(self, _, __, ___):
    return b"Received: localhost"

  def validateFrom(self, _, origin):
    sender = str(origin)
    print(f"Validating sender: {sender}")
    if not self.user.validateSender(sender):
      raise smtp.SMTPBadSender(origin)
    self.senderAddress = sender
    return origin

  def validateTo(self, user):
    recipientAddress = str(user.dest)
    print(f"Validating recipient: {recipientAddress}")
    return lambda: Message(self.user, self.senderAddress, recipientAddress)



@implementer(smtp.IMessage)
class Message:
  def __init__(self, user: User, sender: str, recipient: str):
    self.user = user
    self.sender = sender
    self.recipient = recipient
    self.lines = []

  def lineReceived(self, line):
    self.lines.append(line)

  def connectionLost(self):
    self.lines = None

  def sendEmail(self, sender: str, recipient: str, content: str):
    print(f"Sending email from {sender} to {recipient}")
    file = open(join(MESSAGES_DIR, f"{uuid4()}.eml"), "w")
    file.write(content)
    file.close()

  def eomReceived(self):
    content = b"\n".join(self.lines).decode()
    self.lines = None
    self.sendEmail(self.sender, self.recipient, content)
    return defer.succeed(None)



class SMTPFactory(protocol.ServerFactory):
  def buildProtocol(self, addr):
    p = smtp.ESMTP()
    p.factory = self
    p.host = smtp.DNSNAME
    p.portal = Portal(Realm(), [Checker()])
    p.challengers = {
      b"LOGIN": LOGINCredentials,
      b"PLAIN": PLAINCredentials
    }
    return p

reactor.listenTCP(2490, SMTPFactory())
reactor.run()
