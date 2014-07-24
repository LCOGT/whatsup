from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
import glob, urllib2, os, json
from whatsup.models import Target


from datetime import datetime, timedelta

class Command(BaseCommand):
    args = '<filename>'
    help = 'Ingest Guided Tours from XML files'
    
    def handle(self, *args, **options):
        if args:
         filename = "/%s*.xml" % args[0]
        else:
            filename = '/*.xml' 
        path = os.path.join(settings.STATICFILES_DIRS[0],'tours') + filename
        for gt in glob.glob(path):
            soup = BeautifulSoup(open(gt),'xml')
            try:
                self.stdout.write("\033[91m*** %s ***\033[0m\n" % soup.find('TOUR_NAME').get_text())
            except Exception,e:
                self.stdout.write(gt)
            for sc in soup.find_all('CATEGORY'):
                self.stdout.write("\033[92m%s, %s\033[0m\n" % (sc.find('CATEGORY_NAME').get_text(), len(sc.find_all('SKY_OBJECT'))))
                for so in sc.find_all('SKY_OBJECT'):
                    name = "".join(so.find('OBJECT_NAME').get_text().split())
                    desc = so.find('NOTES').get_text().strip()
                    print desc
                    exp = so.find('EXP_O').get_text().strip()
                    lookup_url = "http://lcogt.net/lookUP/json/?name=%s&callback=lk" % name
                    resp = urllib2.urlopen(lookup_url)
                    content = resp.read()
                    try:
                        obj = json.loads(content[3:-3])
                        if obj['category']['avmcode']:
                            target,new = Target.objects.get_or_create(name=name)
                            params = {
                                'ra'       : obj['ra']['decimal'],
                                'dec'      : obj['dec']['decimal'],
                                'avm_code' : obj['category']['avmcode'],
                                'avm_desc' : obj['category']['avmdesc'],
                                'description' : desc,
                                }
                            if exp:
                                params['exposure'] = float(exp)
                            for attr, value in params.iteritems(): 
                                setattr(target, attr, value)
                            target.save()
                        else:
                            self.stdout.write("\033[91m%s\033[0m\n" % (name))
                    except Exception, e:
                        self.stdout.write("\033[91m%s - %s\033[0m\n" % (name, e))


