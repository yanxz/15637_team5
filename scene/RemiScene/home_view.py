

@login_required
def home(request):
    user = request.user
    friends = Friends.get_friends(user)
    profile = user.get_profile()
    messages = Message.get_messages(user)
    scene_set = []
    person_scenes = PersonScene.get_personScenes_from_user(user)
    for s in person_scenes:
        scene_set.append(s.scene)
    context = {'user':user,
            'profile':profile,
            'scenes':scene_set,
            'friends':friends,
            'messages':messages}
    return render(request, 'blog/home',context)

@transaction.atomic
def register(request)



