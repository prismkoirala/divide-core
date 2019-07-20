from django import forms
from django_countries.fields import CountryField


class CheckoutForm(forms.Form):
    STATES =[
    ('1','STATE 1'),
    ('2','STATE 2'),
    ('3','STATE 3'),
    ('4','STATE 4'),
    ('5','STATE 5')
    ]
    PAYMENT_CHOICES = [
        ('S','Stripe'),
        ('P','Paypal')
    ]
    street_address = forms.CharField(
        widget = forms.TextInput(attrs={
            'placeholder' : 'eg. 1234 main road, near abc landmark',
            'class' : 'form-control'
        }))
    apartment_address = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={
            'placeholder' : 'eg. Apartment or House no.',
            'class' : 'form-control'

            }))
    state = forms.ChoiceField(
                    choices = STATES,
                    widget = forms.widgets.Select(
                        attrs ={
                            'class' : 'browser-default custom-select custom-select-lg mb-3'
                        }
                    ),
                    )
    zip = forms.CharField(widget = forms.TextInput(attrs = {
        'placeholder' : 'eg. 0056',
        'class' : 'form-control custom-select-lg',
        'id' : 'zip'
    }))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget = forms.Select(),
        choices = PAYMENT_CHOICES)
