from django.forms import ModelForm, CharField, Textarea, DateTimeField, IntegerField, ChoiceField, modelformset_factory
from . models import Post, Feedback, Poll, Poll_choice, Cart, CartItem
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.utils import timezone
import pytz
# Form to create a post
class PostForm(ModelForm):
    # body = CharField(label="", 
    #                  widget=Textarea(attrs={'rows':'5',
    #                                         'placeholder':'Post something...'
    #                         }),
    #                        required=False)
    CATEGORY_CHOICES = [
        ('Posts', 'Posts'),
        ('Events', 'Events'),
        ('News', 'News'),
    ]
    category = ChoiceField(label="Category:", choices=CATEGORY_CHOICES)
    def clean_publish_date(self):
        publish_date = self.cleaned_data['publish_date']
        naive_date = timezone.make_naive(publish_date)
        est = pytz.timezone('US/Eastern')
        aware_date = est.localize(naive_date)
        return aware_date.astimezone(pytz.utc)
    class Meta:
        model = Post
        fields = ['synopsis', 'category',  'body', 'publish_date']
        widgets = { 'publish_date': DateTimePickerInput(options={
            'sideBySide': True,
        })}
# Form to create a feedback
class FeedbackForm(ModelForm):
    comment = CharField(label="", 
                     widget=Textarea(attrs={'rows':'5',
                                            'placeholder':'Post something...'
                            }),
                           required=False)
    class Meta:
        model = Feedback
        fields = ['comment']                    
# Form to display carts
class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields= ["count", "total"]
        
CartFormSet = modelformset_factory(CartItem, fields=("quantity",), extra=0)
# Form to create a poll
class PollForm(ModelForm):
    # choices = IntegerField(min_value=1, max_value=10)
    question = CharField(max_length=200)
    def clean_publish_date(self):
        publish_date = self.cleaned_data['publish_date']
        naive_date = timezone.make_naive(publish_date)
        est = pytz.timezone('US/Eastern')
        aware_date = est.localize(naive_date)
        return aware_date.astimezone(pytz.utc)

    class Meta:
        model= Poll
        fields = ['question', 'publish_date' ]
        widgets = { 'publish_date': DateTimePickerInput(
            attrs={
                
                'style': 'left:20px;'
            },options={
            'sideBySide': True,
        })}
# Form to add poll choices
class PollChoiceForm(ModelForm):
    class Meta:
        model = Poll_choice
        fields = ['choice', 'vote']

PollFormSet = modelformset_factory(Poll_choice, fields=("choice",), extra=0, min_num=2, max_num=10)
