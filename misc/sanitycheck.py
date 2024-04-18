#!/usr/bin/env python3
#
# Performs some non-exhaustive tests on tzx.py
# All tests succeed if no output is generated.
#
from modules.tzx import *

# Sanity Check
binary = "\x00" * 10
binary2 = "\x00" * 20
binary3 = "\x00" * 65536
binary4 = "\x00" * 16777216

########################
# LOOP END BLOCK TESTS #
########################
leb1 = Blk_LEB()
leb2 = Blk_LEB()
leb3 = Blk_LEB()

if leb1.id != TZXBLK_LEB:
    print("Sanity Failure: Loop End Block 1")

if leb2.id != TZXBLK_LEB:
    print("Sanity Failure: Loop End Block 2")

if leb3.id != TZXBLK_LEB:
    print("Sanity Failure: Loop End Block 3")

##########################
# LOOP START BLOCK TESTS #
##########################
lsb1 = Blk_LSB()
lsb2 = Blk_LSB(4)
lsb2.repetitions(10)
lsb3 = Blk_LSB(5)

if lsb1.repetitions() != 2:
    print("Sanity Failure: Loop Start Block 1")

if lsb2.repetitions() != 10:
    print("Sanity Failure: Loop Start Block 2")

if lsb3.repetitions() != 5:
    print("Sanity Failure: Loop Start Block 3")

#######################
# JUMP TO BLOCK TESTS #
#######################
jtb1 = Blk_JTB()
jtb2 = Blk_JTB(4)
jtb3 = Blk_JTB(5)
jtb2.jump(10)

if jtb1.jump() != 1:
    print("Sanity Failure: Jump To Block 1")

if jtb2.jump() != 10:
    print("Sanity Failure: Jump To Block 2")

if jtb3.jump() != 5:
    print("Sanity Failure: Jump To Block 3")

#########################
# GROUP END BLOCK TESTS #
#########################
geb1 = Blk_GEB()
geb2 = Blk_GEB()
geb3 = Blk_GEB()

if geb1.id != TZXBLK_GEB:
    print("Sanity Failure: Group End Block 1")

if geb2.id != TZXBLK_GEB:
    print("Sanity Failure: Group End Block 2")

if geb3.id != TZXBLK_GEB:
    print("Sanity Failure: Group End Block 3")

#####################
# PAUSE BLOCK TESTS #
#####################
pb1 = Blk_PB()
pb2 = Blk_PB(4)
pb3 = Blk_PB(5)
pb2.duration(10)

if pb1.duration() != 0:
    print("Sanity Failure: Pause Block 1")

if pb2.duration() != 10:
    print("Sanity Failure: Pause Block 2")

if pb3.duration() != 5:
    print("Sanity Failure: Pause Block 3")

##############################
# PULSE SEQUENCE BLOCK TESTS #
##############################
psb1 = Blk_PSB()
psb2 = Blk_PSB()
psb3 = Blk_PSB()
psb4 = Blk_PSB()

# Add 1 pulse to psb2
psb2.add_pulse(100)

# Add 2 pulses to psb3
psb3.add_pulse(200)
psb3.add_pulse(300)

# Add 255 pulses to psb4
for q in range(255):
    psb4.add_pulse(400)

if psb1.pulsenum() != 0:
    print("Sanity Failure: Pulse Sequence Block 1")

if psb2.pulsenum() != 1:
    print("Sanity Failure: Pulse Sequence Block 2")

if psb3.pulsenum() != 2:
    print("Sanity Failure: Pulse Sequence Block 3")

if psb4.add_pulse(400) != 1:
    print("Sanity Failure: Pulse Sequence Block 4 on Error Check")

if psb4.pulsenum() != 255:
    print("Sanity Failure: Pulse Sequence Block 4")

#########################
# PURE TONE BLOCK TESTS #
#########################
ptb1 = Blk_PTB()
ptb2 = Blk_PTB(100, 500)
ptb3 = Blk_PTB()
ptb4 = Blk_PTB()
ptb3.pulselen(1000)
ptb3.pulsenum(5000)

if ptb1.pulselen() != 0:
    print("Sanity Failure: Pure Tone Block 1, Test 1")

if ptb1.pulsenum() != 0:
    print("Sanity Failure: Pure Tone Block 1, Test 2")

if ptb2.pulselen() != 100:
    print("Sanity Failure: Pure Tone Block 2, Test 1")

