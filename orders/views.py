from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.core.mail import send_mail

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                order_item = OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         custom_message=item.get('custom_message', ''))
                if item.get('addons_objects'):
                    order_item.addons.set(item['addons_objects'])
            # clear the cart
            cart.clear()
            
            # Send email
            subject = f'Order nr. {order.id}'
            message = f'Dear {order.first_name},\n\nYou have successfully placed an order.\nYour order ID is {order.id}.'
            
            # We use a try-except block to prevent crashing if email fails in dev without proper config
            try:
                send_mail(subject, message, 'admin@acholacakes.com', [order.email])
            except Exception as e:
                print(f"Email sending failed: {e}")

            return render(request, 'orders/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html',
                  {'cart': cart, 'form': form})
