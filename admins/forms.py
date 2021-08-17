from django import forms

from products.models import ProductCategory
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserAdminRegisterForm(UserRegisterForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'image', 'first_name', 'last_name', 'password1', 'password2')


class UserAdminProfileForm(UserProfileForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': False}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': False}))


class UserAdminProductCategoryEditForm(forms.ModelForm):
    discount = forms.IntegerField(label='Скидка', required=False,
                                  min_value=0, max_value=90, initial=0)

    class Meta:
        model = ProductCategory
        exclude = ()    # то же самое что fields = '__all__'
