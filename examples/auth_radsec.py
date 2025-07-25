import asyncio
import os

from loguru import logger

from pyrad2.constants import PacketType
from pyrad2.dictionary import Dictionary
from pyrad2.radsec.client import RadSecClient

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 2083

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
CA_CERTFILE = os.path.join(THIS_FOLDER, "certs/ca/ca.cert.pem")
CLIENT_CERTFILE = os.path.join(THIS_FOLDER, "certs/client/client.cert.pem")
CLIENT_KEYFILE = os.path.join(THIS_FOLDER, "certs/client/client.key.pem")


async def main():
    client = RadSecClient(
        server="127.0.0.1",
        secret=b"radsec",
        dict=Dictionary(THIS_FOLDER + "/dictionary"),
        certfile=CLIENT_CERTFILE,
        keyfile=CLIENT_KEYFILE,
        certfile_server=CA_CERTFILE,
    )

    req = client.create_auth_packet(code=PacketType.AccessRequest, User_Name="wichert")
    req["NAS-IP-Address"] = "192.168.1.10"
    req["NAS-Port"] = 0
    req["Service-Type"] = "Login-User"
    req["NAS-Identifier"] = "trillian"
    req["Called-Station-Id"] = "00-04-5F-00-0F-D1"
    req["Calling-Station-Id"] = "00-01-24-80-B3-9C"
    req["Framed-IP-Address"] = "10.0.0.100"

    reply = await client.send_packet(req)
    if reply.code == PacketType.AccessAccept:
        logger.info("Access accepted")
    else:
        logger.warning("Access denied")

    logger.info("Attributes returned by server:")
    for i in reply.keys():
        logger.info("{}: {}", i, reply[i])


if __name__ == "__main__":
    asyncio.run(main())
