from users.models import Preferences

def pref(request):
    if request.user.is_authenticated:
        _preferences = Preferences.objects.filter(user=request.user).last()
            
    else:
        _preferences = None
            
    return {
        'user_pref': _preferences,
    }