if ptb2.pulsenum() != 500:
    print("Sanity Failure: Pure Tone Block 2, Test 2")

if ptb3.pulselen() != 1000:
    print("Sanity Failure: Pure Tone Block 3, Test 1")

if ptb3.pulsenum() != 5000:
    print("Sanity Failure: Pure Tone Block 3, Test 2")

###################################
# STANDARD SPEED DATA BLOCK TESTS #
###################################
ssdb1 = Blk_SSDB()
ssdb2 = Blk_SSDB(5000, binary)
ssdb3 = Blk_SSDB()
ssdb3.encapsulate(binary2)
ssdb3.pause(1200)
ssdb4 = Blk_SSDB(data=binary)
ssdb5 = Blk_SSDB(data=binary3)

if ssdb1.pause() != 1000:
    print("Sanity Failure: Standard Speed Data Block 1, Test 1")

if ssdb1.datalen() != 0:
    print("Sanity Failure: Standard Speed Data Block 1, Test 2")

if ssdb2.pause() != 5000:
    print("Sanity Failure: Standard Speed Data Block 2, Test 1")

if ssdb2.datalen() != 10:
    print("Sanity Failure: Standard Speed Data Block 2, Test 2")

if ssdb3.pause() != 1200:
    print("Sanity Failure: Standard Speed Data Block 3, Test 1")

if ssdb3.datalen() != 20:
    print("Sanity Failure: Standard Speed Data Block 3, Test 2")

if ssdb4.pause() != 1000:
    print("Sanity Failure: Standard Speed Data Block 4, Test 1")

if ssdb4.datalen() != 10:
    print("Sanity Failure: Standard Speed Data Block 4, Test 2")

if ssdb5.datalen() != 0:
    print("Sanity Failure: Standard Speed Data Block 5, Test 1")

if ssdb5.encapsulate(binary3) != 1:
    print("Sanity Failure: Standard Speed Data Block 5, Test 2")

############################################
# STOP THE TAPE IF IN 48K MODE BLOCK TESTS #
############################################
st48mb1 = Blk_ST48MB()
st48mb2 = Blk_ST48MB()
st48mb3 = Blk_ST48MB()

if st48mb1.id != TZXBLK_ST48MB:
    print("Sanity Failure: Stop the Tape if in 48k Mode Block 1")

if st48mb2.id != TZXBLK_ST48MB:
    print("Sanity Failure: Stop the Tape if in 48k Mode Block 2")

if st48mb3.id != TZXBLK_ST48MB:
    print("Sanity Failure: Stop the Tape if in 48k Mode Block 3")

################################
# TEXT DESCRIPTION BLOCK TESTS #
################################
tdb1 = Blk_TDB()
tdb2 = Blk_TDB("MyString")
tdb3 = Blk_TDB()
tdb3.description("Another String")

s = "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog" \
    "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog" \
    "The quick brown fox jumps over the lazy dog. THE TEXT SHOULD BE TRUNCATED AT... 255 BYTES."

tdb4 = Blk_TDB(s)

if tdb1.description() != "Empty Description":
    print("Sanity Failure: Text Description Block 1")

if tdb2.description() != "MyString":
    print("Sanity Failure: Text Description Block 2")

if tdb3.description() != "Another String":
    print("Sanity Failure: Text Description Block 3")

if (tdb4.description() != "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog"
                          "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog"
                          "The quick brown fox jumps over the lazy dog. THE TEXT SHOULD BE TRUNCATED AT..."):
    print("Sanity Failure: Text Description Block 4")

################################
# TURBO SPEED DATA BLOCK TESTS #
################################
tsdb1 = Blk_TSDB()
tsdb2 = Blk_TSDB(1000, 2000, 3000, 4000, 5000, 6000, 255, 7000, binary)
tsdb3 = Blk_TSDB()
tsdb3.pilotpulse(100)
tsdb3.syncpulse1(200)
tsdb3.syncpulse2(300)
tsdb3.bitpulse0(400)
tsdb3.bitpulse1(500)
tsdb3.pilottone(600)
tsdb3.usedbits(5)
tsdb3.pause(700)
tsdb3.encapsulate(binary2)
tsdb4 = Blk_TSDB()

if tsdb1.pilotpulse() != 2168:
    print("Sanity Failure: Turbo Speed Data Block 1, Test 1")

