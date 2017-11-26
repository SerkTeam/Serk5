# -*- coding: utf-8 -*-
#SERK_TEAM

from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.LineThrift.ttypes import Message
from LineAlpha.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._qrLogin("line://au/q/")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

wait = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{},
    'ProtectQR':False,
  #  "Protectguest":False,
  #  "Protectcancel":False,
  #  "protectionOn":True,	
   }

setTime = {}
setTime = wait["setTime"]

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)
	
def NOTIFIED_ADD_CONTACT(op):
    try:
        sendMessage(op.param1, client.getContact(op.param1).displayName + " Thanks udah ngeadd ðŸ˜˜ ")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ADD_CONTACT\n\n")
        return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    #print op
    ginfo = client.getGroup(op.param1)
    try:
        sendMessage(op.param1,"Hi, " + client.getContact(op.param2).displayName + "\nSelamat Datang Di Grup :\n=> " + str(ginfo.name) + "\nOwner Grup Kami Adalah :\n=> " + str(ginfo.creator.displayName))
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return

tracer.addOpInterrupt(17,NOTIFIED_ACCEPT_GROUP_INVITATION)

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
	client.kickoutFromGroup(op.param1,[op.param2])
	sendMessage(op.param1, client.getContact(op.param3).displayName + " Eh Kasian anjir dia dikick ô€œô€…”Har Harô¿¿")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return

tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def NOTIFIED_LEAVE_GROUP(op):
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + " Dada! Jangan kangen ya ô€œô€…”Har Harô¿¿")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_LEAVE_GROUP\n\n")
        return

tracer.addOpInterrupt(15,NOTIFIED_LEAVE_GROUP)

def NOTIFIED_CANCEL_INVITATION_GROUP(op):
    try:
        client.kickoutFromGroup(op.param1,[op.param2])
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_CANCEL_INVITATION_GROUP\n\n")
        return

tracer.addOpInterrupt(32,NOTIFIED_CANCEL_INVITATION_GROUP)

def CANCEL_INVITATION_GROUP(op):
    try:
        client.cancelGroupInvitation(op.param1,[op.param3])
    except Exception as e:
        print e
        print ("\n\nCANCEL_INVITATION_GROUP\n\n")
        return

tracer.addOpInterrupt(31,CANCEL_INVITATION_GROUP)

