from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')


class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


def fidelity_promotion(order):
    """为积分1000以上的顾客提供优惠"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0


def bulk_item_promotion(order):
    """为单个商品20个以上的顾客提供优惠"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount


def large_order_promotion(order):
    """为不同商品超过10个的顾客提供优惠"""
    distinct_item = {item.product for item in order.cart}
    if len(distinct_item) >= 10:
        return order.total() * .07
    return 0


if __name__ == '__main__':
    joe = Customer("John Doe", 0)
    ann = Customer("Ann Smith", 1100)
    cart = [LineItem("banana", 4, .5),
            LineItem("apple", 10, 1.5),
            LineItem("watermellon", 5, 5.0)]
    # 按积分提供优惠
    print(Order(joe, cart, fidelity_promotion))
    print(Order(ann, cart, fidelity_promotion))

    # 单个商品超过10个提供优惠
    banana_cart = [LineItem("banana", 30, .5),
                   LineItem("apple", 10, 1.5)]
    print(Order(joe, banana_cart, bulk_item_promotion))

    # 不同商品超过10个提供优惠
    large_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
    print(Order(joe, large_order, large_order_promotion))
    print(Order(joe, cart, large_order_promotion))
