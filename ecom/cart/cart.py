from store.models import Product
class Cart():
    def __init__(self,request) -> None:
        self.session = request.session
        
        #Get the current session key if it exists
        cart = self.session.get('session_key')
        
        #If the user is new, no session! Create one!
        if 'session_key' not in request.session:
            cart =self.session['session_key'] = {}
            
        #Make syre cart is available on all the pages of site
        self.cart = cart
        
    def add(self,product,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        
        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
        
    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        
        # Use ids to look up products in the database model
        products = Product.objects.filter(id__in=product_ids)
        
        # Return the looked up products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self,product,quantity):
        product_id = str(product)
        product_qty = int(quantity)
        
        #Get Cart
        
        ourcart = self.cart
        ourcart[product_id] = product_qty
        
        self.session.modified = True
        
        thing = self.cart
        
        return thing
    def delete(self,product):
        product_id = str(product)
        
        #delete from dictionary/cart
        
        if product_id in self.cart:
            del self.cart[product_id]
        
        
        self.session.modified = True
             
        