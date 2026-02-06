from decimal import Decimal
from django.conf import settings
from store.models import Product, AddOn

class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False, custom_message='', addons=None):
        """
        Add a product to the cart or update its quantity.
        """
        # Create a unique ID based on product and options
        addon_ids = [str(a.id) for a in addons] if addons else []
        addon_ids.sort()
        
        # We need a unique key for the cart dictionary
        # Format: "productID_sortedAddonIDs_customMessage"
        # We use a hash or just the string to keep it simple but unique
        cart_id = f"{product.id}_{'-'.join(addon_ids)}_{custom_message.replace(' ', '_')}"
        
        if cart_id not in self.cart:
            self.cart[cart_id] = {
                'quantity': 0, 
                'price': str(product.price),
                'product_id': product.id,
                'custom_message': custom_message,
                'addon_ids': addon_ids
            }
        
        if override_quantity:
            self.cart[cart_id]['quantity'] = quantity
        else:
            self.cart[cart_id]['quantity'] += quantity
        self.save()

    def update(self, cart_id, quantity):
        """
        Update the quantity of a specific cart item.
        """
        if cart_id in self.cart:
            self.cart[cart_id]['quantity'] = quantity
            self.save()


    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product_cart_id):
        """
        Remove a product from the cart.
        """
        if product_cart_id in self.cart:
            del self.cart[product_cart_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = {item['product_id'] for item in self.cart.values()}
        products = Product.objects.filter(id__in=product_ids)
        
        # Better: we need to iterate our cart items one by one
        # because the same product ID might appear multiple times with different options
        
        # Optimization: Fetch all needed products and addons in one go
        addon_ids_all = set()
        for item in self.cart.values():
            if 'addon_ids' in item:
                addon_ids_all.update(item['addon_ids'])
        
        fetched_addons = {str(a.id): a for a in AddOn.objects.filter(id__in=addon_ids_all)}
        fetched_products = {p.id: p for p in products}

        cart = self.cart.copy()
        
        for cart_id, item in cart.items():
            item['product'] = fetched_products.get(item['product_id'])
            
            # Re-calculate price including addons
            base_price = Decimal(item['price'])
            addons_cost = Decimal(0)
            
            item_addons = []
            if 'addon_ids' in item:
                for aid in item['addon_ids']:
                    addon = fetched_addons.get(aid)
                    if addon:
                        item_addons.append(addon)
                        addons_cost += addon.price
            
            item['addons_objects'] = item_addons
            item['price'] = base_price + addons_cost
            item['total_price'] = item['price'] * item['quantity']
            item['cart_id'] = cart_id # needed for removal
            
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total = Decimal(0)
        for item in self.__iter__(): # Use __iter__ to get calculated prices
             total += item['total_price']
        return total

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
