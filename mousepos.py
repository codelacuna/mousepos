#!/usr/bin/env python
#Hail Eris

from ctypes import windll, Structure, c_ulong, byref
import socket
import sys
import msvcrt
import re

class POINT( Structure ):
    _fields_ = [ ( "x", c_ulong ), ( "y", c_ulong ) ]

def getMousePos( ):
    pt = POINT( )
    windll.user32.GetCursorPos( byref( pt ) )
    return [ pt.x, pt.y ]

def numfromstr( str ):
    pattern = re.compile( "\[(\d+)\,\s+(\d+)\]" )
    match = pattern.search( str )
    return [match.group( 1 ), match.group( 2 )]

if len( sys.argv ) >= 2:
    if sys.argv[1] == "-s":
        host = ""
        port = 4085
        backlog = 0
        size = 1024
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.bind( ( host, port ) )
        s.listen( backlog )
        client, address = s.accept( )
        while not msvcrt.kbhit( ):
            client.send( bytes( str( getMousePos( ) ), "utf8" ) )

    if sys.argv[1] == "-c":
        addr = ( str( sys.argv[2] ), int( sys.argv[3] ) )
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.connect( addr )
        while 1:
            recv = s.recv( 1024 )
            pos = numfromstr( str( recv ) )
            windll.user32.SetCursorPos( int( pos[0] ), int( pos[1] ) )

else:
    print( str( sys.argv[0] ) + " [-s/-c] [host] [port]" )
    print( "    -s:      Operate in server mode" )
    print( "            (ignores host and port)" )
    print( "    -c:      Operate in client mode" )
