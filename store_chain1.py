import time
from datetime import datetime

class Shop(object):

    AVAILABLE_PRODUCT_TYPES = ["food", "drink", "medicine", "cigarettes", "toys", "parking tickets"]

    def __init__(self, products):
        for product in products:  #Ensuring that only products from the above list are in the shop
            if product._type not in Shop.AVAILABLE_PRODUCT_TYPES:
                raise TypeError(f"Our chain does not sell product of type {product._type} ")
        self.products = products
        self.sell_strategy = None
        self.bill_num = 0
        self.sold_products = []

    #Using strategy pattern to make implementation of sell method more flexible and potentialy reduce code duplication.

    def setSellingStrategy(self, obj):
        self.sell_strategy = obj

    def getSellingStrategy(self):
        return self.sell_strategy

    def sell(self, order, *args, **kwargs):
        # print ("Sell called")
        return self.sell_strategy.sellalgorithm(order, self.products, self.sold_products, self.bill_num)

    def report(self):
        for product in self.sold_products:
            print ("Products sold: ", product._type, product.name, product.quantity, product.price)
        

#Product objects here represent types of product of a certain quantity.

class Product(object):
    def __init__(self, _type, name, price, quantity):
        self._type = _type
        self.name = name
        self.price = price
        self.quantity = quantity

    def display(self):
        return f"Product name: {self.name}, Product quantity: {self.quantity}, Product price: {self.price}"

class Medicine(Product):
    def __init__(self, _type, name, price, quantity, serial_num):
        super().__init__(_type, name, price, quantity)
        self.serial_num = serial_num    #Overriding the parent class __init__ method.

    def display(self):
        return f"Product name: {self.name},Product quantity: {self.quantity}, Product price: {self.price}, Serial_num: {self.serial_num}"
                

class ParkingTicket(Product):
    def __init__(self, _type, name, price, quantity, serial_num):
        super().__init__(_type, name, price, quantity)
        self.serial_num = serial_num    #Overriding the parent class __init__ method.

    def display(self):
        return f"Product name: {self.name}, Product quantity: {self.quantity}, Product price: {self.price}, Serial_num: {self.serial_num}"
                

# Child classes inheriting methods from Shop class adopting different selling strategies bellow.
class Farmacy(Shop):
    def __init__(self, products):
        super().__init__(products)  

    
   
class CornerShop(Shop):
    def __init__(self, products):
        super().__init__(products)

   

class RegularShop(Shop):
    def __init__(self, products):
        super().__init__(products)


class SellStrategy(object):
    def sellalgorithm(self, order):
        raise NotImplementedError("Must be defined in subclass")

#Defining selling strategies

class RegularSellStrategy(SellStrategy):
    def sellalgorithm(self, order, shop_products, total_sold, shop_bill_num):
        # print ("RegularSellStrategy sell algo")
        print ([x._type for x in order.products])
        if "cigarettes" in [x._type for x in order.products] or "medicine" in [x._type for x in order.products]:
           print ("Sorry we don't sell that in this store")
        else:
            #Checking the availabilitty of products
            for i in order.products:
                product_available = False
                for product in shop_products:
                    if i._type == product._type and i.quantity <= product.quantity:
                        product_available = True #Marking that ordered product is in stock
                if product_available == False: #if not in stock...
                    print ("Sorry, product you requested is not in our store or quantity you requested is unavailable.Please make a new order.")
                    return #stopping search 
            for i in order.products:  #starting transaction
                for product in shop_products:
                    if i._type == product._type and i.quantity <= product.quantity:
                        product.quantity -= i.quantity #reducing the quantity of product in stock
                        total_sold.append(i)
        #Creating a bill                         
        return Bill(order, shop_bill_num)

class FarmacySellStrategy(SellStrategy):
    def sellalgorithm(self, order, shop_products, total_sold,shop_bill_num):
        if "cigarettes" in [x._type for x in order.products]:
           print ("Sorry we don't sell that type of product in this store")
        else:
            for i in order.products:
                for product in shop_products:   
                    if i._type == product._type and i.quantity <= product.quantity:
                        product.quantity -= i.quantity
                        total_sold.append(i)
                    else:
                        print ("Sorry, product you requested is not in our store or quantity you requested in unavailable")
        return Bill(order, shop_bill_num)

class CornerShopSellStrategy(SellStrategy):
    def sellalgorithm(self, order, shop_products, total_sold, shop_bill_num):
        if "medicine" in [x._type for x in order.products]:
           print ("Sorry we don't sell that type of product in this store")
        else:
            for i in order.products:
                for product in shop_products:
                    
                    if i._type == product._type and i.quantity <= product.quantity:
                        product.quantity-= i.quantity
                        total_sold.append(i)
                    else:
                        print ("Sorry, product you requested is not in our store or quantity you requested in unavailable")
        return Bill(order, shop_bill_num)
                         
class Order(object):
    def __init__(self, products, customer):
        self.products = products
        self.customer = customer
        self.order_time = datetime.now()

class Bill(object):
    current_year = 2021
    
    def __init__(self, order, shop_bill_num):
        self.order = order
        self.customer_first_name = order.customer.first_name
        self.customer_last_name = order.customer.last_name
        if 2021 == Bill.current_year:
            shop_bill_num += 1
        else:
            shop_bill_num = 0
            Bill.current_year = 2021
        self.bill_num = shop_bill_num
        self.tel_num = order.customer.tel_num
        now = datetime.now()
        self.dateandtime = now.strftime("%d/%m/%Y %H:%M:%S")

    def __str__(self):
        return f"""Bill number: {self.bill_num}, date and time created: {self.dateandtime}, customer: {self.customer_first_name} {self.customer_last_name}, customer phone_num: {self.tel_num},
        Bought products: {[x.display() for x in self.order.products]}
        """


class Customer(object):
    def __init__(self, first_name, last_name, tel_num):
        self.first_name = first_name
        self.last_name = last_name
        self.tel_num = tel_num


#Creating products
product1 = Product("drink", "Pepsi", 60, 1)
product2 = Product("food", "Hamburger", 100, 1)
product3 = Medicine("medicine", "Brufen", 200, 2, 5)

#Creating product lists (analogous to putting things in a shopping cart)
products1 = []
products2 = []

products1.append(product1)
products1.append(product2)
products2.append(product3)

#Creating shops

shop1 = RegularShop(products1)

shop2 = Farmacy(products2)

shop3 = CornerShop(products1)



#Creating selling strategies objects

regularsellstrategy = RegularSellStrategy()
farmacysellstrategy = FarmacySellStrategy()
cornershopsellstrategy = CornerShopSellStrategy()

#Assigning selling strategies to shops

shop1.setSellingStrategy(regularsellstrategy)
shop2.setSellingStrategy(farmacysellstrategy)
shop3.setSellingStrategy(cornershopsellstrategy)

#Creating customers

customer1 = Customer("Foo", "Bar", "06133334444")
customer2 = Customer("Jane", "Doe", "0633333555")


#Making orders for customers

order1 = Order(products1, customer1)

#Printing a bill

print (shop1.sell(order1))

#Submitting a report

shop1.report()



