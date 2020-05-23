from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import DataPoint
from .models import Prediction
import datetime


def index(request):
    template = loader.get_template('app/menu.html')
    context = {
        'events': ["test"]
    }
    return HttpResponse(template.render(context, request))


def get_today_last():
    # 今日, yesterdayのend値を取ってくる
    last = DataPoint.objects.last()
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    if last and last.date == today:
        today = last
        all = DataPoint.objects.all().order_by('-id')
        next(all)
        last = next(all)
        return (today.end, last.end)

    return (None, last.end)


def prediction(request):
    """
    昨日の実測値と今日の予測値をMysqlから撮ってきて
    今日の値動きの予測（上か下か）をページに見せる
    """

    predicted, actual_prev = get_today_last()
    if not predicted:
        from .predictor import predict
        predicted = predict()

    # 取得した値から現在の最新の値（昨日の値）と比較して
    # 高いか低いかを判定する
    higher = True if predicted > actual_prev else False

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        prediction_today = Prediction.objects.get(date=today)
    except:
        pred = Prediction(
            date=today,
            predicted=predicted,
            previous=actual_prev,
            is_higher=higher
        )
        pred.save()

    template = loader.get_template('app/prediction.html')
    context = {
        'date': today,
        'predicted': '{:.02f}'.format(predicted[0]),
        'last': actual_prev,
        'higher': higher
    }

    return HttpResponse(template.render(context, request))


def historical(request):
    date_30days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    predictions = Prediction.objects.filter(date__gte=date_30days_ago.strftime('%Y-%m-%d'))
    dps = DataPoint.objects.filter(date__gte=date_30days_ago.strftime('%Y-%m-%d'))
    actuals = {x.date:x.end for x in dps}
    for p in predictions:
        cur_date = p.date.strftime('%Y-%m-%d')
        if not p.actual and cur_date in actuals:
            p.actual = actuals[cur_date]
            p.result_ok = (p.is_higher and p.actual >= p.previous) \
                or (not p.is_higher and p.actual <= p.previous)
            p.save()

    template = loader.get_template('app/historical.html')
    context = {
        'predictions': predictions
    }
    return HttpResponse(template.render(context, request))


def contact(request):
    template = loader.get_template('app/contact.html')
    context = {
        'events': ["test"]
    }
    return HttpResponse(template.render(context, request))


def bstest(request):
    template = loader.get_template('app/bs_index.html')
    context = {
        'events': ["test"]
    }
    return HttpResponse(template.render(context, request))
    
