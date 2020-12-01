import zlib


str_object1 = open('test.db', 'rb').read()
str_object2 = zlib.compress(str_object1, 9)
f = open('cmp.db', 'wb')
f.write(str_object2)
f.close()

str_object1 = open('cmp.db', 'rb').read()
str_object2 = zlib.decompress(str_object1)
f = open('dcmp.db', 'wb')
f.write(str_object2)
f.close()



original_data = open('test.db', 'rb').read()
compressed_data = zlib.compress(original_data, zlib.Z_BEST_COMPRESSION)

f = open('cmp.db', 'w')
f.write(str(compressed_data))
f.close()

CHUNKSIZE = 1024

data2 = zlib.decompressobj()
my_file = open('cmp.db', 'rb')
buf = my_file.read(CHUNKSIZE)

while buf:
    decompressed_data = data2.decompress(buf)
    buf = my_file.read(CHUNKSIZE)

decompressed_data += data2.flush()

f = open('dcmp.db', 'w')
f.write(str(decompressed_data))
f.close()