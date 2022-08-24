""" 'server.py' starts Here. """

from select import select
from socket import *
from time import localtime, strftime
import sys

# colour print
err = '\033[91m'
wrn = '\033[93m'
norm = '\033[0m'


# Port numbers that this server will use to run
try:
    port1 = int(sys.argv[1])
    port2 = int(sys.argv[2])
    port3 = int(sys.argv[3])
    if sys.argv[4] != None:
        raise Exception
    # check ports are in range 1024 and 64000(inclusive)
    for port in [port1, port2, port3]:
        assert 1024 <= port <= 64000

except IndexError:
    print(f"{err}ERROR: Please put port number.{norm}")
    sys.exit()

except AssertionError:
    print(f"{err}ERROR: One or more ports are not in between 1024 and 64000.{norm}")
    sys.exit()

except ValueError:
    print(f"{err}ERROR: Port has to be number.{norm}\n(Hint: Do not use comma us spacing.)")
    sys.exit()

except Exception:
    print(f"{wrn}MESSAGE: Ignore 4th port number - only need three of them.{norm}")
    sys.exit()



def generate_response(port: int, request_type: int) -> tuple:
    """ Generate response packet """

    mnth = {'01': ['January', 'Kohitatea', 'Januar'], '02': ['February', 'Hui-tanguru', 'Februar'],
            '03': ['March', 'Poutu-te-rangi', 'Marz'], '04': ['April', 'Paenga-whawha', 'April'],
            '05': ['May', 'Haratua', 'Mai'], '06': ['June', 'Pipiri', 'Juni'], '07': ['July', 'Hongongoi', 'Juli'],
            '08': ['August', 'Here-turi-koka', 'August'], '09': ['September', 'Mahuru', 'Septempber'],
            '10': ['October', 'Whiringa-a-nuku', 'Oktober'], '11': ['November', 'Whiringa-a-rangi', 'November'],
            '12': ['December', 'Hakihea', 'Dezember']}

    mg_num = 0x497E
    pak_type = 0x0002
    year_now = strftime("%Y", localtime()).zfill(2)
    month_now = strftime("%m", localtime()).zfill(2)
    day_now = strftime("%d", localtime()).zfill(2)
    hour_now = strftime("%H", localtime()).zfill(2)
    min_now = strftime("%M", localtime()).zfill(2)

    # 'port' is a port number requested by clients
    # 'port1', 'port2', 'port3' is the port numbers that the server is running.
    if port == port1:
        lang_code = 0x0001
        if request_type == 0x0001:  # Date in English
            pay_load = bytes(f"Today's date is {mnth[month_now][0]} {day_now}, {year_now}", encoding='utf-8')

        elif request_type == 0x0002:  # Time in English
            pay_load = bytes(f"The current time is {hour_now}:{min_now}", encoding='utf-8')

    elif port == port2:
        lang_code = 0x0002
        if request_type == 0x0001:  # Date in Te reo Maori
            pay_load = bytes(f"Ko te ra o tenei ra ko {mnth[month_now][1]} {day_now}, {year_now}", encoding='utf-8')

        elif request_type == 0x0002:  # Time in Te reo Maori
            pay_load = bytes(f"Ko te wa o tenei wa {hour_now}:{min_now}", encoding='utf-8')

    elif port == port3:
        lang_code = 0x0003
        if request_type == 0x0001:  # Date in German
            pay_load = bytes(f"Heute ist der {day_now} {mnth[month_now][2]} {year_now}", encoding='utf-8')

        elif request_type == 0x0002:  # Time in German
            pay_load = bytes(f"Die Uhrzeit ist {hour_now}:{min_now}", encoding='utf-8')

    if len(pay_load) > 255:
        print(f"{err}ERROR: Text exceed 255 bytes.{norm}")
        return None

    # DT-Response packet generate begins.
    new_packet = bytearray(13)
    new_packet[0] = mg_num >> 8
    new_packet[1] = mg_num & 0xFF
    new_packet[2] = 0x00
    new_packet[3] = pak_type
    new_packet[4] = 0x00
    new_packet[5] = lang_code
    new_packet[6] = int(year_now) >> 8
    new_packet[7] = int(year_now) & 0xFF
    new_packet[8] = int(month_now)
    new_packet[9] = int(day_now)
    new_packet[10] = int(hour_now)
    new_packet[11] = int(min_now)
    new_packet[12] = len(pay_load)
    new_packet += pay_load

    return new_packet


def dt_request(packet: bytearray) -> int:
    """ check DT-request packet from client and generate packet to send back to client """

    if len(packet) != 6:
        print(f"{err}ERROR: Packet does not contain 6 bytes.{norm}")

    elif (packet[0] << 8) | packet[1] != 0x497e:
        print(f"{err}ERROR: Wrong packet received.{norm}")

    elif (packet[2] << 8) | packet[3] != 0x0001:
        print(f"{err}ERROR: Wrong packet type received.{norm}")

    elif (packet[4] << 8) | packet[5] > 2:
        print(f"{err}ERROR: Unknown Request.{norm}")

    else:
        return (packet[4] << 8) | packet[5]


def server():
    """ main function """
    try:
        sokt_1 = socket(AF_INET, SOCK_DGRAM)
        sokt_1.bind(('', port1))
        sokt_2 = socket(AF_INET, SOCK_DGRAM)
        sokt_2.bind(('', port2))
        sokt_3 = socket(AF_INET, SOCK_DGRAM)
        sokt_3.bind(('', port3))

    except Exception:
        print(f"{err}ERROR: Socket binding Failure.")
        print(f"ERROR: Are the ports have unique value?{norm}")
        sys.exit()

    soc_list = [sokt_1, sokt_2, sokt_3]

    while True:
        try:
            sokt_list, list_ignore, except_list = select(soc_list, [], [])
            if sokt_list[0] in soc_list:
                port = sokt_list[0].getsockname()[1]
                msg, addr = sokt_list[0].recvfrom(50000)
                request_type = dt_request(msg)
                if request_type != None:
                    new_msg = generate_response(port, request_type)
                    sokt_list[0].sendto(new_msg, addr)
                else:
                    print(f"{wrn}FATAL: Packet does not match the requirement.")
                    print(f"FATAL: Cannot give any response packet to client.{norm}")
                    sokt_list.remove(sokt_list[0])

        except KeyboardInterrupt:
            print("\n\nMESSAGE: Shutting down this server.")
            sokt_1.close()
            sokt_2.close()
            sokt_3.close()
            sys.exit()


if __name__ == '__main__':
    server()

""" 'server.py' ends here """