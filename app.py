from flask import Flask, render_template, request, session, redirect, url_for
from pydantic import BaseModel, field_validator, ValidationError
import secrets

###########################VALIDATION###########################

class StockModel(BaseModel):
    """Class for parsing new stock data from a form."""
    stock_symbol: str
    number_of_shares: int
    purchase_price: float

    @field_validator('stock_symbol')
    def stock_symbol_check(cls, value):
        if not value.isalpha() or len(value) > 5:
            raise ValueError('Stock symbol must be 1-5 characters')
        return value.upper()

app = Flask(__name__)

###########################SECRET KEY###########################

app.secret_key = secrets.token_hex()

###########################ROUTES###########################

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html", company_name="data4all")

@app.route('/add_stock', methods=["GET", "POST"])
def add_stock():
    if request.method == "POST":
      for key, value in request.form.items():
          print(f'{key}: {value}')

      try:
            stock_data = StockModel(
                stock_symbol=request.form['stock_symbol'],
                number_of_shares=request.form['number_of_shares'],
                purchase_price=request.form['purchase_price']
            )
            print(stock_data)

            #Save the data into the session object
            session['stock_symbol'] = stock_data.stock_symbol
            session['number_of_shares'] = stock_data.number_of_shares
            session['purchase_price'] = stock_data.purchase_price
            return redirect(url_for('list_stocks'))
      except ValidationError as e:
            print(e)

    return render_template("add_stock.html")

@app.route("/stocks/")
def list_stocks():
    return render_template("stocks.html")

#@app.route('/hello/<message>')
#def hello_message(message):
#    return f'<h1>Welcome {message}!</h1>'

#@app.route('/blog_posts/<int:post_id>')
#def display_blog_post(post_id):
#    return f'<h1>Blog Post #{post_id}...</h1>'