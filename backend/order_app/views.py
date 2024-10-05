import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from product_app.cart import Cart

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import send_order_confirmation_email

stripe.api_key = settings.STRIPE_SECRET_KEY



def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # Clear the cart after checkout
            cart.clear()
            # Send confirmation email
            # send_mail(
            #     'Order Confirmation',
            #     f'Your order #{order.id} has been placed successfully.',
            #     'from@example.com',
            #     [order.email],
            #     fail_silently=False,
            # )
            send_order_confirmation_email(
                'Order Confirmation',
                f'Your order #{order.id} has been placed successfully.',
                'from@example.com'
            )
            # Redirect to payment or order confirmation page
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = OrderCreateForm()
    return render(request, 'order_create.html', {'cart': cart, 'form': form})



def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        # Create a charge
        charge = stripe.Charge.create(
            amount=int(order.get_total_cost() * 100),  # Amount in cents
            currency='usd',
            description=f'Order {order.id}',
            source=request.POST['stripeToken']
        )
        order.paid = True
        order.save()
        return redirect('payment_done')
    else:
        # Stripe payment page
        return render(request, 'payment_process.html', {
            'order': order,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        })