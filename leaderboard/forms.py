from django import forms


class LeaderBoardForm(forms.Form):
    board_name = forms.CharField(label='LeaderBoard Name', max_length=50, required=True)
    sort_key = forms.CharField(label='LeaderBoard Sort Key/Column', max_length=50, required=True)
    board_file = forms.FileField(required=True)
    board_link = forms.CharField(label='Google Sheet Link', required=False)
    board_access_code = forms.IntegerField(label='Board Access Password', required=True)
