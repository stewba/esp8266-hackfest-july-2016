# MicroPython Web Server
try:
    import usocket as socket
except:
    import socket

#Define some web content
SWITCH_AJAX_CONTENT = b"""\
HTTP/1.0 200 OK
Content-type: text/javascript

{ "channel": %d, "result": "%s", "value": %d }
"""

SWITCH_AJAX_ERROR = b"""\
HTTP/1.0 500 Internal Error

Internal Server Error!
"""

PAGE_CONTENT = b"""\
HTTP/1.0 200 OK

<html>
<title>Switchy 1.0</title>
<body>
<h1>Switchy 1.0</h1>
<div id="responsediv"></div>
<div style="clear:left;">
<h2>Turn On</h1>
<ul>
<li><a href="/switch?ch=0?value=1">Channel 1</a></li>
<li><a href="/switch?ch=1?value=1">Channel 2</a></li>
<li><a href="/switch?ch=2?value=1">Channel 3</a></li>
</ul>
</div>
<div style="float:left;">
<h2>Turn Off</h2>
<ul>
<li><a id="ch1_off" href="#">Channel 1</a></li>
<li><a href="/switch?ch=1?value=0">Channel 2</a></li>
<li><a href="/switch?ch=2?value=0">Channel 3</a></li>
</ul>
</div>
<script src="https://code.jquery.com/jquery-2.2.4.min.js"></script>
<script>
function request_switch(channel, value) {
    $.ajax("/switch?ch=" + channel + "?value=" + value, {
        success: function(data) {
            console.log(data);
            $("#responsediv").html("Channel " + data.ch + " switched " + data.value + " (" + data.result + ")");
        },
        error: function(data) {
            $("#responsediv").html("Could not perform switch!");
        }
    });
}
$(function() {
    $("#ch1_off").click(function(e) { e.preventDefault(); request_switch(0, 0); });
    $("#ch2_off").click(function(e) { e.preventDefault(); request_switch(1, 0); });
    $("#ch3_off").click(function(e) { e.preventDefault(); request_switch(2, 0); });
    $("#ch1_on").click(function(e) { e.preventDefault(); request_switch(0, 1); });
    $("#ch2_on").click(function(e) { e.preventDefault(); request_switch(1, 1); });
    $("#ch3_on").click(function(e) { e.preventDefault(); request_switch(2, 1); });
});
</script>
</body>
</html>
"""

ERROR_404 = b"""\
HTTP/1.0 404 Not Found

<html>
<body>
<h1>404 Not Found</h1>
<p>Try again!</p>
</body>
</html>
"""

def switch(channel, value):
    """
    Perform the actual switching with the GPIO here
    """
    # TODO - press the button!!!
    return 'OK'

def perform_switch(request):
    """
    Figure out which channel to switch on or off
    """
    parameters = request.split('?')
    ch = None
    value = None
    for p in parameters:
        print(p)
        if p.startswith('ch='):
            ch = p.split('=')[1]
        elif p.startswith('value='):
            value = p.split('=')[1]
        print(ch)
        print(value)
    if ch is not None and value is not None:
        response = switch(ch, value)
        return SWITCH_AJAX_CONTENT % (int(ch), response, int(value))
    else:
        return SWITCH_AJAX_ERROR

def main():
    s = socket.socket()

    ai = socket.getaddrinfo("0.0.0.0", 8080)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    # The main loop
    while True:
        res = s.accept()
        client_s = res[0]
        print("Request:")
        # MicroPython socket objects support stream (aka file) interface
        # directly.
        req = client_s.readline()
        print(req)
        # Determine which page is being requested
        RESPONSE = None
        if req.startswith(b"GET"):
            request = str(req).split(' ')[1]
            if request == "/":
                RESPONSE = PAGE_CONTENT
            elif request.startswith("/switch"):
                RESPONSE = perform_switch(request)
            else:
                RESPONSE = ERROR_404
        while True:	# Read all the headers (right now we're not going to do anything with them)
            h = client_s.readline()
            if h == b"" or h == b"\r\n":
                break
        # Send the response back to the client
        client_s.write(RESPONSE)
        client_s.close()


main()
