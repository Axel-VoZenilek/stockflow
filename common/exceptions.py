class StockFlowException(Exception):
    pass

class InsufficientStockError(StockFlowException):
    pass

class ProductNotFoundError(StockFlowException):
    pass

class StockNotFoundError(StockFlowException):
    pass