if tsdb1.syncpulse1() != 667:
    print("Sanity Failure: Turbo Speed Data Block 1, Test 2")

if tsdb1.syncpulse2() != 735:
    print("Sanity Failure: Turbo Speed Data Block 1, Test 3")

if tsdb1.bitpulse0() != 855:
    print("Sanity Failure: Turbo Speed Data Block 1, Test 4")

if tsdb1.bitpulse1() != 1710:
    print("Sanity Failure: Turbo Speed Data Block 1, Test 5")

if tsdb1.pilottone() != 8063:
    print("Sanity Failure: Turbo Speed Data Block 1, Test 6")

if tsdb1.usedbits() != 8:
    print("Sanity Failure: Turbo Speed Data Block 1, Test 7")

if tsdb1.pause() != 1000:
    print("Sanity Failure: Turbo Speed Data Block 1, Test 8")

if tsdb1.datalen() != 0:
    print("Sanity Failure: Turbo Speed Data Block 1, Test 9")

if tsdb2.pilotpulse() != 1000:
    print("Sanity Failure: Turbo Speed Data Block 2, Test 1")

if tsdb2.syncpulse1() != 2000:
    print("Sanity Failure: Turbo Speed Data Block 2, Test 2")

if tsdb2.syncpulse2() != 3000:
    print("Sanity Failure: Turbo Speed Data Block 2, Test 3")

if tsdb2.bitpulse0() != 4000:
    print("Sanity Failure: Turbo Speed Data Block 2, Test 4")

if tsdb2.bitpulse1() != 5000:
    print("Sanity Failure: Turbo Speed Data Block 2, Test 5")

if tsdb2.pilottone() != 6000:
    print("Sanity Failure: Turbo Speed Data Block 2, Test 6")

if tsdb2.usedbits() != 8:
    print("Sanity Failure: Turbo Speed Data Block 2, Test 7")

if tsdb2.pause() != 7000:
    print("Sanity Failure: Turbo Speed Data Block 2, Test 8")

if tsdb2.datalen() != 10:
    print("Sanity Failure: Turbo Speed Data Block 2, Test 9")

if tsdb3.pilotpulse() != 100:
    print("Sanity Failure: Turbo Speed Data Block 3, Test 1")

if tsdb3.syncpulse1() != 200:
    print("Sanity Failure: Turbo Speed Data Block 3, Test 2")

if tsdb3.syncpulse2() != 300:
    print("Sanity Failure: Turbo Speed Data Block 3, Test 3")

if tsdb3.bitpulse0() != 400:
    print("Sanity Failure: Turbo Speed Data Block 3, Test 4")

if tsdb3.bitpulse1() != 500:
    print("Sanity Failure: Turbo Speed Data Block 3, Test 5")

if tsdb3.pilottone() != 600:
    print("Sanity Failure: Turbo Speed Data Block 3, Test 6")

if tsdb3.usedbits() != 5:
    print("Sanity Failure: Turbo Speed Data Block 3, Test 7")

if tsdb3.pause() != 700:
    print("Sanity Failure: Turbo Speed Data Block 3, Test 8")

if tsdb3.datalen() != 20:
    print("Sanity Failure: Turbo Speed Data Block 3, Test 9")

if tsdb4.encapsulate(binary2) is not None:
    print("Sanity Failure: Turbo Speed Data Block 4, Test 1")

if tsdb4.encapsulate(binary4) != 1:
    print("Sanity Failure: Turbo Speed Data Block 4, Test 2")

#########################
# PURE DATA BLOCK TESTS #
#########################
pdb1 = Blk_PDB()
pdb2 = Blk_PDB(4000, 5000, 255, 7000, binary)
pdb3 = Blk_PDB()
pdb3.bitpulse0(400)
pdb3.bitpulse1(500)
pdb3.usedbits(5)
pdb3.pause(700)
pdb3.encapsulate(binary2)
pdb4 = Blk_PDB()

if pdb1.bitpulse0() != 855:
    print("Sanity Failure: Pure Data Block 1, Test 1")

if pdb1.bitpulse1() != 1710:
    print("Sanity Failure: Pure Data Block 1, Test 2")

if pdb1.usedbits() != 8:
    print("Sanity Failure: Pure Data Block 1, Test 3")

if pdb1.pause() != 1000:
    print("Sanity Failure: Pure Data Block 1, Test 4")

