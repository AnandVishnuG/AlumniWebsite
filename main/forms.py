from django.forms import ModelForm, CharField, Textarea
from . models import Post, Feedback

# Form to create a post
class PostForm(ModelForm):
    # body = CharField(label="", 
    #                  widget=Textarea(attrs={'rows':'5',
    #                                         'placeholder':'Post something...'
    #                         }),
    #                        required=False)
    class Meta:
        model = Post
        fields = ['synopsis','body']
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