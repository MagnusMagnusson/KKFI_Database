from django.test import TestCase
from sets import Set
from catdb.models import *
from django.utils import timezone
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
# Create your tests here.


class UnitTest(TestCase):
    def setUp(self): #Sets up this unit test, populating the database. 
        print("STARTING SETUP")
        Clast = None
        Cprev = None
        for i in xrange(30):
            C = cat()
            C.name = "kisi_nr_"+ str(i)
            C.birth = timezone.now()
            C.reg_nr = str(i * 100 + i * 23 + i*17 + i*5 + i)
            C.registered = C.birth
            C.gender = (i % 2) == 0
            if(Clast != None):
                C.sire = Clast
            if(Cprev != None):
                C.dam = Cprev
            C.save()
               # ADD PARENT ENTRY
            P = parents()
            P.is_ghost = False
            P.cat = C
            P.save()
                # ADD MICROCHIP ENTRY
            M = microchip()
            M.cat = C
            M.microchip_nr = str(int(C.reg_nr) + 5)
            M.save()
                #ADD NEUTERED ENTRY (only every third cat is neutered)
            if((i%3) == 0):
                N = neutered()
                N.cat = C
                N.date = timezone.now()
                
                #Create imported cats
            if(i%4 == 0):
                IC = cat()
                IC.name = "Imported_cat_"+str(i/4)
                IC.birth = timezone.now()
                IC.registered = IC.birth
                IC.gender = (i%2)
                IC.reg_nr = 12*(i * 100 + i * 23 + i*17 + i*5 + i)
                IC.save()
                I = imp_cat() 
                I.cat = IC
                I.org_country = "ICE"
                I.org_organization = "Orginization"
                j = i/4
                I.org_reg_nr = str(10*(j * 100 + j * 23 + j*17 + j*5 + j))
                I.save()
                
            if((i % 2) != 0):
                Clast = P
            else:
                Cprev = P
        Pdam = parents.objects.get(cat = cat.objects.get(name = "kisi_nr_18").id )
        Psire = parents.objects.get(cat = cat.objects.get(name = "kisi_nr_17").id )
        
        #Brother
        C = cat()
        C.name = "Brother"
        C.gender = True
        C.reg_nr = "12394"
        C.birth = timezone.now()
        C.registered = timezone.now()
        C.dam = Pdam
        C.save()
        M = microchip()
        M.cat = C
        M.microchip_nr = str(int(C.reg_nr) + 5)
        M.save()
        #sister
        C = cat()
        C.name = "Sister"
        C.gender = False
        C.reg_nr = "13234"
        C.birth = timezone.now()
        C.registered = timezone.now()
        C.sire = Psire
        C.save()           
        M = microchip()
        M.cat = C
        M.microchip_nr = str(int(C.reg_nr) + 5)
        M.save()
        #EvilTwin
        C = cat()
        C.name = "EvilTwin"
        C.gender = False
        C.reg_nr = "99999"
        C.birth = timezone.now()
        C.registered = timezone.now()
        C.sire = Psire
        C.dam = Pdam
        C.save()            
        M = microchip()
        M.cat = C
        M.microchip_nr = str(int(C.reg_nr) + 5)
        M.save()

    def test_Ancestor(self):
        print("************ Starting Ancestry Test ************")
        print("Testing Sire ancestry. Expected result is all odd numbered cats below 29 (and 29 itself)");
        C = cat.objects.get(name = "kisi_nr_29")
        while(C != None and C.sire != None):
            print(C.id,C.name,"Fathered by:")
            P = C.sire
            if(P.cat != None):
                C = P.cat
            else:
                print("No parent")
                C = None
        print(C.name)
        print("Sire test complete. Testing Dam ancestry. Expected result is all even numbers below to 29 (and 29 itself)")        
        C = cat.objects.get(name = "kisi_nr_29")
        while(C != None and C.dam != None):
            print(C.id,C.name,"Mothered by:")
            P = C.dam
            if(P.cat != None):
                C = P.cat
            else:
                print("No parent")
                C = None
        print("Dam test complete") #Tests if ancestry foreign keys are working by listing the direct lineage of cat_29
    def test_Children(self): #Tests if Children foreign keys are working by listing all children.
        print("************ Starting Offspring Test ************")
        print("Testing offspring listing. Expected result: cats 20 to 29")
        C = cat.objects.get(name = "kisi_nr_19")
        P = parents.objects.get(cat = C.id)
        MotherOf = P.dam.all()
        MotherOf = MotherOf | (P.sire.all())
        length = -1
        while(length != len(MotherOf)):
            length = len(MotherOf)
            for i in MotherOf:
                P = parents.objects.get(cat = i.id)
                MotherOf = MotherOf | P.sire.all() | P.dam.all()
        for i in MotherOf:
            print(i.name)
        print("offspring listing test ended")
        print("Testing sibling test. Expected results: 'kisi_nr_19 has the siblings: kisi_nr_18, kisi_nr_19, kisi_nr20, Brother,Sister,EvilTwin'")

        Kid = cat.objects.get(name = "kisi_nr_19")
        KidDad = Kid.sire
        KidMom = Kid.dam
        KidSiblings = KidDad.sire.all() | KidMom.dam.all()
        print(Kid.name + " has the siblings:")
        for i in KidSiblings:
            print(i.name)
        print("Sibling test ended")
    def test_Microchip(self): #tests if microchips are correctly implemented
        print("********* Starting microchip test *********")
        print("Finding microchips for one third of registered cats")
        for i in cat.objects.all():
            if(i.id % 3 == 0):
                if((imp_cat.objects.filter(cat = i.id)).count() == 0):
                    try:
                        M = microchip.objects.get(cat = i.id)
                        if(M.microchip_nr == str((int(i.reg_nr) + 5))):
                            print(i.name + " has the correct microchip.")
                        else:
                            print(i.name + " has the incorrect microchip! ( has  "+M.microchip_nr + ", should be "+str((int(i.reg_nr) + 5)) + ")")
                    except ObjectDoesNotExist:
                        #emptyblock
                        print(i.name + " does not have a microchip!")
                        return False
                else:
                    print(i.name + " has no microchip on purpose.")
        print("microchip test ended")

        
        
        
           


            