if pdb1.datalen() != 0:
    print("Sanity Failure: Pure Data Block 1, Test 5")

if pdb2.bitpulse0() != 4000:
    print("Sanity Failure: Pure Data Block 2, Test 1")

if pdb2.bitpulse1() != 5000:
    print("Sanity Failure: Pure Data Block 2, Test 2")

if pdb2.usedbits() != 8:
    print("Sanity Failure: Pure Data Block 2, Test 3")

if pdb2.pause() != 7000:
    print("Sanity Failure: Pure Data Block 2, Test 4")

if pdb2.datalen() != 10:
    print("Sanity Failure: Pure Data Block 2, Test 5")

if pdb3.bitpulse0() != 400:
    print("Sanity Failure: Pure Data Block 3, Test 1")

if pdb3.bitpulse1() != 500:
    print("Sanity Failure: Pure Data Block 3, Test 2")

if pdb3.usedbits() != 5:
    print("Sanity Failure: Pure Data Block 3, Test 3")

if pdb3.pause() != 700:
    print("Sanity Failure: Pure Data Block 3, Test 4")

if pdb3.datalen() != 20:
    print("Sanity Failure: Pure Data Block 3, Test 5")

if pdb4.encapsulate(binary2) is not None:
    print("Sanity Failure: Pure Data Block 4, Test 1")

if pdb4.encapsulate(binary4) != 1:
    print("Sanity Failure: Pure Data Block 4, Test 2")

################################
# DIRECT RECORDING BLOCK TESTS #
################################
drb1 = Blk_DRB()
drb2 = Blk_DRB(4000, 5000, 7, binary)
drb3 = Blk_DRB()
drb3.tstatespersample(400)
drb3.pause(500)
drb3.usedbits(5)
drb3.encapsulate(binary4)

if drb1.tstatespersample() != 0:
    print("Sanity Failure: Direct Recording Block 1, Test 1")

if drb1.pause() != 1000:
    print("Sanity Failure: Direct Recording Block 1, Test 2")

if drb1.usedbits() != 8:
    print("Sanity Failure: Direct Recording Block 1, Test 3")

if drb1.datalen() != 0:
    print("Sanity Failure: Direct Recording Block 1, Test 4")

if drb2.tstatespersample() != 4000:
    print("Sanity Failure: Direct Recording Block 2, Test 1")

if drb2.pause() != 5000:
    print("Sanity Failure: Direct Recording Block 2, Test 2")

if drb2.usedbits() != 7:
    print("Sanity Failure: Direct Recording Block 2, Test 3")

if drb2.datalen() != 10:
    print("Sanity Failure: Direct Recording Block 2, Test 4")

if drb3.tstatespersample() != 400:
    print("Sanity Failure: Direct Recording Block 3, Test 1")

if drb3.pause() != 500:
    print("Sanity Failure: Direct Recording Block 3, Test 2")

if drb3.usedbits() != 5:
    print("Sanity Failure: Direct Recording Block 3, Test 3")

if drb3.datalen() != 0:
    print("Sanity Failure: Direct Recording Block 3, Test 4")

###########################
# GROUP START BLOCK TESTS #
###########################
gsb1 = Blk_GSB()
gsb2 = Blk_GSB("MyString")
gsb3 = Blk_GSB()
gsb3.groupname("Another String")

s = "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog" \
    "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog" \
    "The quick brown fox jumps over the lazy dog. THE TEXT SHOULD BE TRUNCATED AT... 255 BYTES."

gsb4 = Blk_GSB(s)

if gsb1.groupname() != "Empty Group Name":
    print("Sanity Failure: Group Start Block 1")

if gsb2.groupname() != "MyString":
    print("Sanity Failure: Group Start Block 2")

if gsb3.groupname() != "Another String":
    print("Sanity Failure: Group Start Block 3")

if (gsb4.groupname() != "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog"
                        "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog"
                        "The quick brown fox jumps over the lazy dog. THE TEXT SHOULD BE TRUNCATED AT..."):
    print("Sanity Failure: Group Start Block 4")

#############################
# HARDWARE TYPE BLOCK TESTS #
#############################
htb1 = Blk_HTB()
htb2 = Blk_HTB()
htb3 = Blk_HTB()
htb2.add_hardware(HTYPE_COMPUTER, 0, HINFO_RUNS)

