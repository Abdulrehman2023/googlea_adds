import shutil
from django.dispatch import receiver
from django.db.models import signals
from app import models
from app.tasks import capturess
from project import settings
import asyncio,os
from django.utils import timezone
loop = asyncio.get_event_loop()
from django.dispatch import Signal
campaig_created = Signal()
# from apscheduler.schedulers.background import BackgroundScheduler
# scheduler = BackgroundScheduler()
# scheduler.start()
s3 = settings.BotoClient
@receiver(signals.post_delete, sender=models.ClientUrl)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.image.delete(save=False)
    except:
        pass

@receiver(signals.post_delete, sender=models.CampaignImages)
def post_dlt_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.image.delete(save=False)
    except:
        pass
    
@receiver(campaig_created)
def post_update(sender, instance,video, *args, **kwargs):
    print("signal",instance,video)
    capturess()
    # capturess.apply_async(eta=timezone.now(), args=[instance.id,video],id=f'{instance.id}')
    # scheduler.add_job(module.capture_ss,id=f'{instance.id}',max_instances=1,args=[instance,video,scheduler])

@receiver(signals.post_delete, sender=models.Campaign)
def post_delete_image(sender, instance, *args, **kwargs):
    objects_to_delete = s3.list_objects(Bucket="piranhad", Prefix=f"{instance.id}/")
    delete_keys = {'Objects' : []}
    delete_keys['Objects'] = [{'Key' : k} for k in [obj['Key'] for obj in objects_to_delete.get('Contents', [])]]
    if delete_keys['Objects']:
        s3.delete_objects(Bucket="piranhad", Delete=delete_keys)
    if os.path.exists(os.path.join(settings.BASE_DIR/"media", f'{instance.id}')):
        shutil.rmtree(os.path.join(settings.BASE_DIR/"media", f'{instance.id}'))
    if os.path.exists(os.path.join(settings.BASE_DIR/"media", f'{instance.id}_ads')):
        shutil.rmtree(os.path.join(settings.BASE_DIR/"media", f'{instance.id}_ads'))
    try:
        instance.pdf.delete(save=False)
        instance.word.delete(save=False)
        instance.pptx.delete(save=False)
        instance.zip.delete(save=False)
    except:
        pass