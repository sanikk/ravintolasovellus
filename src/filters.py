# template filters used on the jinja pages. these are added in app.


def output_date(the_date):
    return the_date.strftime("%A %d. %m. %Y")


def output_datetime(the_datetime):
    return the_datetime.strftime("%A %d. %m. %Y %I:%M")