for z in range(255):
    htb3.add_hardware(HTYPE_MODEM, 1, HINFO_RUNS_SFX)

if htb1.hardwarenum() != 0:
    print("Sanity Failure: Hardware Type Block 1")

if htb2.hardwarenum() != 1:
    print("Sanity Failure: Hardware Type Block 2")

if htb3.add_hardware(HTYPE_SOUND, 8, HINFO_NORUN) != 1:
    print("Sanity Failure: Hardware Type Block 3")

#######################
# MESSAGE BLOCK TESTS #
#######################
mb1 = Blk_MB()
mb2 = Blk_MB("MyString")
mb2.time(75)
mb3 = Blk_MB(t=100)
mb3.message("Another String")

s = "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog" \
    "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog" \
    "The quick brown fox jumps over the lazy dog. THE TEXT SHOULD BE TRUNCATED AT... 255 BYTES."

mb4 = Blk_MB(s, 20)

if mb1.message() != "Empty Message":
    print("Sanity Failure: Message Block 1, Test 1")

if mb1.time() != 0:
    print("Sanity Failure: Message Block 1, Test 2")

if mb2.message() != "MyString":
    print("Sanity Failure: Message Block 2, Test 1")

if mb2.time() != 75:
    print("Sanity Failure: Message Block 2, Test 2")

if mb3.message() != "Another String":
    print("Sanity Failure: Message Block 3, Test 1")

if mb3.time() != 100:
    print("Sanity Failure: Message Block 3, Test 2")

if (mb4.message() != "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog"
                     "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog"
                     "The quick brown fox jumps over the lazy dog. THE TEXT SHOULD BE TRUNCATED AT..."):
    print("Sanity Failure: Message Block 4, Test 1")

################################
# SET SIGNAL LEVEL BLOCK TESTS #
################################
sslb1 = Blk_SSLB()
sslb2 = Blk_SSLB(1)
sslb3 = Blk_SSLB()
sslb3.signal(1)

if sslb1.signal() != 0:
    print("Sanity Failure: Set Signal Level Block 1, Test 1")

if sslb2.signal() != 1:
    print("Sanity Failure: Set Signal Level Block 2, Test 1")

if sslb3.signal() != 1:
    print("Sanity Failure: Set Signal Level Block 3, Test 1")

#############################
# CALL SEQUENCE BLOCK TESTS #
#############################
csb1 = Blk_CSB()
csb2 = Blk_CSB()
csb3 = Blk_CSB()
csb4 = Blk_CSB()
csb2.add_call(100)
csb3.add_call(-1200)
csb3.add_call(300)

# Add 255 pulses to psb4
for q in range(255):
    csb4.add_call(400)

if csb1.callnum() != 0:
    print("Sanity Failure: Call Sequence Block 1")

if csb2.callnum() != 1:
    print("Sanity Failure: Call Sequence Block 2")

if csb3.callnum() != 2:
    print("Sanity Failure: Call Sequence Block 3")

if csb4.add_call(400) != 1:
    print("Sanity Failure: Call Sequence Block 4 on Error Check")

if csb4.callnum() != 255:
    print("Sanity Failure: Call Sequence Block 4")

####################################
# RETURN FROM SEQUENCE BLOCK TESTS #
####################################
rfsb1 = Blk_RFSB()
rfsb2 = Blk_RFSB()
rfsb3 = Blk_RFSB()

if rfsb1.id != TZXBLK_RFSB:
    print("Sanity Failure: Return From Sequence Block 1")

if rfsb2.id != TZXBLK_RFSB:
    print("Sanity Failure: Return From Sequence Block 2")

if rfsb3.id != TZXBLK_RFSB:
    print("Sanity Failure: Return From Sequence Block 3")

############################
# ARCHIVE INFO BLOCK TESTS #
############################
aib1 = Blk_AIB()
aib1.add_info(AINFO_TITLE, "My Game")
aib2 = Blk_AIB()
aib2.add_info(AINFO_TITLE, "My Game")
aib2.add_info(AINFO_PUBLISHER, "My Publisher")
aib2.add_info(AINFO_PUBYEAR, "1985")
aib2.add_info(AINFO_PRICE, "$10.99")
aib2.add_info(AINFO_COMMENT, "It's fun!")
aib3 = Blk_AIB()

# Add 255 entries to aib3
for q in range(255):
    aib3.add_info(AINFO_COMMENT, "Comment")

