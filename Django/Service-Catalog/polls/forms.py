from django import forms
from polls.models import Post1


class HomeForm(forms.ModelForm):
    Answer_1 = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'i.e. John Doe...'
        }
    ))
	
    class Meta:
        model = Post1
        fields = ('Answer_1',)
		
		
class HomeForm2(forms.ModelForm):
    Answer_2 = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'i.e. Single user, department, etc...'
        }
    ))
	
    class Meta:
        model = Post1
        fields = ('Answer_2',)
		
		
		
class HomeForm3(forms.ModelForm):
    Answer_3 = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'i.e. We need a tool to monitor data sets...'
        }
    ))
	
    class Meta:
        model = Post1
        fields = ('Answer_3',)
		
						
				
class HomeForm4(forms.ModelForm):
    Answer_4 = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'i.e. Are they aware of the request...'
        }
    ))
	
    class Meta:
        model = Post1
        fields = ('Answer_4',)
									
								
								
class HomeForm5(forms.ModelForm):
    Answer_5 = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'i.e. Operations/Legal/Loyalty...'
        }
    ))
	
    class Meta:
        model = Post1
        fields = ('Answer_5',)
								


class HomeForm6(forms.ModelForm):
    Answer_6 = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'i.e. https://example.com/eula'
        }
    ))
	
    class Meta:
        model = Post1
        fields = ('Answer_6',)
		
													

class HomeForm7(forms.ModelForm):
    Answer_7 = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'i.e. QA/Legal/NOC'
        }
    ))
	
    class Meta:
        model = Post1
        fields = ('Answer_7',)
		
				

class HomeForm8(forms.ModelForm):
    Answer_8 = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'i.e. IT Procurement'
        }
    ))
	
    class Meta:
        model = Post1
        fields = ('Answer_8',)
		
		

class HomeForm9(forms.ModelForm):
    Answer_9 = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'i.e. Yes or No'
        }
    ))
	
    class Meta:
        model = Post1
        fields = ('Answer_9',)
		
		

class HomeForm10(forms.ModelForm):
    Answer_10 = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'i.e. Microsoft Word'
        }
    ))
	
    class Meta:
        model = Post1
        fields = ('Answer_10',)
		
											