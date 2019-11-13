# greaseweazle/hfe.py
#
# Written & released by Keir Fraser <keir.xen@gmail.com>
#
# This is free and unencumbered software released into the public domain.
# See the file COPYING for more details, or visit <http://unlicense.org>.

import struct

from greaseweazle.bitcell import Bitcell

class HFE:

    def __init__(self, start_cyl, nr_sides):
        self.start_cyl = start_cyl
        self.nr_sides = nr_sides
        self.nr_revs = None
        self.track_list = []


    @classmethod
    def from_file(cls, dat):
        hfe = cls(0, 2)
        return hfe


    def get_track(self, cyl, side, writeout=False):
        return None
    
        
    def append_track(self, flux):
        bc = Bitcell()
        bc.read_flux(flux)
        self.track_list.append(bc)


    def get_image(self):
        s_cyl = self.start_cyl + len(self.track_list) // self.nr_sides
        bitrate = 250 # XXX
        header = struct.pack("<8s4B2H2BH",
                             b"HXCPICFE",
                             0,
                             s_cyl,
                             self.nr_sides,
                             0xff, # unknown encoding
                             bitrate,
                             0,    # rpm (unused)
                             0xff, # unknown interface
                             1,    # rsvd
                             1)    # track list offset
        header += bytes([0xff] * (0x200 - len(header)))
        header += bytes(self.start_cyl * 4)
        for i in range(0, len(self.track_list), self.nr_sides):
            bc = self.track_list[i]
            bits, _ = bc.revolution_list[0]
            nr_bytes = ((bits.length() + 7) // 8) * 2
            nr_blocks = (nr_bytes + 0x1ff) // 0x200
            print(nr_blocks)
        header += bytes([0xff] * (0x400 - len(header)))
        return header


# Local variables:
# python-indent: 4
# End:
