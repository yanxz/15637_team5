from django.db import models
from django.db.models.signals import *
from django.contrib.auth.models import User
from datetime import *
import os
import random
# initial push version

def get_photo_path(instance, filename):
    date = datetime.now().strftime('%Y%m')
    fname, ext = os.path.splitext(filename)
    return 'image/%s/%d%s' %(date,random.randint(0,1000),ext.lower(),)


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
        (date, 'date'),
        (party, 'party'),
        (study,'study'),
        (hangout,'hangout'),
            )
    tag = models.CharField(max_length=5, choices=TAG, default=OTHER)
    loc = models.CharField(max_length=240,blank=True)

    def __unicode__(self):
        return self.title
    
class PersonScene(models.Model):
    essay = models.TextField(blank=True)
    video_loc = models.FileField(upload_to='video',blank=True)
    music_loc = models.FileField(upload_to='music',blank=True)
    photo_num = models.IntegerField(default=0)
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

'''
class Friends(models.Model):
    user = models.ForeignKey(User, related_name='user')
    friends = models.ManyToManyField(User, related_name='friends')
    is_active = models.BooleanField(default=False)
   
    @staticmethod
    def get_friends(user):
        return Friends.objects.filter(user=user)

    def __unicode__(self):
        friend_names = ""
        for friend in self.friends.all():
            friend_names += friend.first_name + " " + friend.last_name + " "
        return self.user.first_name + " " + self.user.last_name + " -> " + friend_names
'''
class Friends(models.Model):
    user = models.ForeignKey(User)
    friend_id = models.IntegerField(null=True,blank=True)
    is_active = models.BooleanField(default=False)

    @staticmethod
    def get_friends(user):
        return Friends.objects.filter(user=user)

    def __unicode__(self):
        friend_user = User.objects.get(id=self.friend_id)
        return friend_user.first_name +" "+ friend_user.last_name

class Message(models.Model):
    create_time = models.DateTimeField()
    content = models.TextField()
    from_user = models.ForeignKey(User, related_name='fromWho')
    to_user = models.ForeignKey(User, related_name='toWho')
    is_viewed = models.BooleanField(default=False)
    def __unicode__(self):
        return self.content

    @staticmethod
    def get_messages(user):
        return Message.objects.filter(to_user=user).order_by('-create_time')


'''
class Album(models.Model):
    user = models.ForeignKey(User,unique=True)
    person_scene = models.ForeignKey(PersonScene,unique=True)
    title = models.CharField(max_length=255)
'''
class PersonScene_photo(models.Model):
    #user = models.ForeignKey(User,unique=True)
    person_scene = models.ForeignKey(PersonScene,null=True, blank=True, default = None)
    photo = models.ImageField(upload_to=get_photo_path)
    create_time = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.ForeignKey(User,unique=True)
    id_photo = models.ImageField(upload_to='image',default='image/default.png')
    bg_pic = models.ImageField(upload_to='image',default='image/apple.jpg')
    music_id = models.FileField(upload_to='music',blank=True)
    token = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
