from django.shortcuts import render
from .strategy.payment_strategy import (
    PaypalPayment, StripePayment, BkashPayment,
    NagadPayment, RocketPayment, PaymentContext
)

def index(request):
    print(f"Request POST data: {request.POST}")
    message = ""
    if request.method == "POST":
        amount = request.POST.get("amount")
        method = request.POST.get("method")
        
        strategy_map = {
            "paypal": PaypalPayment(),
            "stripe": StripePayment(),
            "bkash": BkashPayment(),
            "nagad": NagadPayment(),
            "rocket": RocketPayment(),
        }
       
        strategy = strategy_map.get(method)
        
        if strategy:
            context = PaymentContext(strategy)
            message = context.make_payment(amount)
        else:
            message = "Invalid payment method."
    return render(request, "payments/index.html", {"message": message})