if aib1.infonum() != 1:
    print("Sanity Failure: Archive Info Block 1")

if aib2.infonum() != 5:
    print("Sanity Failure: Archive Info Block 2")

if aib3.add_info(AINFO_COMMENT, "Comment") != 1:
    print("Sanity Failure: Archive Info Block 3, Test 1")

if aib3.infonum() != 255:
    print("Sanity Failure: Archive Info Block 3, Test 2")

###########################
# CUSTOM INFO BLOCK TESTS #
###########################

cib1 = Blk_CIB("The CIB Identifier", "Any old data!!!")
cib2 = Blk_CIB()
cib3 = Blk_CIB()
cib3.setcid("Hello")
cib3.encapsulate("XXXXX")

if cib1.setcid() != "The CIB Id":
    print("Sanity Failure: Custom Info Block 1, Test 1")

if cib1.datalen() != 15:
    print("Sanity Failure: Custom Info Block 1, Test 2")

if cib2.setcid() != "No ID     ":
    print("Sanity Failure: Custom Info Block 2, Test 1")

if cib2.datalen() != 0:
    print("Sanity Failure: Custom Info Block 2, Test 2")

if cib3.setcid() != "Hello     ":
    print("Sanity Failure: Custom Info Block 3, Test 1")

if cib3.datalen() != 5:
    print("Sanity Failure: Custom Info Block 3, Test 2")

######################
# SELECT BLOCK TESTS #
######################
selb1 = Blk_SELB()
selb1.add_select(1, "Level 1")
selb2 = Blk_SELB()
selb2.add_select(1, "Stage 1")
selb2.add_select(3, "Stage 2")
selb3 = Blk_SELB()

# Add 255 entries to selb3
for q in range(255):
    selb3.add_select(q, "Comment")

if selb1.selectnum() != 1:
    print("Sanity Failure: Select Block 1")

if selb2.selectnum() != 2:
    print("Sanity Failure: Select Block 2")

if selb3.add_select(10, "Final Map") != 1:
    print("Sanity Failure: Select Block 3, Test 1")

if selb3.selectnum() != 255:
    print("Sanity Failure: Select Block 3, Test 2")

#############################
# CSW RECORDING BLOCK TESTS #
#############################
cswrb1 = Blk_CSWRB()
cswrb2 = Blk_CSWRB(100, 11000, CSW_ZRLE, 50, binary)
cswrb3 = Blk_CSWRB()
cswrb3.pause(10)
cswrb3.samplerate(96000)
cswrb3.compression(CSW_RLE)
cswrb3.storedpulses(500)
cswrb3.encapsulate(binary2)

if cswrb1.pause() != 1000:
    print("Sanity Failure: CSW Recording Block 1, Test 1")

if cswrb1.samplerate() != 22050:
    print("Sanity Failure: CSW Recording Block 1, Test 2")

if cswrb1.compression() != CSW_RLE:
    print("Sanity Failure: CSW Recording Block 1, Test 3")

if cswrb1.storedpulses() != 0:
    print("Sanity Failure: CSW Recording Block 1, Test 4")

if cswrb1.datalen() != 0:
    print("Sanity Failure: CSW Recording Block 1, Test 5")

if cswrb2.pause() != 100:
    print("Sanity Failure: CSW Recording Block 2, Test 1")

if cswrb2.samplerate() != 11000:
    print("Sanity Failure: CSW Recording Block 2, Test 2")

if cswrb2.compression() != CSW_ZRLE:
    print("Sanity Failure: CSW Recording Block 2, Test 3")

if cswrb2.storedpulses() != 50:
    print("Sanity Failure: CSW Recording Block 2, Test 4")

if cswrb2.datalen() != 10:
    print("Sanity Failure: CSW Recording Block 2, Test 5")

if cswrb3.pause() != 10:
    print("Sanity Failure: CSW Recording Block 3, Test 1")

if cswrb3.samplerate() != 96000:
    print("Sanity Failure: CSW Recording Block 3, Test 2")

if cswrb3.compression() != CSW_RLE:
    print("Sanity Failure: CSW Recording Block 3, Test 3")

if cswrb3.storedpulses() != 500:
    print("Sanity Failure: CSW Recording Block 3, Test 4")

if cswrb3.datalen() != 20:
    print("Sanity Failure: CSW Recording Block 3, Test 5")
