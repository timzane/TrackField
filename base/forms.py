from django.forms import ModelForm
from .models import Athlete, Performance, Event, User  
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username','email','bio']

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']

class AthleteForm(ModelForm):
    class Meta:
        model = Athlete
        fields = ['First','Last','Athlete','Active','Male','Graduation']
        



class PerformanceForm(ModelForm):
    

    class Meta:
        model = Performance
        fields = ['EventID','MeetID','Mark','EventDate','PerformanceNote','CY','AthleteID','Archive','StateChamp','Notes',
            'MarkRawLarge','MarkRawSmall','Confirmed']
        labels = {
        "EventID":  "Event",
        "MeetID":  "Meet",
    }
    
    def __init__ (self, athletepk=None, eventselect=None , *args, **kwargs):

        queryset = Athlete.objects.filter(Active=1,Male=1)
        for  athlete in athletepk:
            queryset |= Athlete.objects.filter(id=athlete.id)
        
        super(PerformanceForm, self).__init__(*args, **kwargs)
        self.fields["AthleteID"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["AthleteID"].queryset = queryset
        print (eventselect)
        
        if eventselect != None:
            if 'eventid' in eventselect:
                eventselectid = eventselect['eventid']
                self.fields['EventID'].initial = Event.objects.get(id=eventselectid)
            if 'MarkRaw' in eventselect:
                print(eventselect['MarkRaw'])
                
            else:
                print("not mark identified")    
                


            print("something")
        else:
            print("nothing")    
        
      
    






