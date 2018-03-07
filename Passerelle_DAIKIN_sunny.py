# System import ...
import os
import datetime
import sys

class GAMoulinette:

    def run(self):
        try:
            fileName = "daikin_sunny.xml"
            #l'address 0 représente 1-00  et  20 represente 2-00  et 40 represente 3-00 ( groupes Daikin sont décalé de 20 )
            #dans config.exe, taper 99 pour avoir 0 dans l xml
            passerelle_daikin1 = [
                { "type":"nrj" , "address": 0  ,   "label":"1.00" },
                { "type":"nrj" , "address": 1  ,   "label":"1.01" },
                { "type":"nrj" , "address": 2  ,   "label":"1.02" },
                { "type":"nrj" , "address": 3  ,   "label":"1.03" },
                { "type":"nrj" , "address": 4  ,   "label":"1.04" },
                { "type":"nrj" , "address": 5  ,   "label":"1.05" },
                { "type":"nrj" , "address": 6  ,   "label":"1.06" },
                { "type":"nrj" , "address": 7  ,   "label":"" },
                { "type":"nrj" , "address": 8  ,   "label":"" },
                { "type":"nrj" , "address": 9  ,   "label":"" },
                { "type":"nrj" , "address": 10 ,   "label":"" },
                { "type":"nrj" , "address": 11 ,   "label":"" },
                { "type":"nrj" , "address": 12 ,   "label":"" },
                { "type":"nrj" , "address": 13 ,   "label":"" },
                { "type":"nrj" , "address": 14 ,   "label":"" },
                { "type":"nrj" , "address": 15 ,   "label":"" },

                { "type":"nrj" , "address": 20 ,   "label":"2.00" },
                { "type":"nrj" , "address": 21 ,   "label":"2.01" },
                { "type":"nrj" , "address": 22 ,   "label":"2.02" },
                { "type":"nrj" , "address": 23 ,   "label":"" },
                { "type":"nrj" , "address": 24 ,   "label":"" },
                { "type":"nrj" , "address": 25 ,   "label":"" },
                { "type":"nrj" , "address": 26 ,   "label":"" },
                { "type":"nrj" , "address": 27 ,   "label":"" },
                { "type":"nrj" , "address": 28 ,   "label":"" },
                { "type":"nrj" , "address": 29 ,   "label":"" },
                { "type":"nrj" , "address": 30 ,   "label":"" },
                { "type":"nrj" , "address": 31 ,   "label":"" },
                { "type":"nrj" , "address": 32 ,   "label":"" },
                { "type":"nrj" , "address": 33 ,   "label":"" },
                { "type":"nrj" , "address": 34 ,   "label":"" },
                { "type":"nrj" , "address": 35 ,   "label":"" },

                { "type":"nrj" , "address": 40 ,   "label":"" },
                { "type":"nrj" , "address": 41 ,   "label":"" },
                { "type":"nrj" , "address": 42 ,   "label":"" },
                { "type":"nrj" , "address": 43 ,   "label":"" },
                { "type":"nrj" , "address": 44 ,   "label":"" },
                { "type":"nrj" , "address": 45 ,   "label":"" },
                { "type":"nrj" , "address": 46 ,   "label":"" },
                { "type":"nrj" , "address": 47 ,   "label":"" },
                { "type":"nrj" , "address": 48 ,   "label":"" },
                { "type":"nrj" , "address": 49 ,   "label":"" },
                { "type":"nrj" , "address": 50 ,   "label":"" },
                { "type":"nrj" , "address": 51 ,   "label":"" },
                { "type":"nrj" , "address": 52 ,   "label":"" },
                { "type":"nrj" , "address": 53 ,   "label":"" },
                { "type":"nrj" , "address": 54 ,   "label":"" },
                { "type":"nrj" , "address": 55 ,   "label":"" },
                ]
                         
            passerelle_daikin2 = [
                { "type":"eau" , "address": 51 ,   "label":"05 off" },
                ]

            intesisList = {25:passerelle_daikin1 }  # , 26:passerelle_daikin2 , 27:passerelle_daikin3 }  
            topology    = ""
            
            topology += "<?xml version='1.0' encoding='utf-8'?>\n"
            topology += '<Config version="1" name="-" >\n'
            id = 0
            xml  = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
            xml += "<Config version=\"1\">\n"
            xml += "  <ModbusModule>\n"
            xmlreg  = ""
            for intesis in intesisList.keys():
                topology += "  <Port id='" + str(intesis) + "'>\n"
                    
                address = 0
                for currentK7 in intesisList[intesis]:
                    id += 1
                    addresstexte = currentK7["address"]
                    type    = currentK7["type"]
                    label   = currentK7["label"]
                    #futur    
                    table = [
                            [ "unit" , 2 , "Volume" , "conso" , "m3" , "x/1000.0" ],
                            [ "unit" , 2 , "Débit" , "debit" , "m3/h" , "x/1000.0" ],
                            [ "unit" , 2 , "energieh" , "energieh" , "kWh" , "x/1000.0" ],
                            [ "unit" , 2 , "energiec" , "energiec" , "kWh" , "x/1000.0" ]
                            ]
                    config = ""
                    if "nrj" == type:
                        moduleName = "daikin_d3" + "_" + str(addresstexte)
                        adreelle = (address)*3+1001
                        label= "  " + str(address)
                        #moduleName = "saia_compteur_nrj" + "_" + label
                        topology += '    <ModbusModule type="' + moduleName + '" address="' + str(intesis) + '" id="' + str(id) + '" name="' + label + '" />\n'
                        xml += '    <' + moduleName + ' hardwareType="bridgedaikin" messagePause="0.3">\n'
                        xml += '      <Command name="get_state_1" type="Read" function="4"  address="' + str(adreelle-1) + '" length="5" cyclic="True">\n'
                        xml += '        <Value type="uint"   sort="' + str(adreelle) + '" label="Unit capability ' + str((addresstexte//20)+1) + '_' + str(addresstexte%20) + '"    name="unit"       startByte="0"   stopByte="4"   main="True"  unit="" />\n'
                        xml += '        <Value type="sint"   sort="' + str(adreelle+1) + '" label="T consigne froid min"                name="tcsilim"    startByte="4"  stopByte="6"  main="True"  unit="C"  />\n'
                        xml += '        <Value type="sint"   sort="' + str(adreelle+1) + '" label="T consigne froid max"                name="tcsiclim1"     startByte="6"  stopByte="8"  main="True"  unit="C"  />\n'
                        xml += '        <Value type="sint"   sort="' + str(adreelle+2) + '" label="T consigne chaud min"                name="tcsichauf"     startByte="8"  stopByte="10"  main="True"  unit="C"   />\n'
                        xml += '        <Value type="sint"   sort="' + str(adreelle+2) + '" label="T consigne chaud max"                name="tcsichauf1"      startByte="10"  stopByte="12"  main="True"  unit="C"   />\n'
                        xml += '      </Command>\n'
                        adreelle = (address)*6+2001
                        xml += '      <Command name="get_state_2" type="Read" function="4" address="' + str(adreelle-1) + '" length="6" cyclic="True">\n'
                        xml += '        <Value type="mask"   sort="' + str(adreelle) + '" label="Ventilation etat"                      name="etatfan"          startByte="0"   stopByte="4"  mask="0001"  rshift="0"    main="True"  unit="" />\n'
                        xml += '        <Value type="mask"   sort="' + str(adreelle) + '" label="Chauffage etat"                        name="etatchauf"        startByte="0"   stopByte="4"  mask="0002"  rshift="1"    main="True"  unit="" />\n'
                        xml += '        <Value type="mask"   sort="' + str(adreelle) + '" label="Thermo etat"                           name="etatthermo"       startByte="0"   stopByte="4"  mask="0004"  rshift="2"    main="True"  unit="" />\n'
                        xml += '        <Value type="mask"   sort="' + str(adreelle) + '" label="ventil vitesse"                        name="fan"              startByte="0"   stopByte="4"  mask="7000"  rshift="12"   main="True"  unit="" />\n'
                        xml += '        <Value type="mask"   sort="' + str(adreelle+1) + '" label="mode"                                name="mode"             startByte="4"  stopByte="8" mask="000F"  rshift="0"   main="True"  unit="C"  />\n'
                        xml += '        <Value type="sint"   sort="' + str(adreelle+2) + '" label="T consigne"                          name="tcsi"             startByte="8"  stopByte="12"  main="True"  unit="C" calculus="x/10" />\n'
                        xml += '        <Value type="sint"   sort="' + str(adreelle+4) + '" label="T ambiante"                          name="tamb"             startByte="16"  stopByte="20"   main="True"  unit="C" calculus="x/10"   />\n'
                        xml += '      </Command>\n'
                        adreelle = (address)*2+3601
                        xml += '      <Command name="get_state_3" type="Read" function="4" address="' + str(adreelle-1) + '" length="2" cyclic="True">\n'
                        xml += '        <Value type="uint" sort="' + str(adreelle) + '" label="Alarme"           name="alarme"   startByte="0"   stopByte="4"   main="True"  unit="" />\n'
                        xml += '      </Command>\n'
                        adreelle = (address)*3+2001
                        xml += '      <Command name="setonoff"      type="Write" address="' + str(adreelle-1) + '" label="OnOff ' + str(adreelle+0) + '"  mask="0001" lshift="0"  unit="1:marche, 0:arrêt" />\n'
                        xml += '      <Command name="setfan"        type="Write" address="' + str(adreelle-1) + '" label="Ventilateur ' + str(adreelle+0) + '"  mask="0007" lshift="12"   />\n'
                        xml += '      <Command name="setmode"       type="Write" address="' + str(adreelle+0) + '" label="Mode ' + str(adreelle+1) + '"   mask="000F" lshift="0" unit="0:fan 1:chaud 2:froid 3:auto 4:ventilation 7:dry"  />\n'
                        xml += '      <Command name="settcsi"       type="Write" address="' + str(adreelle+1) + '" label="T consigne ' + str(adreelle+2) + '"    unit="C" calculus="x*10"  />\n'
                        xml += "    </" + moduleName + ">\n"
                        xml +=  "\n" 
                
                    if "eau" == type:
                        moduleName = "saia_compteur_eau" + "_" + str(address)
                        adreelle = (address-1)*2+3601
                        topology += '    <ModbusModule type="' + moduleName + '" address="' + str(intesis) + '" id="' + str(id) + '" name="' + label + '" />\n'
                        xml += '    <' + moduleName + ' hardwareType="compteur_eau" messagePause="0.3">\n'
                        xml += '      <Command name="get_state_1" type="Read" address="' + str(adreelle) + '" length="8" cyclic="True">\n'
                        xml += '        <Value type="uint" wordOrder="inverted" sort="' + str(adreelle) + '" label="Volume ' + str(label) + '"  name="volume"   startByte="0"   stopByte="8"   main="True"  unit="m3"   calculus="x/1000.0" />\n'
                        xml += '      </Command>\n'
                        xml += '      <Command name="get_state_2" type="Read" function="1" address="' + str(address) + '" length="1" cyclic="True">\n'
                        xml += '        <Value type="mask" sort="' + str(address) + '" label="Défaut"           name="errcom"   startByte="0"   stopByte="2"   mask="01" rshift="0" main="True" />\n'
                        xml += '      </Command>\n'
                        xml += "    </" + moduleName + ">\n"
                        xml +=  "\n" 
                    
                    address += 1
                
                xml +=  "\n" + "\n" +  "\n" + "\n" + "\n" 
                xml +=  xmlreg +  "\n" 
                    
                
                topology += "  </Port>\n"
                print "   xml=" + str(len(xml)) + "  I=" + str(intesis) 
                print "   xmlreg=" + str(len(xmlreg)) + "  I=" + str(intesis) 

            xml += "  </ModbusModule>\n"
            xml += "</Config>\n"
            #os.remove(fileName)
            try:
                print "  remove1 " + fileName
                os.remove(fileName)
            except:
                print "  PROBLEME DE FICHIER (fichier utilisé par autre prg) : " + fileName
                pass
            xmlFile = os.open(fileName, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
            os.write(xmlFile, xml)
            print "   write" 
            topology += "</Config>\n" 
            try:
                os.remove("config_topology_" + fileName)
            except:
                pass
            xmlFile = os.open("config_topology_" + fileName, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
            os.write(xmlFile, topology)
        except:
            print "Error:", sys.exc_info()
        print "Génération terminée."
        # raw_input()

moulinette = GAMoulinette()
moulinette.run()
