from flask import Flask, request, render_template
from PIL import Image
import io
import base64

app = Flask(__name__)

# Define currency conversion rates
conversion_rates = {
   'INR': {'USD': 0.012, 'EUR': 0.011, 'JPY': 1.77, 'GBP': 0.010, 'AUD': 0.019, 'CAD': 0.017, 'CHF': 0.011, 'CNY': 0.087, 'NZD': 0.020, 'MXN': 0.22},
    'USD': {'INR': 80.75, 'EUR': 0.93, 'JPY': 133.50, 'GBP': 0.78, 'AUD': 1.49, 'CAD': 1.25, 'CHF': 0.91, 'CNY': 7.21, 'NZD': 1.69, 'MXN': 17.76},
    'EUR': {'INR': 79.89, 'USD': 1.08, 'JPY': 143.65, 'GBP': 0.84, 'AUD': 1.60, 'CAD': 1.35, 'CHF': 0.98, 'CNY': 7.77, 'NZD': 1.82, 'MXN': 19.06},
    'JPY': {'INR': 0.61, 'USD': 0.0075, 'EUR': 0.007, 'GBP': 0.0058, 'AUD': 0.011, 'CAD': 0.0094, 'CHF': 0.0068, 'CNY': 0.054, 'NZD': 0.013, 'MXN': 0.13},
    'GBP': {'INR': 102.67, 'USD': 1.28, 'EUR': 1.19, 'JPY': 171.48, 'AUD': 1.91, 'CAD': 1.61, 'CHF': 1.17, 'CNY': 9.23, 'NZD': 2.17, 'MXN': 22.82},
    'AUD': {'INR': 54.02, 'USD': 0.67, 'EUR': 0.62, 'JPY': 89.92, 'GBP': 0.52, 'CAD': 0.84, 'CHF': 0.61, 'CNY': 4.82, 'NZD': 1.13, 'MXN': 11.95},
    'CAD': {'INR': 64.36, 'USD': 0.80, 'EUR': 0.74, 'JPY': 106.73, 'GBP': 0.62, 'AUD': 1.19, 'CHF': 0.72, 'CNY': 5.72, 'NZD': 1.35, 'MXN': 14.20},
    'CHF': {'INR': 84.29, 'USD': 1.10, 'EUR': 1.02, 'JPY': 146.65, 'GBP': 0.85, 'AUD': 1.64, 'CAD': 1.39, 'CNY': 7.94, 'NZD': 2.03, 'MXN': 20.15},
    'CNY': {'INR': 11.18, 'USD': 0.14, 'EUR': 0.13, 'JPY': 18.46, 'GBP': 0.11, 'AUD': 0.21, 'CAD': 0.18, 'CHF': 0.13, 'NZD': 0.26, 'MXN': 2.54},
    'NZD': {'INR': 47.83, 'USD': 0.59, 'EUR': 0.55, 'JPY': 79.52, 'GBP': 0.46, 'AUD': 0.88, 'CAD': 0.74, 'CHF': 0.49, 'CNY': 3.87, 'MXN': 9.69},
    'MXN': {'INR': 4.55, 'USD': 0.056, 'EUR': 0.052, 'JPY': 7.66, 'GBP': 0.044, 'AUD': 0.084, 'CAD': 0.070, 'CHF': 0.050, 'CNY': 0.39, 'NZD': 0.10},
}

currency_images = {
    'INR': 'D:/currency_convertor/static/inr.jpeg',
    'USD': 'D:/currency_convertor/static/usd.jpg',
    'EUR': 'D:/currency_convertor/static/eur.jpg',
    'JPY': 'D:/currency_convertor/static/jpy.jpg',
    'GBP': 'D:/currency_convertor/static/gbp.jpg',
    'AUD': 'D:/currency_convertor/static/aud.jpg',
    'CAD': 'D:/currency_convertor/static/cad.jpg',
    'CHF': 'D:/currency_convertor/static/chf.jpg',
    'CNY': 'D:/currency_convertor/static/cny.jpg',
    'NZD': 'D:/currency_convertor/static/nzd.jpeg',
    'MXN': 'D:/currency_convertor/static/mxn.jpg'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        from_currency = request.form.get('currency')
        amount = request.form.get('amount')
        
        try:
            amount = float(amount)
        except ValueError:
            return render_template('index.html', error="Please enter a valid amount.")
        
        if from_currency in conversion_rates:
            rates = conversion_rates[from_currency]
            result = {key: amount * value for key, value in rates.items()}

            # Fetch the image
            img_path = currency_images.get(from_currency, None)
            img_base64 = None
            if img_path:
                try:
                    with open(img_path, "rb") as image_file:
                        img_base64 = base64.b64encode(image_file.read()).decode('utf-8')
                except FileNotFoundError:
                    img_base64 = None
            
            return render_template('index.html', rates=result, image=img_base64)
        else:
            return render_template('index.html', error="Invalid currency selected.")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
