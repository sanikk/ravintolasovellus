from markupsafe import Markup

# template filters used on the jinja pages. these are added in app.


def output_date(the_date):
    return the_date.strftime("%A %d. %m. %Y")


def output_datetime(the_datetime):
    return the_datetime.strftime("%A %d. %m. %Y %I:%M")


def output_rating_stars(rating: int, size: int = 30):
    star_icon = f'<img src="/static/icons8-star-50.png" alt="Star" style="width:{size}px;height:{size}px;" />'
    return Markup(star_icon * rating)


def output_account_name(row):
    if "firstname" in row._mapping or "lastname" in row._mapping:
        return row._mapping.get("firstname", "") or row._mapping.get("lastname", "")
    if "account_firstname" in row._mapping or "account_lastname" in row._mapping:
        return row._mapping.get("account_firstname", "") or row._mapping.get(
            "account_lastname", ""
        )
    return ""


def output_full_name(row):
    return f"{row._mapping.get("firstname", "")} {row._mapping.get("lastname", "")}".strip()


# <a target="_blank" href="https://icons8.com/icon/104/star">Star</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
