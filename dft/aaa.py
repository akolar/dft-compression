import numpy as np
import struct


def dump(object_, file_):
    # No need to check file_.mode, writing binary data will fail on .write()
    serializer = AAASerializer(object_)

    for chunk in serializer.serialize():
        file_.write(chunk)


def load(file_):
    deserializer = AAADeserializer(file_)
    return deserializer.deserialize()


class AAASerializer:
    """
    Class for serialization of a numpy array into a bit representation.

    AAA Format specification:
        File consists of a header and an arbitrary amount of entries.

        Header
        ======

        <image shape x (2 byte)>
        <image shape y (2 bytes)>
        <bytes per Re record (1 byte)>
        <image is grayscale (1 byte)>

        Entry
        =====

        Entry type 00000000 (no data)
        -----------------------------

        Entry type 00001xxx (color channel)
        -----------------------------------

        Red channel: 000011xx
        Green channel: 00001x1x
        Blue channel: 00001xx1
        Grey channel: 00001000

        For each 1 on the last 3 bits an additional color entry follows:
        <value of real component (size as specified in header)>
    """

    __DATATYPES = ((8, 'b'), (16, 'h'), (32, 'i'))
    _dt_type = '<B'

    def __init__(self, obj):
        self.obj = obj

        # All Re and Im components will always be <= abs(max(A))
        self._bytes_val, dtv, self.delta = self._get_byte_count(
            np.absolute(self.obj.max()))
        self._bytes_val = 32
        self._dt_val = '<{}'.format('i')
        self._grayscale = len(obj.shape) == 2

    def serialize(self):
        yield struct.pack('<H', self.obj.shape[0])
        yield struct.pack('<H', self.obj.shape[1])
        yield struct.pack('<B', self.delta)
        yield struct.pack('<?', self._grayscale)

        if self._grayscale:
            yield from self._serialize_grayscale()
        else:
            yield from self._serialize_rgb()

    def _serialize_grayscale(self):
        for r in self.obj:
            yield from map(
                lambda x:
                struct.pack(self._dt_type, 0b00000000) if x == 0 else
                (
                    struct.pack(self._dt_type, 0b00001000) +
                    struct.pack(self._dt_val, int(x) >> self.delta)
                ),
                r
            )

    def _serialize_rgb(self):
        for r in self.obj:
            yield from map(self._convert_rgb, r)

    def _convert_rgb(self, pixel):
        x = 1
        data = []
        for v in pixel:
            x <<= 1
            if v != 0:
                x += 1
                data.append(struct.pack(self._dt_val, int(v) >> self.delta))

        if not data:
            return struct.pack(self._dt_type, 0)

        res = struct.pack(self._dt_type, x)
        res += b''.join(data)

        return res

    def _get_byte_count(self, x, signed=True):
        log = int(np.ceil(np.log2(x)))

        size_ok = (lambda x: log + 1 <= x) if signed else (lambda x: log <= x)
        for limit, dtype in self.__DATATYPES:
            if size_ok(limit):
                delta = 0
                break
        else:
            delta = log + 1 - limit if signed else log - limit

        return (limit, dtype, delta) if signed else (limit, dtype.upper(), delta)


class AAADeserializer:

    def __init__(self, stream):
        self.stream = stream

    def deserialize(self):
        shape = []
        shape.append(struct.unpack('<H', self.stream.read(2))[0])
        shape.append(struct.unpack('<H', self.stream.read(2))[0])
        delta = struct.unpack('<B', self.stream.read(1))[0]
        gray = struct.unpack('<?', self.stream.read(1))[0]

        if gray:
            image = np.zeros(shape)
        else:
            image = np.zeros(shape + [3])

        x = -1
        y = 0
        byte = self.stream.read(1)
        cnt = 0
        while byte:
            x += 1
            if x >= shape[1]:
                x = 0
                y += 1

            pixel_info = struct.unpack('<B', byte)[0]
            if pixel_info & 0b1000 == 0:
                byte = self.stream.read(1)
                continue

            cnt += 1
            if pixel_info & 0b0111 == 0:  # gray
                image[y, x] = struct.unpack('<i', self.stream.read(4))[0] << delta
            if pixel_info & 0b0100 > 0:  # red channel
                image[y, x, 0] = struct.unpack('<i', self.stream.read(4))[0] << delta
            if pixel_info & 0b0010 > 0:  # green channel
                image[y, x, 1] = struct.unpack('<i', self.stream.read(4))[0] << delta
            if pixel_info & 0b0001 > 0:  # blue channel
                image[y, x, 2] = struct.unpack('<i', self.stream.read(4))[0] << delta

            byte = self.stream.read(1)

        return image
