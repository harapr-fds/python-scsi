#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.pyscsi.scsi_command import OPCODE
from sgio.utils.converter import scsi_ba_to_int

class MockWrite16(object):
   def execute(self, cdb, dataout, datain, sense):
      pass

def main():
    s = SCSI(MockWrite16())
    data = bytearray(27 * 512)

    w = s.write16(1024, 27, data)
    cdb = w._cdb
    assert cdb[0] == OPCODE.WRITE_16
    assert cdb[1] == 0
    assert scsi_ba_to_int(cdb[2:10]) == 1024
    assert scsi_ba_to_int(cdb[10:14]) == 27
    assert cdb[14] == 0
    assert cdb[15] == 0
    cdb = w.unmarshall_cdb(cdb)
    assert cdb['opcode'] == OPCODE.WRITE_16
    assert cdb['wrprotect'] == 0
    assert cdb['dpo'] == 0
    assert cdb['fua'] == 0
    assert cdb['lba'] == 1024
    assert cdb['group'] == 0
    assert cdb['tl'] == 27

    w = s.write16(65536, 27, data, wrprotect=2, dpo=1, fua=1, group=19)
    cdb = w._cdb
    assert cdb[0] == OPCODE.WRITE_16
    assert cdb[1] == 0x58
    assert scsi_ba_to_int(cdb[2:10]) == 65536
    assert scsi_ba_to_int(cdb[10:14]) == 27
    assert cdb[14] == 0x13
    assert cdb[15] == 0
    cdb = w.unmarshall_cdb(cdb)
    assert cdb['opcode'] == OPCODE.WRITE_16
    assert cdb['wrprotect'] == 2
    assert cdb['dpo'] == 1
    assert cdb['fua'] == 1
    assert cdb['lba'] == 65536
    assert cdb['group'] == 19
    assert cdb['tl'] == 27

if __name__ == "__main__":
    main()

