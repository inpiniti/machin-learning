import Predict
import config
import api.naver as naver
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from route.holiday import isHoliday
cron = BackgroundScheduler(daemon=True, job_defaults={'max_instances': 2})

# 5분마다 실행
@cron.scheduled_job('interval', seconds=5, id='test_1')
def job1():
    print('job1 실행')

    # holiday
    h = isHoliday.get()
    if bool(h["holiday"] == 'false'):
        print('오늘은 공휴일이 아닙니다.')


    ## 시간 제한
    #if config.allPredictResult:
    #    now = datetime.today().strftime('%H:%M:%S')
    #    start = '09:00:00' < now
    #    end = '15:50:00' > now
    #    if start & end:
    #        print(f'ok {now}')
    #        config.allPredictResult = Predict.Predict().start()
    #    else:
    #        print(f'not {now}')
    ## allPredictResult 비어있는 경우 무조건 돌림
    #else:
    #    config.allPredictResult = Predict.Predict().start()

# 60초마다 실행
#@cron.scheduled_job('interval', seconds=60, id='test_2')
#def job2():
    #config.stockPredictResult = Predict.Predict() \
    #    .start2(naver.stock()) \
    #    .to_json(force_ascii=False, orient='records', indent=4)

    #config.discussionPredictResult = Predict.Predict() \
    #    .start2(naver.discussion()) \
    #    .to_json(force_ascii=False, orient='records', indent=4)

    #config.newsPredictResult = Predict.Predict() \
    #    .start2(naver.news()) \
    #    .to_json(force_ascii=False, orient='records', indent=4)