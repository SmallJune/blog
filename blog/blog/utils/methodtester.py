import cProfile
import os.path
import sys


from django.core.management import setup_environ


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'lovewith.settings'
from lovewith import settings
setup_environ(settings)

def test(n):
    from lovewith.share.views.modules.attach_like import AttachLikeApi
    result = AttachLikeApi.get_by_user(9193,1,80)
    # print result

# bulk_list = []
# for i in service:
#     print i.name
#     sr = SupplierRecomend(
#         json_data='{}',
#         service_id=i.id,
#         service_name=i.name,
#     )
#     bulk_list.append(sr)
# SupplierRecomend.objects.bulk_create(bulk_list)

if __name__ == '__main__':

    pn=sys.argv[1]
    # test(int(pn))
    cProfile.run('test(1)')
