from markupsafe import Markup
# template filters used on the jinja pages. these are added in app.


def output_date(the_date):
    return the_date.strftime("%A %d. %m. %Y")


def output_datetime(the_datetime):
    return the_datetime.strftime("%A %d. %m. %Y %I:%M")

def output_rating_stars(rating: int):
    star_icon = '<img src="/static/icons8-star-50.png" alt="Star" />'
    return Markup(star_icon * rating)


def output_account_name(datadict):
    if "firstname" in datadict._mapping or "lastname" in datadict._mapping:
        return datadict._mapping.get("firstname", "") or datadict.get("lastname", "")
    if "account_firstname" in datadict._mapping or "account_lastname" in datadict._mapping:
        return datadict._mapping.get("account_firstname", "") or datadict._mapping.get("account_lastname", "")
    return ""

# <a target="_blank" href="https://icons8.com/icon/104/star">Star</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
