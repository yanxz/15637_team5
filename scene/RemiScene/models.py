from django.db import models
from django.db.models.signals import *
from django.contrib.auth.models import User

# initial push version
class Location(models.Model):
    longitude = models.IntegerField()
    latitude = models.IntegerField()
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=240)

class Scene(models.Model):
    title = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    occur_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    image_loc = models.ImageField(upload_to='image', blank=True)
    LIFE = 'life'
    WORK = 'work'
    OTHER = 'other'
    TAG = (
        (LIFE, 'happy'),
        (WORK, 'date'),
        (OTHER, 'party'),
            )
    tag = models.CharField(max_length=5, choices=TAG, default=OTHER)
    location = models.ForeignKey(Location,null=True, blank=True, default = None)

    def __unicode__(self):
        return self.title

    
class PersonScene(models.Model):
    essay = models.TextField(blank=True)
    video_loc = models.FileField(upload_to='video',blank=True)
    music_loc = models.FileField(upload_to='music',blank=True)
    photo_loc = models.ImageField(upload_to='image',blank=True)
    scene = models.ForeignKey(Scene,null=True, blank=True, default = None)
    user = models.ForeignKey(User,null=True, blank=True, default = None)

    def __unicode__(self):
        return self.user.username+" in "+self.scene.title

    @staticmethod
    def get_personScenes_from_scene(this_scene):
        return PersonScene.objects.filter(scene=this_scene)

    @staticmethod
    def get_personScenes_from_user(this_user):
        return PersonScene.objects.filter(user=this_user)

class Comment(models.Model):
    content = models.TextField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    person_scene = models.ForeignKey(PersonScene,null=True, blank=True, default = None)
    def __unicode__(self):
        return self.content

class Privilege(models.Model):
    user = models.ForeignKey(User)
    scene = models.ForeignKey(Scene)
    level = models.IntegerField()

class Friends(models.Model):
    user = models.ForeignKey(User, related_name='user')
    friends = models.ManyToManyField(User, related_name='friends')
   
    @staticmethod
    def get_friends(user):
        return Friends.objects.filter(user=user)

class Message(models.Model):
    create_time = models.DateTimeField()
    content = models.TextField()
    from_user = models.ForeignKey(User, related_name='fromWho')
    to_user = models.ForeignKey(User, related_name='toWho')
    def __unicode__(self):
        return self.content

    @staticmethod
    def get_messages(user):
        return Message.objects.filter(to_user=user).order_by('-create_time')

class Profile(models.Model):
    user = models.ForeignKey(User,unique=True)
    id_photo = models.ImageField(upload_to='image',default='image/default.png')
    bg_pic = models.ImageField(upload_to='image',blank=True)
    music_id = models.FileField(upload_to='music',blank=True)
    token = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
