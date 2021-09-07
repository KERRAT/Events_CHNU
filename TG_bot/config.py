
TOKEN = '1331813134:AAHMENu9f70UHzwSWs_vugq9S9_i6Jwe_r0'

adminlst=(741475126,430143683, 470910174)
password='370920'
admin_id = '430143683'
config_id = '1000'


def binarySearch(alist, item):
    if len(alist) == 0:
        return False
    else:
        midpoint = len(alist)//2
        if alist[midpoint]==item:
          return True
        else:
          if item<alist[midpoint]:
            return binarySearch(alist[:midpoint],item)
          else:
            return binarySearch(alist[midpoint+1:],item)
