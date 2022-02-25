from enum import Enum


class CancelAfter(Enum):
    Min = "min"
    Hour = "hour"
    Day = "day"

    def __str__(self) -> str:
        return self.value


class OrderType(Enum):
    Limit = "limit"
    Market = "market"
    Stop = "stop"

    def __str__(self) -> str:
        return self.value


class SelfTradePrevention(Enum):
    DecreaseCancel = "dc"
    CancelOldest = "co"
    CancelNewest = "cn"
    CancelBoth = "cb"

    def __str__(self) -> str:
        return self.value


class Side(Enum):
    Buy = "buy"
    Sell = "sell"

    def __str__(self) -> str:
        return self.value


class SortedBy(Enum):
    CreatedAt = "created_at"
    Price = "price"
    Size = "size"
    OrderID = "order_id"
    Side = "side"
    Type = "type"

    def __str__(self) -> str:
        return self.value


class Sorting(Enum):
    Descending = "desc"
    Ascending = "asc"

    def __str__(self) -> str:
        return self.value


class StopOrderType(Enum):
    Loss = "loss"
    Entry = "entry"

    def __str__(self) -> str:
        return self.value


class TimeInForce(Enum):
    GoodTillCanceled = "GTC"
    GoodTillTime = "GTT"
    ImmediateOrCancel = "IOC"
    FillOrKill = "FOK"

    def __str__(self) -> str:
        return self.value


class Period(Enum):
    Minute = 60
    Minute5 = 300
    Minute15 = 900
    Hour = 3600
    Hour6 = 21600
    Day = 81400

    def __int__(self) -> int:
        return self.value


class ReportFormat(Enum):
    PDF = "pdf"
    CSV = "csv"

    def __str__(self) -> str:
        return self.value


class ReportType(Enum):
    Fills = "fills"
    Account = "account"
    OTCFills = "otc_fills"
    TransactionHistory = "type_1099k_transaction_history"
    TaxInvoice = "tax_invoice"

    def __str__(self) -> str:
        return self.value
