from django.contrib.auth.forms import UserCreationForm  
from .constants import ACCOUNT_TYPE,GENDER_TYPE
from django.contrib.auth.models import User
from django import forms
from .models import UserBankAccount,UserAddress

class UserRegistrationForm(UserCreationForm):
    # 2 ta models er jonno kaj korlam
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    
    class Meta:
        model = User  # user model ke call kora holo
        fields = ['username','first_name','last_name','email','password1','password2','account_type','gender','birth_date','postal_code','country','city','street_address']


    # form save
    def save(self,commit= True):
        our_user = super().save(commit=False) # data base e ekhon save korbo na
        if commit == True:
            our_user.save() # user model e data save korlam
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            birth_date = self.cleaned_data.get('birth_date')
            city = self.cleaned_data.get('city')
            street_address = self.cleaned_data.get('street_address')

            UserAddress.objects.create(
                user = our_user,
                postal_code = postal_code,
                city = city,
                street_address = street_address,
                country = country,


            )
            UserBankAccount.objects.create(
                user = our_user,
                birth_date = birth_date,
                gender = gender,
                account_type = account_type,
                account_no = 100000 + our_user.id


            )

        return our_user
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })






