from PIL import Image
from bitarray import bitarray
import sys

# DEFINES
BLACK_RGB = (0,0,0)
WHITE_RGB = (255,255,255)

def parseImage(filename):
    """ return all rgb pixel
    """
    print "reading " + filename + " data\n"
    im = Image.open(filename)
    rgb_im = im.convert('RGB')
    (width, height) = im.size
    mapImg = list()
    for y in xrange(height):
        line = list()
        for x in xrange(width):
            line.append(rgb_im.getpixel((x, y)))
        mapImg.append(line)
    return mapImg

def genNoiseImage(filename, mapImg):
    """ create an image to locate lsb
    """
    outname = filename.replace(".bmp", "-noise.bmp")
    size = (len(mapImg[0]), len(mapImg))
    im = Image.new('RGB', size)
    (width, height) = im.size
    for y in xrange(height):
        for x in xrange(width):
            r,g,b = mapImg[y][x]
            im.putpixel((x,y), WHITE_RGB if ((r & 1)  + (g & 1)  + ( b & 1)) == 0 else BLACK_RGB)
    print "saving noise to " + outname + "\n"
    im.save(outname)

def searchForString(filename, mapImg):
    """export lsb to binary file
    """
    outname = filename.replace(".bmp", "-binarydata")
    array = bitarray()
    size = (len(mapImg[0]), len(mapImg))
    im = Image.new('RGB', size)
    (width, height) = im.size
    for y in xrange(height):
        for x in xrange(width):
            r,g,b = mapImg[y][x]
            array.append(r & 1)
            array.append(g & 1)
            array.append(b & 1)
    f = file(outname, "a")
    f.write(array.tobytes())
    f.close()
    print "binary data written to " + outname
    print "`file " + outname + "` to see if binary correspond to some filetype"
    print "`strings " + outname + "` to search for plaintext\n"

def mapToImg(filename, mapImg):
    """export lsb to image
    """
    outname = filename.replace(".bmp", "-binarydata")
    array = bitarray()
    size = (len(mapImg[0]), len(mapImg))
    im = Image.new('RGB', size)
    (width, height) = im.size
    for y in xrange(height):
        for x in xrange(width):
            r,g,b = mapImg[y][x]
            array.append(r & 1)
            array.append(g & 1)
            array.append(b & 1)
    f = file(outname, "a")
    f.write(array.tobytes())
    f.close()
    print "binary data written to " + outname
    print "`file " + outname + "` to see if binary correspond to some filetype"
    print "`strings " + outname + "` to search for plaintext"
    

def main():
    if len(sys.argv) < 2:
        print "./lsb.py [souce-image]"
    else:
        filename =  sys.argv[1]
        mapImg = parseImage(filename)
        genNoiseImage(filename, mapImg)
        searchForString(filename, mapImg)


if __name__ == "__main__":
    sys.exit(main())
