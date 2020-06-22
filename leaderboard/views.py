from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

from .forms import LeaderBoardForm
from .models import LeaderBoard

import pandas as pd
import re
import xlrd
import json


def home_page_view(request):
    return render(request, 'leaderboard/home.html', {})


def board_page_view(request, board_id):
    if request.method == 'GET':
        leader_board = get_object_or_404(LeaderBoard, board_id=board_id)
        return render(request, 'leaderboard/home.html', {'name': leader_board.board_name,
                                                         'data': leader_board.board_data,
                                                         'upload_date': leader_board.upload_date,
                                                         'last_update': leader_board.last_update})
    else:
        response = HttpResponse(status=405)
        response['ALLOW'] = ["GET"]
        return response


def board_page_edit_view(request, board_id):
    return render(request, 'leaderboard/home.html', {})


def board_page_upload(request):
    if request.method == 'POST':
        form = LeaderBoardForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['board_file'].file
            content_type = form.cleaned_data['board_file'].content_type

            excel_formats = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']

            if content_type == 'text/csv':
                try:
                    file_data = pd.read_csv(uploaded_file, index_col=None)
                except Exception as e:
                    return HttpResponse(json.dumps({'error': 'Error occurred while parsing csv file'}), status=404)
            elif content_type in excel_formats:
                try:
                    file_data = pd.read_excel(uploaded_file, index_col=None)
                except xlrd.biffh.XLRDError:
                    return HttpResponse(json.dumps({'error': 'Error occurred while parsing excel file'}), status=404)
            else:
                return HttpResponse(json.dumps({'error': 'Invalid file format'}), status=404)

            # Parse uploaded file data
            if file_data.empty:
                return HttpResponse(json.dumps({'error': 'Uploaded file is empty'}), status=404)
            else:
                # Sort by points and determine position
                sort_keys = [value.strip(' ') for value in form.cleaned_data['sort_key'].split(',')]
                try:
                    file_data.sort_values(sort_keys, inplace=True, ascending=False)
                except KeyError:
                    return HttpResponse(json.dumps({'error': 'Invalid Sort keys - Key is case sensitive'}), status=400)

                file_data_json = []
                position = [pos for pos in range(len(file_data))]
                file_data['position'] = position
                for index in range(len(file_data)):
                    file_data_json.append(file_data.iloc[index].to_dict())

                # save board
                leader_board = LeaderBoard(
                    board_name=form.cleaned_data['board_name'],
                    board_access_code=make_password(form.cleaned_data['board_access_code']),
                    board_data=file_data_json,
                    sort_by_key=json.dumps(form.cleaned_data['sort_key'])
                )

                leader_board.generate_key()
                leader_board.update_form()
                leader_board.save()

                return HttpResponse(json.dumps({'message': 'Leader board created',
                                                'board_id': leader_board.board_id}), status=201)
        else:
            return HttpResponse(json.dumps({'error': form.errors}), status=404)
    else:
        return render(request, 'leaderboard/upload.html', {'form': LeaderBoardForm()})
