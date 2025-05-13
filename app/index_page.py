from flask import Blueprint, render_template


def index_page() -> Blueprint:
    page = Blueprint('index_page', __name__)

    @page.get('/')
    def index():
        return render_template('index.html')

    return page