def NOTIFIED_READ_MESSAGE(op):
    #print op
    try:
        if op.param1 in wait['readPoint']:
            Name = client.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "\nãƒ„1¤7" + Name
                wait['ROM'][op.param1][op.param2] = "ãƒ„1¤7" + Name
        else:
            pass
    except:
        pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
        else:
            pass
    except KeyboardInterrupt:
	       sys.exit(0)
    except Exception as error:
        print error
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            if msg.contentType == 0:
#-----------------------------------------------------------------------------------------------------------------------------------
                if msg.text == "mid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "me":
                    sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
		else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "gid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "ginfo":
                    group = client.getGroup(msg.to)
		    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "Error"
                    md = "[Nama Grup]:\n" + group.name + "\n\n[Id Grup]:\n" + group.id + "\n\n[Pembuat Grup]:\n" + gCreator + "\n\n[Gambar Grup]:\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nKode Url : Diizinkan"
                    else: md += "\n\nKode Url : Diblokir"
                    if group.invitee is None: md += "\nJumlah Member : " + str(len(group.members)) + " Orang" + "\nUndangan Yang Belum Diterima : 0 Orang"
                    else: md += "\nJumlah Member : " + str(len(group.members)) + " Orang" + "\nUndangan Yang Belum Diterima : " + str(len(group.invitee)) + " Orang"
                    sendMessage(msg.to,md)
		if "help" in msg.text:
	       	    sendMessage(msg.to,"\n              LÍ©Í¨Í›Í¬Ì‡ÌŽÌ£Ì©Ì¼ÌÌºÌ˜Í–IÌ€Í‚Ì‰Ì¢Í•ÌªÌ®Ì¤Ì»Ì Ì¬NÌŒÍŠÍÌ¿Í§ÌµÌªÌ™EÍ¤Í¬Í¥Í¨Ì‘Ì„Í®Ì¸Ì–Ì¯Ì—Ì¥ÍÌ³Ì»Ì³ ÍƒÌÍ£Í£Í®Ò‰ÌÍ‡Í“Ì±Í™DÌ¿Ì‰Ì”Í„Í¥Í¨ÍŸÌ¼ÌªEÌˆÌ„ÌŠÌŒÌŽÌ€Ì‹ÍŸÌ¡Ì°Ì«Ì®Í”Í“Ì«VÌ‰ÍƒÌšÍ‹Í¨Í¢ÍžÍšÌ¬Í•ÌÌ£ÍÍ‡Ì²Í–EÍªÌÌ¿Ì‡ÌƒÍ‹Ì‚Í—Í“LÌŽÌ„Ì¾ÍÍ ÍšÌ¦ÌOÌ’Í‚ÌŒÌ¾Í’Í’Ì‡Í€ÌµÍŽÌ¹Ì»Ì˜PÍ¤Í’Í®Ì¿ÌŒÌ•Ì·Í–Ì¬Í…Ì²Í•Ì–ÍEÌ’ÌÌ†Í’Ì“Ì‹Í£ÍˆÌ–Í‰Í–Ì»Í…RÌ”Í¤Í‚Í§Ì‡Ì·ÍŸÌ­ÍšÌ¯SÍ©ÌŒÌŒÌ¾Ì€Ì”Í’Í‘ÌµÌºÌžÍ“Ì¥Ì–ÍÍˆ Ì€Ì†ÍŒÌ¢Ì·Ì§Ì¥ÍŽÌ¯BÌŽÌÍ¯Ì€Ì“Ì‰Í’ÍÍ„Ì›ÍœÌ¶ÍŽÌ¹Ì¯OÌ„Í—Í„Í‹Í¯Í­Í Ò‰ÍÍˆÌ˜Í”Ì™Ì±Ì¯Ì¥Ì¯Í‰TÌƒÍ‹Í§Ì‚ÌŒÌ†Í«Í’Ì’Í Í•Ì¹Ì²Ì±Ì±Ì ÌœSÍ¨Ì“Ì¾Ì‚Í–\n\n-----------------------------------------------------------------\nã€ŒHelp Command [Base Command] :ã€\n=> [seÅ£]\n=> [siÄer]\n=> [Êe]\n=> [Êid]\n=> [Ç¥id]\n=> [Ç¥info]\n=> [Å£ime]\n=> [Ã¾uka]\n=> [Å£utup]\n=> [Âµrl]\n=> [Ç¥ift]\n=> [È¼ancel]\n=> [É¨nvite:ã€ŒBy Midã€]\n=> [È¿how:ã€ŒBy Midã€\n\nã€ŒHelp Command  [Clone/MyBF Command] :ã€\n=> [É¨nvÎ±llÈ¼lone]\n=> [ÐºickÎ±llÈ¼lone]\n=> [È¼ancelÎ±llÈ¼lone]\n=> [É¨nvÎ±llÐ¼ybf]\n=> [ÐºickÎ±llÐ¼ybf]\n=> [È¼ancelÎ±llÐ¼ybf]\n=> [É¨nvÈ¼lone:ã€ŒNo.1-8ã€]\n=> [ÐºickÈ¼lone:ã€ŒNo.1-8ã€]\n=> [È¼ancelÈ¼lone:ã€ŒNo.1-8ã€]\n=> [É¨nvÐ¼ybf:ã€ŒNo.1-8ã€]\n=> [ÐºickÐ¼ybf:ã€ŒNo.1-8ã€]\n=> [È¼ancelÐ¼ybf:ã€ŒNo.1-8ã€]\n=> [â„“istÈ¼lone]\n=> [â„“istÐ¼ybf]\n\nã€ŒHelp Command [Mod Command] :ã€\n=> [Ç¥random:ã€ŒNomorã€]\n=> [Î¼p]\n=> [È¿peed]\n=> [Å£agall]\n=> [Äžn ã€ŒNamaã€]\n=> [Ç¥roupÈ¼reate]\n=> [É¨nvÇ¥È¼reator]\n=> [Ñename:ã€ŒGanti Nama Profilã€]\n=> [Ð²ÏƒÑ‚Ð¼Î±ÐºÑ”Ñ]\n\nã€ŒHelp Command  [Use For Kicker Only] :ã€\n=> [Ðº:ã€ŒBy Nameã€]\n=> [Ð¸Ðºã€ŒBy Tagã€]\n=> [Ð¼ulai]\n=> [Âµni]\n=> [Ð²yeã€ŒBy Tagã€]\n\nã€ŒInfo Bots :ã€\n=> Based on : Vodka\n=> Support By : Line Developers\n=> Modding By : Eqi16\n=> Version Mod : 2.2.1beta\n-----------------------------------------------------------------\n\n              LÍ©Í¨Í›Í¬Ì‡ÌŽÌ£Ì©Ì¼ÌÌºÌ˜Í–IÌ€Í‚Ì‰Ì¢Í•ÌªÌ®Ì¤Ì»Ì Ì¬NÌŒÍŠÍÌ¿Í§ÌµÌªÌ™EÍ¤Í¬Í¥Í¨Ì‘Ì„Í®Ì¸Ì–Ì¯Ì—Ì¥ÍÌ³Ì»Ì³ ÍƒÌÍ£Í£Í®Ò‰ÌÍ‡Í“Ì±Í™DÌ¿Ì‰Ì”Í„Í¥Í¨ÍŸÌ¼ÌªEÌˆÌ„ÌŠÌŒÌŽÌ€Ì‹ÍŸÌ¡Ì°Ì«Ì®Í”Í“Ì«VÌ‰ÍƒÌšÍ‹Í¨Í¢ÍžÍšÌ¬Í•ÌÌ£ÍÍ‡Ì²Í–EÍªÌÌ¿Ì‡ÌƒÍ‹Ì‚Í—Í“LÌŽÌ„Ì¾ÍÍ ÍšÌ¦ÌOÌ’Í‚ÌŒÌ¾Í’Í’Ì‡Í€ÌµÍŽÌ¹Ì»Ì˜PÍ¤Í’Í®Ì¿ÌŒÌ•Ì·Í–Ì¬Í…Ì²Í•Ì–ÍEÌ’ÌÌ†Í’Ì“Ì‹Í£ÍˆÌ–Í‰Í–Ì»Í…RÌ”Í¤Í‚Í§Ì‡Ì·ÍŸÌ­ÍšÌ¯SÍ©ÌŒÌŒÌ¾Ì€Ì”Í’Í‘ÌµÌºÌžÍ“Ì¥Ì–ÍÍˆ Ì€Ì†ÍŒÌ¢Ì·Ì§Ì¥ÍŽÌ¯BÌŽÌÍ¯Ì€Ì“Ì‰Í’ÍÍ„Ì›ÍœÌ¶ÍŽÌ¹Ì¯OÌ„Í—Í„Í‹Í¯Í­Í Ò‰ÍÍˆÌ˜Í”Ì™Ì±Ì¯Ì¥Ì¯Í‰TÌƒÍ‹Í§Ì‚ÌŒÌ†Í«Í’Ì’Í Í•Ì¹Ì²Ì±Ì±Ì ÌœSÍ¨Ì“Ì¾Ì‚Í–\n")
		if "Gn " in msg.text:
		    if msg.toType == 2:
			X = client.getGroup(msg.to)
			X.name = msg.text.replace("Gn ","")
			client.updateGroup(X)
			sendMessage(msg.to,"Udah diganti tuh nama grupnya ô€œô€…”Har Harô¿¿")
		    else:
			client.sendMessage(msg.to,"Gabisa digunain digrup ô€œô€…”Har Harô¿¿")
		if "groupcreate" in msg.text:
		    group = client.getGroup(msg.to)
		    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "Error"
		    sendMessage(msg.to,"Pembuat Grup :\n" + group.name + "\n=> " + gCreator)
                if msg.text == "url":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
		if msg.text == "uni":
		    sendMessage(msg.to,"Hai Perkenalkan.....\nNama saya Eqi saha ya?\n\n1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1\n\nMakasih Sudah Dilihat :)\nJangan Dikick ampun mzz :v")
		if msg.text == "up":
		    sendMessage(msg.to,"eh")
		    sendMessage(msg.to,"eh")
		    sendMessage(msg.to,"eh")
                    sendMessage(msg.to,"eh")
		    sendMessage(msg.to,"eh")
		    sendMessage(msg.to,"eh")
    		    sendMessage(msg.to,"eh")
		    sendMessage(msg.to,"eh")
		    sendMessage(msg.to,"eh")
     		    sendMessage(msg.to,"eh")
		    sendMessage(msg.to,"eh")
		    sendMessage(msg.to,"eh")
		    sendMessage(msg.to,"eh")
		    sendMessage(msg.to,"eh")
		    sendMessage(msg.to,"eh")
    		    sendMessage(msg.to,"eh")
		    sendMessage(msg.to,"eh udah eh spamnya nanti dimarahin ô€œô€…”Har Harô¿¿")
		if msg.text == "buka":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "Sudah dibuka mzque :v")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL dibuka")
                        sendMessage(msg.to,"Link Grup : ")
                        sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                if msg.text == "tutup":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "Sudah ditutup mzque :v")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL ditutup")
                if "kick:" in msg.text:
                    key = msg.text[5:]
                    client.kickoutFromGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+" maapin say ô€œô€…”Har Harô¿¿")
                if "invallclone" in msg.text:
                    print "\n[invite all clone]ok\n"
                    mid1 = ("u6db82b481cff8971ede277f8a5c0b6fb")
                    mid2 = ("u324905ea88407b94a371ddc65d877b8b")
                    mid3 = ("ua2bd76c8b8f57dd524b0d220eb5116e6")
                    mid4 = ("uac1e69cc7b8c53baa9059ff96f46a320")
                    mid5 = ("uf57a34c5ad1bc3e2dafe5e6505c357a5")
                    mid6 = ("ud9169423f358a268e653bd86f5c20313")
                    mid7 = ("ub4d9374d6cc45d1171f60ac4e8d0ba0b")
                    mid8 = ("uaf068b846114a324f7184e7f13aec5d5")
                    try:
                        client.findAndAddContactsByMid(mid1)
                        client.inviteIntoGroup(msg.to,[mid1])
                        client.findAndAddContactsByMid(mid2)
                        client.inviteIntoGroup(msg.to,[mid2])
                        client.findAndAddContactsByMid(mid3)
                        client.inviteIntoGroup(msg.to,[mid3])
                        client.findAndAddContactsByMid(mid4)
                        client.inviteIntoGroup(msg.to,[mid4])
                        client.findAndAddContactsByMid(mid5)
                        client.inviteIntoGroup(msg.to,[mid5])
                        client.findAndAddContactsByMid(mid6)
                        client.inviteIntoGroup(msg.to,[mid6])
                        client.findAndAddContactsByMid(mid7)
                        client.inviteIntoGroup(msg.to,[mid7])
                        client.findAndAddContactsByMid(mid8)
                        client.inviteIntoGroup(msg.to,[mid8])
                        client.sendMessage(msg.to,"Success Invite All Clone")
                    except:
                        pass
                if "kickallclone" in msg.text:
                    group = client.getGroup(msg.to)
                    print "\n[kick all clone]ok\n"
                    mid1 = ("u6db82b481cff8971ede277f8a5c0b6fb")
                    mid2 = ("u324905ea88407b94a371ddc65d877b8b")
                    mid3 = ("ua2bd76c8b8f57dd524b0d220eb5116e6")
                    mid4 = ("uac1e69cc7b8c53baa9059ff96f46a320")
                    mid5 = ("uf57a34c5ad1bc3e2dafe5e6505c357a5")
                    mid6 = ("ud9169423f358a268e653bd86f5c20313")
                    mid7 = ("ub4d9374d6cc45d1171f60ac4e8d0ba0b")
                    mid8 = ("uaf068b846114a324f7184e7f13aec5d5")
                    try:
                        client.kickoutFromGroup(msg.to,[mid1])
                        client.kickoutFromGroup(msg.to,[mid2])
                        client.kickoutFromGroup(msg.to,[mid3])
                        client.kickoutFromGroup(msg.to,[mid4])
                        client.kickoutFromGroup(msg.to,[mid5])
                        client.kickoutFromGroup(msg.to,[mid6])
                        client.kickoutFromGroup(msg.to,[mid7])
                        client.kickoutFromGroup(msg.to,[mid8])
                        client.sendMessage(msg.to,"Success Kick All Clone")
                    except:
                        pass
		if "cancelallclone" in msg.text:
                    group = client.getGroup(msg.to)
                    print "\n[cancel invite all clone]ok\n"
                    mid1 = ("u6db82b481cff8971ede277f8a5c0b6fb")
                    mid2 = ("u324905ea88407b94a371ddc65d877b8b")
                    mid3 = ("ua2bd76c8b8f57dd524b0d220eb5116e6")
                    mid4 = ("uac1e69cc7b8c53baa9059ff96f46a320")
                    mid5 = ("uf57a34c5ad1bc3e2dafe5e6505c357a5")
                    mid6 = ("ud9169423f358a268e653bd86f5c20313")
                    mid7 = ("ub4d9374d6cc45d1171f60ac4e8d0ba0b")
                    mid8 = ("uaf068b846114a324f7184e7f13aec5d5")
                    try:
                        client.cancelGroupInvitation(msg.to,[mid1])
                        client.cancelGroupInvitation(msg.to,[mid2])
                        client.cancelGroupInvitation(msg.to,[mid3])
                        client.cancelGroupInvitation(msg.to,[mid4])
                        client.cancelGroupInvitation(msg.to,[mid5])
                        client.cancelGroupInvitation(msg.to,[mid6])
                        client.cancelGroupInvitation(msg.to,[mid7])
                        client.cancelGroupInvitation(msg.to,[mid8])
                        client.sendMessage(msg.to,"Success Cancel Invitation All Clone")
                    except:
                        pass
		if "invallmybf" in msg.text:
		    print "\n[invite all my best friends]ok\n"
		    mid1 = ("ubd3b0f3cecc30ca33bf939dab7e6848a")
		    mid2 = ("u75a663be511eaef40ce5829de072c5ce")
		    mid3 = ("u22d94aac4e1659eb6f375ffc7cb17a53")
		    try:
                        client.findAndAddContactsByMid(mid1)
                        client.inviteIntoGroup(msg.to,[mid1])
                        client.findAndAddContactsByMid(mid2)
                        client.inviteIntoGroup(msg.to,[mid2])
                        client.findAndAddContactsByMid(mid3)
			client.inviteIntoGroup(msg.to,[mid3])
                    except:
			pass
		if "kickallmybf" in msg.text:
		    group = client.getGroup(msg.to)
		    print "\n[kick all my best friends]ok\n"
		    mid1 = ("ubd3b0f3cecc30ca33bf939dab7e6848a")
		    mid2 = ("u75a663be511eaef40ce5829de072c5ce")
		    mid3 = ("u22d94aac4e1659eb6f375ffc7cb17a53")
		    try:
                        client.kickoutFromGroup(msg.to,[mid1])
                        client.kickoutFromGroup(msg.to,[mid2])
                        client.kickoutFromGroup(msg.to,[mid3])
                    except:
			pass
		if "cancelallmybf" in msg.text:
		    group = client.getGroup(msg.to)
		    print "\n[cancel invitation to all my best friends]ok\n"
		    mid1 = ("ubd3b0f3cecc30ca33bf939dab7e6848a")
		    mid2 = ("u75a663be511eaef40ce5829de072c5ce")
		    mid3 = ("u22d94aac4e1659eb6f375ffc7cb17a53")
		    try:
                        client.cancelGroupInvitation(msg.to,[mid1])
                        client.cancelGroupInvitation(msg.to,[mid2])
                        client.cancelGroupInvitation(msg.to,[mid3])
                    except:
			pass
                if "nk" in msg.text:
                    bamz0 = msg.text.replace("nk ","")
                    bamz1 = bamz0.lstrip()
                    bamz2 = bamz1.replace("@","")
                    bamz3 = bamz2.rstrip()
                    _linedev = bamz3
                    group = client.getGroup(msg.to)
                    Names = [contact.displayName for contact in group.members]
                    Mids = [contact.mid for contact in group.members]
                    if _linedev in Names:
                        kazu = Names.index(_linedev)
                        sendMessage(msg.to, "Dada! Jan kangen njir :v")
                        client.kickoutFromGroup(msg.to, [""+Mids[kazu]+""])
                        contact = client.getContact(Mids[kazu])
                        sendMessage(msg.to, ""+contact.displayName+" maapin say ô€œô€…”Har Harô¿¿")
                    else:
                        sendMessage(msg.to,"salah goblog ô€œô€…”Har Harô¿¿")
		if "k:" in msg.text:
                    key = msg.text[3:]
                    group = client.getGroup(msg.to)
                    Names = [contact.displayName for contact in group.members]
                    Mids = [contact.mid for contact in group.members]
                    if key in Names:
                        kazu = Names.index(key)
                        sendMessage(msg.to, "Dada! Jan kangen njir :v")
                        client.kickoutFromGroup(msg.to, [""+Mids[kazu]+""])
                        contact = client.getContact(Mids[kazu])
                        sendMessage(msg.to, ""+contact.displayName+" maapin say ô€œô€…”Har Harô¿¿")
                    else:
                        sendMessage(msg.to, "salah goblog ô€œô€…”Har Harô¿¿")
		if "Bye " in msg.text:
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    targets = []
                    for x in key["MENTIONEES"]:
                         targets.append(x["M"])
                    for target in targets:
                         try:
                            client.kickoutFromGroup(msg.to,[target])
                         except:
                            pass
		if "grandom:" in msg.text:
		    if msg.toType == 2:
		        strnum = msg.text.replace("grandom:","")
			source_str = 'abcdefghijklmnopqrstuvwxyz1234567890@:;./_][!&%$#)(=~^|'
			try:
			    num = int(strnum)
			    group = client.getGroup(msg.to)
			    for var in range(0,num):
				name = "".join([random.choice(source_str) for x in xrange(10)])
				time.sleep(0.01)
				group.name = name
				client.updateGroup(group)
			except:
			    client.sendMessage(msg.to,"Error bang, coba ulang bang oke ô€œô€…”double thumbs upô¿¿ô€œô€…”Har Harô¿¿")
		if "gid" in msg.text:
		    group = client.getGroup(msg.to)
		    sendMessage(msg.to, group.id)
		if "stealgroupimage" in msg.text:
		    group = client.getGroup(msg.to)
		    sendMessage(msg.to,"http://dl.profile.line-cdn.net/" + group.pictureStatus)
		if msg.text == "cancel":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "Kagak ada yang diinv anjir ô€œô€…”Har Harô¿¿ apaan yang mau dicancel coba ô€œô€…”Har Harô¿¿")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + " Orang Yang udah dicancel Bos")	
		if "invgcreator" in msg.text:
                    if msg.toType == 2:
                         ginfo = client.getGroup(msg.to)
                         gCreator = ginfo.creator.mid
                         try:
                             client.findAndAddContactsByMid(gCreator)
                             client.inviteIntoGroup(msg.to,[gCreator])
			     print "\nSuccess Invite gCreator"
                         except:
                             pass
		if "botmaker" in msg.text:
		    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': "u06d2f30d0ca957ad0bf143960cb82996"}
                    client.sendMessage(M)
		if "invclone:1" in msg.text:
		    mid = ("u6db82b481cff8971ede277f8a5c0b6fb")
		    try:
			client.findAndAddContactsByMid(mid)
                        client.inviteIntoGroup(msg.to,[mid])
                    except:
			pass
		if "invclone:2" in msg.text:
		    mid = ("u324905ea88407b94a371ddc65d877b8b")
		    try:
			client.findAndAddContactsByMid(mid)
                        client.inviteIntoGroup(msg.to,[mid])
                    except:
			pass
		if "invclone:3" in msg.text:
		    mid = ("ua2bd76c8b8f57dd524b0d220eb5116e6")
		    try:
			client.findAndAddContactsByMid(mid)
                        client.inviteIntoGroup(msg.to,[mid])
                    except:
			pass
		if "invclone:4" in msg.text:
		    mid = ("uac1e69cc7b8c53baa9059ff96f46a320")
		    try:
			client.findAndAddContactsByMid(mid)
                        client.inviteIntoGroup(msg.to,[mid])
                    except:
			pass
		if "invclone:5" in msg.text:
		    mid = ("uf57a34c5ad1bc3e2dafe5e6505c357a5")
		    try:
			client.findAndAddContactsByMid(mid)
                        client.inviteIntoGroup(msg.to,[mid])
                    except:
			pass
		if "invclone:6" in msg.text:
		    mid = ("ud9169423f358a268e653bd86f5c20313")
		    try:
			client.findAndAddContactsByMid(mid)
                        client.inviteIntoGroup(msg.to,[mid])
                    except:
			pass
		if "invclone:7" in msg.text:
		    mid = ("ub4d9374d6cc45d1171f60ac4e8d0ba0b")
		    try:
			client.findAndAddContactsByMid(mid)
                        client.inviteIntoGroup(msg.to,[mid])
                    except:
			pass
		if "invclone:8" in msg.text:
		    mid = ("uaf068b846114a324f7184e7f13aec5d5")
		    try:
			client.findAndAddContactsByMid(mid)
                        client.inviteIntoGroup(msg.to,[mid])
                    except:
			pass
		if "kickclone:1" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("u6db82b481cff8971ede277f8a5c0b6fb")
		    try:
			client.kickoutFromGroup(msg.to,[mid])
                    except:
			pass
		if "kickclone:2" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("u324905ea88407b94a371ddc65d877b8b")
		    try:
			client.kickoutFromGroup(msg.to,[mid])
                    except:
			pass
		if "kickclone:3" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("ua2bd76c8b8f57dd524b0d220eb5116e6")
		    try:
			client.kickoutFromGroup(msg.to,[mid])
                    except:
			pass
		if "kickclone:4" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("uac1e69cc7b8c53baa9059ff96f46a320")
		    try:
			client.kickoutFromGroup(msg.to,[mid])
                    except:
			pass
		if "kickclone:5" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("uf57a34c5ad1bc3e2dafe5e6505c357a5")
		    try:
			client.kickoutFromGroup(msg.to,[mid])
                    except:
			pass
		if "kickclone:6" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("ud9169423f358a268e653bd86f5c20313")
		    try:
			client.kickoutFromGroup(msg.to,[mid])
                    except:
			pass
		if "kickclone:7" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("ub4d9374d6cc45d1171f60ac4e8d0ba0b")
		    try:
			client.kickoutFromGroup(msg.to,[mid])
                    except:
			pass
		if "kickclone:8" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("uaf068b846114a324f7184e7f13aec5d5")
		    try:
			client.kickoutFromGroup(msg.to,[mid])
                    except:
			pass
		if "cancelclone:1" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("u6db82b481cff8971ede277f8a5c0b6fb")
		    try:
			client.cancelGroupInvitation(msg.to,[mid])
                    except:
			pass
		if "cancelclone:2" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("u324905ea88407b94a371ddc65d877b8b")
		    try:
			client.cancelGroupInvitation(msg.to,[mid])
                    except:
			pass
		if "cancelclone:3" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("ua2bd76c8b8f57dd524b0d220eb5116e6")
		    try:
			client.cancelGroupInvitation(msg.to,[mid])
                    except:
			pass
		if "cancelclone:4" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("uac1e69cc7b8c53baa9059ff96f46a320")
		    try:
			client.cancelGroupInvitation(msg.to,[mid])
                    except:
			pass
		if "cancelclone:5" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("uf57a34c5ad1bc3e2dafe5e6505c357a5")
		    try:
			client.cancelGroupInvitation(msg.to,[mid])
                    except:
			pass
		if "cancelclone:6" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("ud9169423f358a268e653bd86f5c20313")
		    try:
			client.cancelGroupInvitation(msg.to,[mid])
                    except:
			pass
		if "cancelclone:7" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("ub4d9374d6cc45d1171f60ac4e8d0ba0b")
		    try:
			client.cancelGroupInvitation(msg.to,[mid])
                    except:
			pass
		if "cancelclone:8" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("uaf068b846114a324f7184e7f13aec5d5")
		    try:
			client.cancelGroupInvitation(msg.to,[mid])
                    except:
			pass
		if "invmybf:1" in msg.text:
		    mid = ("ubd3b0f3cecc30ca33bf939dab7e6848a")
		    try:
			client.findAndAddContactsByMid(mid)
                        client.inviteIntoGroup(msg.to,[mid])
                    except:
			pass
		if "invmybf:2" in msg.text:
		    mid = ("u75a663be511eaef40ce5829de072c5ce")
		    try:
			client.findAndAddContactsByMid(mid)
                        client.inviteIntoGroup(msg.to,[mid])
                    except:
			pass
		if "invmybf:3" in msg.text:
		    mid = ("u22d94aac4e1659eb6f375ffc7cb17a53")
		    try:
			client.findAndAddContactsByMid(mid)
                        client.inviteIntoGroup(msg.to,[mid])
                    except:
			pass
		if "kickmybf:1" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("ubd3b0f3cecc30ca33bf939dab7e6848a")
		    try:
			client.kickoutFromGroup(msg.to,[mid])
                    except:
			pass
		if "kickmybf:2" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("u75a663be511eaef40ce5829de072c5ce")
		    try:
			client.kickoutFromGroup(msg.to,[mid])
              except:
			pass
		if "kickmybf:3" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("u22d94aac4e1659eb6f375ffc7cb17a53")
		    try:
			client.kickoutFromGroup(msg.to,[mid])
                    except:
			pass
		if "cancelmybf:1" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("ubd3b0f3cecc30ca33bf939dab7e6848a")
		    try:
			client.cancelGroupInvitation(msg.to,[mid])
                    except:
			pass
		if "cancelmybf:2" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("u75a663be511eaef40ce5829de072c5ce")
		    try:
			client.cancelGroupInvitation(msg.to,[mid])
                    except:
			pass
		if "cancelmybf:3" in msg.text:
		    group = client.getGroup(msg.to)
		    mid = ("u22d94aac4e1659eb6f375ffc7cb17a53")
		    try:
			client.cancelGroupInvitation(msg.to,[mid])
                    except:
			pass
		if "Spam " in msg.text:
                    txt = msg.text.split(" ")
                    jmlh = int(txt[2])
                    teks = msg.text.replace("Spam ") + str(txt[1]) + " " + str(jmlh + " ","")
                    tulisan = jmlh * (teks+"\n")
                    if txt[1] == "on":
                        if jmlh <= 300:
                           for x in range(jmlh):
                               client.sendMessage(msg.to, teks)
                        else:
                           client.sendMessage(msg.to, "Kelebihan batas:v")
                    if txt[1] == "off":
                        if jmlh <= 300:
                            client.sendMessage(msg.to, tulisan)
                        else:
                            client.sendMessage(msg.to, "Kelebihan batas :v")
		if "rename:" in msg.text:
                    string = msg.text.replace("rename:","")
                    if len(string.decode('utf-8')) <= 1000000000:
                        profile_B = client.getProfile()
                        profile_B.displayName = string
                        client.updateProfile(profile_B)
                        client.sendMessage(msg.to,"name " + string + " done")
			sendMessage(msg.to,"Udah diganti namanya, coba cek ô€œô€…”Har Harô¿¿")
		if "InviteMeTo: " in msg.text:
                    gid = msg.text.replace("InviteMeTo: ","")
                    if gid == "":
                        client.sendMessage(msg.to,"Invalid group id")
                    else:
                        try:
                            client.findAndAddContactsByMid(msg.from_)
                            client.inviteIntoGroup(gid,[msg.from_])
                        except:
                            client.sendMessage(msg.to,"Mungkin saya tidak di dalam grup itu")
		if "Mid @" in msg.text:
                    _name = msg.text.replace("Mid @","")
                    _nametarget = _name.rstrip(' ')
                    gs = cl.getGroup(msg.to)
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            client.sendMessage(msg.to, g.mid)
                        else:
                            pass
		if "listclone" in msg.text:
		    mid1 = ("u6db82b481cff8971ede277f8a5c0b6fb")
                    mid2 = ("u324905ea88407b94a371ddc65d877b8b")
                    mid3 = ("ua2bd76c8b8f57dd524b0d220eb5116e6")
                    mid4 = ("uac1e69cc7b8c53baa9059ff96f46a320")
                    mid5 = ("uf57a34c5ad1bc3e2dafe5e6505c357a5")
                    mid6 = ("ud9169423f358a268e653bd86f5c20313")
                    mid7 = ("ub4d9374d6cc45d1171f60ac4e8d0ba0b")
                    mid8 = ("uaf068b846114a324f7184e7f13aec5d5")
                    contact = client.getContact(mid1)
		    contact1 = client.getContact(mid2)
		    contact2 = client.getContact(mid3)
		    contact3 = client.getContact(mid4)
		    contact4 = client.getContact(mid5)
		    contact5 = client.getContact(mid6)
		    contact6 = client.getContact(mid7)
		    contact7 = client.getContact(mid8)
		    sendMessage(msg.to,"[List Clone]:\n=> 1." + contact.displayName + "\n=> 2." + contact1.displayName + "\n=> 3." + contact2.displayName + "\n=> 4." + contact3.displayName + "\n=> 5." + contact4.displayName + "\n=> 6." + contact5.displayName + "\n=> 7." + contact6.displayName + "\n=> 8." + contact7.displayName + "\n\nStatus Clone : Aktif\nStatus diambil pada :\nTanggal : " + datetime.datetime.today().strftime('%d-%m-%y') + "\nWaktu : " + datetime.datetime.today().strftime('%H:%M:%S'))
		if "listmybf" in msg.text:
		    mid1 = ("ubd3b0f3cecc30ca33bf939dab7e6848a")
		    mid2 = ("u75a663be511eaef40ce5829de072c5ce")
		    mid3 = ("u22d94aac4e1659eb6f375ffc7cb17a53")
		    contact = client.getContact(mid1)
		    contact1 = client.getContact(mid2)
		    contact2 = client.getContact(mid3)
		    sendMessage(msg.to,"[List My Best Friends]:\n=> 1." + contact.displayName + "\n=> 2." + contact1.displayName + "\n=> 3." + contact2.displayName + "\n\nCek List dilihat pada :\nTanggal : " + datetime.datetime.today().strftime('%d-%m-%y') + "\nWaktu : " + datetime.datetime.today().strftime('%H:%M:%S'))
                if msg.text == "Mulai":
                    print "Cleaning Member....."
                    _name = msg.text.replace("Mulai","")
                    gs = client.getGroup(msg.to)
                    sendMessage(msg.to,"Hi, B-I-T-C-H")
		    sendMessage(msg.to,"Just fucking cleaning member")
		    sendMessage(msg.to,"1.......2.....3 ready")
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        sendMessage(msg.to,"error")
                    else:
                        for target in targets:
                            try:
                                klist=[client]
                                kicker=random.choice(klist)
                                kicker.kickoutFromGroup(msg.to,[target])
                                print (msg.to,[g.mid])
                            except:
                                sendMessage(msg.to,"Grup sudah Dibersihkan Bos")
		if msg.text == "speed":
                    start = time.time()
                    sendMessage(msg.to, "Menunggu jaringan...")
                    elapsed_time = time.time() - start
                    sendMessage(msg.to, "%s Time" % (elapsed_time))
	        if "invite:" in msg.text:
                    key = msg.text[-33:]
                    client.findAndAddContactsByMid(key)
                    client.inviteIntoGroup(msg.to, [key])
                    contact = client.getContact(key)
                if msg.text == "me":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if "show:" in msg.text:
                    key = msg.text[-33:]
                    sendMessage(msg.to, text=None, contentMetadata={'mid': key}, contentType=13)
                    contact = client.getContact(key)
                    sendMessage(msg.to, "Kontaknya si "+contact.displayName+"")
                if msg.text == "tagall":
		    group = client.getGroup(msg.to)
		    nama = [contact.mid for contact in group.members]
		    cb = ""
		    cb2 = ""
		    strt = int(0)
		    akh = int(0)
		    for md in nama:
			akh = akh + int(5)	
			cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""
			strt = strt + int(6)
			akh = akh + 1
			cb2 += "@nrik\n"
		   
		    cb = (cb[:int(len(cb)-1)])
		    msg.contentType = 0
		    msg.text = cb2
		    msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
		    try:
		        client.sendMessage(msg)
		    except Exception as error:
			    print error	
                if msg.text == "time":
                    sendMessage(msg.to, "Tanggal sekarang = " + datetime.datetime.today().strftime('%d-%m-%y'))
		            sendMessage(msg.to, "Waktu sekarang = " + datetime.datetime.today().strftime('%H:%M:%S'))
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                if msg.text == "set":
                    sendMessage(msg.to, "Dasar sider anjing \nKetik ã€Œsiderã€„1¤7 gua bakal ngasih tau siapa sidernya")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%d-%m-%y %H:%M:%S')
                    wait['ROM'][msg.to] = {}
                    print wait
                if msg.text == "sider":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print rom
                                chiya += rom[1] + "\n"

                        sendMessage(msg.to, "Nih sider anjing %s\nNah.....\n\nYang sider doang kerjaannya\n%sGileee benerrr..\n\nSider dilihat pada tanggal dan waktu:\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "Belom di set dodol ô€œô€…”Har Harô¿¿\nKetik ã€Œsetã€„1¤7 buat lihat siapa sider anjing :v")
                else:
                    pass
        else:
            pass

#-----------------------------------------------------------------------------------------------------------------------------------
    except Exception as e:
        print e
        print ("\n\nSEND_MESSAGE\n\n")
        return

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
