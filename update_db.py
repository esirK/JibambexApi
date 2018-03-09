from crontab import CronTab

# Updates Local Database after every 5 seconds to keep it in sync with online db

my_cron = CronTab(user='isaiahngaruiya')


job = my_cron.new(command='python manage.py update_local_database')
# job = my_cron.new(command='touch /Users/isaiahngaruiya/Desktop/shit.txt ')

job.minute.every(1)

my_cron.write()
