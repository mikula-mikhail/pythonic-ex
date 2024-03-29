from dataclasses import dataclass, field
from enum import Enum, auto
from pos.line_item import LineItem
from pos.customer import Customer

class OrderStatus(Enum):
    """Order status"""

    OPEN = auto()
    PAID = auto()
    CANCELLED = auto()
    DELIVERED = auto()
    RETURNED = auto()


@dataclass
class Order:
    customer: Customer
    items: list[LineItem] = field(default_factory=list)
    _status: OrderStatus = OrderStatus.OPEN
    id: str = ""

    def add_line_item(self, item: LineItem) -> None:
        self.items.append(item)

    def set_status(self, status: OrderStatus):
        self._status = status

    @property
    def total_price(self) -> int:
        return sum(line_item.total_price for line_item in self.items)
