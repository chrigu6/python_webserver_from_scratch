import typing
import socket

class Request(typing.NamedTuple):
    method: str
    path: str
    headers: typing.Mapping[str, str]

    
    @classmethod
    def iter_lines(self, sock: socket.socket, bufsize: int = 16_384) -> typing.Generator[bytes, None, bytes]:
        buff = b""
        while True:
            data = sock.recv(bufsize)
            if not data:
                    return b""

            buff += data
            while True:
                try:
                    i = buff.index(b"\r\n")
                    line, buff = buff[:i], buff[i + 2:]
                    if not line:
                        return buff

                    yield line
                except IndexError:
                    break

    @classmethod
    def from_socket(cls, sock: socket.socket) -> "Request":
        """Read and parse the request from a socket object.

        Raises:
          ValueError: When the request cannot be parsed.
        """
        lines = cls.iter_lines(sock)

        try:
            request_line = next(lines).decode("ascii")
        except StopIteration:
            raise ValueError("Request line missing.")

        try:
            method, path, _ = request_line.split(" ")
        except ValueError:
            raise ValueError(f"Malformed request line {request_line!r}.")

        headers = {}
        for line in lines:
            try:
                name, _, value = line.decode("ascii").partition(":")
                headers[name.lower()] = value.lstrip()
            except ValueError:
                raise ValueError(f"Malformed header line {line!r}.")

        return cls(method=method.upper(), path=path, headers=headers)