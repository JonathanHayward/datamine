#!/usr/bin/python

"""A search engine originally intended to allow searching of the Christian
Classics Ethereal Library Nicene and Post-Nicene Fathers' collection and be
flexible enough to be modifiable to other use.""" 

import cgi
import cPickle
import os
import random
import socket
import sys

DEFAULT_PORT = 1358

servers = [
  ("127.0.0.1",),
  ("127.0.0.1", 1054,),
  ("127.0.0.1", 1055,),
  ("127.0.0.1", 1056,),
  ("127.0.0.1", 1057,),
  #("10.0.0.1",),
  #("10.0.0.64",),
  #("10.0.0.64", 1054,),
  #("10.0.1.4",),
  #("10.0.1.4", 1054,),
  #("10.0.1.4", 1055,),
  #("10.0.1.4", 1056,),
  #("10.0.6.8",),
  ]

def get_page_from_oracle():
    random.shuffle(servers)
    for server in servers:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ip = server[0]
            try:
                port = int(server[1])
            except:
                port = DEFAULT_PORT
            sock.connect((ip, port))
            sockIn = sock.makefile("rb")
            sockOut = sock.makefile("wb")
            cgi_hash = {}
            for key in cgi.FieldStorage().keys():
                cgi_hash[key] = cgi.FieldStorage()[key].value
            cPickle.dump((os.environ, cgi_hash), sockOut)
            sockOut.flush()
            result = cPickle.load(sockIn)
            sock.close()
            sockIn.close()
            sockOut.close()
            return result
        except:
            pass
    return """Content-type: text/html

<html>
    <head>
        <meta http-equiv="Refresh" value="60">
        <title>Orthodox Church Fathers (Down)</title>
        <link rel="stylesheet" href="/fathers/fathers.css">
    </head>
    <body>
        <table border="0" width="100%">
            <tr>
                <td width="100%" height="15">
                </td>
            </tr>
            <tr>
                <td>
                    <h1 id="title"
                    style="text-align: center; margin-top: 0px">Orthodox Church
                    Fathers (presently down)</h1>

                    <p>We're sorry, but this searchable Fathers archive isn't
                    available now. You can still <a
                    href="/fathers/"><strong>browse the
                    Orthodox Church Fathers archive</strong> (<em>Ante-Nicene
                    Fathers</em>, and <em>Nicene and Post-Nicene Fathers</em>:
                    both Series I and Series II).</a></p>
                    
                    <p>(If you need to, you can <a
                    href="http://JonathansCorner.com/contact/">contact the
                    administrator</a>.)</p>
                </td>
            </tr>
        </table>
    </body>
</html>
"""

if __name__ == "__main__":
    sys.stdout.write(get_page_from_oracle())
