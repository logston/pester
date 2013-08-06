"""
Paul Logston 2013

This class defines the functionality for sending a Pester.
"""

from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
import urllib2

class SendPester(object):
    """Encapsulates sending a Pester"""

    def __init__(self):
        self.frm = None
        self.to = None
        self.subject = None
        self.url = None
        self.message = None
        print 'Opening server at localhost...',
        self._start_smtp_server('localhost')
        print 'server: ' + str(self.server)


    def __del__(self):
        self.server.quit()

    def _start_smtp_server(self, server):
        """Start server for message sending"""
        self.server = smtplib.SMTP()
        self.server.connect(server)
        self.server.starttls()

    def _validate_field(self, value_name, value):
        if not value:
            raise ValueError('No %s field given' % value_name)

    def send_pester(self, to, url, frm='pester@pestering.me', subject=None):
        """Build and send message"""
        self._validate_field('FROM', frm)
        self.frm = frm
        self._validate_field('TO', to)
        self.to = to
        self.subject = (subject if subject else str(datetime.now()))
        self._validate_field('URL', url)
        self.url = url
            
        self._build_message()
        self._send_email()
    
    def _build_message(self):
        """Build MIMEMultipart message"""
        mime_msg = MIMEMultipart()
        mime_msg['From'] = self.frm
        mime_msg['To'] = self.to
        mime_msg['Subject'] = self.subject
        mime_msg.attach(MIMEImage(self._get_url_resource(self.url)))
        self.message = mime_msg

    def _get_url_resource(self, url):
        """Return data from url"""
        return urllib2.urlopen(url).read()

    def _send_email(self):
        """Send message via SMTP Server"""
        self.server.sendmail(self.frm, self.to, self.message.as_string())
