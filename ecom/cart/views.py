from django.shortcuts import render,redirect,get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import  messages

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total = cart.cart_total()
    return render(request,"cart_summary.html",{"cart_products":cart_products, "quantities": quantities , "totals":total})
def cart_add(request):
    # Get the cart
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get product
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        # Add to cart
        cart.add(product=product,quantity = product_qty)
        
        # Return JSON response with the cart quantity
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request,("Product added "))
        return response
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get product
        product_id = int(request.POST.get('product_id'))        
        cart.delete(product = product_id)
        
        response = JsonResponse({'product':product_id})
        messages.success(request,("Product deleted... "))
        return response
        #return redirect('cart_summary')
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get product
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        cart.update(product = product_id,quantity = product_qty)
        
        response = JsonResponse({'qty':product_qty})
        messages.success(request,("Cart Updated "))
        return response
        #return redirect('cart_summary')