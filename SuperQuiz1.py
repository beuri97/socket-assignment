def compose_header(version, hdrlen, tosdscp, totallength, identification, flags, fragmentoffset, timetolive, protocoltype, headerchecksum, sourceaddress, destinationaddress):

    total = 0
    if version != 4:
        return 1
    else:
        total += version << 156

    if hdrlen > 0xF or hdrlen < 0:
        return 2
    else:
        total += hdrlen << 152

    if tosdscp > 0x3F or tosdscp < 0:
        return 3
    else:
        total += tosdscp << 144

    if totallength > 0xFFFF or totallength < 0:
        return 4
    else:
        total += totallength << 128

    if identification > 0xFFFF or identification < 0:
        return 5
    else:
        total += identification << 112

    if flags >0x7 or flags < 0:
        return 6
    else:
        total += flags << 109

    if fragmentoffset > 0x1FFF or fragmentoffset < 0:
        return 7
    else:
        total += fragmentoffset << 96

    if timetolive > 0xFF or timetolive < 0:
        return 8
    else:
        total += timetolive << 88

    if protocoltype > 0xFF or protocoltype < 0:
        return 9
    else:
        total += protocoltype << 80

    if headerchecksum > 0xFFFF or headerchecksum < 0:
        return 10
    else:
        total += headerchecksum << 64

    if sourceaddress > 0xFFFFFFFF or sourceaddress <0:
        return 11
    else:
        total += sourceaddress << 32

    if destinationaddress > 0xFFFFFFFF or destinationaddress <0:
        return 12
    else:
        total += destinationaddress

    result = []
    while total != 0:
        a = total & 0xFF
        result.insert(0, a)
        total >>= 8
    
    return result


header = compose_header(4,5,0,1500,24200,0,63,22,6,4711, 2190815565, 3232270145)
print(header)

def compose_header2(version, hdrlen, tosdscp, totallength, identification, flags, fragmentoffset, timetolive, protocoltype, headerchecksum, sourceaddress, destinationaddress):

    result  = bytearray(20)
    if version != 4:
        return 1

    if hdrlen > 0xF or hdrlen < 0:
        return 2

    result[0] = (version << 4) + hdrlen

    if tosdscp > 0x3F or tosdscp < 0:
        return 3
    else:
        total += tosdscp << 144

    if totallength > 0xFFFF or totallength < 0:
        return 4
    else:
        total += totallength << 128

    if identification > 0xFFFF or identification < 0:
        return 5
    else:
        total += identification << 112

    if flags >0x7 or flags < 0:
        return 6
    else:
        total += flags << 109

    if fragmentoffset > 0x1FFF or fragmentoffset < 0:
        return 7
    else:
        total += fragmentoffset << 96

    if timetolive > 0xFF or timetolive < 0:
        return 8
    else:
        total += timetolive << 88

    if protocoltype > 0xFF or protocoltype < 0:
        return 9
    else:
        total += protocoltype << 80

    if headerchecksum > 0xFFFF or headerchecksum < 0:
        return 10
    else:
        total += headerchecksum << 64

    if sourceaddress > 0xFFFFFFFF or sourceaddress <0:
        return 11
    else:
        total += sourceaddress << 32

    if destinationaddress > 0xFFFFFFFF or destinationaddress <0:
        return 12
    else:
        total += destinationaddress

    result = []
    while total != 0:
        a = total & 0xFF
        result.insert(0, a)
        total >>= 8

    return result




def compose_packet(hdrlen, tosdscp, identification, flags, fragmentoffset, timetolive, protocoltype, sourceaddress, destinationaddress, payload) -> bytearray:

    if hdrlen > 0xF or hdrlen < 5:
        return 2

    if tosdscp > 0x3F or tosdscp < 0:
        return 3

    if identification > 0xFFFF or identification < 0:
        return 5

    if flags >0x7 or flags < 0:
        return 6

    if fragmentoffset > 0x1FFF or fragmentoffset < 0:
        return 7

    if timetolive > 0xFF or timetolive < 0:
        return 8

    if protocoltype > 0xFF or protocoltype < 0:
        return 9

    if sourceaddress > 0xFFFFFFFF or sourceaddress <0:
        return 11

    if destinationaddress > 0xFFFFFFFF or destinationaddress <0:
        return 12

    version = 4
    totallength = 4 * hdrlen + len(payload)
    result  = bytearray(hdrlen*4)
    
    result[0] = (version << 4) + hdrlen
    result[1] = tosdscp << 2
    result[2] = totallength >> 8
    result[3] = totallength & 0xFF
    result[4] = identification >> 8
    result[5] = identification & 0xFF
    result[6] = (flags << 5) + (fragmentoffset >> 8) 
    result[7] = fragmentoffset & 0xFF
    result[8] = timetolive
    result[9] = protocoltype
    result[10] = 0
    result[11] = 0
    result[12] = sourceaddress >> 24
    result[13] = (sourceaddress >> 16) & 0xFF
    result[14] = (sourceaddress >> 8) & 0xFF
    result[15] = sourceaddress & 0xFF
    result[16] = destinationaddress >> 24
    result[17] = (destinationaddress >> 16) & 0xFF
    result[18] = (destinationaddress >> 8) & 0xFF
    result[19] = destinationaddress & 0xFF
    if hdrlen == 6:
        result[20] = 0
        result[21] = 0
        result[22] = 0
        result[23] = 0

    X = sum((result[i]<<8) + result[i+1] for i in range(0, hdrlen*4, 2))
    x0 = X & 0xFFFF
    x1 = X >> 16
    X = x0 + x1
    X = 0xFFFF - X
    result[10] = X >> 8
    result[11] = X & 0xFF
    result += payload

    return result

