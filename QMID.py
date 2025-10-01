levels = (
    (0, 0, 0x02, 0x02),
    (0, 0, 0x08, 0x08),
    (2, 1, 0x20, 0x26),
    (5, 3, 0x80, 0x9B),
    (11, 7, 0x200, 0x26F),
    (23, 15, 0x800, 0x9BF),
    (47, 31, 0x2000, 0x26ff),
    (95, 63, 0x8000, 0x9bff),
    (191, 127, 0x20000, 0x26FFF),
    (383, 255, 0x80000, 0x9BFFF),
	(767, 511, 0x200000, 0x26FFFF),
	(1535,	1023,	0x800000,	0x9BFFFF),
	(3071,	2047,	0x2000000,	0x26FFFFF),
	(6143,	4095,	0x8000000,	0x9BFFFFF),
	(12287,	8191,	0x20000000,	0x26FFFFFF),
	(24575,	16383,	0x80000000,	0x9BFFFFFF)
)

def getLevel(dword):
    for number, level in enumerate(levels):
        if level[2] <= dword and dword <= level[3]:
            return level , number

def calcQMIDFromDword(dwordA: int, dwordB):

    level, levelNbr = getLevel(dwordA)
    workA = dwordA - (2 << (2 * levelNbr))

    workB = 0
    if dwordB > 0:
        levelB, levelNbrb = getLevel(dwordB)
        workB = dwordB - (2 << (2 * levelNbrb))

    byteRepr = workA.to_bytes(workA.bit_count(), "little")
    print(byteRepr)
    U01 = byteRepr[0]
    b = byteRepr[1]
    return U01, b, workA